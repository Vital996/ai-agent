import json
from threading import Lock
from pathlib import Path
from config import DATA_DIR
from logger import logger

class OrderQueue:
    def __init__(self):
        self.queue_file = DATA_DIR / 'orders.json'
        self.lock = Lock()
        self._init_file()
    
    def _init_file(self):
        if not self.queue_file.exists():
            self.queue_file.write_text('[]')
    
    def add(self, order):
        with self.lock:
            orders = self._read()
            orders.append(order)
            self._write(orders)
            logger.log_order(order['id'], 'queued', f"Subject: {order['subject']}")
    
    def get_next(self):
        with self.lock:
            orders = self._read()
            for order in orders:
                if order['status'] == 'new':
                    return order
            return None
    
    def get_all(self):
        with self.lock:
            return self._read()
    
    def update(self, order_id, status, result=None):
        with self.lock:
            orders = self._read()
            for order in orders:
                if order['id'] == order_id:
                    order['status'] = status
                    if result:
                        order['result'] = result
                    break
            self._write(orders)
            logger.log_order(order_id, status, f"Updated")
    
    def _read(self):
        try:
            return json.loads(self.queue_file.read_text())
        except:
            return []
    
    def _write(self, data):
        self.queue_file.write_text(json.dumps(data, indent=2))

queue = OrderQueue()
