---
Laboratorio:
título: 'Traducir el discurso'
módulo: 'Módulo 8 - Traducción de voz con Azure AI Speech'
---

# Traducir voz

Azure AI Speech incluye una API de traducción de voz que puede usar para traducir el lenguaje hablado. Por ejemplo, supongamos que desea desarrollar una aplicación de traducción que las personas puedan usar cuando viajen a lugares donde no hablan el idioma local. Podrían decir frases como "¿Dónde está la estación?" o "Necesito encontrar una farmacia" en su propio idioma, y hacer que las traduzca al idioma local.

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
1. Seleccione **Revisar + crear**, luego seleccione **Crear** para aprovisionar el recurso.
1. Espere a que se complete la implementación y, a continuación, vaya al recurso implementado.
1. Vea la  página **Claves y punto de conexión**. Necesitará la información de esta página más adelante en el ejercicio.

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

1. En Visual Studio Code, en el  panel **Explorer**, vaya a la  carpeta **Labfiles/08-speech-translation** y expanda la  carpeta **CSharp** o **Python** en función de su preferencia de idioma y de la  carpeta **translator** que contenga. Cada carpeta contiene los archivos de código específicos del idioma de una aplicación en la que va a integrar la funcionalidad de Azure AI Speech.
1. Haga clic con el botón derecho en la  carpeta **translator** que contiene sus archivos de código y abra un terminal integrado. A continuación, instale el paquete del SDK de Azure AI Speech ejecutando el comando adecuado para su preferencia de idioma:

**C#**

```
dotnet add package Microsoft.CognitiveServices.Speech --version 1.30.0
```

**Pitón**

```
pip install azure-cognitiveservices-speech==1.30.0
```

1. En el  panel **Explorer**, en la  carpeta **translator**, abra el archivo de configuración de su idioma preferido

- **C#**: appsettings.json
- **Pitón**: .env

1. Actualice los valores de configuración para incluir la **región** y una **clave** del recurso de Azure AI Speech que creó (disponible en la  página **Claves y punto de conexión** del recurso de Azure AI Speech en Azure Portal).

> **NOTA**: Asegúrese de agregar la *región* para su recurso, <u>not</u> el punto de conexión!

1. Guarde el archivo de configuración.

## Agregar código para usar el SDK de Voz

1. Tenga en cuenta que la  carpeta **translator** contiene un archivo de código para la aplicación cliente:

- **C#**: Program.cs
- **Pitón**: translator.py

Abra el archivo de código y en la parte superior, debajo de las referencias de espacio de nombres existentes, busque el comentario **Importar espacios de nombres**. A continuación, en este comentario, agregue el siguiente código específico del lenguaje para importar los espacios de nombres que necesitará para usar el SDK de Voz de Azure AI:

**C#**: Program.cs

'''csharp
Importar espacios de nombres
usando Microsoft.Servicios cognitivos.Habla;
usando Microsoft.Servicios cognitivos.Discurso.Audio;
usando Microsoft.Servicios cognitivos.Discurso.Traducción;
```

**Pitón**: translator.py

'''pitón
# Importar espacios de nombres
Importar azure.cognitiveServices.speech como speech_sdk
```

1. En la  función **Main**, tenga en cuenta que ya se ha proporcionado el código para cargar la clave y la región del servicio Azure AI Speech desde el archivo de configuración. Debe usar estas variables para crear un **SpeechTranslationConfig** para el recurso de voz de Azure AI, que usará para traducir la entrada hablada. Agregue el siguiente código debajo del comentario **Configurar traducción**:

**C#**: Program.cs

'''csharp
Configurar la traducción
translationConfig = SpeechTranslationConfig.FromSubscription(aiSvcKey, aiSvcRegion);
traducciónConfig.SpeechRecognitionLanguage = "en-US";
traducciónConfig.AddTargetLanguage("fr");
traducciónConfig.AddTargetLanguage("es");
traducciónConfig.AddTargetLanguage("hola");
Consola.WriteLine("Listo para traducir desde " + translationConfig.SpeechRecognitionLanguage);
```

**Pitón**: translator.py

'''pitón
# Configurar la traducción
translation_config = speech_sdk.translation.SpeechTranslationConfig(ai_key, ai_region)
translation_config.idioma_de_reconocimiento_de_voz = 'en-US'
translation_config.add_target_language('fr')
translation_config.add_target_language('es')
translation_config.add_target_language('hola')
print('Listo para traducir desde',translation_config.speech_recognition_language)
```

1. Utilizará la **SpeechTranslationConfig** para traducir la voz en texto, pero también utilizará una **SpeechConfig** para sintetizar las traducciones en voz. Agregue el siguiente código debajo del comentario **Configurar voz**:

**C#**: Program.cs

'''csharp
Configurar voz
speechConfig = SpeechConfig.FromSubscription(aiSvcKey, aiSvcRegion);
```

**Pitón**: translator.py

'''pitón
# Configurar voz
speech_config = speech_sdk. SpeechConfig (ai_key, ai_region)
```

1. Guarde sus cambios y regrese al terminal integrado para la  carpeta **translator**, e ingrese el siguiente comando para ejecutar el programa:

**C#**

```
Ejecución de dotnet
```

**Pitón**

```
Python translator.py
```

1. Si está usando C#, puede ignorar cualquier advertencia sobre el uso del  operador **await** en métodos asincrónicos: lo solucionaremos más adelante. El código debe mostrar un mensaje que indica que está listo para traducir desde en-US y solicitarle un idioma de destino. Pulse ENTER para finalizar el programa.

## Implementar la traducción de voz

Ahora que tiene un **SpeechTranslationConfig** para el servicio Azure AI Speech, puede usar la API de traducción de Azure AI Speech para reconocer y traducir la voz.

> **IMPORTANTE**: Esta sección incluye instrucciones para dos procedimientos alternativos. Siga el primer procedimiento si tiene un micrófono que funcione. Siga el segundo procedimiento si desea simular la entrada hablada mediante un archivo de audio.

### Si tienes un micrófono que funcione

1. En la  función **Main** de su programa, tenga en cuenta que el código utiliza la  función **Translate** para traducir la entrada hablada.
1. En la  función **Translate**, bajo el comentario **Translate speech**, agregue el siguiente código para crear un  cliente **TranslationRecognizer** que se puede usar para reconocer y traducir voz utilizando el micrófono del sistema predeterminado para la entrada.

**C#**: Program.cs

'''csharp
Traducir voz
usando AudioConfig audioConfig = AudioConfig.FromDefaultMicrophoneInput();
usando el traductor TranslationRecognizer = new TranslationRecognizer(translationConfig, audioConfig);
Consola.WriteLine("Habla ahora...");
TranslationRecognitionResult resultado = esperar traductor.RecognizeOnceAsync();
Consola.WriteLine($"Traduciendo '{resultado.Texto}'");
traducción = resultado.Traducciones[targetLanguage];
Consola.OutputEncoding = Codificación.UTF8;
Consola.WriteLine(traducción);
```

**Pitón**: translator.py

'''pitón
# Traducir voz
audio_config = speech_sdk. AudioConfig(use_default_microphone=Verdadero)
traductor = speech_sdk.translation.TranslationRecognizer(translation_config, audio_config = audio_config)
print("Habla ahora...")
resultado = translator.recognize_once_async().get()
print('Traduciendo "{}"'.format(resultado.texto))
translation = result.translations[targetLanguage]
imprimir(traducción)
```

> **NOTA**
> El código de la aplicación traduce la entrada a los tres idiomas en una sola llamada. Solo se muestra la traducción para el idioma específico, pero puede recuperar cualquiera de las traducciones especificando el código del idioma de destino en la  colección **translations** del resultado.

1. Ahora salte a la  sección **Ejecutar el programa** a continuación.

---

### Alternativamente, use la entrada de audio de un archivo

1. En la ventana del terminal, ingrese el siguiente comando para instalar una biblioteca que puede usar para reproducir el archivo de audio:

**C#**: Program.cs

'''csharp
dotnet add package System.Ventanas.Extensiones --version 4.6.0 
```

**Pitón**: translator.py

'''pitón
pip install playsound==1.3.0
```

1. En el archivo de código de su programa, en las importaciones de espacio de nombres existentes, agregue el siguiente código para importar la biblioteca que acaba de instalar:

**C#**: Program.cs

'''csharp
usando el sistema.Medios de comunicación;
```

**Pitón**: translator.py

'''pitón
Desde playsound importar playsound
```

1. En la  función **Main** de su programa, tenga en cuenta que el código utiliza la  función **Translate** para traducir la entrada hablada. A continuación, en la  función **Translate**, bajo el comentario **Translate speech**, agregue el siguiente código para crear un  cliente **TranslationRecognizer** que se puede usar para reconocer y traducir la voz de un archivo.

**C#**: Program.cs

'''csharp
Traducir voz
string audioFile = "station.wav";
SoundPlayer wavPlayer = nuevo SoundPlayer(audioFile);
wavPlayer.Jugar();
usando AudioConfig audioConfig = AudioConfig.FromWavFileInput(audioFile);
usando el traductor TranslationRecognizer = new TranslationRecognizer(translationConfig, audioConfig);
Consola.WriteLine("Obtener voz del archivo...");
TranslationRecognitionResult resultado = esperar traductor.RecognizeOnceAsync();
Consola.WriteLine($"Traduciendo '{resultado.Texto}'");
traducción = resultado.Traducciones[targetLanguage];
Consola.OutputEncoding = Codificación.UTF8;
Consola.WriteLine(traducción);
```

**Pitón**: translator.py

'''pitón
# Traducir voz
Archivo de audio = 'station.wav'
playsound(archivo de audio)
audio_config = speech_sdk. AudioConfig(nombre de archivo=archivoArchivo)
traductor = speech_sdk.translation.TranslationRecognizer(translation_config, audio_config = audio_config)
print("Obtener voz del archivo...")
resultado = translator.recognize_once_async().get()
print('Traduciendo "{}"'.format(resultado.texto))
translation = result.translations[targetLanguage]
imprimir(traducción)
```

---

### Ejecutar el programa

1. Guarde sus cambios y regrese al terminal integrado para la  carpeta **translator**, e ingrese el siguiente comando para ejecutar el programa:

**C#**

```
Ejecución de dotnet
```

**Pitón**

```
Python translator.py
```

1. Cuando se le solicite, ingrese un código de idioma válido (*fr*, *es* o *hi*), y luego, si usa un micrófono, hable claramente y diga "¿dónde está la estación?" o alguna otra frase que pueda usar cuando viaje al extranjero. El programa debe transcribir su entrada hablada y traducirla al idioma que especificó (francés, español o hindi). Repita este proceso, probando cada idioma compatible con la aplicación. Cuando haya terminado, presione ENTER para finalizar el programa.

TranslationRecognizer le da alrededor de 5 segundos para hablar. Si no detecta ninguna entrada hablada, produce un resultado "No coincide". Es posible que la traducción al hindi no siempre se muestre correctamente en la ventana de la consola debido a problemas de codificación de caracteres.

> **NOTA**: El código de la aplicación traduce la entrada a los tres idiomas en una sola llamada. Solo se muestra la traducción para el idioma específico, pero puede recuperar cualquiera de las traducciones especificando el código del idioma de destino en la  colección **translations** del resultado.

## Sintetizar la traducción a voz

Hasta ahora, la aplicación traduce la entrada hablada a texto; lo que podría ser suficiente si necesita pedir ayuda a alguien mientras viaja. Sin embargo, sería mejor que la traducción se hablara en voz alta con una voz adecuada.

1. En la  función **Translate**, bajo el comentario **Sintetizar traducción**, agregue el siguiente código para usar un  cliente **SpeechSynthesizer** para sintetizar la traducción como voz a través del altavoz predeterminado:

**C#**: Program.cs

'''csharp
Sintetizar la traducción
var voices = new Dictionary<string, string>
{
["fr"] = "fr-FR-HenriNeural",
["es"] = "es-ES-ElviraNeural",
["hola"] = "hi-IN-MadhurNeural"
};
speechConfig.SpeechSynthesisVoiceName = voices[targetLanguage];
Uso del sintetizador de voz Speech Synthesizer = Nuevo sintetizador de voz (speechconfig);
SpeechSynthesisResult speak = await speechSynthesizer.SpeakTextAsync(traducción);
Si (Habla.Razón != ResultadoRazón.SynthesizingAudioCompleted)
{
Consola.WriteLine(hablar.Razón);
}
```

**Pitón**: translator.py

'''pitón
# Sintetizar la traducción
voces = {
"fr": "fr-FR-HenriNeural",
"es": "es-ES-ElviraNeural",
"hi": "hi-IN-MadhurNeural"
}
speech_config.speech_synthesis_voice_name = voices.get(targetLanguage)
speech_synthesizer = speech_sdk. SpeechSynthesizer(speech_config)
hablar = speech_synthesizer.hablar_texto_asíncrono(traducción).get()
if speak.reason != speech_sdk. ResultReason.SynthesizingAudioCompleted:
print(hablar.razón)
```

1. Guarde sus cambios y regrese al terminal integrado para la  carpeta **translator**, e ingrese el siguiente comando para ejecutar el programa:

**C#**

```
Ejecución de dotnet
```

**Pitón**

```
Python translator.py
```

1. Cuando se le solicite, ingrese un código de idioma válido (*fr*, *es* o *hi*) y luego hable claramente por el micrófono y diga una frase que podría usar cuando viaje al extranjero. El programa debe transcribir su entrada hablada y responder con una traducción hablada. Repita este proceso, probando cada idioma compatible con la aplicación. Cuando hayas terminado, pulsa **ENTER** para finalizar el programa.

> **NOTA**
> *En este ejemplo, ha usado un **SpeechTranslationConfig** para traducir voz a texto y, a continuación, ha usado un **SpeechConfig** para sintetizar la traducción como voz. De hecho, puede usar * *SpeechTranslationConfig** para sintetizar la traducción directamente, pero esto solo funciona cuando se traduce a un solo idioma y da como resultado una transmisión de audio que normalmente se guarda como un archivo en lugar de enviarse directamente a un hablante.*

## Más información

Para obtener más información sobre el uso de la API de traducción de voz de Azure AI, consulte la [Documentación de traducción de voz](https://learn.microsoft.com/azure/ai-services/speech-service/speech-translation).

