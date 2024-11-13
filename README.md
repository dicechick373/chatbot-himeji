# chatbot-himeji

## 概要

「土木工事共通仕様書」や「土木技術管理規程集」等の技術図書を学習させたChat-GPT。

目的は「どこにどんなことが書いてあるか」の入り口として利用すること。

答えを得ることが目的ではないので、必ず自分で根拠資料を確認すること。（回答に出典根拠を付与している）

## 使用技術

### UI（画面）

[streamlit](https://streamlit.io/)というライブラリを利用。言語は[python](https://www.python.org/)

全て無料

### 技術図書の学習

[LangChain](https://www.langchain.com/)というライブラリで[RAG（検索拡張生成）](https://python.langchain.com/docs/tutorials/rag/)を実装している。

ベクトルDBには[FAISS](https://ai.meta.com/tools/faiss/)を採用。

全て無料

### Chat Bot

[OpenAI API](https://platform.openai.com/docs/overview)を利用している。APIとは、Chart-GPTの機能を外部アプリから利用できる仕組み。

公式ドキュメントには次のように記載されており、意図的にオプトインしない限り、OpenAIモデルのトレーニングや改善に使用されない。

このため、兵庫県のガイドラインにも抵触しない。（デジタル改革課に確認済）

> Your data is your data.
> As of March 1, 2023, data sent to the OpenAI API will not be used to train or improve OpenAI models (unless you > explicitly opt in). One advantage to opting in is that the models may get better at your use case over time.


APIの利用料金は有料（従量課金）


## 開発

コードはすべて公開しているので、独自開発が可能。

### 事前準備

#### python3.10

[python公式サイト](https://www.python.org/downloads/windows/)からWindowsインストーラーをダウンロードして実行する。

- [Python 3.10.11 - April 5, 2023 Windows installer (64-bit)](https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe)

インストールする際に、「Add python.exr to PATH」にチェックを入れておくこと。

![pythonインストール画面](img/python_install.PNG)

#### VSCode

[公式サイト](https://code.visualstudio.com/download)からWindows版をダウンロードして実行。

日本語化については[この記事](https://www.javadrive.jp/vscode/install/index4.html)を参照。

拡張機能（extention）もインストールしておく

- python
- Pylance

#### proxy環境の確認

「スタートメニュー」＞「設定」＞「ネットワークとインターネット」＞「プロキシ」をクリック。

プロキシ設定の画面内に「スクリプトのアドレス」があるので、そのアドレスをコピーしてブラウザに張り付けると、proxypacのファイルがダウンロードされる。

![スクリプトのアドレス](img/proxy_01.PNG)

メモ帳でファイルを開き、最下段に記載されているIPアドレスとポート番号を確認

```
return "PROXY 202.221.175.116:3128 ; PROXY 210.130.236.140:3128";
```

この場合、IPアドレスは「202.221.175.116」、ポート番号が「3128」

IPアドレスはおそらく２種類記載されているが、どちらか一方でよい。

#### pipの設定

pythonのパッケージ管理ツール「pip」は、python3.10をインストールすれば自動的にインストールされるが、HYOGOドメインに参加しているPC（つまり職場PC）で利用するためには、SSLの設定とプロキシ設定が必要。

##### フォルダオプションの設定変更

エクスプローラーを起動し、「表示」＞「オプション」をクリックするとフォルダーオプションが起動するので、「表示」タブを開いて、下記の設定をしてから「OK」で保存。

1. 『隠しファイル、隠しフォルダー、および隠しドライブを表示する』を選択。
2. 『登録されている拡張子は表示しない』のチェックを外す。

##### pip.iniファイルの作成

下記の場所にpip.iniファイルを作成する。m000000は職員番号。AppDataは隠しフォルダなので薄く表示される。

おそらくRomingフォルダまでは存在するので、その下にpipフォルダを作成する。

```
“C:\Users\m000000\AppData\Roaming\pip\pip.ini”
```

pip.iniファイルは、pipフォルダ内で「右クリック」＞「新規作成」＞「テキストドキュメント」を開き、ファイル名をpip.iniに変更して保存。

※基本的なことだが、フォルダオプションで拡張子を表示する設定にしていないと、pip.iniは作成できない。（pip.ini.txtになってしまう）

pip.iniに下記を張り付ける。

```bash
[global]
trusted-host = pypi.python.org
               pypi.org
               files.pythonhosted.org
proxy = http://<ユーザー名>:<パスワード>@<IPアドレス>:<ポート番号>
```
trusted-hostは信頼済みサイトを登録する。このままコピペでよい。

proxyは各PCやユーザ情報を登録する。

例えば

- 職員番号「m000000」
- パスワード「password」
- IPアドレス「202.221.175.116」
- ポート番号が「3128」

の場合は、下記のとおりとなる。

```bash
proxy = http://m000000:password@202.221.175.116:3128
```

なお、ここでいうパスワードは、HYOGOドメイン（職場PC）にログインする際のパスワードを指す。


### ローカル環境での実行

#### リポジトリのクローン

コマンドプロンプトで下記を実行

```
git clone https://github.com/dicechick373/chatbot-himeji.git
```

VSCodeを起動して、「フォルダを開く」でフォルダを開く。

#### ライブラリのインストール

アプリに必要なライブラリをインストールする

```python
pip install -r requirements.txt
```

必要なライブラリは下記で設定している。
[requirements.txt](requirements.txt)


#### 環境変数の設定

プロジェクト直下に.streamlit/secrets.tomlを作成して、OpenAIのAPIキーを登録する。

APIキーの取得は[こちら](https://platform.openai.com/docs/overview)

```toml
OPENAI_API_KEY=''

```

#### streamlitの起動

VSCode内のターミナルで下記を実行。アプリが起動する。

```bash
streamlit run Home.py
```

## プログラム説明

大きく分けると、次の5つのステップで構成される。

1. PDFのテキスト変換（OCR処理）
2. メタ情報（出典、ページ数）の付与
3. ベクトルDBへの保存
4. ベクトルDBの読込（最近傍探索）
5. 回答の生成（AIによる回答）

### PDFのテキスト変換（OCR処理）

[pdf_loader](utils/pdf_loader.py)という関数を作成している。

LangChainの[RecursiveCharacterTextSplitter](https://python.langchain.com/v0.1/docs/modules/data_connection/document_transformers/recursive_text_splitter/)を利用。

```python
def pdf_loader(pdf_file: str) -> Iterable[Document]:
    '''PDFをLangChainのDocumentに変換する関数'''

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    loader = PyMuPDFLoader(pdf_file)
    docs = loader.load_and_split(text_splitter)

    return docs
```

チャンクサイズとオーバーラップは回答精度に影響を与える設定。
ここを変更して、精度を確認していくことも必要。

```python
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100
```

### メタ情報（出典、ページ数）の付与

Chatの回答に出典（土木技術管理規程集）やページ数を含めるためには、[Documentクラス](https://python.langchain.com/api_reference/core/documents/langchain_core.documents.base.Document.html)のメタデータを設定する必要がある。


format_metadataという関数を作成して対応する。
ただし、文献によって設定が異なるので、出力結果をテストしながら関数を修正していくことが必要。

```python
def format_metadata(docs: Iterable[Document], page_prefix: int)-> Iterable[Document]:
    '''Documentのmetadataを加工する関数'''
    for doc in docs:
        # sourceを修正
        source = doc.metadata["source"].split("/")
        new_source = source[1] + "_" + source[2].split("\\")[0]
        doc.metadata.update({"source": new_source})

        # ページ番号を修正
        new_page = f'{str(page_prefix)}-{str(doc.metadata["page"]+1)}'
        doc.metadata.update({"page": new_page})

    return docs
```

### ベクトルDBへの保存

変換してmetadataを付与したDocumentをローカルファイルに保存する。

無料枠で利用するためには、1文献で1ファイルを作成する必要がある。（このため、画面では対象の文献を指定しなければならないという制約が発生する）

```python
def save_local_faiss(docs: Iterable[Document]):
    '''DocumentをFAISSに保存する関数'''
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    db = FAISS.from_documents(docs, embeddings)
    db.save_local(VECTORSTORE_DIR)
    print(f'{len(docs)}個のドキュメントを{VECTORSTORE_DIR}に保存しました。')
    return
```

### ベクトルDBの読込（最近傍探索）

画面で入力した質問の内容を[embedding](https://python.langchain.com/docs/how_to/embed_text/)して、ベクトルDBの最近傍探索を実施する。

スコアの高いDocumentが複数返却される。

```python
def load_faiss():

    # set embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    # load vectorstore
    vectorstore = FAISS.load_local(VECTORSTORE_DIR, embeddings)

    return vectorstore
```

### 回答の生成（AIによる回答）

最近傍探索結果の情報（Document）を踏まえて、AIが回答を作成する。

```python
def run_llm(query):
    '''ベクトルDBの検索結果を踏まえて回答する関数'''
    vectorstore = load_faiss()

    # set chat-model
    chat = ChatOpenAI(
        openai_api_key=OPENAI_API_KEY,
        verbose=True,
        temperature=0,
        model_name="gpt-4"
    )

    # set chain
    chain = ConversationalRetrievalChain.from_llm(
        llm=chat,
        retriever=vectorstore.as_retriever(),
        return_source_documents=True)

    return chain({"question": query, "chat_history": []})
```