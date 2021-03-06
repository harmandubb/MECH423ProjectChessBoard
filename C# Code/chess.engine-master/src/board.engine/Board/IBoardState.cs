using System;
using System.Collections.Generic;

namespace board.engine.Board
{
    public interface IReadOnlyBoardState<TEntity> where TEntity : class, IBoardEntity
    {
        LocatedItem<TEntity> GetItem(BoardLocation loc);
        bool IsEmpty(BoardLocation location);
//        IEnumerable<LocatedItem<TEntity>> GetItems(params BoardLocation[] locations);
        IEnumerable<LocatedItem<TEntity>> GetItems(int owner);
        IEnumerable<LocatedItem<TEntity>> GetItems(int owner, int entityType);
        IEnumerable<LocatedItem<TEntity>> GetItems();
        string ToTextBoard();
    }

    public interface IBoardState<TEntity> : ICloneable, IReadOnlyBoardState<TEntity> where TEntity : class, IBoardEntity
    {
        void PlaceEntity(BoardLocation loc, TEntity entity);
        void Clear();
        void Remove(BoardLocation loc);

        void RegenerateValidatedPaths();
        void RegenerateValidatedPaths(int owner);

        void RegenerateValidatedPaths(LocatedItem<TEntity> locatedItem);
        void UpdatePaths(LocatedItem<TEntity>[] items);
        void RefreshPathsFor(IEnumerable<LocatedItem<TEntity>> items);
    }
}