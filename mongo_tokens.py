import os
import base64
import hashlib
from pymongo import MongoClient
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# load .env ONLY for local dev
load_dotenv()

# =========================
# ENCRYPTION SETUP
# =========================
SECRET_STRING = os.getenv("SECRET_ENCRYPTION_KEY")

if not SECRET_STRING:
    raise RuntimeError("❌ SECRET_ENCRYPTION_KEY not found in environment")

def derive_key(secret: str) -> bytes:
    digest = hashlib.sha256(secret.encode()).digest()
    return base64.urlsafe_b64encode(digest)

cipher = Fernet(derive_key(SECRET_STRING))

def decrypt_value(value: str) -> str:
    return cipher.decrypt(value.encode()).decode()

# =========================
# MONGO CONNECTION
# =========================
MONGO_URI = os.getenv("MONGO_URL")
DB_NAME   = os.getenv("MONGO_DB")
COL_NAME  = os.getenv("MONGO_COL")

if not MONGO_URI:
    raise RuntimeError("❌ MONGO_URL not found")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
col = db[COL_NAME]

# =========================
# FETCH + DECRYPT TOKEN
# =========================
def get_token(token_key: str) -> str:
    doc = col.find_one({"key": token_key})

    if not doc:
        raise RuntimeError(f"❌ Token not found in MongoDB: {token_key}")

    value = doc["value"]

    # decrypt only if encrypted
    if doc.get("encrypted", False):
        return decrypt_value(value)
    # fallback (in case of legacy plaintext)
    return value
