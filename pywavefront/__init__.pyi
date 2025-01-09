from _typeshed import Incomplete
from pywavefront.exceptions import PywavefrontException as PywavefrontException
from pywavefront.obj import ObjParser as ObjParser
from pywavefront.wavefront import Wavefront as Wavefront

__version__: str
logger: Incomplete
log_handler: Incomplete

def configure_logging(level, formatter: Incomplete | None = None) -> None: ...
