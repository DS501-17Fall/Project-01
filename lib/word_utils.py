def word_trim(word):
    start = 0
    end = len(word) - 1
    while start <= end:
        asc2 = ord(word[start])
        if 47 < asc2 < 58 or 64 < asc2 < 91 or 96 < asc2 < 123:
            break
        else:
            start += 1
    while start <= end:
        asc2 = ord(word[end])
        if 47 < asc2 < 58 or 63 < asc2 < 91 or 96 < asc2 < 123:
            break
        else:
            end -= 1
    if start > end:
        return ''
    else:
        return word[start:end + 1]


def word_filter(word, skipping=True):
    skipping_words = ('rt', 'amp', 'ourselves', 'hers', 'between', 'yourself', 'but', 'again',
                      'there', 'about', 'once',
                      'during', 'out', 'very',
                      'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its',
                      'yours', 'such', 'into',
                      'of', 'most',
                      'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him',
                      'each', 'the',
                      'themselves',
                      'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor',
                      'me', 'were',
                      'her', 'more',
                      'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both',
                      'up', 'to', 'ours',
                      'had',
                      'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and',
                      'been', 'have', 'in',
                      'will', 'on',
                      'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so',
                      'can', 'did', 'not',
                      'now',
                      'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only',
                      'myself', 'which',
                      'those', 'i',
                      'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'a', 'by', 'doing',
                      'it', 'how',
                      'was', 'here', 'than', 'us')
    word = word.lower()
    if len(word) == 0:
        return ''
    if skipping and word in skipping_words:
        return ''
    elif ord(word[0]) > 255:
        return ''
    elif word.startswith('@'):
        return ''
    elif word.startswith('#'):
        return ''
    elif word.startswith('&'):
        return ''
    elif word.startswith('http'):
        return ''
    else:
        return word_trim(word)
