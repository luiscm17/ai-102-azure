---
Laboratorio:
title: 'Extraer entidades personalizadas'
módulo: 'Módulo 3 - Introducción al procesamiento del lenguaje natural'
---

# Extraer entidades personalizadas

Además de otras funcionalidades de procesamiento de lenguaje natural, Azure AI Language Service permite definir entidades personalizadas y extraer instancias de ellas del texto.

Para probar la extracción de entidad personalizada, crearemos un modelo y lo entrenaremos a través de Azure AI Language Studio y, a continuación, usaremos una aplicación de línea de comandos para probarlo.

## Aprovisionamiento de un  recurso de *Azure AI Language*

Si aún no tiene uno en su suscripción, deberá aprovisionar un  recurso **Azure AI Language Service**. Además, utilice la clasificación de texto personalizada, debe habilitar la  función **Clasificación y extracción de texto personalizada**.

1. En un explorador, abra Azure Portal en "https://portal.azure.com" e inicie sesión con su cuenta de Microsoft.
1. Seleccione el  botón **Crear un recurso**,  busque *Idioma* y cree un  recurso de **Servicio lingüístico**. Cuando se encuentre en la página de *Seleccionar características adicionales*, seleccione la característica personalizada que contiene **Extracción de reconocimiento de entidades con nombre personalizada**. Cree el recurso con la siguiente configuración:
- **Suscripción**: *Su suscripción de Azure*
- **Grupo de recursos**: *Seleccione o cree un grupo de recursos*
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
- **Nombre**: *Introduzca un nombre único*
- **Plan de tarifa**: seleccione **F0** (*gratis*) o **S** (*estándar*) si F no está disponible.
- **Cuenta de almacenamiento**: Nueva cuenta de almacenamiento:
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

## Subir anuncios de muestra

Una vez que haya creado el servicio de lenguaje de Azure AI y la cuenta de almacenamiento, deberá subir anuncios de ejemplo para entrenar el modelo más adelante.

1. En una nueva pestaña del navegador, descargue ejemplos de anuncios clasificados de 'https://aka.ms/entity-extraction-ads' y extraiga los archivos a una carpeta de su elección.

2. En Azure Portal, vaya a la cuenta de almacenamiento que creó y selecciónela.

3. En su cuenta de almacenamiento, seleccione **Configuración**, ubicada debajo de **Configuración**, y habilite la opción **Permitir acceso anónimo a Blob** y, a  continuación, seleccione **Guardar**.

4. Seleccione **Contenedores** en el menú de la izquierda, ubicado debajo de **Almacenamiento de datos**. En la pantalla que aparece, seleccione **+ Contenedor**. Asigne al contenedor el nombre 'classifieds' y establezca **Nivel de acceso anónimo** en **Contenedor (acceso de lectura anónimo para contenedores y blobs)**.

> **NOTA**: Al configurar una cuenta de almacenamiento para una solución real, tenga cuidado de asignar el nivel de acceso adecuado. Para obtener más información sobre cada nivel de acceso, consulte la [Documentación de Azure Storage](https://learn.microsoft.com/azure/storage/blobs/anonymous-read-access-configure).

5. Después de crear el contenedor, selecciónelo y haga clic en el  botón **Cargar** y cargue los anuncios de muestra que descargó.

## Crear un proyecto de reconocimiento de entidades con nombre personalizado

Ahora está listo para crear un proyecto de reconocimiento de entidades con nombre personalizado. Este proyecto proporciona un lugar de trabajo para crear, entrenar e implementar el modelo.

> **NOTA**: También puede crear, compilar, entrenar e implementar su modelo a través de la API de REST.

1. En una nueva pestaña del navegador, abra el portal de Azure AI Language Studio en "https://language.cognitive.azure.com/" e inicie sesión con la cuenta de Microsoft asociada a su suscripción de Azure.
1. Si se le pide que elija un recurso de idioma, seleccione la siguiente configuración:

- **Directorio de Azure**: el directorio de Azure que contiene su suscripción.
- **Suscripción de Azure**: Su suscripción de Azure.
- **Tipo de recurso**: Idioma.
- **Recurso de idioma**: el recurso de idioma de Azure AI que creó anteriormente.

Si se le  solicita <u>not</u> que  elija un recurso de idioma, puede deberse a que tiene varios recursos de idioma en su suscripción; en cuyo caso:

1. En la barra de la parte superior de la página, seleccione la opción **Configuración (&#9881;)Botón ** .
2. En la  página **Configuración**, vea la  pestaña **Recursos**.
3. Seleccione el recurso de idioma que acaba de crear y haga clic en **Cambiar recurso**.
4. En la parte superior de la página, haga clic en **Language Studio** para volver a la página de inicio de Language Studio.

1. En la parte superior del portal, en el  menú **Crear nuevo**, seleccione **Reconocimiento de entidad con nombre personalizado**.

1. Cree un nuevo proyecto con los siguientes ajustes:
- **Conectar almacenamiento**: *Es probable que este valor ya esté lleno. Cámbielo a su cuenta de almacenamiento si aún no lo está*
- **Información básica**:
- **Nombre**: 'CustomEntityLab'
- **Idioma principal del texto**: inglés (EE. UU.)
- **¿Su conjunto de datos incluye documentos que no están en el mismo idioma?** : *No*
- **Descripción**: 'Entidades personalizadas en anuncios clasificados'
- **Contenedor**:
- **Contenedor de Blob Store**: clasificados
- **¿Tus archivos están etiquetados con clases?**: No, necesito etiquetar mis archivos como parte de este proyecto

> **Consejo**: Si recibe un error sobre no estar autorizado para realizar esta operación, deberá agregar una asignación de roles. Para solucionar este problema, agregamos el rol "Colaborador de datos de blob de almacenamiento" en la cuenta de almacenamiento del usuario que ejecuta el laboratorio. Se pueden encontrar más detalles [en la página de documentación](https://learn.microsoft.com/azure/ai-services/language-service/custom-named-entity-recognition/how-to/create-project?tabs=portal%2Clanguage-studio#enable-identity-management-for-your-resource)

## Etiqueta tus datos

Ahora que el proyecto está creado, debe etiquetar los datos para entrenar el modelo sobre cómo identificar entidades.

1. Si la  página **Etiquetado de datos** aún no está abierta, en el panel de la izquierda, seleccione **Etiquetado de datos**. Verás una lista de los archivos que has subido a tu cuenta de almacenamiento.
1. En el lado derecho, en el  panel **Actividad**, seleccione **Agregar entidad** y agregue una nueva entidad llamada 'ItemForSale'.
1. Repita el paso anterior para crear las siguientes entidades:
- 'Precio'
- 'Ubicación'
1. Una vez que hayas creado tus tres entidades, selecciona **Ad 1.txt** para que puedas leerlo.
1. En *Ad 1.txt*: 
1. Resalte el texto *cordón frontal de leña* y seleccione la  entidad **ItemForSale**.
1. Resalte el texto *Denver, CO* y seleccione la  entidad **Ubicación**.
1. Resalte el texto *$90* y seleccione la  entidad **Precio**.
1. En el  panel **Actividad**, tenga en cuenta que este documento se agregará al conjunto de datos para entrenar el modelo.
1. Utilice el  botón **Siguiente documento** para pasar al siguiente documento y continúe asignando texto a las entidades apropiadas para todo el conjunto de documentos, agregándolos todos al conjunto de datos de entrenamiento.
1. Cuando haya etiquetado el último documento (*Ad 9.txt*), guarde las etiquetas.

## Entrena tu modelo

Una vez que haya etiquetado los datos, debe entrenar el modelo.

1. Seleccione **Trabajos de formación** en el panel de la izquierda.
2. Seleccione **Iniciar un trabajo de capacitación**
3. Entrene un nuevo modelo llamado 'ExtractAds'
4. Elija **Dividir automáticamente el conjunto de pruebas de los datos de entrenamiento**

> **CONSEJO**: En sus propios proyectos de extracción, utilice la división de prueba que mejor se adapte a sus datos. Para obtener datos más coherentes y conjuntos de datos más grandes, Azure AI Language Service dividirá automáticamente el conjunto de pruebas por porcentaje. Con conjuntos de datos más pequeños, es importante entrenar con la variedad adecuada de documentos de entrada posibles.

5. Haz clic en **Entrenar**

> **IMPORTANTE**: El entrenamiento de su modelo a veces puede llevar varios minutos. Recibirás una notificación cuando se haya completado.

## Evalúa tu modelo

En las aplicaciones del mundo real, es importante evaluar y mejorar el modelo para comprobar que funciona como se espera. Dos páginas a la izquierda muestran los detalles del modelo entrenado y las pruebas que han fallado.

Selecciona **Rendimiento del modelo** en el menú de la izquierda y selecciona tu  modelo de 'ExtractAds'. Allí puede ver la puntuación de su modelo, las métricas de rendimiento y cuándo se entrenó. Podrá ver si se produjo un error en algún documento de prueba, y estos errores le ayudarán a comprender dónde mejorar.

## Implementa tu modelo

Cuando esté satisfecho con el entrenamiento de su modelo, es hora de implementarlo, lo que le permite comenzar a extraer entidades a través de la API.

1. En el panel izquierdo, seleccione **Implementación de un modelo**.
2. Seleccione **Agregar implementación**, luego ingrese el nombre 'AdEntities' y seleccione el  modelo **ExtractAds**.
3. Haga clic en **Implementar** para implementar su modelo.

## Preparación para desarrollar una aplicación en Visual Studio Code

Para probar las funcionalidades de extracción de entidades personalizadas del servicio Azure AI Language, desarrollará una aplicación de consola sencilla en Visual Studio Code.

> **Sugerencia**: Si ya ha clonado el  repositorio **mslearn-ai-language**, ábralo en el código de Visual Studio. De lo contrario, siga estos pasos para clonarlo en su entorno de desarrollo.

1. Inicie Visual Studio Code.
2. Abra la paleta (SHIFT+CTRL+P) y ejecute un  comando **Git: Clone** para clonar el  repositorio 'https://github.com/MicrosoftLearning/mslearn-ai-language' en una carpeta local (no importa qué carpeta).
3. Cuando se haya clonado el repositorio, abra la carpeta en Visual Studio Code.

> **Nota**: Si Visual Studio Code le muestra un mensaje emergente para pedirle que confíe en el código que está abriendo, haga clic en la opción **Sí, confío en los autores** en la ventana emergente.

4. Espere mientras se instalan archivos adicionales para admitir los proyectos de código de C# en el repositorio.

> **Nota**: Si se le solicita que agregue los activos necesarios para compilar y depurar, seleccione **Ahora no**.

## Configura tu aplicación

Se han proporcionado aplicaciones para C# y Python. Ambas aplicaciones cuentan con la misma funcionalidad. En primer lugar, completará algunas partes clave de la aplicación para permitirle usar el recurso de Azure AI Language.

1. En Visual Studio Code, en el  panel **Explorer**, vaya a la  carpeta **Labfiles/05-custom-entity-recognition** y expanda la  carpeta **CSharp** o **Python** en función de su preferencia de lenguaje y de la  carpeta **custom-entities** que contiene. Cada carpeta contiene los archivos específicos del idioma de una aplicación en la que va a integrar la funcionalidad de clasificación de texto del idioma de Azure AI.
1. Haga clic con el botón derecho en la  carpeta **custom-entities** que contiene sus archivos de código y abra un terminal integrado. A continuación, instale el paquete del SDK de Azure AI Language Text Analytics ejecutando el comando adecuado para su preferencia de idioma:

**C#**:

```
dotnet add package Azure.AI.TextAnalytics --version 5.3.0
```

**Pitón**:

```
pip install azure-ai-textanalytics==5.3.0
```

1. En el  panel **Explorer**, en la  carpeta **custom-entities**, abra el archivo de configuración de su idioma preferido

- **C#**: appsettings.json
- **Pitón**: .env
1. Actualice los valores de configuración para incluir el **punto de conexión** y una **clave** del recurso de lenguaje de Azure que creó (disponible en la  página **Claves y punto de conexión** del recurso de lenguaje de IA de Azure en Azure Portal). El archivo ya debe contener los nombres de proyecto e implementación del modelo de extracción de entidades personalizadas.
1. Guarde el archivo de configuración.

## Agregar código para extraer entidades

Ahora está listo para usar el servicio Azure AI Language para extraer entidades personalizadas del texto.

1. Expanda la  carpeta **ads** en la  carpeta **custom-entities** para ver los anuncios clasificados que analizará su aplicación.
1. En la  carpeta **custom-entities**, abra el archivo de código de la aplicación cliente:

- **C#**: Program.cs
- **Pitón**: custom-entities.py

1. Busque el comentario **Importar espacios de nombres**. A continuación, en este comentario, agregue el siguiente código específico del idioma para importar los espacios de nombres que necesitará para usar el SDK de Text Analytics:

**C#**: Programs.cs

'''csharp
Importar espacios de nombres
uso de Azure;
usando Azure.IA.Análisis de texto;
```

**Pitón**: custom-entities.py

'''pitón
# importar espacios de nombres
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
```

1. En la  función **Main**, observe que ya se ha proporcionado el código para cargar el punto de conexión y la clave del servicio Azure AI Language, así como los nombres de proyecto e implementación del archivo de configuración. A continuación, busque el comentario **Crear cliente mediante punto de conexión y clave** y agregue el siguiente código para crear un cliente para la API de análisis de texto:

**C#**: Programs.cs

'''csharp
Creación de un cliente mediante el punto de conexión y la clave
AzureKeyCredential credentials = new(aiSvcKey);
Punto de conexión de URI  = new(aiSvcEndpoint);
TextAnalyticsClient aiClient = new(endpoint, credentials);
```

**Pitón**: custom-entities.py

'''Pitón
# Crear cliente usando punto final y clave
credential = AzureKeyCredential(ai_key)
ai_client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)
```

1. En la  función **Main**, tenga en cuenta que el código existente lee todos los archivos de la  carpeta **ads** y crea una lista que contiene su contenido. En el caso del código C#, se usa una lista de  objetos **TextDocumentInput** para incluir el nombre de archivo como identificador y el idioma. En Python se utiliza una lista simple del contenido del texto.
1. Busque el comentario **Extraer entidades** y agregue el siguiente código:

**C#**: Program.cs

'''csharp
Extraer entidades
RecognizeCustomEntitiesOperation operación = await aiClient.RecognizeCustomEntitiesAsync(WaitUntil.Completado, batchedDocuments, projectName, deploymentName);

await foreach (RecognizeCustomEntitiesResultCollection documentsInPage en funcionamiento.Valor)
{
foreach (RecognizeEntitiesResult documentResult in documentsInPage)
{
Consola.WriteLine($"Resultado para \"{documentResult.Id}\":");

if (documentResult.HasError)
{
Consola.WriteLine($" Error!");
Consola.WriteLine($" Código de error del documento: {documentResult.Error.Código de error}");
Consola.WriteLine($" mensaje: {documentResult.Error.Mensaje}");
Consola.WriteLine();
continuar;
}

Consola.WriteLine($" Reconocido {documentResult.Entidades.Contar} entidades:");

foreach (entidad CategorizedEntity en documentResult.Entidades)
{
Consola.WriteLine($" entidad: {entidad.Texto}");
Consola.WriteLine($" Categoría: {entidad.Categoría}");
Consola.WriteLine($" Desplazamiento: {entidad.Compensación}");
Consola.WriteLine($" Longitud: {entidad.Longitud}");
Consola.WriteLine($" ConfidenceScore: {entidad.ConfidenceScore}");
Consola.WriteLine($" SubCategoría: {entidad.Subcategoría}");
Consola.WriteLine();
}

Consola.WriteLine();
}
}
```

**Pitón**: custom-entities.py

'''Pitón
# Extraer entidades
operación = ai_client.begin_recognize_custom_entities(
batchedDocuments,
project_name=project_name,
deployment_name=deployment_name
)

document_results = operación.resultado()

Para Doc, custom_entities_result en zip(archivos, document_results):
imprimir(doc)
if custom_entities_result.kind == "CustomEntityRecognition":
Para entity en custom_entities_result.entities:
imprimir(
"\tEntity '{}' tiene la categoría '{}' con puntuación de confianza de '{}'".format(
entidad.texto, entidad.categoría, entity.confidence_score
)
)
elif custom_entities_result.is_error es True:
print("\tError con el código '{}' y el mensaje '{}'".format(
custom_entities_result.error.code, custom_entities_result.error.message
)
)
```

1. Guarde los cambios en su archivo de código.

## Pruebe su aplicación

Ahora la aplicación está lista para probar.

1. En el terminal integrado para la  carpeta **classify-text** ingrese el siguiente comando para ejecutar el programa:

- **C#**: 'ejecución de dotnet'
- **Pitón**: 'pitón custom-entities.py'

> **Consejo**: Puede usar el  icono **Maximizar tamaño del panel** (**^**) en la barra de herramientas del terminal para ver más texto de la consola.

1. Observe la salida. La aplicación debe enumerar los detalles de las entidades que se encuentran en cada archivo de texto.

## Limpiar

Cuando ya no necesites tu proyecto, puedes eliminarlo de la  página **Proyectos** de Language Studio. También puede quitar el servicio de lenguaje de IA de Azure y la cuenta de almacenamiento asociada en [Azure Portal](https://portal.azure.com).

