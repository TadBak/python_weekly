from itertools import zip_longest

def tr(from_char, to_char):
    def translate(text):
        if len(to_char) < len(from_char):
            tbl = list(zip_longest(from_char, to_char, fillvalue=to_char[-1]))
        else:
            tbl = list(zip(from_char, to_char))
        txt_list = list(text)        
        for i, c in enumerate(txt_list):
            for original, replacement in tbl:
                if c == original:
                    txt_list[i] = replacement
        return ''.join(txt_list)
    return translate

