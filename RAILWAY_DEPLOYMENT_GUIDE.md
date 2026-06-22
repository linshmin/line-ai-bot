# Railway 雲端部署快速指南 🚀

## 📋 前置準備

### ✅ 已完成
- [x] LINE AI 客服機器人代碼已創建
- [x] 代碼已推送到 GitHub: https://github.com/linshmin/line-ai-bot
- [x] 所有部署配置文件已準備好

### 📝 需要準備的資訊
1. **LINE Developers Console 帳號**
   - LINE Channel Access Token
   - LINE Channel Secret
2. **OpenAI API Key**
3. **GitHub 帳號** (已完成連接)

---

## 🚀 Railway 部署步驟（5分鐘完成）

### 第一步：註冊 Railway ⭐ 不需要信用卡

1. 訪問 [https://railway.app](https://railway.app)
2. 點擊 "Start a New Project" 或 "Sign Up"
3. 使用 **GitHub 帳號**登錄（推薦）
4. Railway 會要求授權訪問您的 GitHub 倉庫
5. **不需要提供信用卡** ✅

### 第二步：連接 GitHub 倉庫

1. 登錄後，點擊 "New Project" 按鈕
2. 選擇 "Deploy from GitHub repo"
3. 搜索您的倉庫：`linshmin/line-ai-bot`
4. 點擊 "Import" 或 "Connect" 按鈕
5. Railway 會自動檢測您的 Python 專案

### 第三步：配置專案

Railway 會自動檢測配置，您需要確認：

**自動檢測的配置：**
- ✅ 專案類型：Python
- ✅ 建置命令：`pip install -r requirements.txt`
- ✅ 啟動命令：`gunicorn app.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`
- ✅ 區域：自動選擇

**需要手動添加的配置：**

1. **添加環境變量**
   - 在專案頁面，點擊 "Variables" 頁籤
   - 點擊 "New Variable"
   - 逐個添加以下變量：

#### 🔑 必需的環境變量：

| 變量名稱 | 說明 | 獲取方式 |
|---------|------|---------|
| `LINE_CHANNEL_ACCESS_TOKEN` | LINE 訊息 API 存取權杖 | LINE Developers Console |
| `LINE_CHANNEL_SECRET` | LINE 頻道密鑰 | LINE Developers Console |
| `OPENAI_API_KEY` | OpenAI API 金鑰 | OpenAI 平台 |

#### 📌 如何獲取這些金鑰：

**1. LINE Channel Access Token & Secret:**
- 訪問 [LINE Developers Console](https://developers.line.biz/console/)
- 登錄您的 LINE 帳號
- 創建或選擇一個 Messaging API 頻道
- 在 "Messaging API" 頁籤中：
  - **Channel Secret**: 在頁面頂部顯示
  - **Channel Access Token**: 點擊 "Issue" 按鈕生成（記得複製保存）

**2. OpenAI API Key:**
- 訪問 [OpenAI Platform](https://platform.openai.com/)
- 登錄您的帳號
- 點擊右上角頭像 → "API Keys"
- 點擊 "Create new secret key"
- 複製並保存 API Key（只顯示一次）

### 第四步：添加 Redis 服務

1. 在專案頁面，點擊 "New Service" 按鈕
2. 選擇 "Database" → "Redis"
3. Railway 會自動創建一個 Redis 實例
4. 創建完成後，Redis 會自動提供連接資訊

**重要：** Railway 會自動設置 `REDIS_URL` 環境變量，您不需要手動添加！

### 第五步：部署應用程式

1. 確認所有配置正確
2. 點擊 "Deploy" 按鈕
3. Railway 會開始部署流程：
   - 構建應用程式
   - 安裝依賴套件
   - 啟動服務
4. 部署大約需要 1-3 分鐘
5. 部署完成後，您會看到一個公開 URL，例如：
   - `https://line-ai-bot-production.up.railway.app`

### 第六步：配置 LINE Webhook

1. 訪問 [LINE Developers Console](https://developers.line.biz/console/)
2. 選擇您的 Messaging API 頻道
3. 點擊 "Messaging API" 頁籤
4. 找到 "Webhook settings" 部分
5. 設置 Webhook URL：
   ```
   https://line-ai-bot-production.up.railway.app/webhook
   ```
   （將 `line-ai-bot-production` 替換為您的實際應用程式名稱）
6. 點擊 "Verify" 按鈕驗證 URL
7. 確保 "Use webhook" 選項已開啟
8. 點擊 "Save"

### 第七步：測試機器人

1. 打開 LINE 應用程式
2. 搜索您的 LINE Official Account
3. 發送測試訊息：
   - "你好" - 測試基本對話
   - "客服時間" - 測試知識庫查詢
   - "退貨政策" - 測試知識庫查詢
   - "付款方式" - 測試知識庫查詢
4. 觀察機器人是否正確回應
5. 檢查快速回覆按鈕是否顯示

---

## 🎉 完成！

恭喜！您的 LINE AI 客服機器人已成功部署到 Railway 雲端。

### 📊 Railway 免費額度說明

- **每月免費額度**: $5 USD
- **預估使用量**:
  - Web Service: 大約 $2-3/月
  - Redis: 大約 $1-2/月
  - **總計**: 大約 $3-5/月（完全在免費額度內）

### ✅ Railway 的優點

1. ✅ **不需要信用卡**
2. ✅ **免費額度足夠**
3. ✅ **部署速度快**（1-3分鐘）
4. ✅ **自動部署**（推送到 GitHub 自動部署）
5. ✅ **支援 Redis**
6. ✅ **自動 SSL**

---

## 🛠️ 故障排除

### 部署失敗

**問題：構建錯誤**
```
Error: Could not find a version that satisfies the requirement
```
**解決方案：**
- 檢查 `requirements.txt` 中的套件版本
- 確保使用 `>=` 版本號而非固定版本

**問題：啟動錯誤**
```
Error: ModuleNotFoundError: No module named 'app'
```
**解決方案：**
- 確保 `Procfile` 中的路徑正確
- 檢查目錄結構是否完整

### Webhook 驗證失敗

**問題：Webhook URL 驗證失敗**
```
Webhook URL is invalid
```
**解決方案：**
1. 確保應用程式已成功部署
2. 檢查 URL 是否正確（包含 `/webhook`）
3. 確認環境變量已正確設置
4. 查看 Railway Dashboard 的 Logs

### 機器人無回應

**問題：發送訊息後沒有回應**
**解決方案：**
1. 檢查 Railway Dashboard 的 Logs
2. 確認環境變量設置正確
3. 驗證 LINE Channel Access Token 和 Secret
4. 檢查 OpenAI API Key 是否有效
5. 確認 Redis 連接正常

---

## 📊 監控與維護

### 查看 Logs

1. 在 Railway Dashboard 點擊您的專案
2. 點擊 Web Service
3. 點擊 "Logs" 頁籤
4. 即時查看應用程式日誌

### 更新應用程式

1. 在本地修改代碼
2. 提交並推送到 GitHub：
   ```bash
   git add .
   git commit -m "更新描述"
   git push origin master
   ```
3. Railway 會自動檢測並重新部署

### 更新知識庫

1. 編輯 `data/knowledge_base/knowledge.json`
2. 提交並推送更改
3. Railway 會自動重新部署

---

## 💡 優化建議

### 1. 降低資源使用
- 使用 GPT-4o-mini（最便宜的模型）
- 減少對話記憶的存儲時間
- 優化知識庫查詢

### 2. 提升回應速度
- 使用 Redis 快取常見問題的答案
- 實施請求佇列處理

### 3. 增強功能
- 添加用戶分析
- 實施多語言支援
- 添加圖片識別功能

---

## 🔐 安全建議

1. **不要將敏感資訊提交到 Git**
   - `.env` 文件已在 `.gitignore` 中
   - 永遠不要提交 API 金鑰

2. **定期更新依賴套件**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

3. **監控資源使用**
   - 定期查看 Railway Dashboard
   - 確保不會超過免費額度

---

## 📞 支援資源

- **Railway 文檔**: https://docs.railway.app/
- **LINE Developers 文檔**: https://developers.line.biz/docs/
- **OpenAI API 文檔**: https://platform.openai.com/docs
- **FastAPI 文檔**: https://fastapi.tiangolo.com/

---

## ✅ 部署檢查清單

部署前確認：
- [ ] 所有代碼已推送到 GitHub
- [ ] `requirements.txt` 包含所有依賴
- [ ] 已準備好 LINE Channel Access Token 和 Secret
- [ ] 已準備好 OpenAI API Key

部署中確認：
- [ ] Railway 帳號已創建並登錄
- [ ] GitHub 倉庫已連接
- [ ] 環境變量已設置
- [ ] Redis 服務已添加

部署後確認：
- [ ] 應用程式成功啟動
- [ ] 公開 URL 可訪問
- [ ] LINE Webhook 已設置並驗證
- [ ] 機器人可以正常回應訊息
- [ ] 知識庫查詢功能正常
- [ ] 快速回覆按鈕正常顯示

---

**祝您部署成功！🎉**

如有任何問題，請隨時查看 Railway Dashboard 的 Logs 或參考故障排除部分。

**特別提醒：** Railway 不需要信用卡，免費額度足夠運行您的 LINE AI 機器人！