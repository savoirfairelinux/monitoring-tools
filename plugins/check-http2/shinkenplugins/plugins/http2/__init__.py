
import pkg_resources
pkg_resources.declare_namespace(__name__)


from .http2 import main
from .http2 import Plugin
