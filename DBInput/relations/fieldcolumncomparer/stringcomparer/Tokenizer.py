import re


def SplitCamelCase(string):
    list_string = re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', string)
    return_strings = ""
    for word in list_string:
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
            print(strings)
            strings.append(word)
            word = ''
        else:
            word = word + str[i]
    if word is not '':
        strings.append(word)
    return strings
