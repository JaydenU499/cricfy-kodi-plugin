import json
from lib.config import ADDON_PATH
from lib.logger import log_error
from lib.crypto_utils import decrypt_data
from lib.req import fetch_url

URL_FILE_PATH = ADDON_PATH / "resources" / "cricfy_url.txt"
FALLBACK_PROVIDERS_FILE_PATH = ADDON_PATH / \
  "resources" / "fallback_providers.json"

URL = open(URL_FILE_PATH, "r").read().strip()
FALLBACK_PROVIDERS = json.loads(open(FALLBACK_PROVIDERS_FILE_PATH, "r").read())


def get_providers():
  response = fetch_url(
    URL,
    timeout=15,
  )
  if response:
    try:
      decrypted_data = decrypt_data(response)
      if not decrypted_data:
        return FALLBACK_PROVIDERS

      providers = json.loads(decrypted_data)
      return providers
    except Exception as e:
      log_error("providers", f"Error parsing providers: {e}")
  return FALLBACK_PROVIDERS
