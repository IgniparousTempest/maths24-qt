_strings = {
    'en': {

    }
}


class Strings:
    def __init__(self, language_code: str):
        self.code = language_code
        self.code_parent = language_code.split('_')[0] if '_' in language_code else language_code

    def get(self, key: str) -> str:
        """
        Returns a string in the correct language.
        Defaults to English if the key is not in the specified language.
        :param key: The key for the string.
        :return: The corresponding string.
        """
        # Try specific language, e.g. 'en_za'
        try:
            return _strings[self.code][key]
        except KeyError:
            pass
        # Try language parent, e.g. 'en'
        try:
            return _strings[self.code_parent][key]
        except KeyError:
            pass
        # Return English
        return _strings['en'][key]