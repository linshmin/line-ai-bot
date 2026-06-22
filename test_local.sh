#!/bin/bash

# LINE AI 客服機器人 - 本地測試腳本

echo "========================================="
echo "  LINE AI 客服機器人 - 本地測試"
echo "========================================="
echo ""

# 檢查虛擬環境
if [ ! -d "venv" ]; then
    echo "創建虛擬環境..."
    python3 -m venv venv
fi

# 激活虛擬環境
source venv/bin/activate

# 安裝依賴
echo "安裝依賴..."
pip install -q -r requirements.txt

# 檢查環境變量
if [ ! -f .env ]; then
    echo "警告: .env 文件不存在"
    echo "複製 .env.example 到 .env 並填入必要的 API Keys"
    cp .env.example .env
    echo "請編輯 .env 文件並填入以下內容:"
    echo "  - LINE_CHANNEL_ACCESS_TOKEN"
    echo "  - LINE_CHANNEL_SECRET"
    echo "  - OPENAI_API_KEY"
    echo "  - REDIS_URL (本地測試可使用: redis://localhost:6379/0)"
    echo ""
    read -p "按 Enter 繼續..."
fi

# 啟動服務
echo ""
echo "啟動服務..."
echo "訪問地址: http://localhost:8000"
echo "API 文檔: http://localhost:8000/docs"
echo ""
echo "按 Ctrl+C 停止服務"
echo ""

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload