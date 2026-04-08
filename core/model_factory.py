import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.embeddings.dashscope import DashScopeEmbeddings
import core.config as config


def create_chat_model():
    """创建 Chat Model 实例（统一使用 OpenAI 兼容 API）"""
    api_key = config.CHAT_MODEL_API_KEY or os.environ.get("DASHSCOPE_API_KEY")
    return ChatOpenAI(
        model=config.CHAT_MODEL_NAME,
        api_key=api_key,
        base_url=config.CHAT_MODEL_BASE_URL,
        temperature=config.CHAT_MODEL_TEMPERATURE,
        max_tokens=config.CHAT_MODEL_MAX_TOKENS,
    )


def create_embedding_model():
    """创建 Embedding Model 实例"""
    base_url = config.EMBEDDING_MODEL_BASE_URL

    # DashScope 使用专用 embeddings 客户端
    if base_url and "dashscope" in base_url:
        return DashScopeEmbeddings(
            model=config.EMBEDDING_MODEL_NAME
        )

    # 其他 OpenAI 兼容 API 使用标准客户端
    api_key = config.EMBEDDING_MODEL_API_KEY or os.environ.get("OPENAI_API_KEY")
    return OpenAIEmbeddings(
        model=config.EMBEDDING_MODEL_NAME,
        api_key=api_key,
        base_url=base_url,
    )
