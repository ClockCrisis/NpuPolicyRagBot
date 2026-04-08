import os

# 获取项目根目录（core 的上一级）
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

md5_path = os.path.join(BASE_DIR, "data", "md5.text")
collection_name = "RAG"
persist_directory = os.path.join(BASE_DIR, "data", "chroma_db")
chunk_size = 500
chunk_overlap = 150
separators = ["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""]
similarity_threshold = 5

# =============================================================================
# Chat Model 配置
# =============================================================================
CHAT_MODEL_NAME = "qwen2.5-72b-awq"
CHAT_MODEL_BASE_URL = "http://10.68.85.41:8080/v1"
CHAT_MODEL_API_KEY = None
CHAT_MODEL_TEMPERATURE = 0.7
CHAT_MODEL_MAX_TOKENS = 2000

# =============================================================================
# Embedding Model 配置
# =============================================================================
EMBEDDING_MODEL_NAME = "text-embedding-v4"
EMBEDDING_MODEL_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
EMBEDDING_MODEL_API_KEY = "sk-330cb98ad9a444f2bc9f7cfd822150c0"

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

# =============================================================================
# 访问统计配置
# =============================================================================
VISIT_COUNT_FILE = os.path.join(BASE_DIR, "data", "visit_count.txt")
