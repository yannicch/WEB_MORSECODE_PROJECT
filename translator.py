from language import rusalf, engalf


def translatee(con, trans, text):
    try:
        if con == 'Russian':
            listoftext = list(text)
            convertedtext = ''.join(list(map(lambda x: rusalf.get(x.lower()) + ' ', listoftext)))
            return convertedtext
        elif con == 'English':
            listoftext = list(text)
            convertedtext = ''.join(list(map(lambda x: engalf.get(x.lower()) + ' ', listoftext)))
            return convertedtext
        elif con == 'Morsecode':
            if trans == 'English':
                listoftext = text.split(' ')
                convertedtext = ''.join(list(map(lambda x: get_key(engalf, value=x), listoftext)))
                return convertedtext
            elif trans == 'Russian':
                listoftext = text.split(' ')
                convertedtext = ''.join(list(map(lambda x: get_key(rusalf, value=x), listoftext)))
                return convertedtext
    except TypeError:
        pass


def get_key(*dictt, value):
    dictt = list(dictt)[0]
    for i, j in dictt.items():
        if j == value:
            return i

