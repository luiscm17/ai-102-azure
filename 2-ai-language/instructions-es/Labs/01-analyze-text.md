---
lab:
    title: 'Analizar texto'
    description: "Usa Azure AI Language para analizar texto, incluyendo detección de idioma, análisis de sentimientos, extracción de frases clave y reconocimiento de entidades."
---

# Analizar Texto

**Azure AI Language** admite el análisis de texto, incluyendo detección de idioma, análisis de sentimientos, extracción de frases clave y reconocimiento de entidades.

Por ejemplo, supongamos que una agencia de viajes quiere procesar las reseñas de hoteles que se han enviado al sitio web de la empresa. Al usar Azure AI Language, pueden determinar el idioma en el que está escrita cada reseña, el sentimiento (positivo, neutral o negativo) de las reseñas, las frases clave que podrían indicar los temas principales discutidos en la reseña y las entidades nombradas, como lugares, puntos de referencia o personas mencionadas en las reseñas. En este ejercicio, usarás el SDK de Python de Azure AI Language para text analytics para implementar una aplicación simple de reseñas de hoteles basada en este ejemplo.

Si bien este ejercicio se basa en Python, puedes desarrollar aplicaciones de análisis de texto usando múltiples SDKs específicos de lenguaje; incluyendo:

- [Biblioteca cliente de Azure AI Text Analytics para Python](https://pypi.org/project/azure-ai-textanalytics/)
- [Biblioteca cliente de Azure AI Text Analytics para .NET](https://www.nuget.org/packages/Azure.AI.TextAnalytics)
- [Biblioteca cliente de Azure AI Text Analytics para JavaScript](https://www.npmjs.com/package/@azure/ai-text-analytics)

Este ejercicio toma aproximadamente **30** minutos.

## Aprovisionar un recurso de *Azure AI Language*

Si aún no tienes uno en tu suscripción, necesitarás aprovisionar un recurso de **servicio de Azure AI Language** en tu suscripción de Azure.

1. Abre el portal de Azure en `https://portal.azure.com` e inicia sesión usando la cuenta Microsoft asociada con tu suscripción de Azure.
1. Selecciona **Create a resource**.
1. En el campo de búsqueda, busca **Language service**. Luego, en los resultados, selecciona **Create** bajo **Language Service**.
1. Selecciona **Continue to create your resource**.
1. Aprovisiona el recurso usando la siguiente configuración:
    - **Subscription**: *Tu suscripción de Azure*.
    - **Resource group**: *Elige o crea un grupo de recursos*.
    - **Region**: *Elige cualquier región disponible*
    - **Name**: *Ingresa un nombre único*.
    - **Pricing tier**: Selecciona **F0** (*gratuito*), o **S** (*estándar*) si F no está disponible.
    - **Responsible AI Notice**: Acepta.
1. Selecciona **Review + create**, luego selecciona **Create** para aprovisionar el recurso.
1. Espera a que la implementación se complete y luego ve al recurso implementado.
1. Visualiza la página **Keys and Endpoint** en la sección **Resource Management**. Necesitarás la información en esta página más adelante en el ejercicio.

## Clonar el repositorio para este curso

Desarrollarás tu código usando Cloud Shell desde el Portal de Azure. Los archivos de código para tu aplicación han sido proporcionados en un repositorio de GitHub.

1. En el Portal de Azure, usa el botón **[\>_]** a la derecha de la barra de búsqueda en la parte superior de la página para crear un nuevo Cloud Shell en el portal de Azure, seleccionando un entorno de ***PowerShell***. El cloud shell proporciona una interfaz de línea de comandos en un panel en la parte inferior del portal de Azure.

    > **Nota**: Si anteriormente creaste un cloud shell que usa un entorno *Bash*, cámbialo a ***PowerShell***.

1. En la barra de herramientas del cloud shell, en el menú **Settings**, selecciona **Go to Classic version** (esto es necesario para usar el editor de código).

    **<font color="red">Asegúrate de haber cambiado a la versión clásica del cloud shell antes de continuar.</font>**

1. En el panel de PowerShell, ingresa los siguientes comandos para clonar el repositorio de GitHub para este ejercicio:

    ```bash
    rm -r mslearn-ai-language -f
    git clone https://github.com/microsoftlearning/mslearn-ai-language
    ```

    > **Tip**: A medida que ingreses comandos en el cloudshell, la salida puede ocupar una gran parte del búfer de pantalla. Puedes limpiar la pantalla ingresando el comando `cls` para que sea más fácil enfocarse en cada tarea.

1. Después de que se haya clonado el repositorio, navega a la carpeta que contiene los archivos de código de la aplicación:  

    ```bash
    cd mslearn-ai-language/Labfiles/01-analyze-text/Python/text-analysis
    ```

## Configurar tu aplicación

1. En el panel de la línea de comandos, ejecuta el siguiente comando para ver los archivos de código en la carpeta **text-analysis**:

    ```bash
    ls -a -l
    ```

    Los archivos incluyen un archivo de configuración (**.env**) y un archivo de código (**text-analysis.py**). El texto que tu aplicación analizará está en la subcarpeta **reviews**.

1. Crea un entorno virtual de Python e instala el paquete del SDK de Azure AI Language Text Analytics y otros paquetes requeridos ejecutando el siguiente comando:

    ```bash
    python -m venv labenv
    ./labenv/bin/Activate.ps1
    pip install -r requirements.txt azure-ai-textanalytics==5.3.0
    ```

1. Ingresa el siguiente comando para editar el archivo de configuración de la aplicación:

    ```bash
    code .env
    ```

    El archivo se abre en un editor de código.

1. Actualiza los valores de configuración para incluir el **endpoint** y una **key** del recurso de Azure Language que creaste (disponible en la página **Keys and Endpoint** de tu recurso de Azure AI Language en el portal de Azure)
1. Después de haber reemplazado los marcadores de posición, dentro del editor de código, usa el comando **CTRL+S** o **Clic derecho > Guardar** para guardar tus cambios y luego usa el comando **CTRL+Q** o **Clic derecho > Salir** para cerrar el editor de código mientras mantienes abierta la línea de comandos del cloud shell.

## Agregar código para conectarte a tu recurso de Azure AI Language

1. Ingresa el siguiente comando para editar el archivo de código de la aplicación:

    ```bash
    code text-analysis.py
    ```

1. Revisa el código existente. Agregarás código para trabajar con el SDK de AI Language Text Analytics.

    > **Tip**: A medida que agregues código al archivo de código, asegúrate de mantener la indentación correcta.

1. En la parte superior del archivo de código, debajo de las referencias de espacios de nombres existentes, encuentra el comentario **Import namespaces** y agrega el siguiente código para importar los espacios de nombres que necesitarás para usar el SDK de Text Analytics:

    ```python
   # import namespaces
   from azure.core.credentials import AzureKeyCredential
   from azure.ai.textanalytics import TextAnalyticsClient
    ```

1. En la función **main**, nota que el código para cargar el endpoint y la key del servicio Azure AI Language desde el archivo de configuración ya ha sido proporcionado. Luego encuentra el comentario **Create client using endpoint and key**, y agrega el siguiente código para crear un cliente para la API de Text Analysis:

    ```Python
   # Create client using endpoint and key
   credential = AzureKeyCredential(ai_key)
   ai_client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)
    ```

1. Guarda tus cambios (CTRL+S), luego ingresa el siguiente comando para ejecutar el programa (puedes maximizar el panel del cloud shell y redimensionar los paneles para ver más texto en el panel de la línea de comandos):

    ```bash
   python text-analysis.py
    ```

1. Observa la salida ya que el código debería ejecutarse sin error, mostrando el contenido de cada archivo de texto de reseña en la carpeta **reviews**. La aplicación crea exitosamente un cliente para la API de Text Analytics pero no lo utiliza. Lo arreglaremos en la siguiente sección.

## Agregar código para detectar idioma

Ahora que has creado un cliente para la API, usémoslo para detectar el idioma en el que está escrita cada reseña.

1. En el editor de código, encuentra el comentario **Get language**. Luego agrega el código necesario para detectar el idioma en cada documento de reseña:

    ```python
   # Get language
   detectedLanguage = ai_client.detect_language(documents=[text])[0]
   print('\nIdioma: {}'.format(detectedLanguage.primary_language.name))
    ```

     > **Nota**: *En este ejemplo, cada reseña se analiza individualmente, resultando en una llamada separada al servicio para cada archivo. Un enfoque alternativo es crear una colección de documentos y pasarlos al servicio en una sola llamada. En ambos enfoques, la respuesta del servicio consiste en una colección de documentos; por lo que en el código Python anterior, se especifica el índice del primer (y único) documento en la respuesta ([0]).*

1. Guarda tus cambios. Luego vuelve a ejecutar el programa.
1. Observa la salida, notando que esta vez se identifica el idioma para cada reseña.

## Agregar código para evaluar sentimiento

*El análisis de sentimientos* es una técnica comúnmente utilizada para clasificar texto como *positivo* o *negativo* (o posiblemente *neutral* o *mixto*). Se usa comúnmente para analizar publicaciones en redes sociales, reseñas de productos y otros elementos donde el sentimiento del texto puede proporcionar información útil.

1. En el editor de código, encuentra el comentario **Get sentiment**. Luego agrega el código necesario para detectar el sentimiento de cada documento de reseña:

    ```python
   # Get sentiment
   sentimentAnalysis = ai_client.analyze_sentiment(documents=[text])[0]
   print("\nSentimiento: {}".format(sentimentAnalysis.sentiment))
    ```

1. Guarda tus cambios. Luego cierra el editor de código y vuelve a ejecutar el programa.
1. Observa la salida, notando que se detecta el sentimiento de las reseñas.

## Agregar código para identificar frases clave

Puede ser útil identificar frases clave en un cuerpo de texto para ayudar a determinar los temas principales que discute.

1. En el editor de código, encuentra el comentario **Get key phrases**. Luego agrega el código necesario para detectar las frases clave en cada documento de reseña:

    ```python
   # Get key phrases
   phrases = ai_client.extract_key_phrases(documents=[text])[0].key_phrases
   if len(phrases) > 0:
        print("\nFrases Clave:")
        for phrase in phrases:
            print('\t{}'.format(phrase))
    ```

1. Guarda tus cambios y vuelve a ejecutar el programa.
1. Observa la salida, notando que cada documento contiene frases clave que dan alguna idea de qué trata la reseña.

## Agregar código para extraer entidades

A menudo, los documentos u otros cuerpos de texto mencionan personas, lugares, períodos de tiempo u otras entidades. La API de Text Analytics puede detectar múltiples categorías (y subcategorías) de entidad en tu texto.

1. En el editor de código, encuentra el comentario **Get entities**. Luego, agrega el código necesario para identificar entidades que se mencionan en cada reseña:

    ```python
   # Get entities
   entities = ai_client.recognize_entities(documents=[text])[0].entities
   if len(entities) > 0:
        print("\nEntidades")
        for entity in entities:
            print('\t{} ({})'.format(entity.text, entity.category))
    ```

1. Guarda tus cambios y vuelve a ejecutar el programa.
1. Observa la salida, notando las entidades que se han detectado en el texto.

## Agregar código para extraer entidades vinculadas

Además de las entidades categorizadas, la API de Text Analytics puede detectar entidades para las cuales hay enlaces conocidos a fuentes de datos, como Wikipedia.

1. En el editor de código, encuentra el comentario **Get linked entities**. Luego, agrega el código necesario para identificar entidades vinculadas que se mencionan en cada reseña:

    ```python
   # Get linked entities
   entities = ai_client.recognize_linked_entities(documents=[text])[0].entities
   if len(entities) > 0:
        print("\nEnlaces")
        for linked_entity in entities:
            print('\t{} ({})'.format(linked_entity.name, linked_entity.url))
    ```

1. Guarda tus cambios y vuelve a ejecutar el programa.
1. Observa la salida, notando las entidades vinculadas que se identifican.

## Limpiar recursos

Si has terminado de explorar el servicio Azure AI Language, puedes eliminar los recursos que creaste en este ejercicio. Así es cómo:

1. Cierra el panel de Azure cloud shell
1. En el portal de Azure, navega al recurso de Azure AI Language que creaste en este laboratorio.
1. En la página del recurso, selecciona **Delete** y sigue las instrucciones para eliminar el recurso.

## Más información

Para más información sobre el uso de **Azure AI Language**, consulta la [documentación](https://learn.microsoft.com/es-es/azure/ai-services/language-service/).
