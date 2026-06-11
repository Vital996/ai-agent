#!/usr/bin/env python3
import time
import threading
from datetime import datetime
from config import CHECK_EMAIL_INTERVAL, MAX_CONCURRENT_ORDERS
from logger import logger
from mailbox import gmail
from order_queue import queue
from claude_api import claude
from executor import executor

class AutonomousAgent:
    def __init__(self):
        self.running = True
        self.active_orders = {}
        self.lock = threading.Lock()
        logger.info("="*50)
        logger.info("AUTONOMOUS AI AGENT STARTED")
        logger.info("="*50)
    
    def check_emails(self):
        while self.running:
            try:
                orders = gmail.fetch_orders()
                for order in orders:
                    queue.add(order)
                if orders:
                    logger.info(f"Found {len(orders)} new orders")
            except Exception as e:
                logger.error(f"Email check failed: {str(e)}")
            time.sleep(CHECK_EMAIL_INTERVAL)
    
    def process_orders(self):
        while self.running:
            try:
                with self.lock:
                    active_count = len(self.active_orders)
                if active_count >= MAX_CONCURRENT_ORDERS:
                    time.sleep(10)
                    continue
                order = queue.get_next()
                if not order:
                    time.sleep(10)
                    continue
                thread = threading.Thread(target=self._execute_order, args=(order,))
                thread.daemon = True
                thread.start()
                with self.lock:
                    self.active_orders[order['id']] = thread
            except Exception as e:
                logger.error(f"Order processing error: {str(e)}")
                time.sleep(5)
    
    def _execute_order(self, order):
        order_id = order['id']
        try:
            logger.log_order(order_id, 'processing', 'Started')
            queue.update(order_id, 'processing')
            task_prompt = f"""Client order:
Subject: {order['subject']}
Message: {order['body']}

Write ready-to-run code solution. Code only, no explanation."""
            logger.log_order(order_id, 'analyzing', 'Asking Claude...')
            solution = claude.ask(task_prompt)
            if not solution:
                raise Exception("Failed to get solution")
            output = ''
            stderr = ''
            if '```python' in solution:
                code = solution.split('```python')[1].split('```')[0]
                logger.log_order(order_id, 'executing', 'Running Python...')
                output, stderr = executor.execute_python(code)
            elif '```bash' in solution:
                code = solution.split('```bash')[1].split('```')[0]
                logger.log_order(order_id, 'executing', 'Running Bash...')
                output, stderr = executor.execute_bash(code)
            result = {'solution': solution, 'output': output, 'errors': stderr, 'completed_at': datetime.now().isoformat()}
            queue.update(order_id, 'completed', result)
            logger.log_order(order_id, 'completed', 'Success')
            logger.log_finance('income', 99, f'Order {order_id} completed')
        except Exception as e:
            logger.error(f"Order {order_id} failed: {str(e)}")
            queue.update(order_id, 'failed', {'error': str(e)})
        finally:
            with self.lock:
                if order_id in self.active_orders:
                    del self.active_orders[order_id]
    
    def start(self):
        email_thread = threading.Thread(target=self.check_emails, daemon=True)
        email_thread.start()
        logger.info("Email checker started")
        order_thread = threading.Thread(target=self.process_orders, daemon=True)
        order_thread.start()
        logger.info("Order processor started")
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Agent stopping...")
            self.running = False

if __name__ == '__main__':
    agent = AutonomousAgent()
    agent.start()
