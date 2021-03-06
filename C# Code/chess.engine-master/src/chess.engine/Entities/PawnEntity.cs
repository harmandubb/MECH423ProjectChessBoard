using System.Collections.Generic;
using board.engine.Movement;
using chess.engine.Game;
using chess.engine.Movement.Pawn;

namespace chess.engine.Entities
{
    public class PawnEntity : ChessPieceEntity
    {
        public PawnEntity(Colours player) : base(player, ChessPieceName.Pawn)
        {
            Piece = ChessPieceName.Pawn;
        }
        public override IEnumerable<IPathGenerator> PathGenerators =>
            new List<IPathGenerator>
            {
                new PawnNormalAndStartingPathGenerator(),
                new PawnTakePathGenerator()
            };

        public bool TwoStep { get; set; }

        public override object Clone()
        {
            return new PawnEntity(Player);
        }

    }
}