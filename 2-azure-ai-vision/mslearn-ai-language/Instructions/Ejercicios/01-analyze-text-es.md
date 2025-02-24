---
Laboratorio:
título: 'Analizar texto'
módulo: 'Módulo 3 - Desarrollo de soluciones de procesamiento del lenguaje natural'
---

# Analizar texto

**Azure Language** admite el análisis de texto, incluida la detección de idioma, el análisis de sentimientos, la extracción de frases clave y el reconocimiento de entidades.

Por ejemplo, supongamos que una agencia de viajes desea procesar las opiniones de los hoteles que se han enviado al sitio web de la empresa. Mediante el uso del lenguaje de Azure AI, pueden determinar el idioma en el que se escribe cada revisión, la opinión (positiva, neutral o negativa) de las reseñas, las frases clave que pueden indicar los temas principales tratados en la revisión y las entidades con nombre, como lugares, puntos de referencia o personas mencionadas en las reseñas.

## Aprovisionamiento de un  recurso de *Azure AI Language*

Si aún no tiene uno en su suscripción, deberá aprovisionar un  recurso **Azure AI Language Service** en su suscripción de Azure.

1. Abra Azure Portal en "https://portal.azure.com" e inicie sesión con la cuenta de Microsoft asociada a su suscripción de Azure.
1. Seleccione **Crear un recurso**.
1. En el campo de búsqueda, busque **Servicio lingüístico**. A continuación, en los resultados, seleccione **Crear** en **Servicio de idioma**.
1. Seleccione **Continuar para crear su recurso**.
1. Aprovisione el recurso con la siguiente configuración:
- **Suscripción**: *Su suscripción de Azure*.
- **Grupo de recursos**: *Elija o cree un grupo de recursos*.
- **Región**:*Elija cualquier región disponible*
- **Nombre**: *Introduzca un nombre único*.
- **Plan de tarifa**: seleccione **F0** (*gratis*) o **S** (*estándar*) si F no está disponible.
- **Aviso de IA responsable**: De acuerdo.
1. Seleccione **Revisar + crear** y, a continuación, seleccione **Crear** para aprovisionar el recurso.
1. Espere a que se complete la implementación y, a continuación, vaya al recurso implementado.
1. Vea la  página **Keys and Endpoint** en la  sección **Resource Management**. Necesitará la información de esta página más adelante en el ejercicio.

## Preparación para desarrollar una aplicación en Visual Studio Code

Desarrollará la aplicación de análisis de texto con Visual Studio Code. Los archivos de código de la aplicación se han proporcionado en un repositorio de GitHub.

> **Sugerencia**: Si ya ha clonado el  repositorio **mslearn-ai-language**, ábralo en el código de Visual Studio. De lo contrario, siga estos pasos para clonarlo en su entorno de desarrollo.

1. Inicie Visual Studio Code.
2. Abra la paleta (SHIFT+CTRL+P) y ejecute un  comando **Git: Clone** para clonar el  repositorio 'https://github.com/MicrosoftLearning/mslearn-ai-language' en una carpeta local (no importa qué carpeta).
3. Cuando se haya clonado el repositorio, abra la carpeta en Visual Studio Code.

> **Nota**: Si Visual Studio Code le muestra un mensaje emergente para pedirle que confíe en el código que está abriendo, haga clic en la opción **Sí, confío en los autores** en la ventana emergente.

4. Espere mientras se instalan archivos adicionales para admitir los proyectos de código de C# en el repositorio.

> **Nota**: Si se le solicita que agregue los activos necesarios para compilar y depurar, seleccione **Ahora no**.

## Configura tu aplicación

Se han proporcionado aplicaciones para C# y Python, así como un archivo de texto de ejemplo que usará para probar el resumen. Ambas aplicaciones cuentan con la misma funcionalidad. En primer lugar, completará algunas partes clave de la aplicación para permitirle usar el recurso de Azure AI Language.

1. En Visual Studio Code, en el  panel **Explorer**, vaya a la  carpeta **Labfiles/01-analyze-text** y expanda la  carpeta **CSharp** o **Python** en función de su preferencia de lenguaje y de la  carpeta **text-analysis** que contenga. Cada carpeta contiene los archivos específicos del idioma de una aplicación en la que va a integrar la funcionalidad de análisis de texto del lenguaje de Azure AI.
2. Haga clic con el botón derecho en la  carpeta **text-analysis** que contiene sus archivos de código y abra un terminal integrado. A continuación, instale el paquete del SDK de Azure AI Language Text Analytics ejecutando el comando adecuado para su preferencia de idioma. Para el ejercicio de Python, instale también el  paquete 'dotenv':

**C#**:

```
dotnet add package Azure.AI.TextAnalytics --version 5.3.0
```

**Pitón**:

```
pip install azure-ai-textanalytics==5.3.0
pip install python-dotenv
```

3. En el  panel **Explorer**, en la  carpeta **text-analysis**, abra el archivo de configuración de su idioma preferido

- **C#**: appsettings.json
- **Pitón**: .env
4. Actualice los valores de configuración para incluir el **punto de conexión** y una **clave** del recurso de lenguaje de Azure que creó (disponible en la  página **Claves y punto de conexión** del recurso de lenguaje de IA de Azure en Azure Portal)
5. Guarde el archivo de configuración.

6. Tenga en cuenta que la  carpeta **text-analysis** contiene un archivo de código para la aplicación cliente:

- **C#**: Program.cs
- **Pitón**: text-analysis.py

Abra el archivo de código y en la parte superior, debajo de las referencias de espacio de nombres existentes, busque el comentario **Importar espacios de nombres**. A continuación, en este comentario, agregue el siguiente código específico del idioma para importar los espacios de nombres que necesitará para usar el SDK de Text Analytics:

**C#**: Programs.cs

'''csharp
Importar espacios de nombres
uso de Azure;
usando Azure.IA.Análisis de texto;
```

**Pitón**: text-analysis.py

'''pitón
# importar espacios de nombres
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
```

7. En la  función **Main**, observe que ya se ha proporcionado el código para cargar el punto de conexión y la clave del servicio Azure AI Language desde el archivo de configuración. A continuación, busque el comentario **Crear cliente mediante punto de conexión y clave** y agregue el siguiente código para crear un cliente para la API de análisis de texto:

**C#**: Programs.cs

'''C#
Creación de un cliente mediante el punto de conexión y la clave
Credenciales AzureKeyCredential  = new AzureKeyCredential(aiSvcKey);
Punto de conexión de Uri  = nuevo Uri(aiSvcEndpoint);
TextAnalyticsClient aiClient = nuevo TextAnalyticsClient(endpoint, credentials);
```

**Pitón**: text-analysis.py

'''Pitón
# Crear cliente usando punto final y clave
credential = AzureKeyCredential(ai_key)
ai_client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)
```

8. Guarde los cambios y regrese al terminal integrado para la  carpeta **text-analysis**,  e ingrese el siguiente comando para ejecutar el programa:

- **C#**: 'ejecución de dotnet'
- **Pitón**: 'pitón text-analysis.py'

> **Consejo**: Puede usar el  icono **Maximizar tamaño del panel** (**^**) en la barra de herramientas del terminal para ver más texto de la consola.

9. Observe la salida, ya que el código debería ejecutarse sin errores, mostrando el contenido de cada archivo de texto de revisión en la  carpeta **reviews**. La aplicación crea correctamente un cliente para la API de Text Analytics, pero no la utiliza. Lo arreglaremos en el siguiente procedimiento.

## Agregar código para detectar el idioma

Ahora que ha creado un cliente para la API, vamos a usarlo para detectar el idioma en el que se escribe cada reseña.

1. En la  función **Principal** de su programa, busque el comentario **Obtener idioma**. A continuación, en este comentario, agregue el código necesario para detectar el idioma en cada documento de revisión:

**C#**: Programs.cs

'''csharp
Obtener idioma
DetectedLanguage detectedLanguage = aiClient.DetectLanguage(texto);
Consola.WriteLine($"\nIdioma: {LenguajeDetectado.Nombre}");
```

**Pitón**: text-analysis.py

'''pitón
# Obtener idioma
detectedLanguage = ai_client.detect_language(documents=[texto])[0]
print('\nIdioma: {}'.format(detectedLanguage.primary_language.nombre))
```

> **Nota**: *En este ejemplo, cada revisión se analiza individualmente, lo que da como resultado una llamada separada al servicio para cada archivo. Un enfoque alternativo es crear una colección de documentos y pasarlos al servicio en una sola llamada. En ambos enfoques, la respuesta del servicio consiste en una recopilación de documentos; por eso en el código Python anterior, se especifica el índice del primer (y único) documento de la respuesta ([0]).*

1. Guarde los cambios. A continuación, regrese al terminal integrado para la  carpeta **text-analysis** y vuelva a ejecutar el programa.
1. Observe el resultado, observando que esta vez se identifica el idioma para cada revisión.

## Agregar código para evaluar el sentimiento

El *análisis de sentimientos* es una técnica comúnmente utilizada para clasificar el texto como *positivo* o *negativo* (o posiblemente *neutro* o *mixto*). Se suele utilizar para analizar publicaciones en redes sociales, reseñas de productos y otros elementos en los que el sentimiento del texto puede proporcionar información útil.

1. En la  función **Principal** de su programa, busque el comentario **Obtener sentimiento**. A continuación, en este comentario, agregue el código necesario para detectar el sentimiento de cada documento de revisión:

**C#**: Program.cs

'''csharp
Obtener opinión
DocumentSentiment sentimentAnalysis = aiClient.AnalyzeSentiment(texto);
Consola.WriteLine($"\nSentimiento: {sentimentAnalysis.Sentimiento}");
```

**Pitón**: text-analysis.py

'''pitón
# Obtener sentimiento
sentimentAnalysis = ai_client.analyze_sentiment(documents=[texto])[0]
print("\nSentimiento: {}".format(sentimentAnalysis.sentiment))
```

1. Guarde los cambios. A continuación, regrese al terminal integrado para la  carpeta **text-analysis** y vuelva a ejecutar el programa.
1. Observe la salida, notando que se detecta el sentimiento de las reseñas.

## Agregar código para identificar frases clave

Puede ser útil identificar frases clave en un cuerpo de texto para ayudar a determinar los temas principales que trata.

1. En la  función **Principal** de su programa, busque el comentario **Obtener frases clave**. A continuación, en este comentario, agregue el código necesario para detectar las frases clave en cada documento de revisión:

**C#**: Program.cs

'''csharp
Obtener frases clave
Frases de KeyPhraseCollection  = aiClient.ExtractKeyPhrases(texto);
Si (frases.Recuento > 0)
{
Consola.WriteLine("\nFrases clave:");
foreach(frase de cadena en frases)
{
Consola.WriteLine($"\t{frase}");
}
}
```

**Pitón**: text-analysis.py

'''pitón
# Obtener frases clave
frases = ai_client.extracto_frases_clave(documentos=[texto])[0].key_frases
if len(frases) > 0:
print("\nFrases clave:")
Para frase en frases:
print('\t{}'.format(frase))
```

1. Guarde los cambios. A continuación, regrese al terminal integrado para la  carpeta **text-analysis** y vuelva a ejecutar el programa.
1. Observe el resultado, observando que cada documento contiene frases clave que brindan algunas ideas sobre de qué se trata la revisión.

## Agregar código para extraer entidades

A menudo, los documentos u otros cuerpos de texto mencionan personas, lugares, períodos de tiempo u otras entidades. La API de Text Analytics puede detectar varias categorías (y subcategorías) de entidad en el texto.

1. En la  función **Principal** de su programa, busque el comentario **Obtener entidades**. A continuación, en este comentario, agregue el código necesario para identificar las entidades que se mencionan en cada revisión:

**C#**: Program.cs

'''csharp
Obtención de entidades
Entidades CategorizedEntityCollection  = aiClient.RecognizeEntities(texto);
Si (entidades.Recuento > 0)
{
Consola.WriteLine("\nEntidades:");
foreach(Entidad categorizada  entidad en entidades)
{
Consola.WriteLine($"\t{entidad.Texto} ({entidad.Categoría})");
}
}
```

**Pitón**: text-analysis.py

'''pitón
# Obtener entidades
entidades = ai_client.reconocer_entidades(documentos=[texto])[0].entidades
Si len(entidades) > 0:
print("\nEntidades")
Para entidad en entidades:
print('\t{} ({})'.format(entidad.texto, entidad.categoría))
```

1. Guarde los cambios. A continuación, regrese al terminal integrado para la  carpeta **text-analysis** y vuelva a ejecutar el programa.
1. Observe la salida, anotando las entidades que se han detectado en el texto.

## Agregar código para extraer entidades vinculadas

Además de las entidades categorizadas, la API de Text Analytics puede detectar entidades para las que hay vínculos conocidos a orígenes de datos, como Wikipedia.

1. En la  función **Principal** de su programa, busque el comentario **Obtener entidades vinculadas**. Luego, en este comentario, agregue el código necesario para identificar las entidades vinculadas que se mencionan en cada revisión:

**C#**: Program.cs

'''csharp
Obtención de entidades vinculadas
LinkedEntityCollection linkedEntities = aiClient.RecognizeLinkedEntities(texto);
if (linkedEntities.Recuento > 0)
{
Consola.WriteLine("\nEnlaces:");
foreach(LinkedEntity, linkedEntity, en linkedEntities)
{
Consola.WriteLine($"\t{linkedEntity.Nombre} ({linkedEntity.url})");
}
}
```

**Pitón**: text-analysis.py

'''pitón
# Obtener entidades vinculadas
entities = ai_client.recognize_linked_entities(documents=[text])[0].entities
Si len(entidades) > 0:
print("\nEnlaces")
Para linked_entity en entidades:
print('\t{} ({})'.format(linked_entity.nombre, linked_entity.url))
```

1. Guarde los cambios. A continuación, regrese al terminal integrado para la  carpeta **text-analysis** y vuelva a ejecutar el programa.
1. Observe la salida, anotando las entidades vinculadas que se identifican.

## Limpiar recursos

Si ha terminado de explorar el servicio de lenguaje de IA de Azure, puede eliminar los recursos que creó en este ejercicio. A continuación, te explicamos cómo hacerlo:

1. Abra Azure Portal en "https://portal.azure.com" e inicie sesión con la cuenta de Microsoft asociada a su suscripción de Azure.

2. Vaya al recurso de Azure AI Language que creó en este laboratorio.

3. En la página del recurso, seleccione **Eliminar** y siga las instrucciones para eliminar el recurso.

## Más información

Para obtener más información sobre el uso  de **Azure AI Language**, consulte la [documentación](https://learn.microsoft.com/azure/ai-services/language-service/).

