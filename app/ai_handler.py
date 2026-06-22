"""
LINE客服AI机器人 - AI对话模块
"""
from openai import OpenAI
from typing import List, Optional, Dict
from config import settings


class AIChatHandler:
    """AI对话处理器"""

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL

    def generate_response(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict]] = None,
        system_prompt: Optional[str] = None,
        knowledge_context: Optional[str] = None
    ) -> str:
        """生成AI回复"""

        # 构建消息列表
        messages = []

        # 添加系统提示词
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        else:
            messages.append({
                "role": "system",
                "content": "你是一个专业的客服AI助手，用繁體中文回答問題，語氣友善且專業。"
            })

        # 添加知识库上下文
        if knowledge_context:
            messages.append({
                "role": "system",
                "content": f"以下是有關的知識庫資訊，請參考這些資訊來回答問題：\n{knowledge_context}"
            })

        # 添加对话历史
        if conversation_history:
            messages.extend(conversation_history)

        # 添加当前用户消息
        messages.append({"role": "user", "content": user_message})

        # 调用OpenAI API
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"抱歉，AI回應發生錯誤：{str(e)}"

    def generate_summary(self, text: str) -> str:
        """生成文本摘要"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "請用繁體中文為以下對話生成簡短摘要，不超過50字。"
                    },
                    {"role": "user", "content": text}
                ],
                temperature=0.3,
                max_tokens=100
            )
            return response.choices[0].message.content
        except Exception as e:
            return text[:50]  # 如果失败，返回前50个字符


# 全局实例
ai_chat = AIChatHandler()