"""
LINE客服AI机器人 - LINE消息处理模块
"""
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    QuickReply,
    QuickReplyButton,
    MessageAction,
    TemplateSendMessage,
    ButtonsTemplate,
    ImageSendMessage,
)
from typing import List, Optional
from config import settings


class LineBotHandler:
    """LINE机器人处理器"""

    def __init__(self):
        self.line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
        self.handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)

    def verify_signature(self, signature: str, body: str) -> bool:
        """验证LINE Webhook签名"""
        try:
            self.handler.handle(body, signature)
            return True
        except InvalidSignatureError:
            return False

    def reply_message(self, reply_token: str, message: str):
        """发送文本回复"""
        self.line_bot_api.reply_message(
            reply_token,
            TextSendMessage(text=message)
        )

    def reply_with_quick_reply(
        self,
        reply_token: str,
        message: str,
        quick_reply_items: List[str]
    ):
        """发送带快速回复的消息"""
        quick_reply = QuickReply(
            items=[
                QuickReplyButton(
                    action=MessageAction(label=item, text=item)
                )
                for item in quick_reply_items
            ]
        )
        self.line_bot_api.reply_message(
            reply_token,
            TextSendMessage(text=message, quick_reply=quick_reply)
        )

    def reply_with_buttons(
        self,
        reply_token: str,
        title: str,
        text: str,
        actions: List[dict]
    ):
        """发送带按钮的模板消息"""
        template = ButtonsTemplate(
            title=title,
            text=text,
            actions=[
                MessageAction(
                    label=action.get("label"),
                    text=action.get("text")
                )
                for action in actions
            ]
        )
        self.line_bot_api.reply_message(
            reply_token,
            TemplateSendMessage(alt_text=title, template=template)
        )

    def reply_with_image(
        self,
        reply_token: str,
        original_content_url: str,
        preview_image_url: str
    ):
        """发送图片消息"""
        self.line_bot_api.reply_message(
            reply_token,
            ImageSendMessage(
                original_content_url=original_content_url,
                preview_image_url=preview_image_url
            )
        )


# 全局实例
line_bot = LineBotHandler()