#include <peglib.h>
#include <cstdlib>

auto main() -> int
{
    auto parser = peg::parser{"ROOT <- ' '"};
    return static_cast<bool>(parser) ? EXIT_SUCCESS : EXIT_FAILURE;
}
