import openai
import streamlit as st
from typing import Any, Dict, List
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI

# OpenAIのAPIキーを設定
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
openai.api_key = OPENAI_API_KEY

def run_llm(query: str, vectordir: str, chat_history: List[Dict[str, Any]] = []) -> Dict[str, Any]:
    """
    LLMを実行してクエリに対する応答を生成する
    
    Args:
        query: ユーザーからの質問
        vectordir: FAISSインデックスのディレクトリパス
        chat_history: チャット履歴
    
    Returns:
        Dict: 質問と回答を含む辞書
    """
    # Embeddingsの設定
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    
    # Vectorstoreの読み込み
    try:
        vectorstore = FAISS.load_local(
            folder_path=vectordir,
            embeddings=embeddings,
            allow_dangerous_deserialization=True
        )
    except Exception as e:
        st.error(f"ベクターストアの読み込みに失敗しました: {str(e)}")
        raise e

    # チャットモデルの設定 - 最新の安定バージョンを使用
    chat = ChatOpenAI(
        openai_api_key=OPENAI_API_KEY,
        verbose=True,
        temperature=0,
        model_name="gpt-4",  # 更新: 最新の安定バージョンを使用
        max_tokens=1000,  # 応答の最大長を設定
        request_timeout=120  # タイムアウトを設定
    )
    
    # チェーンの設定
    chain = ConversationalRetrievalChain.from_llm(
        llm=chat,
        retriever=vectorstore.as_retriever(
            search_kwargs={"k": 3}
        ),
        return_source_documents=True,
        verbose=True
    )
    
    # クエリの実行
    try:
        response = chain(
            {
                "question": query,
                "chat_history": chat_history
            }
        )
        return {
            "question": response["question"],
            "answer": format_answer(response)
        }
    except Exception as e:
        st.error(f"クエリ実行中にエラーが発生しました: {str(e)}")
        raise e

def format_answer(response: Dict[str, Any]) -> str:
    """
    応答をフォーマットする
    
    Args:
        response: LLMからの応答
    
    Returns:
        str: フォーマットされた応答文字列
    """
    sources = []
    for doc in response["source_documents"]:
        source = doc.metadata.get("source", "不明")
        page = doc.metadata.get("page", "不明")
        sources.append(f"{source}P:{page}")
    
    # 重複する出典を削除
    unique_sources = list(dict.fromkeys(sources))
    
    return f"{response['answer']}\n\n出典:{', '.join(unique_sources)}"