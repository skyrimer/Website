from googletrans import Translator

translator = Translator()
results = translator.translate('हॅलो वर्ल्ड')
print(results.text)