import requests, uuid, json
import streamlit as st
from gtts import gTTS
import os

# API key and endpoint for the Microsoft Translator service

# Configuration for the Microsoft Translator API
API_KEY = "B0Yty8EiPvJoTPkGkh5L0PJ6usK3GhDHY4b5mHr5LGTjosskVMI8JQQJ99BGAC3pKaRXJ3w3AAAbACOG0gxn"
ENDPOINT = "https://api.cognitive.microsofttranslator.com"
LOCATION = "eastasia"

# Language options mapping
language_options = {
    'Afrikaans': 'af',
    'Arabic': 'ar',
    'Bangla': 'bn',
    'Bosnian (Latin)': 'bs',
    'Bulgarian': 'bg',
    'Cantonese (Traditional)': 'yue',
    'Catalan': 'ca',
    'Chinese (Literary)': 'lzh',
    'Chinese Simplified': 'zh-Hans',
    'Chinese Traditional': 'zh-Hant',
    'Croatian': 'hr',
    'Czech': 'cs',
    'Danish': 'da',
    'Dutch': 'nl',
    'English': 'en',
    'Estonian': 'et',
    'Fijian': 'fj',
    'Filipino': 'fil',
    'Finnish': 'fi',
    'French': 'fr',
    'German': 'de',
    'Greek': 'el',
    'Haitian Creole': 'ht',
    'Hebrew': 'he',
    'Hindi': 'hi',
    'Hmong Daw': 'mww',
    'Hungarian': 'hu',
    'Icelandic': 'is',
    'Indonesian': 'id',
    'Irish': 'ga',
    'Italian': 'it',
    'Japanese': 'ja',
    'Kiswahili': 'sw',
    'Klingon': 'tlh',
    'Korean': 'ko',
    'Latvian': 'lv',
    'Lithuanian': 'lt',
    'Malagasy': 'mg',
    'Malay': 'ms',
    'Maltese': 'mt',
    'Norwegian': 'nb',
    'Persian': 'fa',
    'Polish': 'pl',
    'Portuguese (Brazil)': 'pt',
    'Romanian': 'ro',
    'Russian': 'ru',
    'Samoan': 'sm',
    'Serbian (Cyrillic)': 'sr-Cyrl',
    'Serbian (Latin)': 'sr-Latn',
    'Slovak': 'sk',
    'Slovenian': 'sl',
    'Spanish': 'es',
    'Swedish': 'sv',
    'Tahitian': 'ty',
    'Tamil': 'ta',
    'Telugu': 'te',
    'Thai': 'th',
    'Tongan': 'to',
    'Turkish': 'tr',
    'Ukrainian': 'uk',
    'Urdu': 'ur',
    'Vietnamese': 'vi',
    'Welsh': 'cy',
    'Yucatec Maya': 'yua',
    'Zulu': 'zu'
}

# UI
st.set_page_config(page_title="Microsoft Translator", page_icon="🌍")
st.title("🌍 Microsoft Translator + TTS")
st.markdown("Translate text into multiple languages and listen to it using text-to-speech.")

# Input text
input_text = st.text_area("Enter text to translate", height=150)

# Auto-detect toggle
auto_detect = st.checkbox("Auto-detect language", value=True)

# If not auto-detect, let user choose source language
if not auto_detect:
    source_lang_name = st.selectbox("Select source language", options=['English'] + list(language_options.keys()))
    source_lang = 'en' if source_lang_name == 'English' else language_options[source_lang_name]
else:
    source_lang = ''  # leave empty to auto-detect

# Target languages
selected_languages = st.multiselect("Select target languages", options=list(language_options.keys()), default=['English'])

# Language selection for translation
selected_languages = st.multiselect(
    "Select languages to translate into",
    options=list(language_options.keys()),
    default=['Urdu']
)


if st.button("Translate"):
    if not input_text.strip():
        st.warning("Please enter some text.")
    elif not selected_languages:
        st.warning("Please select at least one target language.")
    else:
        # Construct request
        constructed_url = ENDPOINT + "/translate"
        params = {
            'api-version': '3.0',
            'to': [language_options[lang] for lang in selected_languages]
        }
        if not auto_detect:
            params['from'] = source_lang

        headers = {
            'Ocp-Apim-Subscription-Key': API_KEY,
            'Ocp-Apim-Subscription-Region': LOCATION,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        body = [{'text': input_text}]

        try:
            response = requests.post(constructed_url, params=params, headers=headers, json=body)
            result = response.json()

            if response.status_code != 200:
                st.error(f"API Error: {result.get('error', {}).get('message', 'Unknown error')}")
            else:
                st.success("Translations:")
                for translation in result[0]["translations"]:
                    lang_code = translation["to"]
                    translated_text = translation["text"]
                    lang_name = [name for name, code in language_options.items() if code == lang_code][0]
                    st.markdown(f"### {lang_name}")
                    st.markdown(f"> {translated_text}")

                    # Generate TTS using gTTS
                    tts = gTTS(text=translated_text, lang=lang_code.split('-')[0], slow=False)
                    audio_file = f"tts_{lang_code}.mp3"
                    tts.save(audio_file)

                    # Play audio
                    st.audio(audio_file, format="audio/mp3")

        except Exception as e:
            st.error(f"Something went wrong: {e}")