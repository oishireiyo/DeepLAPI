import os
import deepl
from typing import Union

# Logging
import logging
logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
handler_format = logging.Formatter('%(asctime)s : [%(name)s - %(lineno)d] %(levelname)-8s - %(message)s')
stream_handler.setFormatter(handler_format)
logger.addHandler(stream_handler)

'''
以下はDeepL Python Library (https://github.com/DeepLcom/deepl-python)のREADME.mdの一部を翻訳したもの。

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

class DeepLTranslator():
  '''
  * So far, only one glossary is available at the same time in this class. Make sure you include every entry in a single glossary.
  '''
  def __init__(self, api_key: Union[str, None]=None) -> None:
    self.DEEPL_API_KEY=api_key if not api_key is None else os.environ['DEEPL_API_KEY']
    self.translator = deepl.Translator(self.DEEPL_API_KEY)
    self.glossaries = {}

  def set_api_key(self, api_key: str) -> bool:
    self.translator = deepl.Translator(api_key)
    return True

  def get_available_source_languages(self) -> None:
    for language in self.translator.get_source_languages():
      logger.info(f'{language.name}: {language.code}')

  def get_available_target_languages(self) -> None:
    for language in self.translator.get_target_languages():
      if language.supports_formality:
        logger.info(f'{language.name}: {language.code} supports formality')
      else:
        logger.info(f'{language.name}: {language.code} not supports formality')

  def get_available_glossary_languages_pair(self) -> None:
    for language_pair in self.translator.get_glossary_languages():
      logger.info(f'from {language_pair.source_lang} to {language_pair.target_lang}')

  def create_glossary_with_entries(self, entries: dict[str, str], glossary_name: str, source_lang: str='EN', target_lang: str='JA'):
    glossary = self.translator.create_glossary(
      glossary_name,
      source_lang=source_lang,
      target_lang=target_lang,
      entries=entries,
    )
    logger.info(
      f'Created: "{glossary.name}" ({glossary.glossary_id})\n'
      f'{glossary.source_lang} -> {glossary.target_lang}\n'
      f'containing {glossary.entry_count} entries\n'
    )
    self.glossaries[glossary_name] = glossary

  def create_glossary_with_csv(self, csvfile: str, glossary_name: str, source_lang: str='EN', target_lang: str='JA') -> None:
    with open(csvfile, 'r', encoding='utf-8') as f:
      f_data = f.read()
    glossary = self.translator.create_glossary_from_csv(
      glossary_name,
      source_lang=source_lang,
      target_lang=target_lang,
      csv_data=f_data,
    )
    logger.info(
      f'Created: "{glossary.name}" ({glossary.glossary_id})\n'
      f'{glossary.source_lang} -> {glossary.target_lang}\n'
      f'containing {glossary.entry_count} entries\n'
    )
    self.glossaries[glossary_name] = glossary

  def get_glossary_entries(self, glossary_name: str, as_dict: bool=False) -> Union[dict[str, str], None]:
    entries = self.translator.get_glossary_entries(self.glossaries[glossary_name])
    for (key, value) in entries.items():
      logger.info(f'{key} -> {value}')
    if as_dict:
      return entries

  def delete_glossary(self, glossary_name: str) -> None:
    self.translator.delete_glossary(self.glossaries[glossary_name])

  def delete_all_glossaries(self) -> None:
    for key in self.glossaries:
      self.delete_glossary(glossary_name=key)

  def translate(self, text: str, glossary_name: Union[str, None]=None, source_lang: str='EN', target_lang: str='JA', split_sentences: str='1') -> str:
    results = self.translator.translate_text(
      text, source_lang=source_lang, target_lang=target_lang, split_sentences=split_sentences,
      glossary=self.glossaries[glossary_name] if glossary_name is not None else None)
    return results.text

if __name__ == '__main__':
  translator = DeepLTranslator()
  translator.create_glossary_with_csv(csvfile='./../glossary/sample_glossary.csv', glossary_name='hogehoge1', source_lang='EN', target_lang='JA')
  result = translator.translate(
    text='In this image, there are three people on what appears to be a set of a Japanese variety show.',
    glossary_name='hogehoge1',
  )

  logger.info(result)

  translator.create_glossary_with_entries(entries={'お猿さん達': 'monkeys'}, glossary_name='hogehoge2', source_lang='JA', target_lang='EN')
  result = translator.translate(
    text='この写真では、日本のバラエティ番組のセットと思われる場所に3人のお猿さん達がいる。',
    glossary_name='hogehoge2',
    source_lang='JA',
    target_lang='EN-US',
  )

  logger.info(result)

  translator.delete_all_glossaries()