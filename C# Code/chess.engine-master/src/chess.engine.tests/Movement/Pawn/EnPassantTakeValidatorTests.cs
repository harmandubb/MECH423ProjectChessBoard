using board.engine;
using board.engine.Movement;
using chess.engine.Game;
using chess.engine.Movement.Pawn;
using chess.engine.tests.Builders;
using NUnit.Framework;
using Shouldly;

namespace chess.engine.tests.Movement.Pawn
{
    [TestFixture]
    public class EnPassantTakeValidatorTests
    {
        private EnPassantTakeValidator _validator;
        private readonly ChessValidationStepsMocker _stepMocker = new ChessValidationStepsMocker();

        private readonly BoardMove AnyBoardMove = BoardMove.Create(BoardLocation.At(1, 1), BoardLocation.At(1, 2), 1);
        private const Colours Friend = Colours.White;
        [SetUp]
        public void Setup()
        {
            _validator = new EnPassantTakeValidator(_stepMocker.Build());

            _stepMocker.SetupLocationEmpty(false)
                .SetupEnpassantFriendlyPawnValid(false, Friend)
                .SetupEnpassantEnemyPawnValid(false);
        }
        [Test]
        public void ValidateMove_fails_when_take_location_not_empty()
        {
            _validator.ValidateMove(AnyBoardMove, null).ShouldBeFalse();
        }
        [Test]
        public void ValidateMove_fails_friendly_pawn_invalid()
        {
            _stepMocker.SetupLocationEmpty(true);

            _validator.ValidateMove(AnyBoardMove, null).ShouldBeFalse();
        }
        [Test]
        public void ValidateMove_fails_enemy_pawn_invalid()
        {
            _stepMocker.SetupLocationEmpty(true)
                .SetupEnpassantFriendlyPawnValid(true, Friend);

            _validator.ValidateMove(AnyBoardMove, null).ShouldBeFalse();
        }
        [Test]
        public void ValidateMove_pass_when_both_pawns_valid()
        {
            _stepMocker.SetupLocationEmpty(true)
                .SetupEnpassantFriendlyPawnValid(true, Friend)
                .SetupEnpassantEnemyPawnValid(true);

            _validator.ValidateMove(AnyBoardMove, null).ShouldBeTrue();
        }
    }
}