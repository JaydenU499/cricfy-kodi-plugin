from pathlib import Path
from xbmcaddon import Addon
from xbmcvfs import translatePath

ADDON_PATH = Path(translatePath(Addon().getAddonInfo('path')))
