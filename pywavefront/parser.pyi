from _typeshed import Incomplete
from collections.abc import Generator

logger: Incomplete

def auto_consume(func):
    """Decorator for auto consuming lines when leaving the function"""

class Parser:
    """This defines a generalized parse dispatcher; all parse functions
    reside in subclasses."""
    auto_post_parse: bool
    file_name: Incomplete
    strict: Incomplete
    encoding: Incomplete
    dir: Incomplete
    dispatcher: Incomplete
    lines: Incomplete
    line: Incomplete
    values: Incomplete
    def __init__(self, file_name, strict: bool = False, encoding: str = 'utf-8') -> None:
        """
        Initializer for the base parser
        :param file_name: Name and path of the file to read
        :param strict: Enable or disable strict mode
        """
    def create_line_generator(self) -> Generator[Incomplete]:
        """
        Creates a generator function yielding lines in the file
        Should only yield non-empty lines
        """
    def next_line(self) -> None:
        """Read the next line from the line generator and split it"""
    def consume_line(self) -> None:
        """
        Tell the parser we are done with this line.
        This is simply by setting None values.
        """
    def parse(self) -> None:
        """
        Parse all the lines in the obj file
        Determines what type of line we are and dispatch appropriately.
        """
    def post_parse(self) -> None:
        """Override to trigger operations after parsing is complete"""
    def parse_fallback(self) -> None:
        """Fallback method when parser doesn't know the statement"""
