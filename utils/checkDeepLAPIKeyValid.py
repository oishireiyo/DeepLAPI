import os
import deepl

# Logging
import logging
logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
handler_format = logging.Formatter('%(asctime)s : [%(name)s - %(lineno)d] %(levelname)-8s - %(message)s')
stream_handler.setFormatter(handler_format)
logger.addHandler(stream_handler)

def CheckAPIKeyValid(api_key: str):
  try:
    logger.info(api_key)
    _translator = deepl.Translator(api_key)
    _result = _translator.translate_text('This is a test.', source_lang='EN', target_lang='JA')
    logger.debug(_result)
  except Exception as e:
    logger.error(e)
    return False
  else:
    logger.info('Given API Key is valid.')
    return True