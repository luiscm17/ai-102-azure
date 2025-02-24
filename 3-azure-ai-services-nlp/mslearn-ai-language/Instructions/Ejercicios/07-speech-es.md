---
lab:
    title: 'Recognize and Synthesize Speech'
    module: 'Module 4 - Create speech-enabled apps with Azure AI services'
---

# Reconocer y sintetizar el habla

**Azure AI Speech** es un servicio que proporciona funcionalidad relacionada con la voz, entre las que se incluyen:

- Una  API de *voz a texto* que le permite implementar el reconocimiento de voz (convertir palabras habladas audibles en texto).
- Una  API de *texto a voz* que le permite implementar la síntesis de voz (convertir texto en voz audible).

En este ejercicio, usará estas dos API para implementar una aplicación de reloj hablante.

> **NOTA**
> Este ejercicio requiere que esté utilizando una computadora con parlantes/auriculares. Para obtener la mejor experiencia, también se requiere un micrófono. Es posible que algunos entornos virtuales alojados puedan capturar audio desde el micrófono local, pero si esto no funciona (o si no tiene un micrófono en absoluto), puede usar un archivo de audio proporcionado para la entrada de voz. Siga las instrucciones cuidadosamente, ya que deberá elegir diferentes opciones dependiendo de si está utilizando un micrófono o el archivo de audio.

## Aprovisionamiento de un  recurso *Azure AI Speech*

Si aún no tiene uno en su suscripción, deberá aprovisionar un  recurso **Azure AI Speech**.

1. Abra Azure Portal en "https://portal.azure.com" e inicie sesión con la cuenta de Microsoft asociada a su suscripción de Azure.
1. En el campo de búsqueda de la parte superior, busque **Azure AI services** y pulse **Intro** y, a continuación, seleccione **Crear** en **Servicio de voz** en los resultados.
1. Cree un recurso con la siguiente configuración:
   - **Suscripción**: *Su suscripción de Azure*
   - **Grupo de recursos**: *Elija o cree un grupo de recursos*
   - **Región**: *Elige cualquier región disponible*
   - **Nombre**: *Introduzca un nombre único*
   - **Plan de tarifa**: seleccione **F0** (*gratis*) o **S** (*estándar*) si F no está disponible.
   - **Aviso de IA responsable**: De acuerdo.
2. Seleccione **Revisar + crear** y, a continuación, seleccione **Crear** para aprovisionar el recurso.
3. Espere a que se complete la implementación y, a continuación, vaya al recurso implementado.
4. Vea la  página **Claves y punto de conexión**. Necesitará la información de esta página más adelante en el ejercicio.

## Preparación para desarrollar una aplicación en Visual Studio Code

Desarrollará la aplicación de voz con Visual Studio Code. Los archivos de código de la aplicación se han proporcionado en un repositorio de GitHub.

> **Sugerencia**: Si ya ha clonado el  repositorio **mslearn-ai-language**, ábralo en el código de Visual Studio. De lo contrario, siga estos pasos para clonarlo en su entorno de desarrollo.

1. Inicie Visual Studio Code.
1. Abra la paleta (SHIFT+CTRL+P) y ejecute un  comando **Git: Clone** para clonar el  repositorio 'https://github.com/MicrosoftLearning/mslearn-ai-language' en una carpeta local (no importa qué carpeta).
1. Cuando se haya clonado el repositorio, abra la carpeta en Visual Studio Code.

    > **Nota**: Si Visual Studio Code le muestra un mensaje emergente para pedirle que confíe en el código que está abriendo, haga clic en la opción **Sí, confío en los autores** en la ventana emergente.

1. Espere mientras se instalan archivos adicionales para admitir los proyectos de código de C# en el repositorio.

    > **Nota**: Si se le solicita que agregue los activos necesarios para compilar y depurar, seleccione **Ahora no**.

## Configura tu aplicación

Se han proporcionado aplicaciones para C# y Python. Ambas aplicaciones cuentan con la misma funcionalidad. En primer lugar, completará algunas partes clave de la aplicación para permitirle usar el recurso de Azure AI Speech.

1. En Visual Studio Code, en el  panel **Explorer**, vaya a la  carpeta **Labfiles/07-speech** y expanda la  carpeta **CSharp** o **Python** en función de su preferencia de idioma y de la  carpeta **speaking-clock** que contenga. Cada carpeta contiene los archivos de código específicos del idioma de una aplicación en la que va a integrar la funcionalidad de Azure AI Speech.
1. Haga clic con el botón derecho en la  carpeta **talk-clock** que contiene sus archivos de código y abra un terminal integrado. A continuación, instale el paquete del SDK de Azure AI Speech ejecutando el comando adecuado para su preferencia de idioma:

    **C#**

    ```
    dotnet add package Microsoft.CognitiveServices.Speech --version 1.30.0
    ```

    **Pitón**

    ```
    pip install azure-cognitiveservices-speech==1.30.0
    ```

1. En el  panel **Explorer**, en la  carpeta **speaking-clock**, abra el archivo de configuración de su idioma preferido

   - **C#**: appsettings.json
   - **Pitón**: .env

2. Actualice los valores de configuración para incluir la **región** y una **clave** del recurso de Azure AI Speech que creó (disponible en la  página **Claves y punto de conexión** del recurso de Azure AI Speech en Azure Portal).

    > **NOTA**: Asegúrese de agregar la *región* para su recurso, <u>not</u> el punto de conexión!

1. Guarde el archivo de configuración.

## Agregar código para usar el SDK de voz de Azure AI

1. Tenga en cuenta que la  carpeta **speaking-clock** contiene un archivo de código para la aplicación cliente:

   - **C#**: Program.cs
   - **Pitón**: speaking-clock.py

    Abra el archivo de código y en la parte superior, debajo de las referencias de espacio de nombres existentes, busque el comentario **Importar espacios de nombres**. A continuación, en este comentario, agregue el siguiente código específico del lenguaje para importar los espacios de nombres que necesitará para usar el SDK de Voz de Azure AI:

    **C#**: Program.cs

    ```csharp
    Importar espacios de nombres
    usando Microsoft.Servicios cognitivos.Habla;
    usando Microsoft.Servicios cognitivos.Discurso.Audio;
    ```
    **Python**: speaking-clock.py

    ```python
    # Importar espacios de nombres
    Importar azure.cognitiveServices.speech como speech_sdk
    ```

2. En la  función **Main**, tenga en cuenta que ya se ha proporcionado el código para cargar la clave de servicio y la región desde el archivo de configuración. Debe usar estas variables para crear un **SpeechConfig** para el recurso de Azure AI Speech. Agregue el siguiente código bajo el comentario **Configurar servicio de voz**:

    **C#**: Program.cs

    ```csharp
    Configurar el servicio de voz
    speechConfig = SpeechConfig.FromSubscription(aiSvcKey, aiSvcRegion);
    Consola.WriteLine("Servicio de voz listo para usar en " + speechConfig.Región);
    Configurar la voz
    speechConfig.SpeechSynthesisVoiceName = "en-US-AriaNeural";
    ```

    **Python**: speaking-clock.py

    ```python
    # Configurar el servicio de voz
    speech_config = speech_sdk. SpeechConfig (ai_key, ai_region)
    print('Servicio de voz listo para usar en:', speech_config.region)
    ```

1. Guarde los cambios y regrese al terminal integrado para la  carpeta **talk-clock**,  e ingrese el siguiente comando para ejecutar el programa:

    **C#**

    ```
    Ejecución de dotnet
    ```

    **Python**

    ```
    speaking-clock.py Python
    ```

1. Si está usando C#, puede ignorar cualquier advertencia sobre el uso del  operador **await** en métodos asincrónicos: lo solucionaremos más adelante. El código debe mostrar la región del recurso del servicio de voz que usará la aplicación.

## Agregar código para reconocer el habla

Ahora que tiene un **SpeechConfig** para el servicio de voz en el recurso de voz de Azure AI, puede usar la  API **Speech-to-text** para reconocer la voz y transcribirla a texto.

> **IMPORTANTE**: Esta sección incluye instrucciones para dos procedimientos alternativos. Siga el primer procedimiento si tiene un micrófono que funcione. Siga el segundo procedimiento si desea simular la entrada hablada mediante un archivo de audio.

### Si tienes un micrófono que funcione

1. En la  función **Main** de su programa, observe que el código utiliza la  función **TranscribeCommand** para aceptar entradas habladas.
1. En la  función **TranscribeCommand**, bajo el comentario **Configurar reconocimiento de voz**, agregue el código apropiado a continuación para crear un  cliente **SpeechRecognizer** que se puede usar para reconocer y transcribir voz usando el micrófono del sistema predeterminado:

    **C#**

    ```csharp
    Configurar el reconocimiento de voz
    usando AudioConfig audioConfig = AudioConfig.FromDefaultMicrophoneInput();
    usando SpeechRecognizer speechRecognizer = new SpeechRecognizer(speechConfig, audioConfig);
    Consola.WriteLine("Habla ahora...");
    ```

    **Python**

    ```python
    # Configurar el reconocimiento de voz
    audio_config = speech_sdk. AudioConfig(use_default_microphone=Verdadero)
    speech_recognizer = speech_sdk. SpeechRecognizer(speech_config, audio_config)
    print('Habla ahora...')
    ```

1. Ahora vaya a la  sección **Agregar código para procesar el comando transcrito** a continuación.

---

### Alternativamente, use la entrada de audio de un archivo

1. En la ventana del terminal, ingrese el siguiente comando para instalar una biblioteca que puede usar para reproducir el archivo de audio:

    **C#**

    ```csharp
    dotnet add package System.Windows.Extensions --version 4.6.0 
    ```

    **Python**

    ```python
    pip install playsound==1.2.2
    ```

1. En el archivo de código de su programa, en las importaciones de espacio de nombres existentes, agregue el siguiente código para importar la biblioteca que acaba de instalar:

    **C#**: Program.cs

    ```csharp
    usando el sistema.Medios de comunicación;
    ```

    **Python**: speaking-clock.py

    ```python
    Desde playsound importar playsound
    ```

1. En la  función **Main**, tenga en cuenta que el código utiliza la  función **TranscribeCommand** para aceptar entradas habladas. A continuación, en la  función **TranscribeCommand**, bajo el comentario **Configurar reconocimiento de voz**, agregue el código adecuado a continuación para crear un  cliente **SpeechRecognizer** que se puede usar para reconocer y transcribir voz de un archivo de audio:

    **C#**: Program.cs

    ```csharp
    Configurar el reconocimiento de voz
    string audioFile = "time.wav";
    SoundPlayer wavPlayer = nuevo SoundPlayer(audioFile);
    wavPlayer.Jugar();
    usando AudioConfig audioConfig = AudioConfig.FromWavFileInput(audioFile);
    usando SpeechRecognizer speechRecognizer = new SpeechRecognizer(speechConfig, audioConfig);
    ```

    **Python**: speaking-clock.py

    ```python
    # Configurar el reconocimiento de voz
    current_dir = os.getcwd()
    Archivode audio = current_dir + '\\time.wav'
    playsound(archivo de audio)
    audio_config = speech_sdk.AudioConfig(nombre de archivo=archivoArchivo)
    speech_recognizer = speech_sdk. SpeechRecognizer(speech_config, audio_config)
    ```

---

### Agregar código para procesar el comando transcrito

1. En la  función **TranscribeCommand**, bajo el comentario **Procesar entrada de voz**, agregue el siguiente código para escuchar la entrada hablada, teniendo cuidado de no reemplazar el código al final de la función que devuelve el comando:

    **C#**: Program.cs

    ```csharp
    Procesar la entrada de voz
    SpeechRecognitionResult speech = await speechRecognizer.RecognizeOnceAsync();
    Si (Discurso.Razón == ResultadoRazón.RecognizedSpeech)
    {
    comando = habla.Texto;
    Consola.WriteLine(comando);
    }
    más
    {
    Consola.WriteLine(speech.Razón);
    Si (Discurso.Razón == ResultadoRazón.Cancelado)
    {
    var cancellation = Detalles de cancelación.FromResult(voz);
    Consola.WriteLine(cancelación.Razón);
    Consola.WriteLine(cancelación.ErrorDetails);
    }
    }
    ```

    **Python**: speaking-clock.py

    ```Python
    # Procesar la entrada de voz
    voz = speech_recognizer.reconocer_una_vez_asíncrono().get()
    if speech.reason == speech_sdk. ResultReason.RecognizedSpeech:
    comando = voz.texto
    imprimir(comando)
    De lo contrario:
    print(discurso.razón)
    if speech.reason == speech_sdk. ResultReason.Cancelado:
    cancelación = speech.cancellation_details
    print(cancelación.motivo)
    imprimir(cancellation.error_details)
    ```

1. Guarde los cambios y regrese al terminal integrado para la  carpeta **talk-clock**,  e ingrese el siguiente comando para ejecutar el programa:

    **C#**

    ```
    Ejecución de dotnet
    ```

    **Python**

    ```
    speaking-clock.py Python
    ```

1. Si usa un micrófono, hable claramente y diga "¿qué hora es?". El programa debe transcribir su entrada hablada y mostrar la hora (según la hora local de la computadora donde se está ejecutando el código, que puede no ser la hora correcta donde se encuentra).

SpeechRecognizer le da alrededor de 5 segundos para hablar. Si no detecta ninguna entrada hablada, produce un resultado "No coincide".

Si SpeechRecognizer encuentra un error, genera un resultado de "Cancelado". A continuación, el código de la aplicación mostrará el mensaje de error. La causa más probable es una clave o región incorrecta en el archivo de configuración.

## Sintetizar el habla

La aplicación de reloj de habla acepta entradas de voz, ¡pero en realidad no habla! Vamos a arreglar eso agregando código para sintetizar el habla.

1. En la  función **Main** de su programa, tenga en cuenta que el código utiliza la  función **TellTime** para indicar al usuario la hora actual.
1. En la  función **TellTime**, bajo el comentario **Configurar síntesis de voz**, agregue el siguiente código para crear un  cliente **SpeechSynthesizer** que se pueda usar para generar salida hablada:

    **C#**: Program.cs

    ```csharp
    Configurar la síntesis de voz
    speechConfig.SpeechSynthesisVoiceName = "es-GB-RyanNeural";
    Uso del sintetizador de voz Speech Synthesizer = Nuevo sintetizador de voz (speechconfig);
    ```

    **Pitón**: speaking-clock.py

    ```python
    # Configurar la síntesis de voz
    speech_config.speech_synthesis_voice_name = "es-ES-RyanNeural"
    speech_synthesizer = speech_sdk. SpeechSynthesizer(speech_config)
    ```

    > **NOTA** La configuración de audio predeterminada utiliza el dispositivo de audio del sistema predeterminado para la salida, por lo que no es necesario proporcionar explícitamente un **AudioConfig**. Si necesita redirigir la salida de audio a un archivo, puede usar un **AudioConfig** con una ruta de archivo para hacerlo.

1. En la  función **TellTime**, bajo el comentario **Sintetizar salida hablada**, agregue el siguiente código para generar salida hablada, teniendo cuidado de no reemplazar el código al final de la función que imprime la respuesta:

    **C#**: Program.cs

    ```csharp
    Sintetizar la salida hablada
    SpeechSynthesisResult speak = await speechSynthesizer.SpeakTextAsync(responseText);
    Si (Habla.Razón != ResultadoRazón.SynthesizingAudioCompleted)
    {
    Consola.WriteLine(hablar.Razón);
    }
    ```

    **Python**: speaking-clock.py

    ```python
    # Sintetizar la salida hablada
    hablar = speech_synthesizer.hablar_texto_asíncrono(response_text).get()
    if speak.reason != speech_sdk. ResultReason.SynthesizingAudioCompleted:
    print(hablar.razón)
    ```

1. Guarde los cambios y regrese al terminal integrado para la  carpeta **talk-clock**,  e ingrese el siguiente comando para ejecutar el programa:

    **C#**

    ```csharp
    Ejecución de dotnet
    ```

    **Python**

    ```python
    speaking-clock.py Python
    ```

1. Cuando se le indique, hable claramente por el micrófono y diga "¿qué hora es?". El programa debe hablar, diciéndote la hora.

## Usa una voz diferente

La aplicación de reloj de habla utiliza una voz predeterminada, que puede cambiar. El servicio de voz admite una variedad de  voces *estándar*, así como voces *neuronales* más parecidas a las humanas  . También puedes crear  voces *personalizadas*.

> **Nota**: Para obtener una lista de voces neuronales y estándar, consulte [Galería de voz](https://speech.microsoft.com/portal/voicegallery) en Speech Studio.

1. En la  función **TellTime**, bajo el comentario **Configurar síntesis de voz**, modifique el código de la siguiente manera para especificar una voz alternativa antes de crear el  cliente **SpeechSynthesizer**:

    **C#**: Program.cs

    ```csharp
    Configurar la síntesis de voz
    speechConfig.SpeechSynthesisVoiceName = "es-GB-LibbyNeural";  Cambia esto
    Uso del sintetizador de voz Speech Synthesizer = Nuevo sintetizador de voz (speechconfig);
    ```

    **Python**: speaking-clock.py

    ```python
    # Configurar la síntesis de voz
    speech_config.speech_synthesis_voice_name = 'en-GB-LibbyNeural' # cambia esto
    speech_synthesizer = speech_sdk. SpeechSynthesizer(speech_config)
    ```

1. Guarde los cambios y regrese al terminal integrado para la  carpeta **talk-clock**,  e ingrese el siguiente comando para ejecutar el programa:

    **C#**

    ```
    Ejecución de dotnet
    ```

    **Python**

    ```
    speaking-clock.py Python
    ```

1. Cuando se le indique, hable claramente por el micrófono y diga "¿qué hora es?". El programa debe hablar con la voz especificada, diciéndole la hora.

## Usar el lenguaje de marcado de síntesis de voz

El lenguaje de marcado de síntesis de voz (SSML) permite personalizar la forma en que se sintetiza la voz mediante un formato basado en XML.

1. En la  función **TellTime**,  reemplace todo el código actual bajo el comentario **Sintetizar la salida hablada** por el siguiente código (deje el código debajo del comentario **Imprimir la respuesta**):

    **C#**: Program.cs

    ```csharp
    Sintetizar la salida hablada
    string responseSsml = $@"
    <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>
    <voice name='es-ES-LibbyNeural'>
    {responseText}
    <fuerza de rotura='débil'/>
    ¡Es hora de terminar este laboratorio!
    </voz>
    </habla>";
    SpeechSynthesisResult speak = await speechSynthesizer.SpeakSsmlAsync(responseSsml);
    Si (Habla.Razón != ResultadoRazón.SynthesizingAudioCompleted)
    {
    Consola.WriteLine(hablar.Razón);
    }
    ```

    **Python**: speaking-clock.py

    ```python
    # Sintetizar la salida hablada
    responseSsml = " \
    <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'> \
    <voice name='es-ES-LibbyNeural'> \
    {} \
    <fuerza de rotura='débil'/> \
    ¡Es hora de terminar este laboratorio! \
    </voz> \
    </hablar>".format(response_text)
    hablar = speech_synthesizer.speak_ssml_async(responseSsml).get()
    if speak.reason != speech_sdk. ResultReason.SynthesizingAudioCompleted:
    print(hablar.razón)
    ```

1. Guarde los cambios y regrese al terminal integrado para la  carpeta **talk-clock**,  e ingrese el siguiente comando para ejecutar el programa:

    **C#**

    ```
    Ejecución de dotnet
    ```

    **Python**

    ```
    speaking-clock.py Python
    ```

1. Cuando se le indique, hable claramente por el micrófono y diga "¿qué hora es?". El programa debe hablar en la voz especificada en el SSML (anulando la voz especificada en SpeechConfig), diciéndole la hora y, después de una pausa, diciéndole que es hora de finalizar este laboratorio, ¡y así es!

## Más información

Para obtener más información sobre el uso de las  API **Speech-to-text** y **Text-to-speech**, consulte [Documentación de conversión de voz a texto](https://learn.microsoft.com/azure/ai-services/speech-service/index-speech-to-text) y [Documentación de conversión de texto a voz](https://learn.microsoft.com/azure/ai-services/speech-service/index-text-to-speech).
