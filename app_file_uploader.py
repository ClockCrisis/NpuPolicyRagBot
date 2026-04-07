import streamlit as st
import tempfile
import os
from io import BytesIO
from knowledge_base import KnowledgeBaseService

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


st.title("西工大政策问答平台 - 文件上传")

file = st.file_uploader("Upload your files here",
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

st.write("已上传" + str(st.session_state["counter"]) + "个文件")
