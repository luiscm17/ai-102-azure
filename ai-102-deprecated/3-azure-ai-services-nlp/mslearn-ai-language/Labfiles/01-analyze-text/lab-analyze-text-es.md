# Analizar texto
__Azure Language__ admite el análisis de texto, incluida la detección de idioma, el análisis de sentimientos, la extracción de frases clave y el reconocimiento de entidades.

Por ejemplo, supongamos que una agencia de viajes desea procesar las opiniones de los hoteles que se han enviado al sitio web de la empresa. Mediante el uso del lenguaje de Azure AI, pueden determinar el idioma en el que se escribe cada revisión, la opinión (positiva, neutral o negativa) de las reseñas, las frases clave que pueden indicar los temas principales tratados en la revisión y las entidades con nombre, como lugares, puntos de referencia o personas mencionadas en las reseñas.

## Aprovisionamiento de un recurso de lenguaje de Azure AI
Si aún no tiene uno en su suscripción, deberá aprovisionar un recurso de service__ de lenguaje de IA __Azure en su suscripción de Azure.

1. Abra Azure Portal en [https://portal.azure.com](https://portal.azure.com) e inicie sesión con la cuenta de Microsoft asociada a su suscripción de Azure.
2. Seleccione __Create un resource__.
3. En el campo de búsqueda, busque __Language service__. A continuación, en los resultados, seleccione __Create__ en __Language Service__.
4. Seleccione Continuar para crear el recurso.
5. Aprovisione el recurso con la siguiente configuración:
    * __Subscription__: Su suscripción a Azure.
    * __Resource group__: elija o cree un grupo de recursos.
    * __Region__:Elija cualquier región disponible
    * __Name__: Introduzca un nombre único.
    * __Pricing tier__: Seleccione F0 (libre) o S (estándar) si F no está disponible.
    * __Responsible Notice__ de IA: De acuerdo.
6. Seleccione __Review + create__ y, a continuación, seleccione __Create__ para aprovisionar el recurso.
7. Espere a que se complete la implementación y, a continuación, vaya al recurso implementado.
8. Vea la página de __Keys y Endpoint__ en la sección __Resource Management__. Necesitará la información de esta página más adelante en el ejercicio.

## Preparación para desarrollar una aplicación en Visual Studio Code
Desarrollará la aplicación de análisis de texto con Visual Studio Code. Los archivos de código de la aplicación se han proporcionado en un repositorio de GitHub.

> [!TIP]
>
> Si ya ha clonado el repositorio __mslearn-ai-language__, ábralo en el código de Visual Studio. De lo contrario, siga estos pasos para clonarlo en su entorno de desarrollo.

1. Inicie Visual Studio Code.
2. Abra la paleta (SHIFT+CTRL+P) y ejecute un comando __Git__: __Clone__ para clonar el repositorio [https://github.com/MicrosoftLearning/mslearn-ai-language](https://github.com/MicrosoftLearning/mslearn-ai-language) en una carpeta local (no importa qué carpeta).
3. Cuando se haya clonado el repositorio, abra la carpeta en Visual Studio Code.

>[!NOTE]
>Si Visual Studio Code le muestra un mensaje emergente para pedirle que confíe en el código que está abriendo, haga clic en __Si, confío en la opción autor__ en la ventana emergente.

4. Espere mientras se instalan archivos adicionales para admitir los proyectos de código de C# en el repositorio.

>[!NOTE]
>Si se le pide que agregue los recursos necesarios para compilar y depurar, seleccione __Not Now__.

## Configura tu aplicación
Se han proporcionado aplicaciones para C# y Python, así como un archivo de texto de ejemplo que usará para probar el resumen. Ambas aplicaciones cuentan con la misma funcionalidad. En primer lugar, completará algunas partes clave de la aplicación para permitirle usar el recurso de Azure AI Language.

1. En Visual Studio Code, en el panel __Explorer__, vaya a la carpeta __Labfiles/01-analyze-text__ y expanda la carpeta __CSharp__ o __Python__ en función de su preferencia de idioma y de la carpeta __text-analysis__ que contenga. Cada carpeta contiene los archivos específicos del idioma de una aplicación en la que va a integrar la funcionalidad de análisis de texto del lenguaje de Azure AI.
2. Haga clic con el botón derecho en la carpeta de análisis de texto que contiene sus archivos de código y abra un terminal integrado. A continuación, instale el paquete del SDK de Azure AI Language Text Analytics ejecutando el comando adecuado para su preferencia de idioma. Para el ejercicio de Python, instale también el paquete `dotenv`:

__C#:__

```csharp
dotnet add package Azure.AI.TextAnalytics --version 5.3.0
```

__Python:__

```
 pip install azure-ai-textanalytics==5.3.0
 pip install python-dotenv
```
3. En el panel __Explorer__, en la carpeta __text-analysis__, abra el archivo de configuración de su idioma preferido

   * __C#__: appsettings.json
   * __Python__: .env
4. Actualice los valores de configuración para incluir el __endpoint__ y un __key__ del recurso de lenguaje de Azure que creó (disponible en la página __Keys y Endpoint__ del recurso de lenguaje de IA de Azure en Azure Portal)
5. Guarde el archivo de configuración.

6. Tenga en cuenta que la carpeta de análisis de texto contiene un archivo de código para la aplicación cliente:

    * __C#__: Program.cs
    * __Python__: text-analysis.py

    Abra el archivo de código y, en la parte superior, debajo de las referencias de espacio de nombres existentes, busque el comentario __Import namespaces__. A continuación, en este comentario, agregue el siguiente código específico del idioma para importar los espacios de nombres que necesitará para usar el SDK de Text Analytics:

    __C#__: Programs.cs
    
    ```csharp
     //Importar espacios de nombres
     using from Azure;
     using Azure.AI.TextAnalytics;
    ```
    __Python__: text-analysis.py

    ```python
     # importar espacios de nombres
     from azure.core.credentials import AzureKeyCredential
     from azure.ai.textanalytics import TextAnalyticsClient
    ```
7. En la función __Main__, tenga en cuenta que ya se ha proporcionado el código para cargar el punto de conexión y la clave del servicio Azure AI Language desde el archivo de configuración. A continuación, busque el cliente de __Create client using endpoint and key__ y agregue el siguiente código para crear un cliente para la API de análisis de texto:

    __C#__: Programs.cs
    ```cs
     // Create client using endpoint and key
     AzureKeyCredential credentials = new AzureKeyCredential(aiSvcKey);
     Uri endpoint = new Uri(aiSvcEndpoint);
     TextAnalyticsClient aiClient = new TextAnalyticsClient(endpoint, credentials);
    ```
    __Python__: text-analysis.py

    ```python
     # Create client using endpoint and key
     credential = AzureKeyCredential(ai_key)
     ai_client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)
    ```
8. Guarde los cambios y regrese al terminal integrado para la carpeta __text-analysis__, e ingrese el siguiente comando para ejecutar el programa:

    * __C#__: ejecución de dotnet
    * __Python__: Python text-analysis.py

>[!TIP]
>Puede usar el icono de tamaño de panel __Maximize (^)__ en la barra de herramientas del terminal para ver más texto de la consola.

9. Observe la salida, ya que el código debería ejecutarse sin errores, mostrando el contenido de cada archivo de texto de revisión en la carpeta __reviews__. La aplicación crea correctamente un cliente para la API de Text Analytics, pero no la utiliza. Lo arreglaremos en el siguiente procedimiento.

## Agregar código para detectar el idioma

Ahora que ha creado un cliente para la API, vamos a usarlo para detectar el idioma en el que se escribe cada reseña.

1. En la función __Main__ de su programa, busque el comentario __Get language__. A continuación, en este comentario, agregue el código necesario para detectar el idioma en cada documento de revisión:

    __C#__: Programs.cs
    ```csharp
     // Get language
     DetectedLanguage detectedLanguage = aiClient.DetectLanguage(text);
     Console.WriteLine($"\nLanguage: {detectedLanguage.Name}");
    ```
    __Python__: text-analysis.py

    ```python
     # Get language
     detectedLanguage = ai_client.detect_language(documents=[text])[0]
     print('\nLanguage: {}'.format(detectedLanguage.primary_language.name))
    ```

    > [!NOTE]
    > En este ejemplo, cada revisión se analiza individualmente, lo que da como resultado una llamada independiente al servicio para cada archivo. Un enfoque alternativo es crear una colección de documentos y pasarlos al servicio en una sola llamada. En ambos enfoques, la respuesta del servicio consiste en una recopilación de documentos; es por eso que en el código Python anterior, se especifica el índice del primer (y único) documento en la respuesta ([0]).

2. Guarde los cambios. A continuación, regrese al terminal integrado para la carpeta __text-analysis__ y vuelva a ejecutar el programa.

3. Observe el resultado, observando que esta vez se identifica el idioma para cada revisión.

## Agregar código para evaluar el sentimiento
___Sentiment analysis___ es una técnica comúnmente utilizada para clasificar texto como _positivo_ o _negativo_ (o posiblemente _neutro_ o _mixto_). Se suele utilizar para analizar publicaciones en redes sociales, reseñas de productos y otros elementos en los que el sentimiento del texto puede proporcionar información útil.

1. En la función __Main__ de su programa, busque el comentario __Get sentiment__. A continuación, en este comentario, agregue el código necesario para detectar el sentimiento de cada documento de revisión:

    __C#__: Program.cs

    ```csharp
     // Get sentiment
     DocumentSentiment sentimentAnalysis = aiClient.AnalyzeSentiment(text);
     Console.WriteLine($"\nSentiment: {sentimentAnalysis.Sentiment}");
    ```

    __Python__: text-analysis.py

    ```python
     # Get sentiment
     sentimentAnalysis = ai_client.analyze_sentiment(documents=[text])[0]
     print("\nSentiment: {}".format(sentimentAnalysis.sentiment))
    ```

2. Guarde los cambios. A continuación, regrese al terminal integrado para la carpeta __text-analysis__ y vuelva a ejecutar el programa.
3. Observe la salida, notando que se detecta el sentimiento de las reseñas.

## Agregar código para identificar frases clave

Puede ser útil identificar frases clave en un cuerpo de texto para ayudar a determinar los temas principales que trata.

1. En la función __Main__ de su programa, busque la clave de comentario __Get phrases__. A continuación, en este comentario, agregue el código necesario para detectar las frases clave en cada documento de revisión:

    __C#__: Program.cs

    ```csharp
     // Get key phrases
     KeyPhraseCollection phrases = aiClient.ExtractKeyPhrases(text);
     if (phrases.Count > 0)
     {
         Console.WriteLine("\nKey Phrases:");
         foreach(string phrase in phrases)
         {
             Console.WriteLine($"\t{phrase}");
         }
     }
    ```

    __Python__: text-analysis.py

    ```python
     # Get key phrases
     phrases = ai_client.extract_key_phrases(documents=[text])[0].key_phrases
     if len(phrases) > 0:
         print("\nKey Phrases:")
         for phrase in phrases:
             print('\t{}'.format(phrase))
    ```
2. Guarde los cambios. A continuación, regrese al terminal integrado para la carpeta __text-analysis__ y vuelva a ejecutar el programa.
3. Observe el resultado, observando que cada documento contiene frases clave que dan una idea de lo que trata la revisión.

## Agregar código para extraer entidades

A menudo, los documentos u otros cuerpos de texto mencionan personas, lugares, períodos de tiempo u otras entidades. La API de Text Analytics puede detectar varias categorías (y subcategorías) de entidad en el texto.

1. En la función __Main__ de su programa, busque el comentario __Get entities__. A continuación, en este comentario, agregue el código necesario para identificar las entidades que se mencionan en cada revisión:

    __C#__: Program.cs

    ```csharp
     // Get entities
     CategorizedEntityCollection entities = aiClient.RecognizeEntities(text);
     if (entities.Count > 0)
     {
         Console.WriteLine("\nEntities:");
         foreach(CategorizedEntity entity in entities)
         {
             Console.WriteLine($"\t{entity.Text} ({entity.Category})");
         }
     }
    ```
    __Python__: text-analysis.py

    ```python
     # Get entities
     entities = ai_client.recognize_entities(documents=[text])[0].entities
     if len(entities) > 0:
         print("\nEntities")
         for entity in entities:
             print('\t{} ({})'.format(entity.text, entity.category))
    ```

2. Guarde los cambios. A continuación, regrese al terminal integrado para la carpeta __text-analysis__ y vuelva a ejecutar el programa.
3. Observar la salida, anotando las entidades que se han detectado en el texto.

## Agregar código para extraer entidades vinculadas

Además de las entidades categorizadas, la API de Text Analytics puede detectar entidades para las que hay vínculos conocidos a orígenes de datos, como Wikipedia.

1. En la función __Main__ de su programa, busque el comentario __Get vinculado entities__. Luego, en este comentario, agregue el código necesario para identificar las entidades vinculadas que se mencionan en cada revisión:

    __C#__: Program.cs
    
    ```csharp
     // Get linked entities
     LinkedEntityCollection linkedEntities = aiClient.RecognizeLinkedEntities(text);
     if (linkedEntities.Count > 0)
     {
         Console.WriteLine("\nLinks:");
         foreach(LinkedEntity linkedEntity in linkedEntities)
         {
             Console.WriteLine($"\t{linkedEntity.Name} ({linkedEntity.Url})");
         }
     }
    ```
    __Python__: text-analysis.py
    
    ```python
     # Get linked entities
     entities = ai_client.recognize_linked_entities(documents=[text])[0].entities
     if len(entities) > 0:
         print("\nLinks")
         for linked_entity in entities:
             print('\t{} ({})'.format(linked_entity.name, linked_entity.url))
    ```
2. Guarde los cambios. A continuación, regrese al terminal integrado para la carpeta __text-analysis__ y vuelva a ejecutar el programa.
3. Observe la salida, anotando las entidades vinculadas que se identifican.

## Limpiar recursos
Si ha terminado de explorar el servicio de lenguaje de IA de Azure, puede eliminar los recursos que creó en este ejercicio. A continuación, te explicamos cómo hacerlo:

1. Abra Azure Portal en [https://portal.azure.com](https://portal.azure.com) e inicie sesión con la cuenta de Microsoft asociada a su suscripción de Azure.

2. Vaya al recurso de Azure AI Language que creó en este laboratorio.

3. En la página del recurso, seleccione __Delete__ y siga las instrucciones para eliminar el recurso.

### Más información
Para obtener más información sobre el uso de __Azure Language__ de IA, consulte la [documentación](https://learn.microsoft.com/azure/ai-services/language-service/).
