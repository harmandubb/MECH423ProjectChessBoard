using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using board.engine;
using board.engine.Board;
using board.engine.Movement;
using chess.engine.Entities;
using chess.engine.Extensions;
using chess.engine.Pieces;

namespace chess.engine.Game
{
    public static class ChessGameConvert
    {
        public static int ToBoardIdx(this (int x, int y) location) 
            => ((8 - location.y) * 8) + location.x - 1;

        public static int ToBoardIdx(this BoardLocation location) 
            => (location.X, location.Y).ToBoardIdx();

        public static string Serialise(ChessGame chessGameBoard)
        {
            var sb = new StringBuilder();
                
            sb.Append(SerialiseBoard(chessGameBoard.BoardState));

            sb.Append(SerialiseCurrentPlayer(chessGameBoard));

            sb.Append(CheckForCastleEligibility(chessGameBoard));

            return sb.ToString();
        }

        public static string SerialiseCurrentPlayer(ChessGame chessGameBoard)
        {
            return chessGameBoard.CurrentPlayer.ToString().First().ToString();
        }

        public static string SerialiseBoard(IBoardState<ChessPieceEntity> boardState)
        {
            var sb = new StringBuilder();

            for (var y = 8; y >= 1; y--)
            {
                for (var x = 1; x <= 8; x++)
                {
                    var item = boardState.GetItem(BoardLocation.At(x, y));
                    var c = AsChar(item);
                    sb.Append(c);
                }
            }

            return sb.ToString();
        }


        private static string CheckForCastleEligibility(ChessGame chessGameBoard)
        {
            var sb = new StringBuilder();
            LocatedItem<ChessPieceEntity> GetKing(Colours colours) =>
                chessGameBoard.BoardState.GetItem(King.StartPositionFor(colours));

            void AddCastleEligibility(IReadOnlyCollection<BoardMove> kingMoves)
            {
                bool CanCastle(ChessMoveTypes castleSide)
                {
                    return kingMoves.Any(p => p.MoveType == (int) castleSide);
                }

                sb.Append(CanCastle(ChessMoveTypes.CastleQueenSide) ? "1" : "0");
                sb.Append(CanCastle(ChessMoveTypes.CastleKingSide) ? "1" : "0");
            }

            AddCastleEligibility(GetKing(Colours.White)?.Paths.FlattenMoves().ToList() ?? new List<BoardMove>());
            AddCastleEligibility(GetKing(Colours.Black)?.Paths.FlattenMoves().ToList() ?? new List<BoardMove>());
            return sb.ToString();
        }

        private static char AsChar(LocatedItem<ChessPieceEntity> item)
        {
            if (item == null) return '.';

            var displayChar = ChessPieceNameMapper.ToChar(item.Item.Piece, item.Item.Player);

            if (item.Item.Piece == ChessPieceName.Pawn)
            {
                var pawn = (PawnEntity) item.Item;

                if (pawn.TwoStep)
                {
                    displayChar = pawn.Player == Colours.White ? 'E' : 'e';
                }
            }

            return displayChar;
        }

        public static ChessGame Deserialise(string boardformat69Char)
        {
            if (boardformat69Char.Length != 69) Throw.InvalidBoardFormat($"Invalid serialised board, must be 69 characters long (yours was {boardformat69Char.Length})");

            // TODO: Handling of invalid formats
            int idx = 1;

            var setup = CreatePieceEntitiesSetupActions(boardformat69Char.Substring(0, 64), idx);

            var whoseTurn = boardformat69Char[64] == 'W'
                ? Colours.White
                : Colours.Black;

            // TODO: King/Castle location history stuff
            
            var chessGame = new ChessGame(
                ChessFactory.ChessBoardEngineProvider(),
                ChessFactory.CheckDetectionService(),
                setup,
                whoseTurn
            );
            return chessGame;
        }

        private static DeserialisedBoardSetup CreatePieceEntitiesSetupActions(string pieces, int idx)
        {
            var toBePlaced = new List<Action<BoardEngine<ChessPieceEntity>>>();

            foreach (var piece in pieces)
            {
                var locX = (idx - 1) % 8 + 1;
                var locY = 8 - (idx - 1) / 8;

                if (piece != '.' && piece != ' ')
                {
                    var newPiece = BuildEntity(piece);

                    toBePlaced.Add((engine) =>
                    {
                        engine.AddPiece(newPiece, BoardLocation.At(locX, locY));

                    });
                }

                idx++;
            }

            return new DeserialisedBoardSetup(toBePlaced);
        }

        private static ChessPieceEntity BuildEntity(char piece)
        {
            // TODO: TwoStep pawn check
            var chessPieceName = ChessPieceNameMapper.FromChar(piece);
            var colour = char.IsUpper(piece) ? Colours.White : Colours.Black;
            var newPiece = ChessFactory.ChessPieceEntityFactory().Create(new ChessPieceEntityFactory.ChessPieceEntityFactoryTypeExtraData
            {
                PieceName = chessPieceName, Owner = colour
            });


            if (piece.ToString().ToLower() == "e")
            {
                var pawn = newPiece as PawnEntity;
                pawn.TwoStep = true;
            }
            return newPiece;
        }

        private class DeserialisedBoardSetup : IBoardSetup<ChessPieceEntity>
        {
            private readonly IEnumerable<Action<BoardEngine<ChessPieceEntity>>> _toBePlaced;

            public DeserialisedBoardSetup(IEnumerable<Action<BoardEngine<ChessPieceEntity>>> toBePlaced)
            {
                _toBePlaced = toBePlaced;
            }


            public void SetupPieces(BoardEngine<ChessPieceEntity> engine)
            {
                foreach (var action in _toBePlaced)
                {
                    action(engine);
                }
            }
        }
    }
}