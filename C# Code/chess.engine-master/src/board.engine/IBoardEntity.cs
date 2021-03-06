using System;
using System.Collections.Generic;
using board.engine.Movement;

namespace board.engine
{
    public interface IBoardEntity: ICloneable
    {
        IEnumerable<IPathGenerator> PathGenerators { get; }
        IEnumerable<BoardLocation> LocationHistory { get; }
        string EntityName { get; }

        int EntityType { get; }

        int Owner { get; }

        void AddMoveTo(BoardLocation location);
    }

    public interface IBoardEntityFactory<T> where T : IBoardEntity
    {
        T Create(object typeData);
        string ValidPieces { get; }
    }
}