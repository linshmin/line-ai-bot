"""
LINE客服AI机器人 - 上下文记忆模块（Redis）
"""
import redis
import json
from typing import List, Optional, Dict
from datetime import timedelta
from config import settings


class ConversationMemory:
    """对话记忆管理器"""

    def __init__(self):
        self.redis_client = redis.from_url(settings.REDIS_URL)
        self.expiration_hours = 24  # 对话历史保存24小时

    def _get_key(self, user_id: str) -> str:
        """获取Redis键"""
        return f"conversation:{user_id}"

    def save_message(self, user_id: str, role: str, content: str):
        """保存单条消息"""
        key = self._get_key(user_id)
        message = {"role": role, "content": content}

        # 使用列表存储消息
        self.redis_client.rpush(key, json.dumps(message))
        # 设置过期时间
        self.redis_client.expire(key, timedelta(hours=self.expiration_hours))

    def get_conversation_history(
        self,
        user_id: str,
        max_messages: int = 10
    ) -> List[Dict]:
        """获取对话历史"""
        key = self._get_key(user_id)
        messages = self.redis_client.lrange(key, -max_messages, -1)
        return [json.loads(msg) for msg in messages]

    def clear_conversation(self, user_id: str):
        """清除对话历史"""
        key = self._get_key(user_id)
        self.redis_client.delete(key)

    def get_conversation_summary(self, user_id: str) -> str:
        """获取对话摘要"""
        history = self.get_conversation_history(user_id)
        if not history:
            return ""

        # 将对话历史转换为文本
        conversation_text = "\n".join(
            [f"{msg['role']}: {msg['content']}" for msg in history]
        )
        return conversation_text


# 全局实例
memory = ConversationMemory()