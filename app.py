from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from bson.objectid import ObjectId # Thêm dòng này để xử lý ID

app = Flask(__name__)

# Link kết nối của bạn (Giữ nguyên link Atlas của bạn nhé)
mongo_uri = "mongodb+srv://nhatminh31082k_db_user:pIH1UwtJ3RjGXdaB@cluster0.zhmxffs.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(mongo_uri)
db = client.task_db
tasks_collection = db.tasks

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/tasks', methods=['GET', 'POST'])
def handle_tasks():
    if request.method == 'POST':
        content = request.json.get('content')
        if content:
            tasks_collection.insert_one({'content': content})
            return jsonify({"status": "Thành công"})
    
    # Lấy thêm cả trường _id và chuyển nó về dạng chuỗi (string)
    all_tasks = []
    for task in tasks_collection.find():
        all_tasks.append({
            "id": str(task['_id']), 
            "content": task['content']
        })
    return jsonify(all_tasks)

# ROUTE MỚI: Dùng để xóa công việc
@app.route('/api/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    tasks_collection.delete_one({'_id': ObjectId(task_id)})
    return jsonify({"status": "Đã xóa"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)