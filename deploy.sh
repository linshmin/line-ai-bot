#!/bin/bash

# LINE AI 客服機器人 - 雲端部署指南

echo "========================================="
echo "  LINE AI 客服機器人 - 雲端部署指南"
echo "========================================="
echo ""

# 檢查必要的環境變量
echo "步驟 1: 檢查環境變量配置"
echo "----------------------------------------"
if [ ! -f .env ]; then
    echo "❌ 錯誤: .env 文件不存在"
    echo "請先複製 .env.example 並填入必要的 API Keys:"
    echo "  cp .env.example .env"
    echo "  nano .env  # 編輯 .env 文件"
    exit 1
fi

source .env

# 檢查必要的環境變量
required_vars=("LINE_CHANNEL_ACCESS_TOKEN" "LINE_CHANNEL_SECRET" "OPENAI_API_KEY")
missing_vars=()

for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        missing_vars+=("$var")
    fi
done

if [ ${#missing_vars[@]} -gt 0 ]; then
    echo "❌ 錯誤: 缺少以下環境變量:"
    printf '%s\n' "${missing_vars[@]}"
    echo ""
    echo "請在 .env 文件中設置這些變量:"
    echo "  LINE_CHANNEL_ACCESS_TOKEN: 從 LINE Developers Console 獲取"
    echo "  LINE_CHANNEL_SECRET: 從 LINE Developers Console 獲取"
    echo "  OPENAI_API_KEY: 從 OpenAI 平台獲取"
    exit 1
fi

echo "✅ 環境變量檢查通過"
echo ""

# 提示部署選項
echo "步驟 2: 選擇部署平台"
echo "----------------------------------------"
echo "推薦選項:"
echo "  1. Render (推薦) - 免費層，自動 SSL，支持 Redis"
echo "  2. Railway - 免費層，簡單易用"
echo "  3. Fly.io - 免費層，全球部署"
echo ""
echo "請選擇部署平台 (1/2/3):"
read platform

case $platform in
    1)
        echo ""
        echo "步驟 3: 部署到 Render"
        echo "----------------------------------------"
        echo "1. 將代碼推送到 GitHub:"
        echo "   git init"
        echo "   git add ."
        echo "   git commit -m 'Initial commit: LINE AI客服機器人'"
        echo "   git branch -M main"
        echo "   git remote add origin https://github.com/YOUR_USERNAME/line-ai-bot.git"
        echo "   git push -u origin main"
        echo ""
        echo "2. 訪問 https://render.com 並註冊/登錄"
        echo ""
        echo "3. 創建新的 Web Service:"
        echo "   - Name: line-ai-bot"
        echo "   - Environment: Python 3"
        echo "   - Build Command: pip install -r requirements.txt"
        echo "   - Start Command: uvicorn app.main:app --host 0.0.0.0 --port \$PORT"
        echo ""
        echo "4. 連接 GitHub 倉庫並選擇 render.yaml 配置"
        echo ""
        echo "5. 添加環境變量 (在 Render Dashboard 中):"
        echo "   - LINE_CHANNEL_ACCESS_TOKEN=$LINE_CHANNEL_ACCESS_TOKEN"
        echo "   - LINE_CHANNEL_SECRET=$LINE_CHANNEL_SECRET"
        echo "   - OPENAI_API_KEY=$OPENAI_API_KEY"
        echo "   - REDIS_URL: (Render 會自動提供 Redis URL)"
        echo ""
        echo "6. 部署完成後，獲取公開 URL"
        echo "   例如: https://line-ai-bot.onrender.com"
        echo ""
        echo "7. 設置 LINE Webhook:"
        echo "   - 訪問 LINE Developers Console"
        echo "   - 選擇您的 Messaging API channel"
        echo "   - 設置 Webhook URL: https://line-ai-bot.onrender.com/webhook"
        echo "   - 啟用 'Use webhook'"
        echo ""
        echo "✅ 部署完成！"
        ;;
    2)
        echo ""
        echo "步驟 3: 部署到 Railway"
        echo "----------------------------------------"
        echo "1. 將代碼推送到 GitHub (同上)"
        echo ""
        echo "2. 訪問 https://railway.app 並註冊/登錄"
        echo ""
        echo "3. 創建新專案並連接 GitHub 倉庫"
        echo ""
        echo "4. 添加環境變量:"
        echo "   - LINE_CHANNEL_ACCESS_TOKEN"
        echo "   - LINE_CHANNEL_SECRET"
        echo "   - OPENAI_API_KEY"
        echo "   - REDIS_URL: (添加 Redis 服務)"
        echo ""
        echo "5. 部署完成後，獲取公開 URL"
        echo ""
        echo "6. 設置 LINE Webhook (同上)"
        echo ""
        echo "✅ 部署完成！"
        ;;
    3)
        echo ""
        echo "步驟 3: 部署到 Fly.io"
        echo "----------------------------------------"
        echo "1. 安裝 Fly CLI:"
        echo "   curl -L https://fly.io/install.sh | sh"
        echo ""
        echo "2. 登錄 Fly:"
        echo "   fly auth signup"
        echo "   fly auth login"
        echo ""
        echo "3. 初始化應用:"
        echo "   fly launch"
        echo ""
        echo "4. 添加 Redis:"
        echo "   fly redis create"
        echo ""
        echo "5. 設置環境變量:"
        echo "   fly secrets set LINE_CHANNEL_ACCESS_TOKEN=$LINE_CHANNEL_ACCESS_TOKEN"
        echo "   fly secrets set LINE_CHANNEL_SECRET=$LINE_CHANNEL_SECRET"
        echo "   fly secrets set OPENAI_API_KEY=$OPENAI_API_KEY"
        echo "   fly secrets set REDIS_URL=<your-redis-url>"
        echo ""
        echo "6. 部署:"
        echo "   fly deploy"
        echo ""
        echo "7. 設置 LINE Webhook (同上)"
        echo ""
        echo "✅ 部署完成！"
        ;;
    *)
        echo "❌ 無效選項"
        exit 1
        ;;
esac

echo ""
echo "步驟 4: 測試機器人"
echo "----------------------------------------"
echo "1. 在 LINE 中搜尋您的 LINE Official Account"
echo "2. 發送測試消息:"
echo "   - 你好"
echo "   - 客服時間"
echo "   - 退貨政策"
echo "   - 付款方式"
echo "   - 配送方式"
echo "   - 技術支援"
echo ""
echo "3. 驗證機器人回應:"
echo "   - 應該有智能回覆"
echo "   - 應該有快速回覆按鈕"
echo "   - 應該記住對話上下文"
echo ""
echo "========================================="
echo "  部署指南完成！"
echo "========================================="
echo ""
echo "常見問題:"
echo "  Q: 如何修改機器人的回覆風格?"
echo "  A: 修改 app/main.py 中的 system_prompt 變量"
echo ""
echo "  Q: 如何添加更多知識庫內容?"
echo "  A: 編輯 data/knowledge_base/knowledge.json 文件"
echo ""
echo "  Q: 如何更換 AI 模型?"
echo "  A: 修改 app/ai_handler.py 中的 model 參量"
echo ""
echo "  Q: 如何查看日誌?"
echo "  A: Render: 在 Dashboard 中查看 Logs"
echo "     Railway: 在專案頁面查看 Logs"
echo "     Fly.io: 使用 'fly logs' 命令"
echo ""
echo "詳細文檔請參考 README.md"
echo ""