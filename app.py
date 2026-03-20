from flask import Flask, request, jsonify, render_template
import os
from pymongo import MongoClient

app = Flask(__name__)

# Kết nối MongoDB qua mạng nội bộ của Docker Compose
# Kết nối MongoDB Atlas (Database trên mây)
mongo_uri = "mongodb+srv://nhatminh31082k_db_user:pIH1UwtJ3RjGXdaB@cluster0.zhmxffs.mongodb.net/task_db?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(mongo_uri)
db = client.task_db
tasks_collection = db.tasks

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/tasks', methods=['GET', 'POST'])
def handle_tasks():
    if request.method == 'POST':
        # Thêm công việc mới vào Database
        content = request.json.get('content')
        if content:
            tasks_collection.insert_one({'content': content})
            return jsonify({"status": "Thành công"})
        return jsonify({"status": "Lỗi"}), 400
    
    # GET: Lấy toàn bộ danh sách công việc từ Database để hiển thị
    all_tasks = list(tasks_collection.find({}, {'_id': 0}))
    return jsonify(all_tasks)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)