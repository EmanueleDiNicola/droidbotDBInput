import re


def SplitCamelCase(string):
    list_string = re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', string)).split()
    return_strings = ""
    for word in list_string:
        if word is not '':
            return_strings = return_strings + word + " "
    return return_strings


def SplitSeparators(str):
    separators = (
        ' ', '-', '_', '.', ',', ';', ':', '|', '(', ')', '@', '&', '=', '“', '\"', '!', '?', '\'', '$', '+', '*', '#',
        '/', '\\', '[', ']', '{', '}')
    strings = list()
    word = ""
    for i in range(len(str)):
        if str[i] in separators:
            strings.append(word)
            word = ''
        else:
            word = word + str[i]
    if word is not '':
        strings.append(word)
    return strings
