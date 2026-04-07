import time
from rag import RagService
import streamlit as st
import config as config

# 标题
st.title("西工大政策问答平台")
st.divider()            # 分隔符

if "message" not in st.session_state:
    st.session_state["message"] = [{"role": "assistant", "content": "您好，我是西工大政策问答助手，有什么政策问题可以问我？"}]

if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()

# 刷新知识库按钮
col1, col2 = st.columns([1, 5])
with col1:
    if st.button("🔄 刷新知识库"):
        st.session_state["rag"].refresh_vector_store()
        st.success("知识库已刷新！")

with col2:
    st.caption("点击刷新以加载最新上传的文档")

st.divider()

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

# 在页面最下方提供用户输入栏
prompt = st.chat_input()

if prompt:

    # 在页面输出用户的提问
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})

    ai_res_list = []
    with st.spinner("AI思考中..."):
        res_stream = st.session_state["rag"].chain.stream({"input": prompt}, config.session_config)
        # yield

        def capture(generator, cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                yield chunk

        st.chat_message("assistant").write_stream(capture(res_stream, ai_res_list))
        st.session_state["message"].append({"role": "assistant", "content": "".join(ai_res_list)})

