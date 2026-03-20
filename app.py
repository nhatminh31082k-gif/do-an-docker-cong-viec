from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)

# KẾT NỐI MONGODB ATLAS (Thay mật khẩu của bạn vào chỗ pIH1UwtJ3RjGXdaB nếu cần)
mongo_uri = "mongodb+srv://nhatminh31082k_db_user:pIH1UwtJ3RjGXdaB@cluster0.zhmxffs.mongodb.net/task_db?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(mongo_uri)
db = client.task_db
tasks_collection = db.tasks

@app.route('/')
def home():
    return render_template('index.html')

# Lấy danh sách và Thêm công việc
@app.route('/api/tasks', methods=['GET', 'POST'])
def handle_tasks():
    if request.method == 'POST':
        data = request.json
        content = data.get('content')
        description = data.get('description', '')
        priority = data.get('priority', 'Normal')
        if content:
            tasks_collection.insert_one({
                'content': content, 
                'description': description,
                'priority': priority,
                'completed': False
            })
            return jsonify({"status": "Success"})
    
    all_tasks = []
    for task in tasks_collection.find():
        all_tasks.append({
            "id": str(task['_id']), 
            "content": task['content'],
            "description": task.get('description', ''),
            "priority": task.get('priority', 'Normal'),
            "completed": task.get('completed', False)
        })
    return jsonify(all_tasks)

# Đảo ngược trạng thái hoàn thành (Check/Uncheck)
@app.route('/api/tasks/<task_id>/toggle', methods=['PATCH'])
def toggle_task(task_id):
    task = tasks_collection.find_one({'_id': ObjectId(task_id)})
    if task:
        new_status = not task.get('completed', False)
        tasks_collection.update_one({'_id': ObjectId(task_id)}, {'$set': {'completed': new_status}})
    return jsonify({"status": "Updated"})

# Xóa công việc
@app.route('/api/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    tasks_collection.delete_one({'_id': ObjectId(task_id)})
    return jsonify({"status": "Deleted"})

if __name__ == '__main__':
    # Chạy trên cổng 5000 cho Docker
    app.run(host='0.0.0.0', port=5000)