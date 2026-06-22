"""
LINE客服AI机器人 - 测试模块
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """测试客户端"""
    return TestClient(app)


def test_root_endpoint(client):
    """测试根路径"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "status" in response.json()


def test_health_check(client):
    """测试健康检查"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_webhook_without_signature(client):
    """测试没有签名的webhook请求"""
    response = client.post("/webhook", json={})
    assert response.status_code == 400


def test_webhook_with_invalid_signature(client):
    """测试无效签名的webhook请求"""
    headers = {"X-Line-Signature": "invalid_signature"}
    response = client.post(
        "/webhook",
        json={},
        headers=headers
    )
    assert response.status_code == 400


if __name__ == "__main__":
    pytest.main([__file__, "-v"])