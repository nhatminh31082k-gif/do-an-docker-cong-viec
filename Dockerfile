# Sử dụng Python image chính thức
FROM python:3.9

# Thiết lập thư mục làm việc
WORKDIR /app

# Copy và cài đặt thư viện
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code vào
COPY . .

# Mở port 5000
EXPOSE 5000

# Chạy ứng dụng
CMD ["python", "app.py"]