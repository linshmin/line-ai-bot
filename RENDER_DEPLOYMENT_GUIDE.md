# Render 雲端部署詳細指南

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

## 🚀 Render 部署步驟

### 第一步：註冊/登錄 Render

1. 訪問 [https://render.com](https://render.com)
2. 點擊右上角的 "Sign Up" 或 "Login"
3. 使用 GitHub 帳號登錄（推薦，因為我們的代碼在 GitHub）
4. 如果是第一次使用，Render 會要求授權訪問您的 GitHub 倉庫

### 第二步：連接 GitHub 倉庫

1. 登錄後，點擊 Dashboard 上的 "New +" 按鈕
2. 選擇 "Web Service"
3. 在 "Connect a repository" 部分：
   - 搜索您的倉庫：`linshmin/line-ai-bot`
   - 點擊 "Connect" 按鈕
4. Render 會自動檢測 `render.yaml` 配置文件

### 第三步：配置 Web Service

由於我們已經準備了 `render.yaml`，大部分配置會自動完成：

**自動配置的項目：**
- ✅ 名稱：`line-ai-bot`
- ✅ 區域：`Oregon (US West)`
- ✅ 分支：`master`
- ✅ 運行命令：`gunicorn app.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`
- ✅ 實例類型：`Free`

**需要確認的項目：**
1. **Environment**: 選擇 `Python 3`
2. **Build Command**: 留空（會自動使用 `pip install -r requirements.txt`）
3. **Start Command**: 留空（會使用 render.yaml 中的配置）

### 第四步：添加環境變量

在部署之前，必須添加以下環境變量：

1. 在 Web Service 配置頁面，找到 "Environment" 部分
2. 點擊 "Add Environment Variable"
3. 逐個添加以下變量：

#### 🔑 必需的環境變量：

| 變量名稱 | 說明 | 獲取方式 |
|---------|------|---------|
| `LINE_CHANNEL_ACCESS_TOKEN` | LINE 訊息 API 存取權杖 | LINE Developers Console |
| `LINE_CHANNEL_SECRET` | LINE 頻道密鑰 | LINE Developers Console |
| `OPENAI_API_KEY` | OpenAI API 金鑰 | OpenAI 平台 |
| `REDIS_URL` | Redis 連接字串 | Render 會自動提供（見下方） |

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

**3. Redis URL (Render 自動提供):**
- 先不要手動添加 `REDIS_URL`
- 在創建 Web Service 之後，Render 會自動創建一個 Redis 實例
- 在 Redis 實例的頁面會顯示連接字串
- 複製該字串並添加到 Web Service 的環境變量中

### 第五步：部署應用程式

1. 確認所有配置正確
2. 點擊頁面底部的 "Create Web Service" 按鈕
3. Render 會開始部署流程：
   - 構建 Docker 鏡像
   - 安裝依賴套件
   - 啟動應用程式
4. 部署大約需要 2-5 分鐘
5. 部署完成後，您會看到一個公開 URL，例如：
   - `https://line-ai-bot.onrender.com`

### 第六步：配置 Redis 連接

1. 在 Render Dashboard，點擊 "New +" → "Redis"
2. 名稱：`line-ai-bot-redis`
3. 區域：與 Web Service 相同（Oregon）
4. 實例類型：`Free`
5. 點擊 "Create Redis"
6. 創建完成後，在 Redis 頁面複製 "Internal Connection String"
7. 回到 Web Service 頁面：
   - 點擊 "Environment"
   - 添加環境變量 `REDIS_URL`
   - 粘貼複製的連接字串
   - 點擊 "Save Changes"
8. Render 會自動重新部署應用程式

### 第七步：配置 LINE Webhook

1. 訪問 [LINE Developers Console](https://developers.line.biz/console/)
2. 選擇您的 Messaging API 頻道
3. 點擊 "Messaging API" 頁籤
4. 找到 "Webhook settings" 部分
5. 設置 Webhook URL：
   ```
   https://line-ai-bot.onrender.com/webhook
   ```
   （將 `line-ai-bot` 替換為您的實際應用程式名稱）
6. 點擊 "Verify" 按鈕驗證 URL
7. 確保 "Use webhook" 選項已開啟
8. 點擊 "Save"

### 第八步：測試機器人

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
3. 確保環境變量已正確設置
4. 查看 Render Dashboard 的 Logs

### 機器人無回應

**問題：發送訊息後沒有回應**
**解決方案：**
1. 檢查 Render Dashboard 的 Logs
2. 確認環境變量設置正確
3. 驗證 LINE Channel Access Token 和 Secret
4. 檢查 OpenAI API Key 是否有效
5. 確認 Redis 連接正常

### Redis 連接錯誤

**問題：Redis 連接失敗**
```
Error: Redis connection refused
```
**解決方案：**
1. 確認 Redis 實例正在運行
2. 檢查 `REDIS_URL` 環境變量是否正確
3. 確保 Redis 和 Web Service 在同一個區域

---

## 📊 監控與維護

### 查看 Logs

1. 在 Render Dashboard 點擊您的 Web Service
2. 點擊 "Logs" 頁籤
3. 即時查看應用程式日誌
4. 可以過濾特定關鍵字（如 `ERROR`, `WARNING`）

### 監控資源使用

1. 在 Web Service 頁面查看 CPU 和記憶體使用量
2. 免費層限制：
   - 512 MB RAM
   - 0.1 CPU
   - 750 小時/月

### 更新應用程式

1. 在本地修改代碼
2. 提交並推送到 GitHub：
   ```bash
   git add .
   git commit -m "更新描述"
   git push origin master
   ```
3. Render 會自動檢測並重新部署

### 更新知識庫

1. 編輯 `data/knowledge_base/knowledge.json`
2. 提交並推送更改
3. Render 會自動重新部署

---

## 💡 優化建議

### 1. 提升回應速度
- 使用 Redis 快取常見問題的答案
- 實施請求佇列處理

### 2. 降低成本
- 監控 OpenAI API 使用量
- 使用 GPT-4o-mini（最便宜的模型）
- 實施本地快存機制

### 3. 增強功能
- 添加用戶分析
- 實施多語言支援
- 添加圖片識別功能
- 整合其他 LINE 功能（如 Flex Message）

---

## 🔐 安全建議

1. **不要將敏感資訊提交到 Git**
   - `.env` 文件已在 `.gitignore` 中
   - 永遠不要提交 API 金鑰

2. **定期更新依賴套件**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

3. **監控異常活動**
   - 定期查看 Render Logs
   - 設置警報通知

4. **備份重要數據**
   - 定期備份知識庫
   - 保存配置文件

---

## 📞 支援資源

- **Render 文檔**: https://render.com/docs
- **LINE Developers 文檔**: https://developers.line.biz/docs/
- **OpenAI API 文檔**: https://platform.openai.com/docs
- **FastAPI 文檔**: https://fastapi.tiangolo.com/

---

## ✅ 部署檢查清單

部署前確認：
- [ ] 所有代碼已推送到 GitHub
- [ ] `render.yaml` 文件存在且正確
- [ ] `Dockerfile` 文件存在且正確
- [ ] `Procfile` 文件存在且正確
- [ ] `requirements.txt` 包含所有依賴

部署中確認：
- [ ] Render 帳號已創建並登錄
- [ ] GitHub 倉庫已連接
- [ ] 環境變量已設置
- [ ] Redis 實例已創建並連接

部署後確認：
- [ ] 應用程式成功啟動
- [ ] 公開 URL 可訪問
- [ ] LINE Webhook 已設置並驗證
- [ ] 機器人可以正常回應訊息
- [ ] 知識庫查詢功能正常
- [ ] 快速回覆按鈕正常顯示

---

**祝您部署成功！🎉**

如有任何問題，請隨時查看 Render Dashboard 的 Logs 或參考故障排除部分。