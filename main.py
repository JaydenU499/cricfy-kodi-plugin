from pathlib import Path
import os
import json

CURRENT_DIR = Path(__file__).resolve().parent
CRICFY_PLUGIN_DIR = CURRENT_DIR / 'plugin.video.cricfy'
CRICFY_PLUGIN_RESOURCES_DIR = CRICFY_PLUGIN_DIR / 'resources'

CRICFY_SECRET_FILE_PATH = CRICFY_PLUGIN_RESOURCES_DIR / 'secret.txt'
CRICFY_PROPERTIES_FILE_PATH = CRICFY_PLUGIN_RESOURCES_DIR / 'cricfy_properties.json'


def main():
  CRICFY_FIREBASE_API_KEY = os.getenv('CRICFY_FIREBASE_API_KEY')
  CRICFY_FIREBASE_APP_ID = os.getenv('CRICFY_FIREBASE_APP_ID')
  CRICFY_PACKAGE_NAME = os.getenv('CRICFY_PACKAGE_NAME')
  CRICFY_SECRET = os.getenv('CRICFY_SECRET')

  if not CRICFY_FIREBASE_API_KEY or not CRICFY_FIREBASE_APP_ID or not CRICFY_PACKAGE_NAME or not CRICFY_SECRET:
    raise Exception("Required environment variables not set.")

  with open(CRICFY_SECRET_FILE_PATH, 'w') as f:
    f.write(CRICFY_SECRET)

  cricfy_properties = {
    "cricfy_firebase_api_key": CRICFY_FIREBASE_API_KEY,
    "cricfy_firebase_app_id": CRICFY_FIREBASE_APP_ID,
    "cricfy_package_name": CRICFY_PACKAGE_NAME
  }
  with open(CRICFY_PROPERTIES_FILE_PATH, 'w') as f:
    json.dump(cricfy_properties, f, separators=(',', ':'))

  print("All Operations completed successfully.")


if __name__ == "__main__":
  main()
