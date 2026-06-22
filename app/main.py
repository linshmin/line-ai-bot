"""
LINE客服AI机器人 - 主应用模块
"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from linebot.exceptions import InvalidSignatureError
import logging

from app.line_handler import line_bot
from app.ai_handler import ai_chat
from app.memory import memory
from app.knowledge_base import knowledge_base
from config import settings

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="LINE客服AI机器人",
    description="基于FastAPI和OpenAI的LINE客服机器人",
    version="1.0.0"
)


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "LINE客服AI机器人运行中",
        "status": "healthy"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


@app.post("/webhook")
async def webhook(request: Request):
    """LINE Webhook端点"""
    # 获取请求体和签名
    signature = request.headers.get("X-Line-Signature", "")
    body = await request.body()
    body_str = body.decode("utf-8")

    # 验证签名
    if not line_bot.verify_signature(signature, body_str):
        logger.error("无效的签名")
        raise HTTPException(status_code=400, detail="Invalid signature")

    # 处理事件
    try:
        events = line_bot.handler.parse(body_str, signature)
        for event in events:
            await handle_event(event)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    except Exception as e:
        logger.error(f"处理事件时出错: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

    return JSONResponse(content={"status": "ok"})


async def handle_event(event):
    """处理单个事件"""
    if not isinstance(event, MessageEvent):
        return

    if not isinstance(event.message, TextMessage):
        return

    user_id = event.source.user_id
    user_message = event.message.text
    reply_token = event.reply_token

    logger.info(f"收到用户 {user_id} 的消息: {user_message}")

    try:
        # 保存用户消息到记忆
        memory.save_message(user_id, "user", user_message)

        # 获取对话历史
        conversation_history = memory.get_conversation_history(user_id, max_messages=6)

        # 搜索相关知识
        knowledge_context = knowledge_base.get_context_for_query(user_message, top_k=2)

        # 生成AI回复
        system_prompt = """你是一個專業的客服AI助手，用繁體中文回答問題，語氣友善且專業。
請根據知識庫資訊回答問題，如果知識庫中沒有相關資訊，請基於你的知識回答。
回答要簡潔明了，避免過於冗長。"""

        ai_response = ai_chat.generate_response(
            user_message=user_message,
            conversation_history=conversation_history,
            system_prompt=system_prompt,
            knowledge_context=knowledge_context
        )

        # 保存AI回复到记忆
        memory.save_message(user_id, "assistant", ai_response)

        # 判断是否需要快速回复
        quick_reply_items = []
        if "客服時間" in user_message or "營業時間" in user_message:
            quick_reply_items = ["退貨政策", "付款方式", "運費說明"]
        elif "退貨" in user_message:
            quick_reply_items = ["客服時間", "付款方式", "技術支援"]
        elif "付款" in user_message:
            quick_reply_items = ["客服時間", "退貨政策", "運費說明"]
        elif "運費" in user_message:
            quick_reply_items = ["客服時間", "退貨政策", "付款方式"]

        # 发送回复
        if quick_reply_items:
            line_bot.reply_with_quick_reply(
                reply_token=reply_token,
                message=ai_response,
                quick_reply_items=quick_reply_items
            )
        else:
            line_bot.reply_message(reply_token=reply_token, message=ai_response)

        logger.info(f"发送回复: {ai_response}")

    except Exception as e:
        logger.error(f"处理消息时出错: {str(e)}")
        line_bot.reply_message(
            reply_token=reply_token,
            message="抱歉，處理您的請求時發生錯誤，請稍後再試。"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.DEBUG
    )