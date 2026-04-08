import sys
import os

# 将项目根目录添加到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import tempfile
from io import BytesIO
from core.knowledge_base import KnowledgeBaseService
import core.config as config

# 初始化 session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "counter" not in st.session_state:
    st.session_state["counter"] = 0
if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()


def extract_text(file) -> str:
    """从 PDF/DOCX/TXT 文件提取文本"""
    suffix = file.name.lower().split('.')[-1]

    if suffix == 'txt':
        return file.getvalue().decode("utf-8")

    elif suffix == 'pdf':
        from langchain_community.document_loaders import PyPDFLoader
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            tmp.write(file.getvalue())
            tmp_path = tmp.name
        try:
            loader = PyPDFLoader(tmp_path)
            docs = loader.load()
            return "\n\n".join(doc.page_content for doc in docs)
        finally:
            os.unlink(tmp_path)

    elif suffix == 'docx':
        from langchain_community.document_loaders import Docx2txtLoader
        with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp:
            tmp.write(file.getvalue())
            tmp_path = tmp.name
        try:
            loader = Docx2txtLoader(tmp_path)
            docs = loader.load()
            return "\n\n".join(doc.page_content for doc in docs)
        finally:
            os.unlink(tmp_path)

    else:
        raise ValueError(f"不支持的文件类型: {suffix}")


# 登录页面
def show_login():
    st.title("西工大政策问答平台 - 文件上传")
    st.divider()
    st.subheader("请先登录")

    with st.form("login_form"):
        username = st.text_input("用户名")
        password = st.text_input("密码", type="password")
        submitted = st.form_submit_button("登录", type="primary")

        if submitted:
            if username == config.ADMIN_USERNAME and password == config.ADMIN_PASSWORD:
                st.session_state["logged_in"] = True
                st.rerun()
            else:
                st.error("用户名或密码错误")


def show_uploader():
    st.title("西工大政策问答平台 - 文件上传")

    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("退出登录"):
            st.session_state["logged_in"] = False
            st.rerun()
    with col2:
        st.caption("当前已登录")

    st.divider()

    file = st.file_uploader("上传文件",
                     type=["pdf", "docx", "txt"],
                     accept_multiple_files=False)
    if file is not None:
        st.write("File uploaded successfully!")
        st.write("Filename:", file.name)
        st.write("File type:", file.type)
        st.write("File size:", file.size, "bytes")

        try:
            text = extract_text(file)
            st.session_state["service"].upload_by_str(text, file.name)
            st.session_state["counter"] += 1
            st.success("文件上传成功！")
        except Exception as e:
            st.error(f"文件处理失败: {str(e)}")

    st.divider()

    # 直接粘贴文本上传
    st.subheader("或直接粘贴文本")

    col1, col2 = st.columns([4, 1])
    with col1:
        text_input = st.text_area(
            "在此粘贴文本内容",
            height=200,
            placeholder="请输入要上传的文本内容..."
        )
    with col2:
        filename = st.text_input("文件名", value="粘贴文本.txt")

    if st.button("提交文本", type="primary"):
        if text_input.strip():
            st.session_state["service"].upload_by_str(text_input, filename)
            st.session_state["counter"] += 1
            st.success("文本上传成功！")
        else:
            st.warning("请输入文本内容")

    st.divider()

    st.write("已上传" + str(st.session_state["counter"]) + "个文件（文件+文本）")


# 根据登录状态显示不同页面
if st.session_state["logged_in"]:
    show_uploader()
else:
    show_login()
