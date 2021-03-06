using board.engine;
using board.engine.Actions;
using board.engine.Movement;
using chess.engine.Entities;
using chess.engine.Game;

namespace chess.engine.Movement.Pawn
{
    public class PawnNormalAndStartingPathGenerator : IPathGenerator
    {
        public Paths PathsFrom(BoardLocation location, int forPlayer)
        {
            var paths = new Paths();

            var playerIdx = (Colours) forPlayer;
            var oneSquareForward = location.MoveForward(playerIdx);
            if (oneSquareForward.Y != ChessGame.EndRankFor(playerIdx))
            {
                var move = new BoardMove(location, oneSquareForward, (int)DefaultActions.MoveOnly);

                var path = new Path {move};
                if (location.Y == Pieces.Pawn.StartRankFor(playerIdx))
                {
                    BoardLocation to = location.MoveForward(playerIdx, 2);
                    path.Add(new BoardMove(location, to, (int)ChessMoveTypes.PawnTwoStep));
                }
                paths.Add(path);
            }
            else
            {
                foreach (var promotionPieces in new[] { ChessPieceName.Queen, ChessPieceName.Rook, ChessPieceName.Bishop, ChessPieceName.Knight })
                {
                    var move = new BoardMove(location, oneSquareForward, (int)DefaultActions.UpdatePiece, new ChessPieceEntityFactory.ChessPieceEntityFactoryTypeExtraData
                    {
                        Owner = playerIdx,
                        PieceName = promotionPieces
                    });
                    paths.Add(new Path { move });
                }
            }


            return paths;
        }
    }
}