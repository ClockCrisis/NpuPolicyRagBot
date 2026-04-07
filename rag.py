from langchain_core.output_parsers import StrOutputParser

from file_history_store import get_history
from vector_store import VectorStoreService
from model_factory import create_chat_model, create_embedding_model
import config
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda


class RagService(object):
    def __init__(self):
        self.vector_service = VectorStoreService(
            embedding=create_embedding_model()
        )
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", """根据提供的参考资料回答问题。

要求：
1. 以参考资料为主，参考资料中没有的信息不要编造
2. 如有冲突，以最新参考资料为准
3. 回答要简洁，引用相关来源
4. 如果参考资料中没有相关信息，请如实说明

参考资料：
{context}"""),
                ("system", "已有的历史记录如下:"),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{input}")
            ]
        )
        self.chat_model = create_chat_model()
        self.chain = self.get_chain()


    def get_chain(self):
        retriever = self.vector_service.get_retriever()

        def format_docs(docs):
            if not docs:
                return "没有相关资料"
            formated_str = ""
            for doc in docs:
                formated_str += doc.page_content + "\n"
            return formated_str

        def print_prompt(prompt):
            print("=====prompt start=====")
            print(prompt.to_string())
            print("=====prompt end=====")
            return  prompt

        def format_for_retriever(inputs):
            query = inputs["input"]
            return query
        def format_for_prompt(inputs):
            new_values = {
                "input": inputs["input"]["input"],
                "context": inputs["context"],
                "history": inputs["input"]["history"]
            }
            return new_values

        chain = {
                    "input": RunnablePassthrough(),
                    "context": RunnableLambda(format_for_retriever) | retriever | format_docs
                } | RunnableLambda(format_for_prompt) |self.prompt_template | print_prompt | self.chat_model | StrOutputParser()

        #创建一个增强链用于存储历史会话, 增强链输入必须是字典
        newchain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key = "input",  # 表示用户输入在模板中的占位符
            history_messages_key = "history"
        )
        return newchain

if __name__ == "__main__":
    #配置session_id
    session_config = {
        "configurable": {
            "session_id": "user_001",
        }
    }
    service = RagService()
    input = "我身高185,体重65kg,应该穿什么码的衣服？夏天沙滩写代码应该穿什么颜色"
    input = "我一共有几只小猫"
    res = service.chain.invoke({"input":input},session_config)
    print(res)