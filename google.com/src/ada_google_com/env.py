"""
Keep here all env imports
"""
import os
import sys
from pathlib import Path

# secret file is required for generate the token file
_value = os.getenv('ADA_LEARNING_GOOGLE_COM_CLIENT_SECRETS_FILE')
CLIENT_SECRETS_FILE = Path(_value).resolve() if _value else None

# config
_value = os.environ['ADA_LEARNING_GOOGLE_COM_CONFIG']
assert _value, 'env ADA_LEARNING_GOOGLE_COM_CONFIG has to be a path'
if not _value:
    sys.exit("Empty env ``ADA_LEARNING_GOOGLE_COM_CONFIG``, expected to be a path")

CONFIG = Path(_value).resolve()
if not CONFIG.exists():
    sys.exit(f"Env ``ADA_LEARNING_GOOGLE_COM_CONFIG`` path '{CONFIG}' does not exists")

# token
_value = os.getenv('ADA_LEARNING_GOOGLE_COM_TOKEN_JSON')
if not _value:
    sys.exit("Empty env ``ADA_LEARNING_GOOGLE_COM_TOKEN_JSON``, expected to be a path")

TOKEN_JSON = Path(_value).resolve()
