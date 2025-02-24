---
Laboratorio:
title: 'Clasificación de texto personalizada'
módulo: 'Módulo 3 - Introducción al procesamiento del lenguaje natural'
---

# Clasificación de texto personalizada

Azure AI Language proporciona varias funcionalidades de NLP, incluida la identificación de frases clave, el resumen de texto y el análisis de sentimientos. El servicio de idioma también proporciona características personalizadas como respuestas a preguntas personalizadas y clasificación de texto personalizada.

Para probar la clasificación de texto personalizada del servicio de lenguaje de IA de Azure, configuraremos el modelo mediante Language Studio y, a continuación, usaremos una pequeña aplicación de línea de comandos que se ejecute en Cloud Shell para probarlo. El mismo patrón y funcionalidad que se usan aquí se puede seguir para las aplicaciones del mundo real.

## Aprovisionamiento de un  recurso de *Azure AI Language*

Si aún no tiene uno en su suscripción, deberá aprovisionar un  recurso **Azure AI Language Service**. Además, utilice la clasificación de texto personalizada, debe habilitar la  función **Clasificación y extracción de texto personalizada**.

1. En un explorador, abra Azure Portal en "https://portal.azure.com" e inicie sesión con su cuenta de Microsoft.
1. Seleccione el campo de búsqueda en la parte superior del portal, busque "Servicios de IA de Azure" y cree un  recurso de **Servicio lingüístico**.
1. Seleccione la casilla que incluye **Clasificación de texto personalizada**. A continuación, seleccione **Continuar para crear el recurso**.
1. Cree un recurso con la siguiente configuración:
- **Suscripción**: *Su suscripción de Azure*.
- **Grupo de recursos**: *Seleccione o cree un grupo de recursos*.
- **Región**: *Elija una de las siguientes regiones*\*
- Este de Australia
- Centro de la India
- Este de EE. UU.
- Este de EE. UU. 2
- Norte de Europa
- Centro-sur de EE. UU.
- Suiza Norte
- Sur del Reino Unido
- Europa Occidental
- Oeste de EE. UU. 2
- Oeste de EE. UU. 3
- **Nombre**: *Introduzca un nombre único*.
- **Plan de tarifa**: seleccione **F0** (*gratis*) o **S** (*estándar*) si F no está disponible.
- **Cuenta de almacenamiento**: Nueva cuenta de almacenamiento
- **Nombre de la cuenta de almacenamiento**: *Escriba un nombre único*.
- **Tipo de cuenta de almacenamiento**: LRS estándar
- **Aviso de IA responsable**: Seleccionado.

1. Seleccione **Revisar + crear** y, a continuación, seleccione **Crear** para aprovisionar el recurso.
1. Espere a que se complete la implementación y, a continuación, vaya al recurso implementado.
1. Vea la  página **Claves y punto de conexión**. Necesitará la información de esta página más adelante en el ejercicio.

## Roles para tu usuario
> **NOTA**: Si omites este paso, tendrás un error 403 al intentar conectarte a tu proyecto personalizado. Es importante que el usuario actual tenga este rol para acceder a los datos de blob de la cuenta de almacenamiento, incluso si es el propietario de la cuenta de almacenamiento.**

1. Vaya a la página de la cuenta de almacenamiento en Azure Portal.
2. Seleccione **Control de acceso (IAM)** en el menú de navegación de la izquierda.
3. Seleccione **Agregar** para agregar asignaciones de roles y elija el  rol **Colaborador de datos de blobs de almacenamiento** en la cuenta de almacenamiento.
4. En **Asignar acceso a**, seleccione **Usuario, grupo o entidad de servicio**.
5. Seleccione **Seleccionar miembros**.
6. Seleccione su Usuario. Puede buscar nombres de usuario en el  campo **Seleccionar**.

## Subir artículos de muestra

Una vez que haya creado el servicio de lenguaje de IA de Azure y la cuenta de almacenamiento, deberá cargar artículos de ejemplo para entrenar el modelo más adelante.

1. En una nueva pestaña del navegador, descargue artículos de muestra de 'https://aka.ms/classification-articles' y extraiga los archivos a una carpeta de su elección.

1. En Azure Portal, vaya a la cuenta de almacenamiento que ha creado y selecciónela.

1. En su cuenta de almacenamiento, seleccione **Configuración**, ubicado debajo de **Configuración**. En la pantalla Configuración, habilite la opción **Permitir acceso anónimo a Blob** y, a continuación, seleccione **Guardar**.

1. Seleccione **Contenedores** en el menú de la izquierda, ubicado debajo de **Almacenamiento de datos**. En la pantalla que aparece, seleccione **+ Contenedor**. Asigne al contenedor el nombre 'articles' y establezca **Nivel de acceso anónimo** en **Container (acceso de lectura anónimo para contenedores y blobs)**.

> **NOTA**: Al configurar una cuenta de almacenamiento para una solución real, tenga cuidado de asignar el nivel de acceso adecuado. Para obtener más información sobre cada nivel de acceso, consulte la [Documentación de Azure Storage](https://learn.microsoft.com/azure/storage/blobs/anonymous-read-access-configure).

1. Una vez que hayas creado el contenedor, selecciónalo y luego selecciona el  botón **Cargar**. Seleccione **Buscar archivos** para buscar los artículos de muestra que descargó. A continuación, seleccione **Subir**.

## Crear un proyecto de clasificación de texto personalizado

Una vez completada la configuración, cree un proyecto de clasificación de texto personalizado. Este proyecto proporciona un lugar de trabajo para crear, entrenar e implementar el modelo.

> **NOTA**: Este laboratorio utiliza **Language Studio**, pero también puede crear, compilar, entrenar e implementar su modelo a través de la API de REST.

1. En una nueva pestaña del navegador, abra el portal de Azure AI Language Studio en "https://language.cognitive.azure.com/" e inicie sesión con la cuenta de Microsoft asociada a su suscripción de Azure.
1. Si se le pide que elija un recurso de idioma, seleccione la siguiente configuración:

- **Directorio de Azure**: el directorio de Azure que contiene su suscripción.
- **Suscripción de Azure**: Su suscripción de Azure.
- **Tipo de recurso**: Idioma.
- **Recurso de idioma**: el recurso de idioma de Azure AI que creó anteriormente.

Si se le  solicita <u>not</u> que  elija un recurso de idioma, puede deberse a que tiene varios recursos de idioma en su suscripción; en cuyo caso:

1. En la barra en la parte superior de la página, seleccione la **Configuración (&#9881;)Botón ** .
2. En la  página **Configuración**, vea la  pestaña **Recursos**.
3. Seleccione el recurso de idioma que acaba de crear y haga clic en **Cambiar recurso**.
4. En la parte superior de la página, haz clic en **Language Studio** para volver a la página de inicio de Language Studio

1. En la parte superior del portal, en el  menú **Crear nuevo**, seleccione **Clasificación de texto personalizada**.
1. Aparecerá la  página **Conectar almacenamiento**. Todos los valores ya se habrán rellenado. Así que seleccione **Siguiente**.
1. En la  página **Seleccionar tipo de proyecto**, seleccione **Clasificación de etiqueta única**. A continuación, seleccione **Siguiente**.
1. En el  panel **Introducir información básica**, establezca lo siguiente:
- **Nombre**: 'ClassifyLab' 
- **Idioma principal del texto**: inglés (EE. UU.)
- **Descripción**: 'Laboratorio de texto personalizado'

1. Seleccione **Siguiente**.
1. En la  página **Elegir contenedor**,  establezca el  menú desplegable **Contenedor de almacén de blobs** en el contenedor *articles*.
1. Seleccione la  opción **No, necesito etiquetar mis archivos como parte de este proyecto**. A continuación, seleccione **Siguiente**.
1. Selecciona **Crear proyecto**.

> **Consejo**: Si recibe un error sobre no estar autorizado para realizar esta operación, deberá agregar una asignación de roles. Para solucionar este problema, agregamos el rol "Colaborador de datos de blob de almacenamiento" en la cuenta de almacenamiento del usuario que ejecuta el laboratorio. Se pueden encontrar más detalles [en la página de documentación](https://learn.microsoft.com/azure/ai-services/language-service/custom-named-entity-recognition/how-to/create-project?tabs=portal%2Clanguage-studio#enable-identity-management-for-your-resource)

## Etiqueta tus datos

Ahora que el proyecto está creado, debe etiquetar los datos para entrenar al modelo sobre cómo clasificar el texto.

1. A la izquierda, seleccione **Etiquetado de datos**, si aún no está seleccionado. Verás una lista de los archivos que has subido a tu cuenta de almacenamiento.
1. En el lado derecho, en el  panel **Actividad**, seleccione **+ Agregar clase**. Los artículos de este laboratorio se dividen en cuatro clases que deberá crear: "Clasificados", "Deportes", "Noticias" y "Entretenimiento".

! [Captura de pantalla que muestra la página de datos de la etiqueta y el botón agregar clase.](.. /media/tag-data-add-class-new.png#lightbox)

1. Una vez que hayas creado tus cuatro clases, selecciona **Artículo 1** para comenzar. Aquí puede leer el artículo, definir qué clase es este archivo y a qué conjunto de datos (de entrenamiento o de prueba) asignarlo.
1. Asigne a cada artículo la clase y el conjunto de datos adecuados (entrenamiento o prueba) utilizando el  panel **Actividad** de la derecha. Puede seleccionar una etiqueta de la lista de etiquetas de la derecha y establecer cada artículo como **entrenamiento** o **prueba** utilizando las opciones en la parte inferior del panel Actividad. Seleccione **Siguiente documento** para pasar al siguiente documento. Para los fines de este laboratorio, definiremos cuáles se usarán para entrenar el modelo y probarlo:

| Artículo | Clase | Conjunto de datos |
|---------|---------|---------|
| Artículo 1 | Deportes | Capacitación |
| Artículo 10 | Noticias | Capacitación |
| Artículo 11 | Entretenimiento | Pruebas |
| Artículo 12 | Noticias | Pruebas |
| Artículo 13 | Deportes | Pruebas |
| Artículo 2 | Deportes | Capacitación |
| Artículo 3 | Clasificados | Capacitación |
| Artículo 4 | Clasificados | Capacitación |
| Artículo 5 | Entretenimiento | Capacitación |
| Artículo 6 | Entretenimiento | Capacitación |
| Artículo 7 | Noticias | Capacitación |
| Artículo 8 | Noticias | Capacitación |
| Artículo 9 | Entretenimiento | Capacitación |

> **NOTA**
> Los archivos de Language Studio se enumeran alfabéticamente, por lo que la lista anterior no está en orden secuencial. Asegúrese de visitar ambas páginas de los documentos al etiquetar sus artículos.

1. Seleccione **Guardar etiquetas** para guardar sus etiquetas.

## Entrena tu modelo

Una vez que haya etiquetado los datos, debe entrenar el modelo.

1. Seleccione **Trabajos de formación** en el menú de la izquierda.
1. Seleccione **Iniciar un trabajo de formación**.
1. Entrene un nuevo modelo denominado 'ClassifyArticles'.
1. Seleccione **Usar una división manual de los datos de entrenamiento y prueba**.

> **CONSEJO**
> En sus propios proyectos de clasificación, el servicio Azure AI Language dividirá automáticamente el conjunto de pruebas por porcentaje, lo que resulta útil con un conjunto de datos grande. Con conjuntos de datos más pequeños, es importante entrenar con la distribución de clases correcta.

1. Selecciona **Tren**

> **IMPORTANTE**
> El entrenamiento del modelo a veces puede llevar varios minutos. Recibirás una notificación cuando se haya completado.

## Evalúa tu modelo

En las aplicaciones del mundo real de la clasificación de texto, es importante evaluar y mejorar el modelo para comprobar que funciona como se espera.

1. Seleccione **Rendimiento del modelo** y seleccione su  modelo **ClassifyArticles**. Allí puede ver la puntuación de su modelo, las métricas de rendimiento y cuándo se entrenó. Si la puntuación del modelo no es del 100 %, significa que uno de los documentos utilizados para las pruebas no se evaluó con la etiqueta que tenía. Estos fracasos pueden ayudarte a entender dónde mejorar.
1. Seleccione la  pestaña **Detalles del conjunto de pruebas**. Si hay algún error, esta pestaña le permite ver los artículos que indicó para las pruebas y cómo los predijo el modelo y si eso entra en conflicto con su etiqueta de prueba. De forma predeterminada, la pestaña solo muestra predicciones incorrectas. Puede alternar la  opción **Mostrar solo discrepancias** para ver todos los artículos que indicó para la prueba y cómo se predijo cada uno de ellos.

## Implementa tu modelo

Cuando esté satisfecho con el entrenamiento de su modelo, es el momento de implementarlo, lo que le permite comenzar a clasificar texto a través de la API.

1. En el panel izquierdo, seleccione **Modelo de implementación**.
1. Seleccione **Agregar implementación**, luego ingrese 'articles' en el  campo **Crear un nuevo nombre de implementación** y seleccione **ClassifyArticles** en el  campo **Model**.
1. Seleccione **Implementar** para implementar su modelo.
1. Una vez que se implemente el modelo, deje esa página abierta. Necesitará el nombre del proyecto y la implementación en el paso siguiente.

## Preparación para desarrollar una aplicación en Visual Studio Code

Para probar las funcionalidades de clasificación de texto personalizadas del servicio Azure AI Language, desarrollará una aplicación de consola sencilla en Visual Studio Code.

> **Sugerencia**: Si ya ha clonado el  repositorio **mslearn-ai-language**, ábralo en el código de Visual Studio. De lo contrario, siga estos pasos para clonarlo en su entorno de desarrollo.

1. Inicie Visual Studio Code.
2. Abra la paleta (SHIFT+CTRL+P) y ejecute un  comando **Git: Clone** para clonar el  repositorio 'https://github.com/MicrosoftLearning/mslearn-ai-language' en una carpeta local (no importa qué carpeta).
3. Cuando se haya clonado el repositorio, abra la carpeta en Visual Studio Code.

> **Nota**: Si Visual Studio Code le muestra un mensaje emergente para pedirle que confíe en el código que está abriendo, haga clic en la opción **Sí, confío en los autores** en la ventana emergente.

4. Espere mientras se instalan archivos adicionales para admitir los proyectos de código de C# en el repositorio.

> **Nota**: Si se le solicita que agregue los activos necesarios para compilar y depurar, seleccione **Ahora no**.

## Configura tu aplicación

Se han proporcionado aplicaciones para C# y Python, así como un archivo de texto de ejemplo que usará para probar el resumen. Ambas aplicaciones cuentan con la misma funcionalidad. En primer lugar, completará algunas partes clave de la aplicación para permitirle usar el recurso de Azure AI Language.

1. En Visual Studio Code, en el  panel **Explorer**, vaya a la  carpeta **Labfiles/04-text-classification** y expanda la  carpeta **CSharp** o **Python** en función de su preferencia de lenguaje y de la  carpeta **classify-text** que contenga. Cada carpeta contiene los archivos específicos del idioma de una aplicación en la que va a integrar la funcionalidad de clasificación de texto del idioma de Azure AI.
1. Haga clic con el botón derecho en la  carpeta **classify-text** que contiene sus archivos de código y abra un terminal integrado. A continuación, instale el paquete del SDK de Azure AI Language Text Analytics ejecutando el comando adecuado para su preferencia de idioma:

**C#**:

```
dotnet add package Azure.AI.TextAnalytics --version 5.3.0
```

**Pitón**:

```
pip install azure-ai-textanalytics==5.3.0
```

1. En el  panel **Explorer**, en la  carpeta **classify-text**,  abra el archivo de configuración de su idioma preferido

- **C#**: appsettings.json
- **Pitón**: .env
1. Actualice los valores de configuración para incluir el **punto de conexión** y una **clave** del recurso de lenguaje de Azure que creó (disponible en la  página **Claves y punto de conexión** del recurso de lenguaje de IA de Azure en Azure Portal). El archivo ya debe contener los nombres del proyecto y de la implementación del modelo de clasificación de texto.
1. Guarde el archivo de configuración.

## Agregar código para clasificar documentos

Ahora está listo para usar el servicio de lenguaje de Azure AI para clasificar documentos.

1. Expanda la  carpeta **articles** en la  carpeta **classify-text** para ver los artículos de texto que clasificará su aplicación.
1. En la  carpeta **classify-text**, abra el archivo de código de la aplicación cliente:

- **C#**: Program.cs
- **Pitón**: classify-text.py

1. Busque el comentario **Importar espacios de nombres**. A continuación, en este comentario, agregue el siguiente código específico del idioma para importar los espacios de nombres que necesitará para usar el SDK de Text Analytics:

**C#**: Programs.cs

'''csharp
Importar espacios de nombres
uso de Azure;
usando Azure.IA.Análisis de texto;
```

**Pitón**: classify-text.py

'''pitón
# importar espacios de nombres
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
```

1. En la  función **Main**, observe que ya se ha proporcionado el código para cargar el punto de conexión y la clave del servicio Azure AI Language, así como los nombres de proyecto e implementación del archivo de configuración. A continuación, busque el comentario **Crear cliente mediante punto de conexión y clave** y agregue el siguiente código para crear un cliente para la API de análisis de texto:

**C#**: Programs.cs

'''csharp
Creación de un cliente mediante el punto de conexión y la clave
Credenciales AzureKeyCredential  = new AzureKeyCredential(aiSvcKey);
Punto de conexión de Uri  = nuevo Uri(aiSvcEndpoint);
TextAnalyticsClient aiClient = nuevo TextAnalyticsClient(endpoint, credentials);
```

**Pitón**: classify-text.py

'''Pitón
# Crear cliente usando punto final y clave
credential = AzureKeyCredential(ai_key)
ai_client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)
```

1. En la  función **Main**, tenga en cuenta que el código existente lee todos los archivos de la  carpeta **articles** y crea una lista que contiene su contenido. A continuación, busque el comentario **Obtener clasificaciones** y agregue el siguiente código:

**C#**: Program.cs

'''csharp
Obtener clasificaciones
Operación ClassifyDocumentOperation  = await aiClient.SingleLabelClassifyAsync(WaitUntil.Completado, batchedDocuments, projectName, deploymentName);

fichero intNo  = 0;
await foreach (ClassifyDocumentResultCollection documentsInPage en funcionamiento.Valor)
{
foreach (ClassifyDocumentResult documentResult en documentsInPage)
{
Consola.WriteLine(archivos[archivoNo].Nombre);
if (documentResult.HasError)
{
Consola.WriteLine($" Error!");
Consola.WriteLine($" Código de error del documento: {documentResult.Error.Código de error}");
Consola.WriteLine($" mensaje: {documentResult.Error.Mensaje}");
continuar;
}

Consola.WriteLine($" Predijo la siguiente clase:");
Consola.WriteLine();

foreach (ClasificaciónCategoría clasificación en documentResult.ClasificaciónCategorías)
{
Consola.WriteLine($" Categoría: {clasificación.Categoría}");
Consola.WriteLine($" Puntuación de confianza: {classification.ConfidenceScore}");
Consola.WriteLine();
}
archivoNo++;
}
}
```
**Pitón**: classify-text.py

'''Pitón
# Obtener clasificaciones
operación = ai_client.begin_single_label_classify(
batchedDocuments,
project_name=project_name,
deployment_name=deployment_name
)

document_results = operación.resultado()

Para Doc, classification_result en zip (archivos, document_results):
if classification_result.kind == "CustomDocumentClassification":
clasificación = classification_result.clasificaciones[0]
print("{} se clasificó como '{}' con puntuación de confianza {}.".formato(
doc, classification.category, classification.confidence_score)
)
elif classification_result.is_error es verdadero:
print("{} tiene un error con el código '{}' y el mensaje '{}'".format(
doc, classification_result.error.code, classification_result.error.message)
)
```

1. Guarde los cambios en su archivo de código.

## Pruebe su aplicación

Ahora la aplicación está lista para probar.

1. En el terminal integrado para la  carpeta **classify-text**,  e ingrese el siguiente comando para ejecutar el programa:

- **C#**: 'ejecución de dotnet'
- **Pitón**: 'pitón classify-text.py'

> **Consejo**: Puede usar el  icono **Maximizar tamaño del panel** (**^**) en la barra de herramientas del terminal para ver más texto de la consola.

1. Observe la salida. La aplicación debe enumerar una clasificación y una puntuación de confianza para cada archivo de texto.


## Limpiar

Cuando ya no necesites tu proyecto, puedes eliminarlo de la  página **Proyectos** de Language Studio. También puede quitar el servicio de lenguaje de IA de Azure y la cuenta de almacenamiento asociada en [Azure Portal](https://portal.azure.com).

