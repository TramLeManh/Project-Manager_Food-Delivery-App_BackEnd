FROM python:3.12-slim
# 0. Thiết lập biến môi trường để Python chạy chuẩn production
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1
# 1. Install system dependencies and pandoc
RUN apt-get update && apt-get install -y --no-install-recommends \
    pandoc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 2. Cài gói hệ thống cần thiết (nếu cần build deps)
RUN apt-get update && apt-get install -y --no-install-recommends build-essential curl && \
    rm -rf /var/lib/apt/lists/*

# 3. Tạo thư mục làm việc
WORKDIR /app

# 4. Copy file requirements trước (tối ưu layer cache)
COPY src/requirements.txt ./requirements.txt

# 5. Cài dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt


# 6. Expose port
EXPOSE 1412

# 7. Lệnh chạy (development hoặc simple production)
#File main.py locate at container: /app/main.py
CMD ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "1412"]
