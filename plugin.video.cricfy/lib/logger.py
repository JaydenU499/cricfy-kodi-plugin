import xbmc


def log_error(component: str, message: str) -> None:
  xbmc.log(f"Cricfy Plugin [{component}]: {message}", xbmc.LOGERROR)


def log_info(component: str, message: str) -> None:
  xbmc.log(f"Cricfy Plugin [{component}]: {message}", xbmc.LOGINFO)