import imaplib
import email
from datetime import datetime
from config import GMAIL_EMAIL, GMAIL_APP_PASSWORD, DATA_DIR
from logger import logger

class Gmail:
    def __init__(self):
        self.email = GMAIL_EMAIL
        self.password = GMAIL_APP_PASSWORD
    
    def fetch_orders(self):
        """Читает новые письма с заказами"""
        
        try:
            mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
            mail.login(self.email, self.password)
            mail.select('INBOX')
            
            status, msgs = mail.search(None, 'UNSEEN')
            
            if status != 'OK' or not msgs[0]:
                mail.close()
                return []
            
            orders = []
            for msg_id in msgs[0].split()[-10:]:  # последние 10
                status, data = mail.fetch(msg_id, '(RFC822)')
                msg = email.message_from_bytes(data[0][1])
                
                # Парсим
                order = {
                    'id': msg_id.decode(),
                    'time': datetime.now().isoformat(),
                    'from': msg.get('From', ''),
                    'subject': msg.get('Subject', ''),
                    'body': self._get_body(msg),
                    'status': 'new'
                }
                
                orders.append(order)
                logger.log_order(order['id'], 'received', f"From: {order['from']}")
                
                # Mark read
                mail.store(msg_id, '+FLAGS', '\\Seen')
            
            mail.close()
            return orders
            
        except Exception as e:
            logger.error(f"Gmail fetch failed: {str(e)}")
            return []
    
    def _get_body(self, msg):
        """Извлекает текст из письма"""
        body = ''
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = msg.get_payload(decode=True).decode()
        return body

gmail = Gmail()
