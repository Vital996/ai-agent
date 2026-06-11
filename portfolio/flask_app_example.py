#!/usr/bin/env python3
"""
Simple Flask Web Application
REST API для выполнения задач
"""
from flask import Flask, jsonify, request
from datetime import datetime
import json

app = Flask(__name__)

# Простое хранилище задач в памяти
tasks = []

@app.route('/')
def home():
    """Главная страница"""
    return jsonify({
        'status': 'online',
        'message': 'Task Executor API',
        'endpoints': {
            'GET /tasks': 'Get all tasks',
            'POST /task': 'Create new task',
            'GET /task/<id>': 'Get task by ID',
            'DELETE /task/<id>': 'Delete task'
        }
    })

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Получить все задачи"""
    return jsonify({
        'count': len(tasks),
        'tasks': tasks
    })

@app.route('/task', methods=['POST'])
def create_task():
    """Создать новую задачу"""
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({'error': 'Missing title'}), 400
    
    task = {
        'id': len(tasks) + 1,
        'title': data['title'],
        'description': data.get('description', ''),
        'status': 'pending',
        'created_at': datetime.now().isoformat()
    }
    
    tasks.append(task)
    return jsonify(task), 201

@app.route('/task/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Получить задачу по ID"""
    task = next((t for t in tasks if t['id'] == task_id), None)
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify(task)

@app.route('/task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Удалить задачу"""
    global tasks
    tasks = [t for t in tasks if t['id'] != task_id]
    return jsonify({'message': 'Task deleted'}), 200

@app.route('/stats', methods=['GET'])
def get_stats():
    """Статистика"""
    return jsonify({
        'total_tasks': len(tasks),
        'pending': len([t for t in tasks if t['status'] == 'pending']),
        'completed': len([t for t in tasks if t['status'] == 'completed'])
    })

if __name__ == '__main__':
    print("🚀 Flask App Starting...")
    print("=" * 50)
    print("📍 http://localhost:5000")
    print("📝 API Documentation at http://localhost:5000/")
    print("=" * 50)
    app.run(debug=True, host='localhost', port=5000)
