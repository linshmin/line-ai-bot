"""
LINE客服AI机器人 - 知识库模块（向量存储）
"""
import os
import json
from typing import List, Optional, Dict
from sentence_transformers import SentenceTransformer
import numpy as np
from config import settings


class KnowledgeBase:
    """知识库管理器"""

    def __init__(self):
        self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
        self.knowledge_path = settings.KNOWLEDGE_BASE_PATH
        self.documents = []
        self.embeddings = None

        # 确保知识库目录存在
        os.makedirs(self.knowledge_path, exist_ok=True)

        # 加载知识库
        self.load_knowledge_base()

    def load_knowledge_base(self):
        """加载知识库"""
        knowledge_file = os.path.join(self.knowledge_path, "knowledge.json")

        if os.path.exists(knowledge_file):
            with open(knowledge_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.documents = data.get("documents", [])
                embeddings_data = data.get("embeddings", [])

                if embeddings_data:
                    self.embeddings = np.array(embeddings_data)
                elif self.documents:
                    # 如果没有嵌入向量，重新生成
                    self._generate_embeddings()
        else:
            # 创建示例知识库
            self._create_sample_knowledge()

    def _create_sample_knowledge(self):
        """创建示例知识库"""
        self.documents = [
            {
                "id": "1",
                "content": "我們的客服時間是週一至週五，上午9點到下午6點。",
                "category": "客服時間"
            },
            {
                "id": "2",
                "content": "如果您需要退貨，請在購買後7天內聯繫我們，並保持商品完整。",
                "category": "退貨政策"
            },
            {
                "id": "3",
                "content": "我們接受信用卡、PayPal、銀行轉帳等多種付款方式。",
                "category": "付款方式"
            },
            {
                "id": "4",
                "content": "運費根據地區不同，一般訂單免運費，急件另收費用。",
                "category": "運費說明"
            },
            {
                "id": "5",
                "content": "如需技術支援，請提供您的訂單號碼和問題描述，我們會盡快回覆。",
                "category": "技術支援"
            }
        ]

        self._generate_embeddings()
        self.save_knowledge_base()

    def _generate_embeddings(self):
        """生成文档嵌入向量"""
        if not self.documents:
            return

        texts = [doc["content"] for doc in self.documents]
        self.embeddings = self.embedding_model.encode(
            texts,
            show_progress_bar=False
        )

    def save_knowledge_base(self):
        """保存知识库"""
        knowledge_file = os.path.join(self.knowledge_path, "knowledge.json")

        data = {
            "documents": self.documents,
            "embeddings": self.embeddings.tolist() if self.embeddings is not None else []
        }

        with open(knowledge_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_document(self, content: str, category: str = "一般"):
        """添加文档到知识库"""
        doc_id = str(len(self.documents) + 1)
        document = {
            "id": doc_id,
            "content": content,
            "category": category
        }

        self.documents.append(document)
        self._generate_embeddings()
        self.save_knowledge_base()

    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """搜索相关知识"""
        if not self.documents or self.embeddings is None:
            return []

        # 生成查询嵌入
        query_embedding = self.embedding_model.encode(
            [query],
            show_progress_bar=False
        )

        # 计算相似度
        similarities = np.dot(
            self.embeddings,
            query_embedding.T
        ).flatten()

        # 获取top-k结果
        top_indices = np.argsort(similarities)[-top_k:][::-1]

        results = []
        for idx in top_indices:
            if similarities[idx] > 0.3:  # 相似度阈值
                results.append({
                    "document": self.documents[idx],
                    "similarity": float(similarities[idx])
                })

        return results

    def get_context_for_query(self, query: str, top_k: int = 2) -> str:
        """获取查询的相关上下文"""
        results = self.search(query, top_k)

        if not results:
            return ""

        context_parts = []
        for result in results:
            doc = result["document"]
            context_parts.append(
                f"[{doc.get('category', '一般')}] {doc['content']}"
            )

        return "\n\n".join(context_parts)


# 全局实例
knowledge_base = KnowledgeBase()