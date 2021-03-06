using System.Collections.Generic;
using System.Diagnostics;
using board.engine;
using board.engine.Movement;
using chess.engine.Game;

namespace chess.engine.Entities
{
    [DebuggerDisplay("{DebuggerDisplayText}")]
    public abstract class ChessPieceEntity : IBoardEntity
    {
        private readonly List<BoardLocation> _locationHistory = new List<BoardLocation>();
        private string DebuggerDisplayText => $"{Player} {Piece}";
        public int EntityType { get; }
        public abstract IEnumerable<IPathGenerator> PathGenerators { get; }
        public string EntityName { get; }
        public int Owner { get; }
        public IEnumerable<BoardLocation> LocationHistory
            => _locationHistory;
        public void AddMoveTo(BoardLocation location)
        {
            _locationHistory.Add(location);
        }
        
        public Colours Player { get; }
        public ChessPieceName Piece { get; protected set; }

        protected ChessPieceEntity(Colours player, ChessPieceName piece)
        {
            EntityType = (int) piece;
            EntityName = piece.ToString();
            Owner = (int) player;

            Player = player;
            Piece = piece;
        }

        public bool Is(Colours owner, ChessPieceName piece) => owner == Player && piece == Piece;
        public bool Is(ChessPieceName piece) => piece == Piece;
        public bool Is(Colours owner) => owner == Player;
        public abstract object Clone();

    }
}