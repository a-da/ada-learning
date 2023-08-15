"""
Keep here all env imports
"""
import os
from pathlib import Path

_value = os.getenv('ADA_LEARNING_GOOGLE_COM_CLIENT_SECRETS_FILE')
CLIENT_SECRETS_FILE = Path(_value).resolve() if _value else None

_value = os.environ['ADA_LEARNING_GOOGLE_COM_CONFIG']
assert _value, 'env ADA_LEARNING_GOOGLE_COM_CONFIG has to be a path'
CONFIG = Path(_value).resolve()
assert CONFIG.exists()

_value = os.getenv('ADA_LEARNING_GOOGLE_COM_TOKEN_JSON')
assert _value, 'env ADA_LEARNING_GOOGLE_COM_TOKEN_JSON has to be a path'
TOKEN_JSON = Path(_value).resolve()
