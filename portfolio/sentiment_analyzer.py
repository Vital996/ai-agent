#!/usr/bin/env python3
"""
Sentiment Analysis Tool
Анализирует отзывы/комментарии на эмоции: позитив/негатив/нейтраль
"""
import csv
from datetime import datetime

class SentimentAnalyzer:
    def __init__(self):
        # Простой словарь позитивных и негативных слов
        self.positive_words = {
            'good', 'great', 'excellent', 'amazing', 'love', 'best', 'awesome',
            'wonderful', 'fantastic', 'brilliant', 'perfect', 'brilliant', 'nice',
            'хороший', 'отличный', 'классный', 'супер', 'прекрасный', 'замечательный'
        }
        
        self.negative_words = {
            'bad', 'terrible', 'awful', 'hate', 'worst', 'horrible', 'poor',
            'disgusting', 'useless', 'broken', 'fail', 'error', 'issue',
            'плохой', 'ужасный', 'отвратительный', 'тупой', 'хрень', 'говно'
        }
    
    def analyze_sentiment(self, text):
        """Анализирует тон текста"""
        
        text_lower = text.lower()
        words = text_lower.split()
        
        positive_count = sum(1 for word in words if word in self.positive_words)
        negative_count = sum(1 for word in words if word in self.negative_words)
        
        if positive_count > negative_count:
            return 'positive', positive_count
        elif negative_count > positive_count:
            return 'negative', negative_count
        else:
            return 'neutral', 0
    
    def analyze_file(self, input_file='reviews.csv'):
        """Анализирует CSV файл с отзывами"""
        
        print("💬 Sentiment Analysis Tool")
        print("=" * 60)
        print(f"Input: {input_file}")
        print()
        
        try:
            reviews = []
            with open(input_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                reviews = list(reader)
            
            print(f"📥 Loaded: {len(reviews)} reviews")
            print()
            
            results = []
            stats = {'positive': 0, 'negative': 0, 'neutral': 0}
            
            for review in reviews:
                if 'text' not in review:
                    continue
                
                sentiment, score = self.analyze_sentiment(review['text'])
                stats[sentiment] += 1
                
                result = {
                    'text': review['text'][:100],
                    'sentiment': sentiment,
                    'score': score,
                    'analyzed_at': datetime.now().isoformat()
                }
                results.append(result)
            
            # Сохраняем результаты
            output_file = f"sentiment_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['text', 'sentiment', 'score', 'analyzed_at'])
                writer.writeheader()
                writer.writerows(results)
            
            # Статистика
            total = len(results)
            print("📊 Results:")
            print("-" * 60)
            print(f"✅ Positive: {stats['positive']} ({stats['positive']/total*100:.1f}%)")
            print(f"❌ Negative: {stats['negative']} ({stats['negative']/total*100:.1f}%)")
            print(f"➖ Neutral:  {stats['neutral']} ({stats['neutral']/total*100:.1f}%)")
            print()
            
            print("📋 Sample Analysis:")
            print("-" * 60)
            for i, result in enumerate(results[:5], 1):
                emoji = "✅" if result['sentiment'] == 'positive' else "❌" if result['sentiment'] == 'negative' else "➖"
                print(f"{i}. {emoji} [{result['sentiment'].upper()}] {result['text']}...")
                print()
            
            print("-" * 60)
            print(f"📈 Total analyzed: {total} reviews")
            print(f"💾 Saved to: {output_file}")
            
            return True
        
        except FileNotFoundError:
            print(f"❌ File not found: {input_file}")
            print()
            print("📝 Creating demo file with sample reviews...")
            
            # Создаём демо файл
            demo_reviews = [
                ['text', 'author'],
                ['This product is absolutely amazing! Love it!', 'John'],
                ['Terrible quality, waste of money', 'Sarah'],
                ['It works fine, nothing special', 'Mike'],
                ['Best purchase ever, highly recommend!', 'Lisa'],
                ['Broke after one week, very disappointed', 'Tom'],
            ]
            
            with open('reviews.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(demo_reviews)
            
            print("✅ Created reviews.csv")
            print()
            
            # Анализируем демо
            return self.analyze_file('reviews.csv')
        
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False

if __name__ == '__main__':
    analyzer = SentimentAnalyzer()
    analyzer.analyze_file('reviews.csv')
