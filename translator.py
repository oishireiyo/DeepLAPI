import os
import deepl
from typing import Union

'''
以下は”DeepL Python Library (https://github.com/DeepLcom/deepl-python)のREADME.mdの一部を翻訳したもの。”

テキスト翻訳オプション
* source_lang: 入力言語の種別を指定する。自動で検出できる場合は省略可能。
* target_lang: 出力言語の種別を指定する。
* split_sentences: どのように入力テキストをセンテンスに分割するかを指定する。デフォルトでは'on'
  * on: 句読点、改行により入力テキストは分割される。
  * off: 入力テキストは分割されない。単一のセンテンスを持つ入力に用いるのが望ましい。
  * nonewlines: 句読点を用いたセンテンスの分割は行われるが、改行はしない。
* preserve_formatting: automatic-formatting-correctionに関する設定。デフォルトでは'True'
* formality: 翻訳機がフォーマルまたはインフォーマルのどちらを採用するか。限られた言語でのみ設定可能。(日本語は設定可能)
  * less: インフォーマル
  * more: フォーマル
* glossary: 用語集を使用するか否かを指定する。
* context: 自身は翻訳されないが、本文に影響を与えるであろう追加のコンテキストを入力に与えることができる。(Alpha feature)
* tag_handling: 内容が'html'か'xml'か
'''

DEEPL_API_KEY = os.environ['DEEPL_API_KEY']

class DeepLTranslator():
  '''
  * Only one glossary is available at the same time in this class. Make sure you include every entry in a glossary.
  '''
  def __init__(self, api_key: Union[str, None]=None) -> None:
    self.DEEPL_API_KEY=api_key if not api_key is None else os.environ['DEEPL_API_KEY']
    self.translator = deepl.Translator(self.DEEPL_API_KEY)
    self.glossary = None

  def get_available_source_languages(self) -> None:
    for language in self.translator.get_source_languages():
      print(f'{language.name}: {language.code}')

  def get_available_target_languages(self) -> None:
    for language in self.translator.get_target_languages():
      if language.supports_formality:
        print(f'{language.name}: {language.code} supports formality')
      else:
        print(f'{language.name}: {language.code} not supports formality')

  def create_glossary_with_entries(self, entries: dict[str, str], source_lang: str='EN', target_lang: str='JA'):
    self.glossary = self.translate.create_glossary(
      'My glossary',
      source_lang=source_lang,
      target_lang=target_lang,
      entries=entries,
    )
    print(
      f'Created: "{self.glossary.name}" ({self.glossary.glossary_id})\n'
      f'{self.glossary.source_lang} -> {self.glossary.target_lang}\n'
      f'containing {self.glossary.entry_count} entries\n'
    )

  def create_glossary_with_csv(self, csvfile: str, source_lang: str='EN', target_lang: str='JA') -> None:
    with open(csvfile, 'r', encoding='utf-8') as f:
      f_data = f.read()
    self.glossary = self.translator.create_glossary_from_csv(
      'My glossary',
      source_lang=source_lang,
      target_lang=target_lang,
      csv_data=f_data,
    )
    print(
      f'Created: "{self.glossary.name}" ({self.glossary.glossary_id})\n'
      f'{self.glossary.source_lang} -> {self.glossary.target_lang}\n'
      f'containing {self.glossary.entry_count} entries\n'
    )

  def get_glossary_entries(self) -> None:
    entries = self.translator.get_glossary_entries(self.glossary)
    for (key, value) in entries.items():
      print(f'{key} -> {value}')

  def delete_glossary(self) -> None:
    self.translator.delete_glossary(self.glossary)

  def translate(self, text: str, source_lang: str='EN', target_lang: str='JA', split_sentences: str='1') -> str:
    results = self.translator.translate_text(
      text, source_lang=source_lang, target_lang=target_lang, split_sentences=split_sentences, glossary=self.glossary)
    return results.text

if __name__ == '__main__':
  translator = DeepLTranslator()
  translator.create_glossary_with_csv(csvfile='./sample_glossary.csv')
  result = translator.translate(
    text='In this image, there are three people on what appears to be a set of a Japanese variety show.'
  )

  print(result)