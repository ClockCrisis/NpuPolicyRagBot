# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.
以下内容非常重要:"本项目目前启动环境为conda管理下的rag.配置环境的时候往rag里面配置.不要配置错了!!!!!!!!"

## 项目概述

这是一个基于 LangChain + Chroma 向量数据库 + DashScope（阿里云）API 的 RAG（检索增强生成）应用。提供两个 Streamlit 界面：问答系统和知识库文件上传。


## 常用命令

```bash
# 启动问答界面
streamlit run app_qa.py

# 启动文件上传界面
streamlit run app_file_uploader.py

# 测试单个模块
python rag.py
python knowledge_base.py
python vector_store.py
```

## 架构说明

**RAG 管道**（`rag.py`）：基于 LCEL 的核心 LangChain 链：
- `VectorStoreService` 从 Chroma 检索相关文档
- 文档格式化后作为上下文注入提示词
- `RunnableWithMessageHistory` 包装链路，支持基于会话的聊天历史
- 使用阿里云 DashScope 的 `qwen3-max` 对话模型和 `text-embedding-v4` 嵌入模型

**知识库**（`knowledge_base.py`）：文档摄入与 MD5 去重：
- `str_to_md5()` 计算 MD5 用于重复检测
- `RecursiveCharacterTextSplitter` 文本分割，chunk_size=1000，重叠=100
- Chroma 持久化到 `./chroma_db/`

**聊天历史**（`file_history_store.py`）：基于文件的会话存储：
- `FileChatMessageHistory` 将会话以 JSON 格式存储在 `./chat_history/{session_id}`
- 使用 LangChain 的 `message_to_dict`/`messages_from_dict` 序列化

**向量库**（`vector_store.py`）：Chroma 封装，返回 retriever，相似度阈值 k=3。

## 依赖

核心包：`langchain`、`langchain-community`、`langchain-chroma`、`dashscope`、`chromadb`、`streamlit`

## 配置

所有配置项集中在 `config.py` 中：collection 名称、持久化目录、文本分割参数、模型名称、相似度阈值、会话配置。
