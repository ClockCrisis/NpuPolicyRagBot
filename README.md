# 西工大政策问答平台

基于 LangChain + Chroma 向量数据库的 RAG（检索增强生成）应用，提供政策文档问答和文件上传功能。

## 环境配置

### 1. 创建 conda 环境

```bash
conda create -n rag python=3.10 -y
conda activate rag
```

### 2. 安装依赖

```bash
# 核心依赖
pip install langchain langchain-community langchain-chroma langchain-openai
pip install chromadb dashscope streamlit

# 文件解析
pip install pypdf python-docx

# 向量文本分割
pip install langchain-text-splitters
```

### 3. 配置模型

编辑 `config.py`：

```python
# Chat Model (LLM)
CHAT_MODEL_NAME = "你的模型名"           # 如 qwen2.5-72b-awq
CHAT_MODEL_BASE_URL = "http://你的LLM地址:8080/v1"

# Embedding Model
EMBEDDING_MODEL_NAME = "text-embedding-v4"
EMBEDDING_MODEL_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
```

如使用通义千问 API，设置环境变量：
```bash
export DASHSCOPE_API_KEY="你的API密钥"
```

## 运行

```bash
# 问答界面
streamlit run app_qa.py

# 文件上传界面
streamlit run app_file_uploader.py
```

## 项目结构

| 文件 | 说明 |
|------|------|
| `config.py` | 配置文件（模型、向量库参数） |
| `model_factory.py` | 模型工厂（统一创建 Chat/Embedding 模型） |
| `rag.py` | RAG 核心链（检索 + 生成） |
| `knowledge_base.py` | 知识库（文件解析、MD5 去重、向量存储） |
| `vector_store.py` | Chroma 向量库封装 |
| `file_history_store.py` | 会话历史管理 |
| `app_qa.py` | Streamlit 问答界面 |
| `app_file_uploader.py` | Streamlit 文件上传界面 |

#### 功能特性

- 支持任意 OpenAI 兼容 API 的 LLM（通过 `base_url` 配置）
- 支持 PDF、DOCX、TXT 文件解析并存入知识库
- MD5 去重机制防止重复上传
- 会话历史持久化存储
