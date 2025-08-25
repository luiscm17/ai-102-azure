---
lab:
    title: 'Traducir Texto'
    description: "Traduce texto proporcionado entre cualquier idioma compatible con Azure AI Translator."
---

# Traducir Texto

**Azure AI Translator** es un servicio que te permite traducir texto entre idiomas. En este ejercicio, lo usarás para crear una aplicación simple que traduzca entradas en cualquier idioma compatible al idioma objetivo de tu elección.

Si bien este ejercicio está basado en Python, puedes desarrollar aplicaciones de traducción de texto usando múltiples SDKs específicos de lenguaje; incluyendo:

- [Biblioteca cliente de Azure AI Translation para Python](https://pypi.org/project/azure-ai-translation-text/)
- [Biblioteca cliente de Azure AI Translation para .NET](https://www.nuget.org/packages/Azure.AI.Translation.Text)
- [Biblioteca cliente de Azure AI Translation para JavaScript](https://www.npmjs.com/package/@azure-rest/ai-translation-text)

Este ejercicio toma aproximadamente **30** minutos.

## Aprovisionar un recurso de *Azure AI Translator*

Si aún no tienes uno en tu suscripción, necesitarás aprovisionar un recurso de **Azure AI Translator**.

1. Abre Azure Portal en `https://portal.azure.com`, e inicia sesión usando la cuenta Microsoft asociada con tu suscripción de Azure.
1. En el campo de búsqueda en la parte superior, busca **Translators** luego selecciona **Translators** en los resultados.
1. Crea un recurso con la siguiente configuración:
    - **Subscription**: *Tu suscripción de Azure*
    - **Resource group**: *Elige o crea un grupo de recursos*
    - **Region**: *Elige cualquier región disponible*
    - **Name**: *Ingresa un nombre único*
    - **Pricing tier**: Selecciona **F0** (*gratuito*), o **S** (*estándar*) si F no está disponible.
1. Selecciona **Review + create**, luego selecciona **Create** para aprovisionar el recurso.
1. Espera a que la implementación se complete, y luego ve al recurso implementado.
1. Ve la página **Keys and Endpoint**. Necesitarás la información en esta página más adelante en el ejercicio.

## Prepararse para desarrollar una app en Cloud Shell

Para probar las capacidades de traducción de texto de Azure AI Translator, desarrollarás una aplicación simple de consola en Azure Cloud Shell.

1. En Azure Portal, usa el botón **[\>_]** a la derecha de la barra de búsqueda en la parte superior de la página para crear un nuevo Cloud Shell en Azure portal, seleccionando un entorno ***PowerShell***. El cloud shell proporciona una interfaz de línea de comandos en un panel en la parte inferior de Azure portal.

    > **Nota**: Si previamente creaste un cloud shell que usa un entorno *Bash*, cámbialo a ***PowerShell***.

1. En la barra de herramientas del cloud shell, en el menú **Settings**, selecciona **Go to Classic version** (esto es requerido para usar el editor de código).

    **<font color="red">Asegúrate de haber cambiado a la versión clásica del cloud shell antes de continuar.</font>**

1. En el panel de PowerShell, ingresa los siguientes comandos para clonar el repositorio GitHub de este ejercicio:

    ```bash
    rm -r mslearn-ai-language -f
    git clone https://github.com/microsoftlearning/mslearn-ai-language
    ```

    > **Tip**: Al ingresar comandos en el cloudshell, la salida puede ocupar una gran parte del búfer de pantalla. Puedes limpiar la pantalla ingresando el comando `cls` para facilitar el enfoque en cada tarea.

1. Después de que el repositorio haya sido clonado, navega a la carpeta que contiene los archivos de código de la aplicación:

    ```bash
    cd mslearn-ai-language/Labfiles/06-translator-sdk/Python/translate-text
    ```

## Configurar tu aplicación

1. En el panel de línea de comandos, ejecuta el siguiente comando para ver los archivos de código en la carpeta **translate-text**:

    ```bash
    ls -a -l
    ```

    Los archivos incluyen un archivo de configuración (**.env**) y un archivo de código (**translate.py**).

1. Crea un entorno virtual de Python e instala el paquete del SDK de Azure AI Translation y otros paquetes requeridos ejecutando el siguiente comando:

    ```bash
    python -m venv labenv
    ./labenv/bin/Activate.ps1
    pip install -r requirements.txt azure-ai-translation-text==1.0.1
    ```

1. Ingresa el siguiente comando para editar el archivo de configuración de la aplicación:

    ```bash
    code .env
    ```

    El archivo se abre en un editor de código.

1. Actualiza los valores de configuración para incluir la **region** y una **key** del recurso de Azure AI Translator que creaste (disponibles en la página **Keys and Endpoint** de tu recurso de Azure AI Translator en Azure Portal).

    > **NOTA**: ¡Asegúrate de agregar la *región* para tu recurso, <u>no</u> el endpoint!

1. Después de que hayas reemplazado los marcadores de posición, dentro del editor de código, usa el comando **CTRL+S** o **Clic derecho > Save** para guardar tus cambios y luego usa el comando **CTRL+Q** o **Clic derecho > Quit** para cerrar el editor de código mientras mantienes abierta la línea de comandos del cloud shell.

## Agregar código para traducir texto

1. Ingresa el siguiente comando para editar el archivo de código de la aplicación:

    ```bash
    code translate.py
    ```

1. Revisa el código existente. Agregarás código para trabajar con el SDK de Azure AI Translation.

    > **Tip**: A medida que agregas código al archivo de código, asegúrate de mantener la sangría correcta.

1. En la parte superior del archivo de código, bajo las referencias de espacio de nombres existentes, encuentra el comentario **Import namespaces** y agrega el siguiente código para importar los espacios de nombres que necesitarás para usar el SDK de Translation:

    ```python
   # import namespaces
   from azure.core.credentials import AzureKeyCredential
   from azure.ai.translation.text import *
   from azure.ai.translation.text.models import InputTextItem
    ```

1. En la función **main**, nota que el código existente lee la configuración de ajustes.
1. Encuentra el comentario **Create client using endpoint and key** y agrega el siguiente código:

    ```python
   # Create client using endpoint and key
   credential = AzureKeyCredential(translatorKey)
   client = TextTranslationClient(credential=credential, region=translatorRegion)
    ```

1. Encuentra el comentario **Choose target language** y agrega el siguiente código, que usa el servicio Text Translator para devolver una lista de idiomas compatibles para traducción, y solicita al usuario que seleccione un código de idioma para el idioma objetivo:

    ```python
   # Choose target language
   languagesResponse = client.get_supported_languages(scope="translation")
   print("{} idiomas compatibles.".format(len(languagesResponse.translation)))
   print("(Ver https://learn.microsoft.com/azure/ai-services/translator/language-support#translation)")
   print("Ingresa un código de idioma objetivo para traducción (por ejemplo, 'en'):")
   targetLanguage = "xx"
   supportedLanguage = False
   while supportedLanguage == False:
        targetLanguage = input()
        if  targetLanguage in languagesResponse.translation.keys():
            supportedLanguage = True
        else:
            print("{} no es un idioma compatible.".format(targetLanguage))
    ```

1. Encuentra el comentario **Translate text** y agrega el siguiente código, que repetidamente solicita al usuario texto para traducir, usa el servicio Azure AI Translator para traducirlo al idioma objetivo (detectando el idioma de origen automáticamente), y muestra los resultados hasta que el usuario ingresa *quit*:

    ```python
   # Translate text
   inputText = ""
   while inputText.lower() != "quit":
        inputText = input("Ingresa texto para traducir ('quit' para salir):")
        if inputText != "quit":
            input_text_elements = [InputTextItem(text=inputText)]
            translationResponse = client.translate(body=input_text_elements, to_language=[targetLanguage])
            translation = translationResponse[0] if translationResponse else None
            if translation:
                sourceLanguage = translation.detected_language
                for translated_text in translation.translations:
                    print(f"'{inputText}' fue traducido de {sourceLanguage.language} a {translated_text.to} como '{translated_text.text}'.")
    ```

1. Guarda tus cambios (CTRL+S), luego ingresa el siguiente comando para ejecutar el programa (puedes maximizar el panel del cloud shell y redimensionar los paneles para ver más texto en el panel de línea de comandos):

    ```bash
    python translate.py
    ```

1. Cuando se solicite, ingresa un idioma objetivo válido de la lista mostrada.
1. Ingresa una frase para traducir (por ejemplo `This is a test` o `C'est un test`) y observa los resultados, que deberían detectar el idioma de origen y traducir el texto al idioma objetivo.
1. Cuando hayas terminado, ingresa `quit`. Puedes ejecutar la aplicación nuevamente y elegir un idioma objetivo diferente.

## Limpiar recursos

Si has terminado de explorar el servicio Azure AI Translator, puedes eliminar los recursos que creaste en este ejercicio. Así es cómo:

1. Cierra el panel de Azure cloud shell
1. En Azure Portal, navega al recurso de Azure AI Translator que creaste en este laboratorio.
1. En la página del recurso, selecciona **Delete** y sigue las instrucciones para eliminar el recurso.

## Más información

Para más información sobre el uso de **Azure AI Translator**, consulta la [documentación de Azure AI Translator](https://learn.microsoft.com/azure/ai-services/translator/).
