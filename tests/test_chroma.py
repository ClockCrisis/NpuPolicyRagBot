from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import CSVLoader

# Chroma 向量数据库（轻量级的）
# 确保 langchain-chroma chromadb 这两个库安装了的，没有的话请pip install

vector_store = Chroma(
    collection_name="test",     # 当前向量存储起个名字，类似数据库的表名称
    embedding_function=DashScopeEmbeddings(),       # 嵌入模型
    persist_directory="./chroma_db"     # 指定数据存放的文件夹
)
chunks = ["data123"]

meta_data = {
    "source": "1",
    "operator": "xz"
}
vector_store.add_texts(chunks, metadatas=[meta_data] * len(chunks))
print("数据已添加到 Chroma 向量数据库中！")
