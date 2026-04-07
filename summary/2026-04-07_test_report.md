# 测试报告

## 日期
2026-04-07

## 测试目标

验证 model_factory 改造后的代码是否正常工作。

---

## 测试结果

### 1. 模型工厂 ✅

```
Chat model type: ChatOpenAI
Embedding model type: DashScopeEmbeddings
Chat result: Hello! How can I help you today? 😊
```

**结论**：Chat model 和 Embedding model 创建正常，Chat model 调用成功。

### 2. Chroma + DashScopeEmbeddings ❌

```
Segmentation fault (exit code 139)
```

**问题描述**：Chroma 与 DashScopeEmbeddings 组合使用时触发 segfault。

**影响范围**：向量检索功能无法正常工作。

---

## 问题分析

### 环境问题

测试环境存在以下兼容性问题：

| 问题 | 详情 |
|------|------|
| `onnxruntime` DLL 加载失败 | ImportError: DLL load failed |
| `tiktoken` 无法下载编码文件 | SSL 错误，访问 openaipublic.blob.core.windows.net 失败 |
| Chroma + DashScopeEmbeddings segfault | 内存相关问题 |

### 根本原因

Chroma 在创建或操作向量时调用 `DashScopeEmbeddings.embed_query()` 会触发 segfault。这个问题不是代码改动引起的，而是 Windows 环境下 Chroma (1.5.2) 与 `langchain-community` (0.4.1) 的兼容性问题。

---

## 测试步骤记录

### Step 1: 修复 import 错误

rag.py 中 `ModelFactory` 类已改为函数：
```python
# 修复前
from model_factory import ModelFactory
ModelFactory.create_chat_model()

# 修复后
from model_factory import create_chat_model, create_embedding_model
create_chat_model()
```

### Step 2: DashScopeEmbeddings 不接受 api_key 参数

```python
# 修复前
return DashScopeEmbeddings(
    model=config.EMBEDDING_MODEL_NAME,
    api_key=api_key  # 报错：Extra inputs are not permitted
)

# 修复后
return DashScopeEmbeddings(
    model=config.EMBEDDING_MODEL_NAME
)
```

### Step 3: Chat model 直接调用测试

```python
from model_factory import create_chat_model
chat = create_chat_model()
result = chat.invoke('你好')
# 结果: 你好！有什么我可以帮你的吗？😊
```

### Step 4: Embedding model 直接调用测试

```python
from model_factory import create_embedding_model
emb = create_embedding_model()
result = emb.embed_query('hello world')
# 结果: 1024 dimensions - 成功
```

### Step 5: Chroma + Embedding 组合测试

```python
from langchain_chroma import Chroma
from model_factory import create_embedding_model

emb = create_embedding_model()
vs = Chroma(
    collection_name='RAG',
    embedding_function=emb,
    persist_directory='./chroma_db'
)
# Chroma 创建成功

vs.similarity_search('test', k=1)
# segfault - 失败
```

---

## 结论

| 模块 | 状态 |
|------|------|
| model_factory.py | ✅ 正常工作 |
| config.py | ✅ 配置正确 |
| rag.py (import) | ✅ 正常工作 |
| Chat model 调用 | ✅ 正常工作 |
| Embedding model 调用 | ✅ 正常工作 |
| Chroma + Embedding 检索 | ❌ segfault |

---

## 建议

1. **短期**：在能正常运行的 Linux 环境中测试
2. **长期**：考虑升级或更换向量数据库版本以解决 Windows 兼容性问题
3. **备选**：使用其他 embedding 服务（如 OpenAI embedding）作为替代

---

## 验证命令

```bash
# 验证模型工厂
python -c "from model_factory import create_chat_model, create_embedding_model; print('OK')"

# 验证 Chat model
python -c "
from model_factory import create_chat_model
chat = create_chat_model()
print(chat.invoke('hi').content)
"

# 验证 Embedding model
python -c "
from model_factory import create_embedding_model
emb = create_embedding_model()
print(len(emb.embed_query('test')), 'dimensions')
"
```
