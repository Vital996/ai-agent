import logging
import json
from datetime import datetime
from pathlib import Path

class Logger:
    def __init__(self, log_dir):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Setup основного логгера
        logging.basicConfig(
            level=logging.INFO,
            format='[%(asctime)s] %(levelname)s: %(message)s',
            handlers=[
                logging.FileHandler(self.log_dir / 'agent.log'),
                logging.StreamHandler()
            ]
        )
        self.log = logging.getLogger('Agent')
    
    def info(self, msg):
        self.log.info(msg)
    
    def error(self, msg):
        self.log.error(msg)
    
    def log_order(self, order_id, status, msg):
        self.log.info(f"[ORDER {order_id}] {status}: {msg}")
    
    def log_finance(self, type_, amount, desc):
        entry = {
            'time': datetime.now().isoformat(),
            'type': type_,
            'amount': amount,
            'desc': desc
        }
        with open(self.log_dir / 'finance.log', 'a') as f:
            f.write(json.dumps(entry) + '\n')
        self.log.info(f"[${amount}] {type_}: {desc}")

from config import LOGS_DIR
logger = Logger(LOGS_DIR)
