from pathlib import Path
import os
import requests
import base64
import json
from Crypto.Cipher import AES

CURRENT_DIR = Path(__file__).resolve().parent
CRICFY_PLUGIN_DIR = CURRENT_DIR / 'plugin.video.cricfy'
CRICFY_PLUGIN_RESOURCES_DIR = CRICFY_PLUGIN_DIR / 'resources'

CRICFY_URL_FILE_PATH = CRICFY_PLUGIN_RESOURCES_DIR / 'cricfy_url.txt'
FALLBACK_PROVIDERS_FILE_PATH = CRICFY_PLUGIN_RESOURCES_DIR / 'fallback_providers.json'
CRICFY_SECRET_FILE_PATH = CRICFY_PLUGIN_RESOURCES_DIR / 'secret.txt'


def fetch_encrypted_providers(url: str) -> str:
  try:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    if response.status_code != 200:
      print(f"Failed to fetch providers, status code: {response.status_code}")
      return ""
    return response.text
  except Exception as e:
    print(f"Failed to fetch providers: {e}")
    return ""


def decrypt_data(encrypted_base64: str, secret: str) -> str:
  try:
    clean_base64 = (
      encrypted_base64.strip()
      .replace("\n", "")
      .replace("\r", "")
      .replace(" ", "")
      .replace("\t", "")
    )

    # 1. Extract IV — reverse first 16 chars
    iv_raw = secret[:16][::-1]
    iv = iv_raw.encode("utf-8")

    # 2. Extract AES key — reverse substring from 11 to len - 1
    key_raw = secret[11:-1][::-1]
    key = key_raw.encode("iso-8859-1")

    # 3. Decode base64
    decoded = base64.b64decode(clean_base64)

    # 4. AES decrypt (CBC mode, PKCS5 padding)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(decoded)

    # 5. Handle padding
    pad_len = decrypted[-1]
    if pad_len <= 0 or pad_len > 16:
      # invalid padding
      return decrypted.decode("utf-8", errors="ignore").rstrip("\x00")
    plaintext = decrypted[:-pad_len]
    return plaintext.decode("utf-8", errors="ignore")

  except Exception as e:
    print(f"Decryption failed: {e}")
    return ""


def main():
  CRICFY_URL = os.getenv('CRICFY_URL')
  CRICFY_SECRET = os.getenv('CRICFY_SECRET')

  if not CRICFY_URL or not CRICFY_SECRET:
    raise Exception("CRICFY_URL and CRICFY_SECRET environment variables must be set.")

  content = fetch_encrypted_providers(CRICFY_URL)
  if not content:
    raise Exception("No content fetched from CRICFY_URL.")

  decrypted_content = decrypt_data(content, CRICFY_SECRET)
  if not decrypted_content:
    raise Exception("Decryption failed or returned empty content.")

  providers = json.loads(decrypted_content)

  with open(CRICFY_URL_FILE_PATH, 'w') as f:
    f.write(CRICFY_URL)

  with open(CRICFY_SECRET_FILE_PATH, 'w') as f:
    f.write(CRICFY_SECRET)

  with open(FALLBACK_PROVIDERS_FILE_PATH, 'w') as f:
    json.dump(providers, f, separators=(",", ":"))

  print("All Operations completed successfully.")


if __name__ == "__main__":
  main()
