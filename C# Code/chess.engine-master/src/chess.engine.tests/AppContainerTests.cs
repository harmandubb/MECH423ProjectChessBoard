using NUnit.Framework;
using Shouldly;

namespace chess.engine.tests
{
    public class AppContainerTests
    {
        [Test]
        public void Should_resolve_all_chess_dependencies()
        {
            var x = AppContainer.ServiceProvider;
            var count = 0;
            foreach (var service in AppContainer.ServiceCollection)
            {
                var ns = service.ServiceType.Namespace;
                if (ns.StartsWith("board.") || ns.StartsWith("chess."))
                {
                    var y = x.GetService(service.ServiceType);
                    count++;
                }
            }

            count.ShouldBeGreaterThan(0);
        }
    }
}