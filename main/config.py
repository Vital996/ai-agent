import os
from pathlib import Path

BASE_DIR = Path(os.path.expanduser('~/ai_agent'))
MAIN_DIR = BASE_DIR / 'main'
DATA_DIR = BASE_DIR / 'data'
LOGS_DIR = BASE_DIR / 'logs'
WEB_DIR = BASE_DIR / 'web'

ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', 'not-set')
GMAIL_EMAIL = 'smeyan.management@gmail.com'
GMAIL_APP_PASSWORD = os.environ.get('GMAIL_APP_PASSWORD', '')

PRICING = {'simple': 49, 'medium': 99, 'complex': 199}

CHECK_EMAIL_INTERVAL = 300
MAX_CONCURRENT_ORDERS = 3
ORDER_TIMEOUT = 14400

API_COST_INPUT = 3.0
API_COST_OUTPUT = 15.0

for d in [DATA_DIR, LOGS_DIR]:
    d.mkdir(parents=True, exist_ok=True)
