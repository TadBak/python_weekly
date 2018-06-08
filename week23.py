def str_range(first_char, last_char, step=1):
    return (chr(n) for n in range(ord(first_char), ord(last_char)+1, step)
                    if n <= 0x10FFFF)

