from pathlib import Path

# The __init__.py file needs to be located next to the toxfile.
ToxFile = Path( Path(  __file__ ).parent, "Browser.tox" )

# If several components want to instanciate this ToxFile, but only one is required in the project,
# this member allows for a clearly defined global op shortcut.
# Using an UUID is not the worst approach, so there are now conflicts. 
# But usng something like PACKAGE_COMP name is also totaly apropiate.

DefaultGlobalOpShortcut = "PP1_TDPBROWSER"


from typing import TYPE_CHECKING
if TYPE_CHECKING:
  # This allows for importing Typing without having to import and instanciate the object an additional time.
  # Defining the typing as classes allows for te use of opex().asType which is a big improvement.
    from .extTdpBrowser import extTdpBrowser
    class Typing(extTdpBrowser, containerCOMP):
        class par( extTdpBrowser.par, containerCOMP._ContainerCOMPPars):
            pass
        pass
else:
    class Typing:
        pass

# Make sure to only export required members.
__all__ = ["ToxFile", "Typing", "DefaultGlobalOpShortcut"]