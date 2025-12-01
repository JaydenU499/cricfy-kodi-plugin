import requests

# Custom Headers for fetching M3U playlists
custom_headers = {
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0",
  "Accept": "*/*",
  "Cache-Control": "no-cache, no-store",
}

license_headers = {
  "Content-Type": "*/*",
  "User-Agent": "Dalvik/2.1.0 (Linux; U; Android)",
}


def fetch_url(url: str, timeout: int = 15) -> str:
  response = requests.get(
    url=url,
    headers=custom_headers,
    timeout=timeout,
  )
  response.raise_for_status()
  if response.status_code != 200:
    return ""
  return response.text
