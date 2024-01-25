import streamlit as st
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# openAIのAPIキーを設定
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# proxy設定
# os.environ["http_proxy"] = st.secrets["PROXY"]
# os.environ["https_proxy"] = st.secrets["PROXY"]

# チャンクサイズとオーバーラップの設定
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100


def pdf_loader(pdf_file: str):
    '''PDFをOCR処理してLangChainのDocumentに変換する関数'''

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    loader = PyMuPDFLoader(pdf_file)

    docs = loader.load_and_split(text_splitter)

    return docs


if __name__ == "__main__":
    # PDFファイルを指定
    file = 'static/土木技術管理規程集/道路１編/第１章_道路一般.pdf'

    # Documentに変換
    docs = pdf_loader(file)

    print(f'{len(docs)}個のChunkを読み込みました。')
    print('-------------------------------------------------------------------------')
    print(f'page_content:{docs[0].page_content}')
    print('-------------------------------------------------------------------------')
    print(f'source:{docs[0].metadata["source"]}')
    print('-------------------------------------------------------------------------')
    print(f'page:{docs[0].metadata["page"]}')
    print('-------------------------------------------------------------------------')
