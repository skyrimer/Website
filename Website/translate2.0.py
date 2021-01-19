from googletrans import Translator
from subprocess import call
from os.path import join, exists
from os import remove
from colorama import init, Fore
from codecs import open
init()
language = input('Enter the language:')


def get_lines(file_name):
    """Gets the file and returns

    Args:
        file_name (file): file which needs translation

    Returns:
        phrase_dict (dict): index of the line -- phrase to translate
        file_text (list): list with lines of the file
    """
    phrase_dict = {}
    file_text = file_name.readlines()
    for line_index, line in enumerate(file_text):
        if line.startswith('msgid '):
            line = line[7:-2]
            if line:
                phrase_dict[line_index] = line
    return phrase_dict, file_text


def translate(phrase_dict: dict, file_text: list, dest=language):
    """Translate the file for flask_babel

    Args:
        lines_to_translate (list): list of indexes of lines to translate
        file_data (list): list of lines from the file

    Returns:
        list: list of lines with translations, which will be comverted to a file
    """
    translator = Translator()
    translated_phrase_list = translator.translate(list(phrase_dict.values()), dest=dest)                             
    print(Fore.GREEN + "Translated successfully!!" + Fore.RESET)
    #phrase_dict = {k: phrase.text for phrase in translated_phrase_list for k in phrase_dict}
    key_list = list(phrase_dict.keys())
    for i in range(len(key_list)): 
        phrase_dict[key_list[i]] = translated_phrase_list[i].text
    for index_line, translated_phrase in phrase_dict.items():
        print(Fore.CYAN + f'Writen as: {translated_phrase}')
        file_text[index_line+1] = f'msgstr "{translated_phrase}"'
    return file_text


def delete_files():
    remove('babel.cfg')
    remove('messages.pot')
    # remove(trans_path)




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
with open(trans_path, 'r', 'utf-8') as translation_file:
    translated_file_data = translate(*get_lines(translation_file))
with open(trans_path, 'w', 'utf-8') as translation_file:
    for line in translated_file_data:
        translation_file.write(line)
print(Fore.GREEN + 'Pass pass the translations!!!' + Fore.RESET)

# compiling
# call('pybabel compile -d translations')
print(Fore.GREEN + 'Pass initializing!!!' + Fore.RESET)

# removing all the unnecessary files
delete_files()
print(Fore.GREEN + 'Unnesesary files deleted' + Fore.RESET)

print(Fore.GREEN + 'Done!!!')
