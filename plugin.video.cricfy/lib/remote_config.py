import requests
import uuid
import json
from lib.config import ADDON_PATH
from lib.logger import log_error

"""
  Firebase Remote Config Fetcher
  Fetches remote config from Firebase to get API endpoints dynamically.

  Credits:
  - https://github.com/NivinCNC/CNCVerse-Cloud-Stream-Extension/blob/master/CricifyProvider/src/main/kotlin/com/cncverse/FirebaseRemoteConfigFetcher.kt
"""

CRICFY_PROPERTIES_FILE_PATH = ADDON_PATH / \
  "resources" / "cricfy_properties.json"
CRICFY_PROPERTIES = json.loads(
  CRICFY_PROPERTIES_FILE_PATH.read_text(encoding="utf-8"))

# Constants
CRICFY_PACKAGE_NAME = CRICFY_PROPERTIES.get("cricfy_package_name")
CRICFY_FIREBASE_API_KEY = CRICFY_PROPERTIES.get("cricfy_firebase_api_key")
CRICFY_FIREBASE_APP_ID = CRICFY_PROPERTIES.get("cricfy_firebase_app_id")
PROJECT_NUMBER = CRICFY_FIREBASE_APP_ID.split(":")[1]


def _get_random_instance_id():
  """Generates a random UUID without dashes"""
  return uuid.uuid4().hex


def fetch_remote_config():
  """
  Fetches Firebase Remote Config and returns the entries map.
  :return: Dictionary of config entries or None if fetch fails.
  """
  # Basic validation
  if not CRICFY_FIREBASE_API_KEY or not CRICFY_FIREBASE_APP_ID or not PROJECT_NUMBER:
    log_error("remote_config", "Error: Missing Firebase Credentials (CRICFY_FIREBASE_API_KEY, CRICFY_FIREBASE_APP_ID, or PROJECT_NUMBER)")
    return None

  url = f"https://firebaseremoteconfig.googleapis.com/v1/projects/{PROJECT_NUMBER}/namespaces/firebase:fetch"
  # Generate fake instance ID (clean hex string)
  app_instance_id = _get_random_instance_id()

  # Request Payload
  payload = {
    "appInstanceId": app_instance_id,
    "appInstanceIdToken": "",
    "appId": CRICFY_FIREBASE_APP_ID,
    "countryCode": "US",
    "languageCode": "en-US",
    "platformVersion": "30",
    "timeZone": "UTC",
    "appVersion": "5.0",
    "appBuild": "50",
    "packageName": CRICFY_PACKAGE_NAME,
    "sdkVersion": "22.1.0",
    "analyticsUserProperties": {}
  }

  # Headers
  headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-Android-Package": CRICFY_PACKAGE_NAME,
    "X-Goog-Api-Key": CRICFY_FIREBASE_API_KEY,
    "X-Google-GFE-Can-Retry": "yes"
  }

  try:
    response = requests.post(
      url,
      headers=headers,
      json=payload,
      timeout=30,
    )

    if response.status_code == 200:
      response_data = response.json()

      # The structure usually has an 'entries' key holding the actual config
      return response_data.get("entries")
    else:
      log_error("remote_config",
                f"Firebase Request Failed: {response.status_code} - {response.text}")
      return None

  except Exception as e:
    log_error("remote_config", f"Exception fetching remote config: {e}")
    return None


def get_provider_api_url():
  """
  Gets the provider API URL from Firebase Remote Config.
  Prioritizes 'cric_api2' then falls back to 'cric_api1'.
  """
  try_count = 1
  entries = None

  while try_count <= 3:
    entries = fetch_remote_config()
    if entries:
      break
    try_count += 1

  if not entries:
    return None

  return entries.get("cric_api2") or entries.get("cric_api1")


def get_api_urls():
  """
  Gets all available API URLs.
  :return: Tuple (api1, api2)
  """
  entries = fetch_remote_config()
  if not entries:
    return None

  return (entries.get("cric_api1"), entries.get("cric_api2"))
