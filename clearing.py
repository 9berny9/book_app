import pandas as pd


def publisher_languages():
    languages = {"English": ["0", "1"], "French": "2", "German": "3"}
    return languages


def get_language(data, selected_language):
    language_condition = publisher_languages()
    return data[data["ISBN"].str.startswith(tuple(language_condition[selected_language]), na=False)]
