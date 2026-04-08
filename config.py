md5_path = "md5.text"
collection_name = "RAG"
persist_directory = "./chroma_db"
chunk_size = 500              # 优化: 减小到 300-500，保留更精确的语义
chunk_overlap = 150           # 优化: 增加 overlap 防止边界信息丢失
separators = ["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""]  # 优化: 中文友好分割符
similarity_threshold = 5      # 优化: 增加 k 值，返回更多相关结果

# =============================================================================
# Chat Model 配置
# =============================================================================
# 所有模型统一使用 OpenAI 兼容 API，通过 base_url 指定端点
# CHAT_MODEL_NAME = "qwen3-max"
# CHAT_MODEL_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
# CHAT_MODEL_API_KEY = None              # None = 从环境变量 DASHSCOPE_API_KEY 读取
# CHAT_MODEL_TEMPERATURE = 0.7
# CHAT_MODEL_MAX_TOKENS = 2000

CHAT_MODEL_NAME = "qwen2.5-72b-awq"
CHAT_MODEL_BASE_URL = "http://10.68.85.41:8080/v1"
CHAT_MODEL_API_KEY = None              # None = 从环境变量 DASHSCOPE_API_KEY 读取
CHAT_MODEL_TEMPERATURE = 0.7
CHAT_MODEL_MAX_TOKENS = 2000

# =============================================================================
# Embedding Model 配置
# =============================================================================
EMBEDDING_MODEL_NAME = "text-embedding-v4"
EMBEDDING_MODEL_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
EMBEDDING_MODEL_API_KEY = None

# =============================================================================
# Session 配置
# =============================================================================
session_config = {
    "configurable": {"session_id": "user_001"}
}

# =============================================================================
# 管理员登录配置
# =============================================================================
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"  # 生产环境请修改为强密码
