import sys
from urllib.parse import urlencode, parse_qsl
import xbmcgui
import xbmcplugin
from lib.providers import get_providers

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


def router(param_string):
  params = dict(parse_qsl(param_string))
  mode = params.get('mode')

  if mode is None:
    list_providers()
  else:
    xbmcgui.Dialog().notification(
      'Error', 'Not yet implemented', xbmcgui.NOTIFICATION_ERROR)


if __name__ == '__main__':
  router(sys.argv[2][1:])
