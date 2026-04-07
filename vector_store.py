from langchain_chroma import Chroma
import config

# 向量数据库服务类，提供获取检索器的接口,返回见做到的资料
class VectorStoreService(object):
    def __init__(self,embedding):
        self.embedding = embedding
        self.vector_store = Chroma(
            collection_name=config.collection_name,
            embedding_function=self.embedding,
            persist_directory=config.persist_directory
        )
    def get_retriever(self):
        # 启用 MMR (最大边际相关性) 增加结果多样性
        return self.vector_store.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": config.similarity_threshold,      # 最终返回数量
                "fetch_k": 20                          # 从数据库获取更多候选
            }
        )

if __name__ == "__main__":
    from langchain_community.embeddings import DashScopeEmbeddings
    embedding = DashScopeEmbeddings(model = "text-embedding-v4")
    service = VectorStoreService(embedding)
    retriever = service.get_retriever()
    # res = retriever.invoke("我身高185,体重65kg,应该穿什么码的衣服？")
    res = retriever.invoke("攻击实验的最终成功率是多少")
    print(res)