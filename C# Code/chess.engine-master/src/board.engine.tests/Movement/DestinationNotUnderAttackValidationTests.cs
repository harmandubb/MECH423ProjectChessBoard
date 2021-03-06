using board.engine.Actions;
using board.engine.Movement;
using board.engine.Movement.Validators;
using board.engine.tests.utils;
using NUnit.Framework;
using Shouldly;

namespace board.engine.tests.Movement
{
    [TestFixture]
    public class DestinationNotUnderAttackValidationTests : ValidationTestsBase
    {
        private DestinationNotUnderAttackValidator<TestBoardEntity> _validator;

        [SetUp]
        public void SetUp()
        {
            InitMocks();
            _validator = new DestinationNotUnderAttackValidator<TestBoardEntity>();
        }

        [Test]
        public void Should_return_false_for_square_under_enemy_attack()
        {
            var move = BoardMove.Create(BoardLocation.At(5,1), BoardLocation.At(4, 1), (int) DefaultActions.MoveOrTake);
            SetupFromEntity(move, new TestBoardEntity());
            SetupGetNonOwnerEntities(move, new TestBoardEntity(Enemy));

            _validator.ValidateMove(move, RoBoardStateMock.Object).ShouldBeFalse();
        }

        [Test]
        public void Should_return_true_for_square_under_friendly_attack()
        {
            var move = BoardMove.Create(BoardLocation.At(5, 1), BoardLocation.At(6, 1), (int) DefaultActions.MoveOrTake);

            SetupFromEntity(move, new TestBoardEntity());
            SetupGetNonOwnerEntities(move, new TestBoardEntity());

            _validator.ValidateMove(move, RoBoardStateMock.Object).ShouldBeTrue();

        }
        [Test]
        public void Should_return_true_for_square_under_no_attack()
        {
            var move = BoardMove.Create(BoardLocation.At(5, 1), BoardLocation.At(5, 2), (int) DefaultActions.MoveOrTake);

            SetupFromEntity(move, new TestBoardEntity());
            SetupGetNonOwnerEntitiesReturnsNone();

            _validator.ValidateMove(move, RoBoardStateMock.Object).ShouldBeTrue();
        }
    }
}