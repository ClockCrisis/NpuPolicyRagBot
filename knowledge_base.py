import os
from datetime import datetime

from langchain_community.embeddings import DashScopeEmbeddings
import config
import hashlib
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
#查重
def check_md5(md5_str):
    if not os.path.exists(config.md5_path):
        open(config.md5_path,'w').close()
        print("md5文件不存在，已创建新文件")
        return False
    else:
        for line in open(config.md5_path,'r', encoding="utf-8").readlines():
            line = line.strip()#去掉换行符
            if md5_str ==line:
                print("记录已存在，md5值为："+md5_str)
                return True
        print("记录不存在: "+md5_str)
        return False

#保存文件
def save_md5(md5_str):
    with open(config.md5_path,'a', encoding="utf-8") as f:
        f.write(md5_str+'\n')
    print("记录已添加，md5值为："+md5_str)

#字符串转换为md5
def str_to_md5(input_str,enconding="utf-8"):
    #字符串转换为字节流
    str_byte = input_str.encode(enconding)
    #得到md5对象
    md5_obj=hashlib.md5()
    #更新内容
    md5_obj.update(str_byte)
    # md5_obj.hexdigest()
    return md5_obj.hexdigest()#得到16进制字符串

class KnowledgeBaseService:
    def __init__(self):
        os.makedirs(config.persist_directory, exist_ok=True)
        self.chroma = Chroma(
            collection_name=config.collection_name,
            embedding_function=DashScopeEmbeddings(model = "text-embedding-v4"),
            persist_directory=config.persist_directory
        ) #向量数据库

        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,         # 分段的最大字符数
            chunk_overlap=config.chunk_overlap,       # 分段之间允许重叠字符数
            # 文本自然段落分隔的依据符号
            separators=config.separators,
            length_function=len,    # 统计字符的依据函数
        )#文本分割器

    #传入字符串，生成MD5值,查重并存入chroma数据库
    def upload_by_str(self,data,file_name):
        #生成MD5值
        md5 = str_to_md5(data)
        if check_md5(md5):
            print("文件已存在，无需上传")
            return False
        else:
            #文本分割
            if len(data) > config.chunk_size:
                print("文本长度超过分段大小，启动进行文本分割")
                chunks = self.spliter.split_text(data)
            else:
                print("文本长度未超过分段大小，已跳过文本分割")
                chunks = [data]

            meta_data = {
                "source": file_name,
                "creat_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "operator": "xz"
            }
            print("meta_data:"+str(meta_data))
            #存入chroma向量数据库,metadata需要是列表
            self.chroma.add_texts(chunks, metadatas=[meta_data]*len(chunks))
            #保存MD5值
            save_md5(md5)
            print("文件上传成功，载入向量库")
            return True

if __name__ == "__main__":
    # res = str_to_md5("hello world")
    # print(res)
    # print(str_to_md5("hello world1"))
    #
    # if not check_md5("5eb63bbbe01eeed093cb22bb8f5acdc3"):
    #     save_md5("5eb63bbbe01eeed093cb22bb8f5acdc3")
    kb = KnowledgeBaseService()
    kb.upload_by_str("hello world","test")