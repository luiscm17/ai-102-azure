---
lab:
    title: 'Traducir Voz'
    description: "Traduce voz de un idioma a voz e impleméntalo en tu propia app."
---

# Traducir Voz

Azure AI Speech incluye una API de traducción de voz que puedes usar para traducir lenguaje hablado. Por ejemplo, supón que quieres desarrollar una aplicación traductora que las personas puedan usar cuando viajen a lugares donde no hablan el idioma local. Podrían decir frases como "¿Dónde está la estación?" o "Necesito encontrar una farmacia" en su propio idioma, y hacer que se traduzcan al idioma local. En este ejercicio, usarás el SDK de Azure AI Speech para Python para crear una aplicación simple basada en este ejemplo.

Si bien este ejercicio está basado en Python, puedes desarrollar aplicaciones de traducción de voz usando múltiples SDKs específicos de lenguaje; incluyendo:

- [SDK de Azure AI Speech para Python](https://pypi.org/project/azure-cognitiveservices-speech/)
- [SDK de Azure AI Speech para .NET](https://www.nuget.org/packages/Microsoft.CognitiveServices.Speech)
- [SDK de Azure AI Speech para JavaScript](https://www.npmjs.com/package/microsoft-cognitiveservices-speech-sdk)

Este ejercicio toma aproximadamente **30** minutos.

> **NOTA**
> Este ejercicio está diseñado para completarse en Azure cloud shell, donde el acceso directo al hardware de sonido de tu computadora no es compatible. El laboratorio por lo tanto usará archivos de audio para flujos de entrada y salida de voz. El código para lograr los mismos resultados usando un micrófono y altavoz se proporciona para tu referencia.

## Crear un recurso de Azure AI Speech

Comencemos creando un recurso de Azure AI Speech.

1. Abre el [Azure portal](https://portal.azure.com) en `https://portal.azure.com`, e inicia sesión usando la cuenta Microsoft asociada con tu suscripción de Azure.
1. En el campo de búsqueda superior, busca **Speech service**. Selecciónalo de la lista, luego selecciona **Create**.
1. Aprovisiona el recurso usando la siguiente configuración:
    - **Subscription**: *Tu suscripción de Azure*.
    - **Resource group**: *Elige o crea un grupo de recursos*.
    - **Region**:*Elige cualquier región disponible*
    - **Name**: *Ingresa un nombre único*.
    - **Pricing tier**: Selecciona **F0** (*gratuito*), o **S** (*estándar*) si F no está disponible.
1. Selecciona **Review + create**, luego selecciona **Create** para aprovisionar el recurso.
1. Espera a que la implementación se complete, y luego ve al recurso implementado.
1. Ve la página **Keys and Endpoint** en la sección **Resource Management**. Necesitarás la información en esta página más adelante en el ejercicio.

## Prepararse para desarrollar una app en Cloud Shell

1. Dejando la página **Keys and Endpoint** abierta, usa el botón **[\>_]** a la derecha de la barra de búsqueda en la parte superior de la página para crear un nuevo Cloud Shell en Azure portal, seleccionando un entorno ***PowerShell***. El cloud shell proporciona una interfaz de línea de comandos en un panel en la parte inferior de Azure portal.

    > **Nota**: Si previamente creaste un cloud shell que usa un entorno *Bash*, cámbialo a ***PowerShell***.

1. En la barra de herramientas del cloud shell, en el menú **Settings**, selecciona **Go to Classic version** (esto es requerido para usar el editor de código).

    **<font color="red">Asegúrate de haber cambiado a la versión clásica del cloud shell antes de continuar.</font>**

1. En el panel de PowerShell, ingresa los siguientes comandos para clonar el repositorio GitHub de este ejercicio:

    ```bash
    rm -r mslearn-ai-language -f
    git clone https://github.com/microsoftlearning/mslearn-ai-language
    ```

    > **Tip**: Al ingresar comandos en el cloudshell, la salida puede ocupar una gran parte del búfer de pantalla. Puedes limpiar la pantalla ingresando el comando `cls` para facilitar el enfoque en cada tarea.

1. Después de que el repositorio haya sido clonado, navega a la carpeta que contiene los archivos de código:

    ```bash
    cd mslearn-ai-language/Labfiles/08-speech-translation/Python/translator
    ```

1. En el panel de línea de comandos, ejecuta el siguiente comando para ver los archivos de código en la carpeta **translator**:

    ```bash
    ls -a -l
    ```

    Los archivos incluyen un archivo de configuración (**.env**) y un archivo de código (**translator.py**).

1. Crea un entorno virtual de Python e instala el paquete del SDK de Azure AI Speech y otros paquetes requeridos ejecutando el siguiente comando:

    ```bash
    python -m venv labenv
    ./labenv/bin/Activate.ps1
    pip install -r requirements.txt azure-cognitiveservices-speech==1.42.0
    ```

1. Ingresa el siguiente comando para editar el archivo de configuración que ha sido proporcionado:

    ```bash
    code .env
    ```

    El archivo se abre en un editor de código.

1. Actualiza los valores de configuración para incluir la **region** y una **key** del recurso de Azure AI Speech que creaste (disponibles en la página **Keys and Endpoint** de tu recurso de Azure AI Translator en Azure Portal).
1. Después de que hayas reemplazado los marcadores de posición, usa el comando **CTRL+S** para guardar tus cambios y luego usa el comando **CTRL+Q** para cerrar el editor de código mientras mantienes abierta la línea de comandos del cloud shell.

## Agregar código para usar el SDK de Azure AI Speech

> **Tip**: A medida que agregas código, asegúrate de mantener la sangría correcta.

1. Ingresa el siguiente comando para editar el archivo de código que ha sido proporcionado:

    ```bash
    code translator.py
    ```

1. En la parte superior del archivo de código, bajo las referencias de espacio de nombres existentes, encuentra el comentario **Import namespaces**. Luego, bajo este comentario, agrega el siguiente código específico del lenguaje para importar los espacios de nombres que necesitarás para usar el SDK de Azure AI Speech:

    ```python
   # Import namespaces
   from azure.core.credentials import AzureKeyCredential
   import azure.cognitiveservices.speech as speech_sdk
    ```

1. En la función **main**, bajo el comentario **Get config settings**, nota que el código carga la key y la región que definiste en el archito de configuración.

1. Encuentra el siguiente código bajo el comentario **Configure translation**, y agrega el siguiente código para configurar tu conexión al endpoint de Speech de Azure AI Services:

    ```python
   # Configure translation
   translation_config = speech_sdk.translation.SpeechTranslationConfig(speech_key, speech_region)
   translation_config.speech_recognition_language = 'en-US'
   translation_config.add_target_language('fr')
   translation_config.add_target_language('es')
   translation_config.add_target_language('hi')
   print('Listo para traducir desde',translation_config.speech_recognition_language)
    ```

1. Usarás el **SpeechTranslationConfig** para traducir voz a texto, pero también usarás un **SpeechConfig** para sintetizar traducciones a voz. Agrega el siguiente código bajo el comentario **Configure speech**:

    ```python
   # Configure speech
   speech_config = speech_sdk.SpeechConfig(speech_key, speech_region)
   print('Listo para usar el servicio de voz en:', speech_config.region)
    ```

1. Guarda tus cambios (*CTRL+S*), pero deja el editor de código abierto.

## Ejecutar la app

Hasta ahora, la app no hace nada más que conectarse a tu recurso de Azure AI Speech, pero es útil ejecutarla y verificar que funcione antes de agregar funcionalidad de voz.

1. En la línea de comandos, ingresa el siguiente comando para ejecutar la app traductora:

    ```bash
    python translator.py
    ```

    El código debería mostrar la región del recurso del servicio de voz que la aplicación usará, un mensaje de que está listo para traducir desde en-US y solicitarte un idioma objetivo. Una ejecución exitosa indica que la app se ha conectado a tu servicio de Azure AI Speech. Presiona ENTER para terminar el programa.

## Implementar traducción de voz

Ahora que tienes un **SpeechTranslationConfig** para el servicio de Azure AI Speech, puedes usar la API de traducción de voz de Azure AI Speech para reconocer y traducir voz.

1. En el archivo de código, nota que el código usa la función **Translate** para traducir entrada hablada. Luego en la función **Translate**, bajo el comentario **Translate speech**, agrega el siguiente código para crear un cliente **TranslationRecognizer** que pueda usarse para reconocer y traducir voz desde un archivo.

    ```python
   # Translate speech
   current_dir = os.getcwd()
   audioFile = current_dir + '/station.wav'
   audio_config_in = speech_sdk.AudioConfig(filename=audioFile)
   translator = speech_sdk.translation.TranslationRecognizer(translation_config, audio_config = audio_config_in)
   print("Obteniendo voz desde archivo...")
   result = translator.recognize_once_async().get()
   print('Traduciendo "{}"'.format(result.text))
   translation = result.translations[targetLanguage]
   print(translation)
    ```

1. Guarda tus cambios (*CTRL+S*), y re-ejecuta el programa:

    ```bash
    python translator.py
    ```

1. Cuando se solicite, ingresa un código de idioma válido (*fr*, *es*, o *hi*). El programa debería transcribir tu archivo de entrada y traducirlo al idioma que especificaste (Francés, Español, o Hindi). Repite este proceso, probando cada idioma compatible con la aplicación.

    > **NOTA**: La traducción al Hindi puede no mostrarse siempre correctamente en la ventana de la Consola debido a problemas de codificación de caracteres.

1. Cuando hayas terminado, presiona ENTER para terminar el programa.

> **NOTA**: El código en tu aplicación traduce la entrada a los tres idiomas en una sola llamada. Solo se muestra la traducción para el idioma específico, pero podrías recuperar cualquiera de las traducciones especificando el código del idioma objetivo en la colección **translations** del resultado.

## Sintetizar la traducción a voz

Hasta ahora, tu aplicación traduce entrada hablada a texto; lo que podría ser suficiente si necesitas pedirle ayuda a alguien mientras viajas. Sin embargo, sería mejor tener la traducción hablada en voz alta en una voz adecuada.

> **Nota**: Debido a las limitaciones de hardware del cloud shell, dirigiremos la salida de voz sintetizada a un archivo.

1. En la función **Translate**, encuentra el comentario **Synthesize translation**, y agrega el siguiente código para usar un cliente **SpeechSynthesizer** para sintetizar la traducción como voz y guardarla como un archivo .wav:

    ```python
   # Synthesize translation
   output_file = "output.wav"
   voices = {
            "fr": "fr-FR-HenriNeural",
            "es": "es-ES-ElviraNeural",
            "hi": "hi-IN-MadhurNeural"
   }
   speech_config.speech_synthesis_voice_name = voices.get(targetLanguage)
   audio_config_out = speech_sdk.audio.AudioConfig(filename=output_file)
   speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config, audio_config_out)
   speak = speech_synthesizer.speak_text_async(translation).get()
   if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)
   else:
        print("Salida hablada guardada en " + output_file)
    ```

1. Guarda tus cambios (*CTRL+S*), y re-ejecuta el programa:

    ```bash
    python translator.py
    ```

1. Revisa la salida de la aplicación, que debería indicar que la salida hablada de la traducción fue guardada en un archivo. Cuando hayas terminado, presiona **ENTER** para terminar el programa.
1. Si tienes un reproductor de medios capaz de reproducir archivos de audio .wav, descarga el archivo que fue generado ingresando el siguiente comando:

    ```bash
    download ./output.wav
    ```

    El comando download crea un enlace emergente en la parte inferior derecha de tu navegador, que puedes seleccionar para descargar y abrir el archivo.

> **NOTA**
> *En este ejemplo, has usado un **SpeechTranslationConfig** para traducir voz a texto, y luego usado un **SpeechConfig** para sintetizar la traducción como voz. De hecho, puedes usar el **SpeechTranslationConfig** para sintetizar la traducción directamente, pero esto solo funciona cuando se traduce a un solo idioma, y resulta en un flujo de audio que típicamente se guarda como un archivo.*

## Limpiar recursos

Si has terminado de explorar el servicio Azure AI Speech, puedes eliminar los recursos que creaste en este ejercicio. Así es cómo:

1. Cierra el panel de Azure cloud shell
1. En Azure Portal, navega al recurso de Azure AI Speech que creaste en este laboratorio.
1. En la página del recurso, selecciona **Delete** y sigue las instrucciones para eliminar el recurso.

## ¿Qué pasa si tienes un micrófono y altavoz?

En este ejercicio, usaste archivos de audio para la entrada y salida de voz. Veamos cómo se puede modificar el código para usar hardware de audio.

### Usar traducción de voz con un micrófono

1. Si tienes un micrófono, puedes usar el siguiente código para capturar entrada hablada para traducción de voz:

    ```python
   # Translate speech
   audio_config_in = speech_sdk.AudioConfig(use_default_microphone=True)
   translator = speech_sdk.translation.TranslationRecognizer(translation_config, audio_config = audio_config_in)
   print("Habla ahora...")
   result = translator.recognize_once_async().get()
   print('Traduciendo "{}"'.format(result.text))
   translation = result.translations[targetLanguage]
   print(translation)
    ```

> **Nota**: ¡El micrófono predeterminado del sistema es la entrada de audio predeterminada, por lo que también podrías omitir el AudioConfig por completo!

### Usar síntesis de voz con un altavoz

1. Si tienes un altavoz, puedes usar el siguiente código para sintetizar voz.

    ```python
   # Synthesize translation
   voices = {
            "fr": "fr-FR-HenriNeural",
            "es": "es-ES-ElviraNeural",
            "hi": "hi-IN-MadhurNeural"
   }
   speech_config.speech_synthesis_voice_name = voices.get(targetLanguage)
   audio_config_out = speech_sdk.audio.AudioConfig(use_default_speaker=True)
   speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config, audio_config_out)
   speak = speech_synthesizer.speak_text_async(translation).get()
   if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)
    ```

> **Nota**: ¡El altavoz predeterminado del sistema es la salida de audio predeterminada, por lo que también podrías omitir el AudioConfig por completo!

## Más información

Para más información sobre el uso de la API de traducción de voz de Azure AI Speech, consulta la [documentación de traducción de voz](https://learn.microsoft.com/azure/ai-services/speech-service/speech-translation).
