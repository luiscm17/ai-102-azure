---
lab:
    title: 'Reconocer y Sintetizar Voz'
    description: "Implementa un reloj parlante que convierte voz a texto, y texto a voz."
---

# Reconocer y sintetizar voz

**Azure AI Speech** es un servicio que proporciona funcionalidad relacionada con la voz, incluyendo:

- Una API de *voz a texto* que te permite implementar reconocimiento de voz (convertir palabras habladas audibles en texto).
- Una API de *texto a voz* que te permite implementar síntesis de voz (convertir texto en voz audible).

En este ejercicio, usarás ambas APIs para implementar una aplicación de reloj parlante.

Si bien este ejercicio está basado en Python, puedes desarrollar aplicaciones de voz usando múltiples SDKs específicos de lenguaje; incluyendo:

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

## Preparar y configurar la app de reloj parlante

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

1. Después de que el repositorio haya sido clonado, navega a la carpeta que contiene los archivos de código de la aplicación de reloj parlante:

    ```bash
    cd mslearn-ai-language/Labfiles/07-speech/Python/speaking-clock
    ```

1. En el panel de línea de comandos, ejecuta el siguiente comando para ver los archivos de código en la carpeta **speaking-clock**:

    ```bash
    ls -a -l
    ```

    Los archivos incluyen un archivo de configuración (**.env**) y un archivo de código (**speaking-clock.py**). Los archivos de audio que tu aplicación usará están en la subcarpeta **audio**.

1. Crea un entorno virtual de Python e instala el paquete del SDK de Azure AI Speech y otros paquetes requeridos ejecutando el siguiente comando:

    ```bash
    python -m venv labenv
    ./labenv/bin/Activate.ps1
    pip install -r requirements.txt azure-cognitiveservices-speech==1.42.0
    ```

1. Ingresa el siguiente comando para editar el archivo de configuración:

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
    code speaking-clock.py
    ```

1. En la parte superior del archivo de código, bajo las referencias de espacio de nombres existentes, encuentra el comentario **Import namespaces**. Luego, bajo este comentario, agrega el siguiente código específico del lenguaje para importar los espacios de nombres que necesitarás para usar el SDK de Azure AI Speech:

    ```python
   # Import namespaces
   from azure.core.credentials import AzureKeyCredential
   import azure.cognitiveservices.speech as speech_sdk
    ```

1. En la función **main**, bajo el comentario **Get config settings**, nota que el código carga la key y la región que definiste en el archivo de configuración.

1. Encuentra el comentario **Configure speech service**, y agrega el siguiente código para usar la key de AI Services y tu región para configurar tu conexión al endpoint de Speech de Azure AI Services:

    ```python
   # Configure speech service
   speech_config = speech_sdk.SpeechConfig(speech_key, speech_region)
   print('Listo para usar el servicio de voz en:', speech_config.region)
    ```

1. Guarda tus cambios (*CTRL+S*), pero deja el editor de código abierto.

## Ejecutar la app

Hasta ahora, la app no hace nada más que conectarse a tu servicio Azure AI Speech, pero es útil ejecutarla y verificar que funcione antes de agregar funcionalidad de voz.

1. En la línea de comandos, ingresa el siguiente comando para ejecutar la app de reloj parlante:

    ```bash
    python speaking-clock.py
    ```

    El código debería mostrar la región del recurso del servicio de voz que la aplicación usará. Una ejecución exitosa indica que la app se ha conectado a tu recurso de Azure AI Speech.

## Agregar código para reconocer voz

Ahora que tienes un **SpeechConfig** para el servicio de voz en el recurso de Azure AI Services de tu proyecto, puedes usar la API de **Voz a texto** para reconocer voz y transcribirla a texto.

En este procedimiento, la entrada de voz se captura desde un archivo de audio, que puedes reproducir aquí:

<video controls src="https://github.com/MicrosoftLearning/mslearn-ai-language/raw/refs/heads/main/Instructions/media/Time.mp4" title="What time is it?" width="150"></video>

1. En el archivo de código, nota que el código usa la función **TranscribeCommand** para aceptar entrada hablada. Luego en la función **TranscribeCommand**, encuentra el comentario **Configure speech recognition** y agrega el código apropiado debajo para crear un cliente **SpeechRecognizer** que pueda usarse para reconocer y transcribir voz desde un archivo de audio:

    ```python
   # Configure speech recognition
   current_dir = os.getcwd()
   audioFile = current_dir + '/time.wav'
   audio_config = speech_sdk.AudioConfig(filename=audioFile)
   speech_recognizer = speech_sdk.SpeechRecognizer(speech_config, audio_config)
    ```

1. En la función **TranscribeCommand**, bajo el comentario **Process speech input**, agrega el siguiente código para escuchar entrada hablada, teniendo cuidado de no reemplazar el código al final de la función que devuelve el comando:

    ```python
   # Process speech input
   print("Escuchando...")
   speech = speech_recognizer.recognize_once_async().get()
   if speech.reason == speech_sdk.ResultReason.RecognizedSpeech:
        command = speech.text
        print(command)
   else:
        print(speech.reason)
        if speech.reason == speech_sdk.ResultReason.Canceled:
            cancellation = speech.cancellation_details
            print(cancellation.reason)
            print(cancellation.error_details)
    ```

1. Guarda tus cambios (*CTRL+S*), y luego en la línea de comandos debajo del editor de código, re-ejecuta el programa:
1. Revisa la salida, que debería "escuchar" exitosamente el habla en el archivo de audio y devolver una respuesta apropiada (¡nota que tu Azure cloud shell puede estar ejecutándose en un servidor que está en una zona horaria diferente a la tuya!)

    > **Tip**: Si el SpeechRecognizer encuentra un error, produce un resultado de "Cancelled". El código en la aplicación luego mostrará el mensaje de error. La causa más probable es un valor de región incorrecto en el archivo de configuración.

## Sintetizar voz

¡Tu aplicación de reloj parlante acepta entrada hablada, pero en realidad no habla! Arreglemos eso agregando código para sintetizar voz.

Una vez más, debido a las limitaciones de hardware del cloud shell dirigiremos la salida de voz sintetizada a un archivo.

1. En el archivo de código, nota que el código usa la función **TellTime** para decirle al usuario la hora actual.
1. En la función **TellTime**, bajo el comentario **Configure speech synthesis**, agrega el siguiente código para crear un cliente **SpeechSynthesizer** que pueda usarse para generar salida hablada:

    ```python
   # Configure speech synthesis
   output_file = "output.wav"
   speech_config.speech_synthesis_voice_name = "en-GB-RyanNeural"
   audio_config = speech_sdk.audio.AudioConfig(filename=output_file)
   speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config, audio_config,)
    ```

1. En la función **TellTime**, bajo el comentario **Synthesize spoken output**, agrega el siguiente código para generar salida hablada, teniendo cuidado de no reemplazar el código al final de la función que imprime la respuesta:

    ```python
   # Synthesize spoken output
   speak = speech_synthesizer.speak_text_async(response_text).get()
   if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)
   else:
        print("Salida hablada guardada en " + output_file)
    ```

1. Guarda tus cambios (*CTRL+S*) y re-ejecuta el programa, que debería indicar que la salida hablada fue guardada en un archivo.

1. Si tienes un reproductor de medios capaz de reproducir archivos de audio .wav, descarga el archivo que fue generado ingresando el siguiente comando:

    ```bash
    download ./output.wav
    ```

    El comando download crea un enlace emergente en la parte inferior derecha de tu navegador, que puedes seleccionar para descargar y abrir el archivo.

    El archivo debería sonar similar a esto:

    <video controls src="https://github.com/MicrosoftLearning/mslearn-ai-language/raw/refs/heads/main/Instructions/media/Output.mp4" title="The time is 2:15" width="150"></video>

## Usar Speech Synthesis Markup Language

Speech Synthesis Markup Language (SSML) te permite personalizar la forma en que se sintetiza tu voz usando un formato basado en XML.

1. En la función **TellTime**, reemplaza todo el código actual bajo el comentario **Synthesize spoken output** con el siguiente código (deja el código bajo el comentario **Print the response**):

    ```python
   # Synthesize spoken output
   responseSsml = " \
       <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'> \
           <voice name='en-GB-LibbyNeural'> \
               {} \
               <break strength='weak'/> \
               Time to end this lab! \
           </voice> \
       </speak>".format(response_text)
   speak = speech_synthesizer.speak_ssml_async(responseSsml).get()
   if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
       print(speak.reason)
   else:
       print("Salida hablada guardada en " + output_file)
    ```

1. Guarda tus cambios y re-ejecuta el programa, que debería una vez más indicar que la salida hablada fue guardada en un archivo.
1. Descarga y reproduce el archivo generado, que debería sonar similar a esto:

    <video controls src="https://github.com/MicrosoftLearning/mslearn-ai-language/raw/refs/heads/main/Instructions/media/Output2.mp4" title="The time is 5:30. Time to end this lab." width="150"></video>

## (OPCIONAL) ¿Qué pasa si tienes un micrófono y altavoz?

En este ejercicio, usaste archivos de audio para la entrada y salida de voz. Veamos cómo se puede modificar el código para usar hardware de audio.

### Usar reconocimiento de voz con un micrófono

Si tienes un micrófono, puedes usar el siguiente código para capturar entrada hablada para reconocimiento de voz:

```python
# Configure speech recognition
audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
speech_recognizer = speech_sdk.SpeechRecognizer(speech_config, audio_config)
print('Habla ahora...')

# Process speech input
speech = speech_recognizer.recognize_once_async().get()
if speech.reason == speech_sdk.ResultReason.RecognizedSpeech:
    command = speech.text
    print(command)
else:
    print(speech.reason)
    if speech.reason == speech_sdk.ResultReason.Canceled:
        cancellation = speech.cancellation_details
        print(cancellation.reason)
        print(cancellation.error_details)

```

> **Nota**: ¡El micrófono predeterminado del sistema es la entrada de audio predeterminada, por lo que también podrías omitir el AudioConfig por completo!

### Usar síntesis de voz con un altavoz

Si tienes un altavoz, puedes usar el siguiente código para sintetizar voz.

```python
response_text = 'The time is {}:{:02d}'.format(now.hour,now.minute)

# Configure speech synthesis
speech_config.speech_synthesis_voice_name = "en-GB-RyanNeural"
audio_config = speech_sdk.audio.AudioOutputConfig(use_default_speaker=True)
speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config, audio_config)

# Synthesize spoken output
speak = speech_synthesizer.speak_text_async(response_text).get()
if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
    print(speak.reason)
```

> **Nota**: ¡El altavoz predeterminado del sistema es la salida de audio predeterminada, por lo que también podrías omitir el AudioConfig por completo!

## Limpiar

Si has terminado de explorar Azure AI Speech, deberías eliminar los recursos que has creado en este ejercicio para evitar incurrir en costos de Azure innecesarios.

1. Cierra el panel de Azure cloud shell
1. En Azure Portal, navega al recurso de Azure AI Speech que creaste en este laboratorio.
1. En la página del recurso, selecciona **Delete** y sigue las instrucciones para eliminar el recurso.

## Más información

Para más información sobre el uso de las APIs de **Voz a texto** y **Texto a voz**, consulta la [documentación de Voz a texto](https://learn.microsoft.com/azure/ai-services/speech-service/index-speech-to-text) y [documentación de Texto a voz](https://learn.microsoft.com/azure/ai-services/speech-service/index-text-to-speech).
