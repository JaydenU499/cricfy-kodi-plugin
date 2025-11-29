import sys
from urllib.parse import urlencode, parse_qsl
import xbmcgui
import xbmcplugin
from lib.providers import get_providers
from lib.logger import log_error
from lib.req import fetch_url
from lib.m3u_parser import parse_m3u

# Base URL for the addon
BASE_URL = sys.argv[0]
ADDON_HANDLE = int(sys.argv[1])


def build_url(query):
  return f'{BASE_URL}?{urlencode(query)}'


def list_providers():
  """
  Lists the providers from Cricfy
  """
  provider_list = get_providers()

  for prov in provider_list:
    title = prov.get('title', 'Unknown')
    image = prov.get(
      'image', 'https://www.iconexperience.com/_img/v_collection_png/256x256/shadow/unknown.png')
    cat_link = prov.get('catLink', '')

    if not cat_link:
      continue

    # Create a folder item for this provider
    li = xbmcgui.ListItem(label=title)
    li.setArt({'icon': image, 'thumb': image})

    url = build_url({'mode': 'list_channels', 'url': cat_link, 'title': title})
    xbmcplugin.addDirectoryItem(
      handle=ADDON_HANDLE, url=url, listitem=li, isFolder=True)

  xbmcplugin.endOfDirectory(ADDON_HANDLE)


def list_channels(m3u_url):
  """
  Fetches the M3U from the specific provider and lists channels.
  """
  try:
    # Fetch M3U content with custom headers
    content = fetch_url(m3u_url, timeout=15)
    if not content:
      xbmcgui.Dialog().notification(
        'Error', 'Failed to fetch playlist content', xbmcgui.NOTIFICATION_ERROR)
      xbmcplugin.endOfDirectory(ADDON_HANDLE)
      return

    # Parse M3U
    channels = parse_m3u(content)

    for ch in channels:
      li = xbmcgui.ListItem(label=ch.title)
      li.setArt({'thumb': ch.tvg_logo, 'icon': ch.tvg_logo})
      li.setInfo('video', {'title': ch.title, 'genre': ch.group_title})
      li.setProperty('IsPlayable', 'true')

      # Construct URL for playback mode
      # We encode the channel data into the URL so we don't have to re-parse on playback
      # TODO: Use a cache to eliminate stale URLs (if item was added to favorites, etc)
      params = {
        'mode': 'play',
        'url': ch.url,
        'ua': ch.user_agent,
        'cookie': ch.cookie,
        'referer': ch.referer,
        'lic': ch.license_string,
        'headers': ch.headers
      }

      url = build_url(params)
      xbmcplugin.addDirectoryItem(
        handle=ADDON_HANDLE, url=url, listitem=li, isFolder=False)
    xbmcplugin.endOfDirectory(ADDON_HANDLE)

  except Exception as e:
    log_error("main", f"Error listing channels: {e}")
    xbmcgui.Dialog().notification('Error', str(e), xbmcgui.NOTIFICATION_ERROR)
    xbmcplugin.endOfDirectory(ADDON_HANDLE)


def router(param_string):
  params = dict(parse_qsl(param_string))
  mode = params.get('mode')

  if mode is None:
    list_providers()
  elif mode == 'list_channels':
    list_channels(params.get('url'))
  else:
    xbmcgui.Dialog().notification(
      'Error', 'Not yet implemented', xbmcgui.NOTIFICATION_ERROR)


if __name__ == '__main__':
  router(sys.argv[2][1:])
