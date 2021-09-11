import deepl

class Deepl():

    def translate(self, text):

        translator = deepl.Translator("YOUR_AUTH_KEY")
        result = translator.translate_text(text, target_lang="EN")
        print(result)  # "Bonjour, le monde !"
        # Note: printing or converting the result to a string uses the output text

        # Translate multiple texts into British English
        result = translator.translate_text(["お元気ですか？", "¿Cómo estás?"], target_lang="EN-GB")
        print(result[0].text)  # "How are you?"
        print(result[0].detected_source_lang)  # "JA"
        print(result[1].text)  # "How are you?"
        print(result[1].detected_source_lang)  # "ES"

        # Translating documents
        translator.translate_document_from_filepath(
            "Instruction Manual.docx",
            "Bedienungsanleitlung.docx",
            target_lang="DE",
            formality="more"
        )

        # Check account usage
        usage = translator.get_usage()
        if usage.character.limit_exceeded:
            print("Character limit exceeded.")

        # Source and target languages
        for language in translator.get_source_languages():
            print(f"{language.code} ({language.name})")  # Example: "DE (German)"

        num_languages = sum([language.supports_formality
                            for language in translator.get_target_languages()])
        print(f"{num_languages} target languages support formality parameter")





* в чём разница между Deepl api и бесплатной версией
* Интерфейс: Deepl().translate(text_text_text) # => "translate_translate_translate"