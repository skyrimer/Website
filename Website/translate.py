from googletrans import Translator
from subprocess import call
from os.path import join, exists
from os import remove
from colorama import init, Fore
import codecs
init()


def translate(lines_to_translate, file_data):
    translator = Translator()
    for line in lines_to_translate:
        phrase = file_data[line][7:-2]
        translated_phrase = translator.translate(phrase, dest=language)
        translated_phrase = translated_phrase.text.capitalize()
        if phrase == translated_phrase:
            print(Fore.RED + 'Unable to translate. Googletrans issues')
            file_data[line+1] = f'msgstr "{phrase}"'
        else:
            print(Fore.CYAN + f'Transalted: {translated_phrase}')
            file_data[line+1] = f'msgstr "{translated_phrase}"'
    return file_data


def get_lines(file_name):
    lines = file_name.readlines()
    translation_list = []
    for line in range(len(lines)):
        if lines[line].startswith('msgid '):
            translation_list.append(line)
    return translation_list[1:], lines


def delete_files():
    remove('babel.cfg')
    remove('messages.pot')
    # remove(trans_path)


language = input('Enter the language:')

# writing the babel.cfg file
with open('babel.cfg', 'w') as f:
    f.write("""[python: **.py]
[jinja2: **/templates/**.html]
extensions=jinja2.ext.autoescape,jinja2.ext.with_
""")

# creating the template
call('pybabel extract -F babel.cfg -o messages.pot .')
print(Fore.GREEN + 'Pass the template!!!' + Fore.RESET)

# initializing the localization
call(f'pybabel init -i messages.pot -d translations -l {language}')
print(Fore.GREEN + 'Pass the init of translations!!!' + Fore.RESET)

# localization
trans_path = join(f'translations\{language}\LC_MESSAGES', 'messages.po')
with open(trans_path, 'r') as translation_file:
    translated_file_data = translate(*get_lines(translation_file))
with codecs.open(trans_path, 'w', 'utf-8') as translation_file:
    for line in translated_file_data:
        translation_file.write(line)
print(Fore.GREEN + 'Pass pass the translations!!!' + Fore.RESET)

# compiling
call('pybabel compile -d translations')

# removing all the unnecessary files
delete_files()

print(Fore.GREEN + 'Done!!!')
