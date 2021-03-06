from .base import PushItem
from .. import compat_attr as attr


@attr.s()
class ModulemdPushItem(PushItem):
    """A push item representing a modulemd stream.

    For push items of this type, the ``src`` attribute refers to a
    file containing a YAML document stream. The stream is expected
    to contain one or more modulemd or modulemd-defaults documents.

    This library does not verify that the referenced file is a valid
    modulemd stream.
    """
