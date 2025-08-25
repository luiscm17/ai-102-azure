---
lab:
    title: 'Extraer entidades personalizadas'
    description: "Entrena un modelo para extraer entidades personalizadas de entradas de texto usando Azure AI Language."
---

# Extraer entidades personalizadas

Además de otras capacidades de procesamiento de lenguaje natural, Azure AI Language Service te permite definir entidades personalizadas y extraer instancias de ellas desde texto.

Para probar la extracción de entidades personalizadas, crearemos un modelo y lo entrenaremos a través de Azure AI Language Studio, luego usaremos una aplicación Python para probarlo.

Si bien este ejercicio está basado en Python, puedes desarrollar aplicaciones de clasificación de texto usando múltiples SDKs específicos de lenguaje; incluyendo:

- [Biblioteca cliente de Azure AI Text Analytics para Python](https://pypi.org/project/azure-ai-textanalytics/)
- [Biblioteca cliente de Azure AI Text Analytics para .NET](https://www.nuget.org/packages/Azure.AI.TextAnalytics)
- [Biblioteca cliente de Azure AI Text Analytics para JavaScript](https://www.npmjs.com/package/@azure/ai-text-analytics)

Este ejercicio toma aproximadamente **35** minutos.

## Aprovisionar un recurso de *Azure AI Language*

Si aún no tienes uno en tu suscripción, necesitarás aprovisionar un recurso de **servicio Azure AI Language**. Adicionalmente, para usar la clasificación de texto personalizada, necesitas habilitar la característica **Clasificación y extracción de texto personalizada**.

1. En un navegador, abre Azure Portal en `https://portal.azure.com`, e inicia sesión con tu cuenta Microsoft.
1. Selecciona el botón **Create a resource**, busca *Language*, y crea un recurso **Language Service**. Cuando estés en la página de *Select additional features*, selecciona la característica personalizada que contiene **Custom named entity recognition extraction**. Crea el recurso con la siguiente configuración:
    - **Subscription**: *Tu suscripción de Azure*
    - **Resource group**: *Selecciona o crea un grupo de recursos*
    - **Region**: *Elige una de las siguientes regiones*\*
        - Australia East
        - Central India
        - East US
        - East US 2
        - North Europe
        - South Central US
        - Switzerland North
        - UK South
        - West Europe
        - West US 2
        - West US 3
    - **Name**: *Ingresa un nombre único*
    - **Pricing tier**: Selecciona **F0** (*gratuito*), o **S** (*estándar*) si F no está disponible.
    - **Storage account**: Nueva cuenta de almacenamiento:
      - **Storage account name**: *Ingresa un nombre único*.
      - **Storage account type**: Standard LRS
    - **Responsible AI notice**: Seleccionado.

1. Selecciona **Review + create**, luego selecciona **Create** para aprovisionar el recurso.
1. Espera a que la implementación se complete, y luego ve al recurso implementado.
1. Ve la página **Keys and Endpoint**. Necesitarás la información en esta página más adelante en el ejercicio.

## Configurar el acceso basado en roles para tu usuario

> **NOTA**: Si omites este paso, tendrás un error 403 al intentar conectarte a tu proyecto personalizado. Es importante que tu usuario actual tenga este rol para acceder a los datos blob de la cuenta de almacenamiento, incluso si eres el propietario de la cuenta de almacenamiento.

1. Ve a la página de tu cuenta de almacenamiento en Azure Portal.
2. Selecciona **Access Control (IAM)** en el menú de navegación izquierdo.
3. Selecciona **Add** para Agregar Asignaciones de Rol, y elige el rol **Storage Blob Data Contributor** en la cuenta de almacenamiento.
4. Dentro de **Assign access to**, selecciona **User, group, or service principal**.
5. Selecciona **Select members**.
6. Selecciona tu Usuario. Puedes buscar nombres de usuario en el campo **Select**.

## Cargar anuncios de ejemplo

Después de que hayas creado el Servicio Azure AI Language y la cuenta de almacenamiento, necesitarás cargar anuncios de ejemplo para entrenar tu modelo más tarde.

1. En una nueva pestaña del navegador, descarga anuncios clasificados de ejemplo desde `https://aka.ms/entity-extraction-ads` y extrae los archivos a una carpeta de tu elección.

2. En Azure Portal, navega a la cuenta de almacenamiento que creaste y selecciónala.

3. En tu cuenta de almacenamiento selecciona **Configuration**, ubicado debajo de **Settings**, y en la pantalla habilita la opción para **Allow Blob anonymous access** luego selecciona **Save**.

4. Selecciona **Containers** desde el menú izquierdo, ubicado debajo de **Data storage**. En la pantalla que aparece, selecciona **+ Container**. Dale al contenedor el nombre `classifieds`, y establece **Anonymous access level** a **Container (anonymous read access for containers and blobs)**.

    > **NOTA**: Cuando configures una cuenta de almacenamiento para una solución real, ten cuidado de asignar el nivel de acceso apropiado. Para aprender más sobre cada nivel de acceso, consulta la [documentación de Azure Storage](https://learn.microsoft.com/azure/storage/blobs/anonymous-read-access-configure).

5. Después de crear el contenedor, selecciónalo y haz clic en el botón **Upload** y carga los anuncios de ejemplo que descargaste.

## Crear un proyecto de reconocimiento de entidades con nombre personalizado

Ahora estás listo para crear un proyecto de reconocimiento de entidades con nombre personalizado. Este proyecto proporciona un espacio de trabajo para construir, entrenar e implementar tu modelo.

> **NOTA**: También puedes crear, construir, entrenar e implementar tu modelo a través de la API REST.

1. En una nueva pestaña del navegador, abre el portal de Azure AI Language Studio en `https://language.cognitive.azure.com/` e inicia sesión usando la cuenta Microsoft asociada con tu suscripción de Azure.
1. Si se te solicita elegir un recurso de Language, selecciona la siguiente configuración:

    - **Azure Directory**: El directorio de Azure que contiene tu suscripción.
    - **Azure subscription**: Tu suscripción de Azure.
    - **Resource type**: Language.
    - **Language resource**: El recurso de Azure AI Language que creaste anteriormente.

    Si <u>no</u> se te solicita elegir un recurso de lenguaje, puede ser porque tienes múltiples recursos de Language en tu suscripción; en cuyo caso:

    1. En la barra en la parte superior de la página, selecciona el botón **Settings (&#9881;)**.
    2. En la página **Settings**, ve a la pestaña **Resources**.
    3. Selecciona el recurso de lenguaje que acabas de crear y haz clic en **Switch resource**.
    4. En la parte superior de la página, haz clic en **Language Studio** para volver a la página de inicio de Language Studio.

1. En la parte superior del portal, en el menú **Create new**, selecciona **Custom named entity recognition**.

1. Crea un nuevo proyecto con la siguiente configuración:
    - **Connect storage**: *Este valor probablemente ya esté completado. Cámbialo a tu cuenta de almacenamiento si no lo está ya*
    - **Basic information**:
    - **Name**: `CustomEntityLab`
        - **Text primary language**: English (US)
        - **Does your dataset include documents that are not in the same language?** : *No*
        - **Description**: `Custom entities in classified ads`
    - **Container**:
        - **Blob store container**: classifieds
        - **Are your files labeled with classes?**: No, I need to label my files as part of this project

> **Tip**: Si obtienes un error sobre no estar autorizado para realizar esta operación, necesitarás agregar una asignación de rol. Para solucionarlo, agregamos el rol "Storage Blob Data Contributor" en la cuenta de almacenamiento para el usuario que ejecuta el laboratorio. Más detalles se pueden encontrar [en la página de documentación](https://learn.microsoft.com/azure/ai-services/language-service/custom-named-entity-recognition/how-to/create-project?tabs=portal%2Clanguage-studio#enable-identity-management-for-your-resource)

## Etiquetar tus datos

Ahora que tu proyecto está creado, necesitas etiquetar tus datos para entrenar a tu modelo sobre cómo identificar entidades.

1. Si la página **Data labeling** no está ya abierta, en el panel de la izquierda, selecciona **Data labeling**. Verás una lista de los archivos que cargaste a tu cuenta de almacenamiento.
1. En el lado derecho, en el panel **Activity**, selecciona **Add entity** y agrega una nueva entidad llamada `ItemForSale`.
1. Repite el paso anterior para crear las siguientes entidades:
    - `Price`
    - `Location`
1. Después de que hayas creado tus tres entidades, selecciona **Ad 1.txt** para poder leerlo.
1. En *Ad 1.txt*:
    1. Resalta el texto *face cord of firewood* y selecciona la entidad **ItemForSale**.
    1. Resalta el texto *Denver, CO* y selecciona la entidad **Location**.
    1. Resalta el texto *$90* y selecciona la entidad **Price**.
1. En el panel **Activity**, nota que este documento se agregará al conjunto de datos para entrenar el modelo.
1. Usa el botón **Next document** para moverte al siguiente documento, y continúa asignando texto a las entidades apropiadas para todo el conjunto de documentos, agregándolos todos al conjunto de datos de entrenamiento.
1. Cuando hayas etiquetado el último documento (*Ad 9.txt*), guarda las etiquetas.

## Entrenar tu modelo

Después de que hayas etiquetado tus datos, necesitas entrenar tu modelo.

1. Selecciona **Training jobs** en el panel de la izquierda.
2. Selecciona **Start a training job**
3. Entrena un nuevo modelo llamado `ExtractAds`
4. Elige **Automatically split the testing set from training data**

    > **TIP**: En tus propios proyectos de extracción, usa la división de pruebas que mejor se adapte a tus datos. Para datos más consistentes y conjuntos de datos más grandes, el Servicio Azure AI Language dividirá automáticamente el conjunto de prueba por porcentaje. Con conjuntos de datos más pequeños, es importante entrenar con la variedad correcta de documentos de entrada posibles.

5. Haz clic en **Train**

    > **IMPORTANTE**: Entrenar tu modelo a veces puede tomar varios minutos. Recibirás una notificación cuando esté completo.

## Evaluar tu modelo

En aplicaciones del mundo real, es importante evaluar y mejorar tu modelo para verificar que esté funcionando como esperas. Dos páginas a la izquierda te muestran los detalles de tu modelo entrenado y cualquier prueba que falló.

Selecciona **Model performance** en el menú del lado izquierdo, y selecciona tu modelo `ExtractAds`. Allí puedes ver la puntuación de tu modelo, las métricas de rendimiento y cuándo fue entrenado. Podrás ver si algún documento de prueba falló, y estos fallos te ayudan a entender dónde mejorar.

## Implementar tu modelo

Cuando estés satisfecho con el entrenamiento de tu modelo, es hora de implementarlo, lo que te permite comenzar a extraer entidades a través de la API.

1. En el panel izquierdo, selecciona **Deploying a model**.
2. Selecciona **Add deployment**, luego ingresa el nombre `AdEntities` y selecciona el modelo **ExtractAds**.
3. Haz clic en **Deploy** para implementar tu modelo.

## Prepararse para desarrollar una app en Cloud Shell

Para probar las capacidades de extracción de entidades personalizadas del servicio Azure AI Language, desarrollarás una aplicación simple de consola en Azure Cloud Shell.

1. En Azure Portal, usa el botón **[\>_]** a la derecha de la barra de búsqueda en la parte superior de la página para crear un nuevo Cloud Shell en Azure portal, seleccionando un entorno ***PowerShell***. El cloud shell proporciona una interfaz de línea de comandos en un panel en la parte inferior de Azure portal.

    > **Nota**: Si previamente creaste un cloud shell que usa un entorno *Bash*, cámbialo a ***PowerShell***.

1. En la barra de herramientas del cloud shell, en el menú **Settings**, selecciona **Go to Classic version** (esto es requerido para usar el editor de código).

    **<font color="red">Asegúrate de haber cambiado a la versión clásica del cloud shell antes de continuar.</font>**

1. En el panel de PowerShell, ingresa los siguientes comandos para clonar el repositorio GitHub de este ejercicio:

    ```bash
    rm -r mslearn-ai-language -f
    git clone https://github.com/microsoftlearning/mslearn-ai-language
    ```

    > **Tip**: Al pegar comandos en el cloudshell, la salida puede ocupar una gran parte del búfer de pantalla. Puedes limpiar la pantalla ingresando el comando `cls` para facilitar el enfoque en cada tarea.

1. Después de que el repositorio haya sido clonado, navega a la carpeta que contiene los archivos de código de la aplicación:

    ```bash
    cd mslearn-ai-language/Labfiles/05-custom-entity-recognition/Python/custom-entities
    ```

## Configurar tu aplicación

1. En el panel de línea de comandos, ejecuta el siguiente comando para ver los archivos de código en la carpeta **custom-entities**:

    ```bash
    ls -a -l
    ```

    Los archivos incluyen un archivo de configuración (**.env**) y un archivo de código (**custom-entities.py**). El texto que tu aplicación analizará está en la subcarpeta **ads**.

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

1. Actualiza los valores de configuración para incluir el **endpoint** y una **key** del recurso de Azure Language que creaste (disponibles en la página **Keys and Endpoint** de tu recurso de Azure AI Language en Azure Portal). El archivo ya debería contener los nombres del proyecto y del despliegue para tu modelo de extracción de entidades personalizadas.
1. Después de que hayas reemplazado los marcadores de posición, dentro del editor de código, usa el comando **CTRL+S** o **Clic derecho > Save** para guardar tus cambios y luego usa el comando **CTRL+Q** o **Clic derecho > Quit** para cerrar el editor de código mientras mantienes abierta la línea de comandos del cloud shell.

## Agregar código para extraer entidades

1. Ingresa el siguiente comando para editar el archivo de código de la aplicación:

    ```bash
    code custom-entities.py
    ```

1. Revisa el código existente. Agregarás código para trabajar con el SDK de AI Language Text Analytics.

    > **Tip**: A medida que agregas código al archivo de código, asegúrate de mantener la sangría correcta.

1. En la parte superior del archivo de código, bajo las referencias de espacio de nombres existentes, encuentra el comentario **Import namespaces** y agrega el siguiente código para importar los espacios de nombres que necesitarás para usar el SDK de Text Analytics:

    ```python
   # import namespaces
   from azure.core.credentials import AzureKeyCredential
   from azure.ai.textanalytics import TextAnalyticsClient
    ```

1. En la función **main**, nota que el código para cargar el endpoint y la key del servicio Azure AI Language y los nombres del proyecto y del despliegue desde el archivo de configuración ya ha sido proporcionado. Luego encuentra el comentario **Create client using endpoint and key**, y agrega el siguiente código para crear un cliente de análisis de texto:

    ```Python
   # Create client using endpoint and key
   credential = AzureKeyCredential(ai_key)
   ai_client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)
    ```

1. Nota que el código existente lee todos los archivos en la carpeta **ads** y crea una lista que contiene sus contenidos. Luego encuentra el comentario **Extract entities** y agrega el siguiente código:

    ```Python
   # Extract entities
   operation = ai_client.begin_recognize_custom_entities(
        batchedDocuments,
        project_name=project_name,
        deployment_name=deployment_name
   )

   document_results = operation.result()

   for doc, custom_entities_result in zip(files, document_results):
        print(doc)
        if custom_entities_result.kind == "CustomEntityRecognition":
            for entity in custom_entities_result.entities:
                print(
                    "\tEntity '{}' has category '{}' with confidence score of '{}'".format(
                        entity.text, entity.category, entity.confidence_score
                    )
                )
        elif custom_entities_result.is_error is True:
            print("\tError with code '{}' and message '{}'".format(
                custom_entities_result.error.code, custom_entities_result.error.message
                )
            )
    ```

1. Guarda tus cambios (CTRL+S), luego ingresa el siguiente comando para ejecutar el programa (puedes maximizar el panel del cloud shell y redimensionar los paneles para ver más texto en el panel de línea de comandos):

    ```bash
    python custom-entities.py
    ```

1. Observa la salida. La aplicación debería listar detalles de las entidades encontradas en cada archivo de texto.

## Limpiar

Cuando ya no necesites tu proyecto, puedes eliminarlo desde tu página **Projects** en Language Studio. También puedes eliminar el servicio Azure AI Language y la cuenta de almacenamiento asociada en el [Azure portal](https://portal.azure.com).
