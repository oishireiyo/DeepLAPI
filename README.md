# DeepLAPI
このrepositoryは、[DeepL Python Library](https://github.com/DeepLcom/deepl-python)の機能を利用し、個人的に使いやすいようにパッケージングした物です。他のPythonパッケージでの翻訳機能の利用などに利用可能です。

## 認証キー、DeepL Python Libraryを取得する
[公式サイト](https://www.deepl.com/ja/pro/change-plan?utm_source=github&utm_medium=github-python-readme#developer)から認証キーを取得し、環境変数として扱えるように設定します。
```bash:.zshrc
export DEEPL_API_KEY="123456...." # ご自身が取得した認証キーを記載
```
次にDeepL Python Libraryをインストールする。
```bash
pip install --upgrade deepl
```
無料プランでも、1ヶ月に50万字以内の利用が可能です。

## Clone、利用
以下のコマンドから利用可能です。
```bash
git clone git@github.com:oishireiyo/DeepLAPI.git
cd DeepLAPI
python traslator.py
```