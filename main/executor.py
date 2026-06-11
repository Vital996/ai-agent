import subprocess
import tempfile
import os
from logger import logger

class CodeExecutor:
    def execute_bash(self, code, timeout=300):
        """Выполняет bash код"""
        try:
            result = subprocess.run(
                code,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                executable='/bin/bash'
            )
            return result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return '', 'Timeout exceeded'
        except Exception as e:
            return '', str(e)
    
    def execute_python(self, code, timeout=300):
        """Выполняет Python код"""
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                f.flush()
                
                result = subprocess.run(
                    ['python3', f.name],
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
                
                os.unlink(f.name)
                return result.stdout, result.stderr
                
        except subprocess.TimeoutExpired:
            return '', 'Timeout exceeded'
        except Exception as e:
            return '', str(e)
    
    def execute(self, code, lang='python'):
        """Выполняет код на указанном языке"""
        if lang == 'python':
            return self.execute_python(code)
        elif lang == 'bash':
            return self.execute_bash(code)
        else:
            return '', f'Language {lang} not supported'

executor = CodeExecutor()
