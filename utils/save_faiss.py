
import glob
import streamlit as st
import copy

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from utils.pdf_loader import pdf_loader


# openAIのAPIキーを設定
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]


# 作業ディレクトリの設定
WORK_DIR = "static/土木技術管理規程集/道路１編"


# vectorstoreを保存するディレクトリの設定
# 日本語のディレクトリ名はエラーになる
VECTORSTORE_DIR = "vectorstore/faiss/kiteisyuu/douro1"


def format_docs(org_docs, page_prefix: int):
    """Documentのmetadataを加工する関数"""
    docs = copy.deepcopy(org_docs)
    for doc in docs:
        # sourceを「土木技術管理規程集_道路１編」のフォーマットに修正
        source = doc.metadata["source"].split("/")
        new_source = source[1] + "_" + source[2].split("\\")[0]
        doc.metadata.update({"source": new_source})

        # ページ番号を「1-1」のフォーマットに修正
        new_page = f'{str(page_prefix)}-{str(doc.metadata["page"]+1)}'
        doc.metadata.update({"page": new_page})

    return docs


def save_local_faiss(docs):
    """DocumentをFAISSに保存する関数"""
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, verify=False)
    db = FAISS.from_documents(docs, embeddings)
    db.save_local(VECTORSTORE_DIR)
    print(f"{len(docs)}個のドキュメントを{VECTORSTORE_DIR}に保存しました。")
    return


if __name__ == "__main__":
    # ディレクトリ内のPDFファイルを取得
    pdf_files = glob.glob(f"{WORK_DIR}/*.pdf")

    # ディレクトリ内のPDFを単一のリストに格納
    result = []

    # 全PDFファイルを処理
    for i, file in enumerate(pdf_files):
        print(f"{file}を処理中・・・")

        # PDFをOCR処理してDocumentクラスに格納
        docs = pdf_loader(file)

        # Documentクラスのメタデータ（出典・ページ番号）を加工
        format = format_docs(docs, i + 1)

        result.extend(format)
        print(f"{len(format)}個のドキュメントを格納しました")
        print(f"ドキュメントの総数は{len(result)}個になりました。")

    # ベクトルDBに保存
    save_local_faiss(result)
