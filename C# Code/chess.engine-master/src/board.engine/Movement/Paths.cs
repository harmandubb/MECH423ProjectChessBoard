using System;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;

namespace board.engine.Movement
{
    [DebuggerDisplay("{DebuggerDisplay}")]
    public class Paths : IEnumerable<Path>, ICloneable
    {
#if DEBUG
        // NOTE: string.Join make the debugger a little slow
        private string DebuggerDisplay
            => $"{string.Join(", ", _paths.Select(m => m.ToString()))}";
#endif
        private readonly List<Path> _paths;

        public Paths() => _paths = new List<Path>();

        public Paths(IEnumerable<Path> paths) => _paths = new List<Path>(paths);

        public void Add(Path path) => _paths.Add(path);

        public void AddRange(IEnumerable<Path> paths) => _paths.AddRange(paths);

        public IEnumerable<BoardMove> FlattenMoves() => _paths.SelectMany(ps => ps);

        public bool ContainsMoveTo(BoardLocation location) => FlattenMoves().Any(m => m.To.Equals(location));

        public bool ContainsMoveTypeTo(BoardLocation location, params int[] moveTypesAndActions)
            => FlattenMoves().Any(m => m.To.Equals(location) && moveTypesAndActions.Any(mt => mt == m.MoveType));

        public BoardMove FindMove(BoardLocation from, BoardLocation destination, object extraData = null) 
            => FlattenMoves().FindMove(@from, destination, extraData);

        public object Clone() => new Paths(_paths.Select(ps => ps.Clone() as Path));

        #region Equality, Enumerator and Overrides

        protected bool Equals(Paths other) => _paths.All(other.Contains);

        public override bool Equals(object obj)
        {
            if (ReferenceEquals(null, obj)) return false;
            if (ReferenceEquals(this, obj)) return true;
            if (obj.GetType() != this.GetType()) return false;
            return Equals((Paths)obj);
        }

        public override int GetHashCode() => _paths.GetHashCode();

        public IEnumerator<Path> GetEnumerator() => _paths.GetEnumerator();
        IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();

#if DEBUG
        public override string ToString()
        {
            return DebuggerDisplay;
        }
#endif

        #endregion
    }
}