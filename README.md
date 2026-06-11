# 🤖 Autonomous AI Agent

Полностью автономный ИИ-агент для выполнения заказов. Читает email, выполняет задачи через Claude API, 24/7 работает на Termux.

## 🚀 Возможности

- 📬 Email Monitoring — проверяет почту каждые 5 минут
- 🔄 Parallel Processing — выполняет несколько заказов одновременно
- 🤖 Claude Integration — использует Claude API для решения задач
- 💾 Task Queue — управляет очередью заказов
- 💰 Finance Tracking — отслеживает доход и расходы
- 📊 Logging — полное логирование всех операций

## 📋 Структура

ai_agent/
├── main/
│   ├── agent.py
│   ├── config.py
│   ├── claude_api.py
│   ├── mailbox.py
│   ├── order_queue.py
│   ├── executor.py
│   └── logger.py
├── portfolio/
│   ├── youtube_downloader.py
│   ├── web_scraper_example.py
│   └── flask_app_example.py
├── data/
├── logs/
└── requirements.txt

## 🛠️ Установка

pip install -r requirements.txt --break-system-packages

## 🚀 Запуск

export ANTHROPIC_API_KEY="sk-ant-api03-your-key"
export GMAIL_APP_PASSWORD="your-gmail-app-password"
cd ~/ai_agent/main
python3 agent.py

## 💼 Примеры услуг

YouTube Downloader - скачивание музыки ($49-99)
Web Scraper - парсинг данных ($79-149)
Flask API - REST приложения ($99-199)
Python Scripts - автоматизация ($49-99)

## 📧 Контакт

Email: smeyan.management@gmail.com

Status: Ready for production
