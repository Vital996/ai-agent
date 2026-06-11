#!/usr/bin/env python3
"""Batch File Processor - переименовывает/обрабатывает 1000 файлов сразу"""
import os
from pathlib import Path
from datetime import datetime

def process_files(directory='.', operation='rename'):
    print("📂 Batch File Processor")
    print("=" * 50)
    
    files = [f for f in Path(directory).glob('*') if f.is_file()]
    
    if not files:
        print("❌ No files found")
        return
    
    print(f"📊 Found {len(files)} files")
    processed = 0
    
    for file in files:
        try:
            if operation == 'rename':
                new_name = file.name.upper()
                new_path = file.parent / new_name
                file.rename(new_path)
                print(f"✅ {file.name} → {new_name}")
                processed += 1
            
            elif operation == 'add_timestamp':
                timestamp = datetime.now().strftime('%Y%m%d')
                new_name = f"{file.stem}_{timestamp}{file.suffix}"
                new_path = file.parent / new_name
                file.rename(new_path)
                print(f"✅ {file.name} → {new_name}")
                processed += 1
        
        except Exception as e:
            print(f"❌ {file.name}: {str(e)}")
    
    print(f"\n✅ Processed: {processed}/{len(files)} files")

if __name__ == '__main__':
    process_files('.', 'rename')
