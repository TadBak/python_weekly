import string

def create_password_checker(min_uppercase, min_lowercase, min_punctuation,
                            min_digits):
    def test_password(passwd):
        counts = {}
        counts['uppercase'] = sum(char in string.ascii_uppercase
                                  for char in passwd) - min_uppercase
        counts['lowercase'] = sum(char in string.ascii_lowercase
                                  for char in passwd) - min_lowercase
        counts['punctuation'] = sum(char in string.punctuation
                                    for char in passwd) - min_punctuation
        counts['digits'] = sum(char in string.digits
                               for char in passwd) - min_digits
        valid = True
        for num in counts.values():
            valid &= num >= 0
        return valid, counts
    return test_password

