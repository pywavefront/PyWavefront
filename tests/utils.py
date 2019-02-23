from pathlib import Path

print()

def fixture(name: str):
    """
    Construct an absolute path to the fixture directory
    """
    return str(Path(Path(__file__).parent.absolute(), 'fixtures', name))
