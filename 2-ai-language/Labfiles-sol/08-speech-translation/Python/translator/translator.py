from dotenv import load_dotenv
from datetime import datetime
import os

# Import namespaces
from azure.core.credentials import AzureKeyCredential
import azure.cognitiveservices.speech as speech_sdk

def main():
    try:
        global speech_config
        global translation_config

        # Get Configuration Settings
        load_dotenv()
        speech_key = os.getenv('KEY')
        speech_region = os.getenv('REGION')

        # Configure translation
        translation_config = speech_sdk.translation.SpeechTranslationConfig(
            speech_key,
            speech_region
        )
        translation_config.speech_recognition_language = 'en-US'
        translation_config.add_target_language('fr')
        translation_config.add_target_language('es')
        translation_config.add_target_language('hi') 
        print(f'Ready to translate from: {translation_config.speech_recognition_language}')

        # Configure speech
        speech_config = speech_sdk.SpeechConfig(
            speech_key,
            speech_region
        )
        print(f'Ready to use speech service in: {speech_config.region}')


        # Get user input
        targetLanguage = ''
        while targetLanguage != 'quit':
            targetLanguage = input('\nEnter a target language\n fr = French\n es = Spanish\n hi = Hindi\n Enter anything else to stop\n').lower()
            if targetLanguage in translation_config.target_languages:
                Translate(targetLanguage)
            else:
                targetLanguage = 'quit'
                

    except Exception as ex:
        print(ex)

def Translate(targetLanguage):
    translation = ''

    # Translate speech
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # audio_file = os.path.join(current_dir, "station.wav")
    # audio_config_in = speech_sdk.AudioConfig(
    #     filename=audio_file
    # )
    # translator = speech_sdk.translation.TranslationRecognizer(
    #     translation_config=translation_config,
    #     audio_config=audio_config_in
    # )
    # print("Getting speech from file...")
    # result = translator.recognize_once_async().get()
    # print(f'Translating {result.text}')
    # translation = result.translations[targetLanguage]
    # print(translation)

    # Translate speech with microphone
    audio_config_in = speech_sdk.AudioConfig(
        use_default_microphone=True
    )
    translator = speech_sdk.translation.TranslationRecognizer(
        translation_config=translation_config,
        audio_config=audio_config_in
    )
    print('Speak now...')
    result = translator.recognize_once_async().get()
    print(f'Translating {result.text}')
    translation = result.translations[targetLanguage]
    print(translation)

    # Synthesize translation
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, "output.wav")
    voices = {
        "fr": "fr-FR-HenriNeural",
        "es": "es-ES-ElviraNeural",
        "hi": "hi-HI-MadhurNeural"
    }
    speech_config.speech_synthesis_voice_name = voices.get(targetLanguage)
    audio_config_out = speech_sdk.audio.AudioConfig(filename=output_file)
    speech_synthesizer = speech_sdk.SpeechSynthesizer(
        speech_config=speech_config,
        audio_config=audio_config_out
        )
    speak = speech_synthesizer.speak_text_async(translation).get()
    if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)
    else:
        print(f'Spoken output saved to {output_file}')


if __name__ == "__main__":
    main()
