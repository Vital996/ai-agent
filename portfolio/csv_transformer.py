#!/usr/bin/env python3
"""CSV Data Transformer - удаляет дубликаты, очищает, трансформирует"""
import csv
from pathlib import Path
from datetime import datetime

def transform_csv(input_file='data.csv'):
    print("📊 CSV Data Transformer")
    print("=" * 50)
    
    try:
        rows = []
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        print(f"📥 Loaded: {len(rows)} rows")
        
        # Удаляем дубликаты
        unique_rows = []
        seen = set()
        
        for row in rows:
            row_tuple = tuple(row.values())
            if row_tuple not in seen:
                unique_rows.append(row)
                seen.add(row_tuple)
        
        print(f"🔄 Removed duplicates: {len(rows) - len(unique_rows)}")
        
        # Фильтруем пустые
        clean_rows = [r for r in unique_rows if any(r.values())]
        
        # Сохраняем
        output_file = f"data_clean_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        if clean_rows:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=clean_rows[0].keys())
                writer.writeheader()
                writer.writerows(clean_rows)
            
            print(f"\n✅ Output: {output_file}")
            print(f"📈 Final rows: {len(clean_rows)}")
        
        return True
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == '__main__':
    transform_csv('data.csv')
