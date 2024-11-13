import openai
from utils.llm_faiss import run_llm
import streamlit as st
from pathlib import Path
import json

# OpenAI APIキー設定
openai.api_key = st.secrets["OPENAI_API_KEY"]


def load_vectorstore_config():
    """
    JSONファイルから vectorstore の設定を読み込む
    """
    config_path = Path("config/vectorstore.json")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"設定ファイルが見つかりません: {config_path}")
        return {}
    except json.JSONDecodeError:
        st.error(f"JSONファイルの形式が正しくありません: {config_path}")
        return {}

def vectorstore_dir(stock):
    """
    選択された図書に対応するベクターストアのパスを返す
    """
    config = load_vectorstore_config()
    return config.get(stock, "")


# header
st.header("chatbot-himeji🦜🔗")

# sidebar
with st.sidebar:
    stock = st.radio(
        label="対象図書を選択してください",
        options=(
            "土木工事共通仕様書",
            "土木請負工事必携",
            "規程集【道路Ⅰ編】",
            "規程集【道路Ⅱ編】",
            "規程集【河川編】",
            "規程集【砂防編_砂防】",
            "規程集【砂防編_急傾斜】",
            "規程集【砂防編_地すべり】",
            "地整便覧【土木工事共通編】",
            "地整便覧【道路編】",
            "地整便覧【河川編】",
            "道路構造令",
            "河川管理事務必携",
            "河川管理施設等構造令",
        ),
        index=0,
    )

    st.subheader("Link")
    st.markdown("""
    * [OpenAI API](https://platform.openai.com)
    * [LangChain](https://python.langchain.com/docs/introduction/)
    * [streamlit](https://streamlit.io/)
    """)

VECTORSTORE_DIR = vectorstore_dir(stock)

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "質問を入力してください"}
    ]

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = run_llm(
        query=prompt,
        vectordir=VECTORSTORE_DIR,
        chat_history=st.session_state["chat_history"],
    )
    msg = response["answer"]
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.session_state.chat_history.append((prompt, response["answer"]))
    st.chat_message("assistant").write(msg)
