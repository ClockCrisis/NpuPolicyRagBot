import sys
import os

# 将项目根目录添加到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from core.rag import RagService
import streamlit as st
import core.config as config

# 获取 data 目录的绝对路径
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def get_visit_count():
    """获取访问次数"""
    try:
        visit_file = os.path.join(DATA_DIR, "visit_count.txt")
        if os.path.exists(visit_file):
            with open(visit_file, "r") as f:
                return int(f.read().strip())
    except:
        pass
    return 0


def increment_visit_count():
    """增加访问次数"""
    count = get_visit_count() + 1
    visit_file = os.path.join(DATA_DIR, "visit_count.txt")
    # 确保 data 目录和文件存在
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(visit_file):
        with open(visit_file, "w") as f:
            f.write("0")
    with open(visit_file, "w") as f:
        f.write(str(count))
    return count


# 每次页面加载增加访问计数
if "visit_counted" not in st.session_state:
    st.session_state["visit_counted"] = True
    current_count = increment_visit_count()
else:
    current_count = get_visit_count()

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

# 页面底部显示访问统计
st.divider()
st.caption(f"总访问量: {current_count} 人")
