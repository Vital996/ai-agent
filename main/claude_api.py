import requests
from config import ANTHROPIC_API_KEY, API_COST_INPUT, API_COST_OUTPUT
from logger import logger

class ClaudeAPI:
    def __init__(self):
        self.key = ANTHROPIC_API_KEY
        self.url = 'https://api.anthropic.com/v1/messages'
        self.model = 'claude-3-5-sonnet-latest'
    
    def ask(self, prompt, max_tokens=2000):
        """Спрашивает Claude как выполнить задачу"""
        
        if not self.key or self.key == 'not-set':
            logger.error("API key not set!")
            return None
        
        headers = {
            'x-api-key': self.key,
            'anthropic-version': '2023-06-01',
            'content-type': 'application/json'
        }
        
        data = {
            'model': self.model,
            'max_tokens': max_tokens,
            'messages': [{'role': 'user', 'content': prompt}]
        }
        
        try:
            r = requests.post(self.url, headers=headers, json=data, timeout=60)
            result = r.json()
            
            if 'error' in result:
                logger.error(f"Claude error: {result['error']['message']}")
                return None
            
            text = result['content'][0]['text']
            
            # Log API cost
            input_tokens = result['usage']['input_tokens']
            output_tokens = result['usage']['output_tokens']
            cost = (input_tokens / 1e6) * API_COST_INPUT + (output_tokens / 1e6) * API_COST_OUTPUT
            logger.log_finance('expense', cost, f'Claude API (in:{input_tokens} out:{output_tokens})')
            
            return text
            
        except Exception as e:
            logger.error(f"Claude request failed: {str(e)}")
            return None

claude = ClaudeAPI()
