from pathlib import Path

FIXTURE_PATH = Path(__file__).parent.absolute() / 'fixtures'


def fixture(name: str):
    """
    Construct an absolute path to the fixture directory
    """
    return Path(FIXTURE_PATH, name)
