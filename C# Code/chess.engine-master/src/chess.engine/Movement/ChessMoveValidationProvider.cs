using board.engine.Movement;
using board.engine.Movement.Validators;
using chess.engine.Entities;
using chess.engine.Movement.King;
using chess.engine.Movement.Pawn;

namespace chess.engine.Movement
{
    public class ChessMoveValidationProvider : MoveValidationProvider<ChessPieceEntity>
    {
        public ChessMoveValidationProvider(IChessValidationSteps chessValidationSteps)
        {
            Validators.Add((int)ChessMoveTypes.KingMove, new BoardMovePredicate<ChessPieceEntity>[] {
                (move, boardState) =>
                {
                    return new DestinationIsEmptyOrContainsEnemyValidator<ChessPieceEntity>().ValidateMove(move, boardState);
                },
                (move, boardState) =>
                {
                    return new DestinationNotUnderAttackValidator<ChessPieceEntity>().ValidateMove(move, boardState);
                }
            });

            Validators.Add((int)ChessMoveTypes.TakeEnPassant,
                new BoardMovePredicate<ChessPieceEntity>[]
                {(move, boardState) =>
                    {
                        return new EnPassantTakeValidator(chessValidationSteps).ValidateMove(move, boardState);
                    }
                });

            Validators.Add((int)ChessMoveTypes.PawnTwoStep,
                new BoardMovePredicate<ChessPieceEntity>[]
                {(move, boardState) =>
                    {
                        return new DestinationIsEmptyValidator<ChessPieceEntity>().ValidateMove(move, boardState);
                    }
                });
            Validators.Add((int)ChessMoveTypes.CastleKingSide,
                new BoardMovePredicate<ChessPieceEntity>[]
                { (move, boardState) =>
                    {
                        return new KingCastleValidator(chessValidationSteps).ValidateMove(move, boardState);
                    }
                });
            Validators.Add((int)ChessMoveTypes.CastleQueenSide,
                new BoardMovePredicate<ChessPieceEntity>[]
                    {(move, boardState) =>
                        {
                            return new KingCastleValidator(chessValidationSteps).ValidateMove(move, boardState);
                        }
                    });

        }
    }
}