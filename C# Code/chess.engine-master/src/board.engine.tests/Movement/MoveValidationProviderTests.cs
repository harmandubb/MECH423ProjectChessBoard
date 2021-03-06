using System;
using board.engine.Actions;
using board.engine.Movement;
using board.engine.tests.utils;
using NUnit.Framework;
using Shouldly;

namespace board.engine.tests.Movement
{
    [TestFixture]
    public class MoveValidationProviderTests
    {
        private MoveValidationProvider<TestBoardEntity> _provider;

        [SetUp]
        public void SetUp()
        {
            _provider = new MoveValidationProvider<TestBoardEntity>();
        }
        [Test]
        public void FactorySupportsAllMoveTypes()
        {
            foreach (ChessMoveTypes type in Enum.GetValues(typeof(DefaultActions)))
            {
                Should.NotThrow(()=> _provider.Create((int)type, null), $"{type} is not support");
            }
        }
    }
}