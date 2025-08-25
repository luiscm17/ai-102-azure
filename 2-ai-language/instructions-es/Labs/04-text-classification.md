---
lab:
    title: 'Clasificación de texto personalizada'
    description: "Aplica clasificaciones personalizadas a entradas de texto usando Azure AI Language."
---

# Clasificación de texto personalizada

Azure AI Language proporciona varias capacidades de NLP, incluyendo la identificación de frases clave, resumen de texto y análisis de sentimientos. El servicio Language también proporciona características personalizadas como preguntas y respuestas personalizadas y clasificación de texto personalizada.

Para probar la clasificación de texto personalizada del servicio Azure AI Language, configurarás el modelo usando Language Studio y luego usarás una aplicación Python para probarlo.

Si bien este ejercicio está basado en Python, puedes desarrollar aplicaciones de clasificación de texto usando múltiples SDKs específicos de lenguaje; incluyendo:

- [Biblioteca cliente de Azure AI Text Analytics para Python](https://pypi.org/project/azure-ai-textanalytics/)
- [Biblioteca cliente de Azure AI Text Analytics para .NET](https://www.nuget.org/packages/Azure.AI.TextAnalytics)
- [Biblioteca cliente de Azure AI Text Analytics para JavaScript](https://www.npmjs.com/package/@azure/ai-text-analytics)

Este ejercicio toma aproximadamente **35** minutos.

## Aprovisionar un recurso de *Azure AI Language*

Si aún no tienes uno en tu suscripción, necesitarás aprovisionar un recurso de **servicio Azure AI Language**. Adicionalmente, para usar la clasificación de texto personalizada, necesitas habilitar la característica **Clasificación y extracción de texto personalizada**.

1. Abre Azure Portal en `https://portal.azure.com`, e inicia sesión usando la cuenta Microsoft asociada con tu suscripción de Azure.
1. Selecciona **Crear un recurso**.
1. En el campo de búsqueda, busca **Language service**. Luego, en los resultados, selecciona **Crear** bajo **Language Service**.
1. Selecciona la casilla que incluye **Custom text classification**. Luego selecciona **Continue to create your resource**.
1. Crea un recurso con la siguiente configuración:
    - **Subscription**: *Tu suscripción de Azure*.
    - **Resource group**: *Selecciona o crea un grupo de recursos*.
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
    - **Name**: *Ingresa un nombre único*.
    - **Pricing tier**: Selecciona **F0** (*gratuito*), o **S** (*estándar*) si F no está disponible.
    - **Storage account**: Nueva cuenta de almacenamiento
      - **Storage account name**: *Ingresa un nombre único*.
      - **Storage account type**: Standard LRS
    - **Responsible AI notice**: Seleccionado.

1. Selecciona **Review + create,** luego selecciona **Create** para aprovisionar el recurso.
1. Espera a que la implementación se complete, y luego ve al grupo de recursos.
1. Encuentra la cuenta de almacenamiento que creaste, selecciónala y verifica que el *Account kind* sea **StorageV2**. Si es v1, actualiza el tipo de cuenta de almacenamiento en la página de ese recurso.

## Configurar el acceso basado en roles para tu usuario

> **NOTA**: Si omites este paso, obtendrás un error 403 al intentar conectarte a tu proyecto personalizado. Es importante que tu usuario actual tenga este rol para acceder a los datos blob de la cuenta de almacenamiento, incluso si eres el propietario de la cuenta de almacenamiento.

1. Ve a la página de tu cuenta de almacenamiento en Azure Portal.
2. Selecciona **Access Control (IAM)** en el menú de navegación izquierdo.
3. Selecciona **Add** para Agregar Asignaciones de Rol, y elige el rol **Storage Blob Data Owner** en la cuenta de almacenamiento.
4. Dentro de **Assign access to**, selecciona **User, group, or service principal**.
5. Selecciona **Select members**.
6. Selecciona tu Usuario. Puedes buscar nombres de usuario en el campo **Select**.

## Cargar artículos de ejemplo

Una vez que hayas creado el servicio Azure AI Language y la cuenta de almacenamiento, necesitarás cargar artículos de ejemplo para entrenar tu modelo más tarde.

1. En una nueva pestaña del navegador, descarga artículos de ejemplo desde `https://aka.ms/classification-articles` y extrae los archivos a una carpeta de tu elección.

1. En Azure Portal, navega a la cuenta de almacenamiento que creaste y selecciónala.

1. En tu cuenta de almacenamiento selecciona **Configuration**, ubicado debajo de **Settings**. En la pantalla Configuration habilita la opción para **Allow Blob anonymous access** luego selecciona **Save**.

1. Selecciona **Containers** en el menú izquierdo, ubicado debajo de **Data storage**. En la pantalla que aparece, selecciona **+ Container**. Dale al contenedor el nombre `articles`, y establece **Anonymous access level** a **Container (anonymous read access for containers and blobs)**.

    > **NOTA**: Cuando configures una cuenta de almacenamiento para una solución real, ten cuidado de asignar el nivel de acceso apropiado. Para aprender más sobre cada nivel de acceso, consulta la [documentación de Azure Storage](https://learn.microsoft.com/azure/storage/blobs/anonymous-read-access-configure).

1. Después de haber creado el contenedor, selecciónalo luego selecciona el botón **Upload**. Selecciona **Browse for files** para buscar los artículos de ejemplo que descargaste. Luego selecciona **Upload**.

## Crear un proyecto de clasificación de texto personalizada

Después de que la configuración esté completa, crea un proyecto de clasificación de texto personalizada. Este proyecto proporciona un espacio de trabajo para construir, entrenar e implementar tu modelo.

> **NOTA**: Este laboratorio utiliza **Language Studio**, pero también puedes crear, construir, entrenar e implementar tu modelo a través de la API REST.

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

1. En la parte superior del portal, en el menú **Create new**, selecciona **Custom text classification**.
1. Aparecerá la página **Connect storage**. Todos los valores ya estarán completados. Así que selecciona **Next**.
1. En la página **Select project type**, selecciona **Single label classification**. Luego selecciona **Next**.
1. En el panel **Enter basic information**, establece lo siguiente:
    - **Name**: `ClassifyLab`  
    - **Text primary language**: English (US)
    - **Description**: `Custom text lab`

1. Selecciona **Next**.
1. En la página **Choose container**, establece el dropdown **Blob store container** a tu contenedor *articles*.
1. Selecciona la opción **No, I need to label my files as part of this project**. Luego selecciona **Next**.
1. Selecciona **Create project**.

> **Tip**: Si obtienes un error sobre no estar autorizado para realizar esta operación, necesitarás agregar una asignación de rol. Para solucionarlo, agregamos el rol "Storage Blob Data Contributor" en la cuenta de almacenamiento para el usuario que ejecuta el laboratorio. Más detalles se pueden encontrar [en la página de documentación](https://learn.microsoft.com/azure/ai-services/language-service/custom-named-entity-recognition/how-to/create-project?tabs=portal%2Clanguage-studio#enable-identity-management-for-your-resource)

## Etiquetar tus datos

Ahora que tu proyecto está creado, necesitas etiquetar, o taggear, tus datos para entrenar a tu modelo sobre cómo clasificar texto.

1. A la izquierda, selecciona **Data labeling**, si no está ya seleccionado. Verás una lista de los archivos que cargaste a tu cuenta de almacenamiento.
1. En el lado derecho, en el panel **Activity**, selecciona **+ Add class**. Los artículos en este laboratorio caen en cuatro clases que necesitarás crear: `Classifieds`, `Sports`, `News`, y `Entertainment`.

    ![Captura de pantalla que muestra la página de etiquetado de datos y el botón agregar clase.](../media/tag-data-add-class-new.png#lightbox)

1. Después de haber creado tus cuatro clases, selecciona **Article 1** para comenzar. Aquí puedes leer el artículo, definir a qué clase pertenece este archivo y a qué conjunto de datos (entrenamiento o prueba) asignarlo.
1. Asigna cada artículo a la clase apropiada y al conjunto de datos (entrenamiento o prueba) usando el panel **Activity** a la derecha. Puedes seleccionar una etiqueta de la lista de etiquetas a la derecha, y establecer cada artículo como **training** o **testing** usando las opciones en la parte inferior del panel Activity. Selecciona **Next document** para moverte al siguiente documento. Para los propósitos de este laboratorio, definiremos cuáles se usarán para entrenar el modelo y probar el modelo:

    | Artículo  | Clase         | Conjunto de datos |
    |---------|---------------|-----------------|
    | Article 1  | Sports        | Training        |
    | Article 10 | News          | Training        |
    | Article 11 | Entertainment | Testing         |
    | Article 12 | News          | Testing         |
    | Article 13 | Sports        | Testing         |
    | Article 2  | Sports        | Training        |
    | Article 3  | Classifieds   | Training        |
    | Article 4  | Classifieds   | Training        |
    | Article 5  | Entertainment | Training        |
    | Article 6  | Entertainment | Training        |
    | Article 7  | News          | Training        |
    | Article 8  | News          | Training        |
    | Article 9  | Entertainment | Training        |

    > **NOTA**
    > Los archivos en Language Studio se listan alfabéticamente, por lo que la lista anterior no está en orden secuencial. Asegúrate de visitar ambas páginas de documentos cuando etiquetes tus artículos.

1. Selecciona **Save labels** para guardar tus etiquetas.

## Entrenar tu modelo

Después de haber etiquetado tus datos, necesitas entrenar tu modelo.

1. Selecciona **Training jobs** en el menú del lado izquierdo.
1. Selecciona **Start a training job**.
1. Entrena un nuevo modelo llamado `ClassifyArticles`.
1. Selecciona **Use a manual split of training and testing data**.

    > **TIP**
    > En tus propios proyectos de clasificación, el servicio Azure AI Language dividirá automáticamente el conjunto de prueba por porcentaje, lo cual es útil con un conjunto de datos grande. Con conjuntos de datos más pequeños, es importante entrenar con la distribución de clase correcta.

1. Selecciona **Train**

> **IMPORTANTE**
> Entrenar tu modelo a veces puede tomar varios minutos. Recibirás una notificación cuando esté completo.

## Evaluar tu modelo

En aplicaciones del mundo real de clasificación de texto, es importante evaluar y mejorar tu modelo para verificar que esté funcionando como esperas.

1. Selecciona **Model performance**, y selecciona tu modelo **ClassifyArticles**. Allí puedes ver la puntuación de tu modelo, las métricas de rendimiento y cuándo fue entrenado. Si la puntuación de tu modelo no es del 100%, significa que uno de los documentos usados para pruebas no se evaluó como estaba etiquetado. Estos fallos pueden ayudarte a entender dónde mejorar.
1. Selecciona la pestaña **Test set details**. Si hay algún error, esta pestaña te permite ver los artículos que indicaste para pruebas y qué predijo el modelo para ellos y si eso entra en conflicto con su etiqueta de prueba. La pestaña muestra por defecto solo las predicciones incorrectas. Puedes alternar la opción **Show mismatches only** para ver todos los artículos que indicaste para pruebas y qué predijo cada uno de ellos.

## Implementar tu modelo

Cuando estés satisfecho con el entrenamiento de tu modelo, es hora de implementarlo, lo que te permite comenzar a clasificar texto a través de la API.

1. En el panel izquierdo, selecciona **Deploying model**.
1. Selecciona **Add deployment**, luego ingresa `articles` en el campo **Create a new deployment name**, y selecciona **ClassifyArticles** en el campo **Model**.
1. Selecciona **Deploy** para implementar tu modelo.
1. Una vez que tu modelo esté implementado, deja esa página abierta. Necesitarás tu nombre de proyecto y despliegue en el siguiente paso.

## Prepararse para desarrollar una app en Cloud Shell

Para probar las capacidades de clasificación de texto personalizada del servicio Azure AI Language, desarrollarás una aplicación simple de consola en Azure Cloud Shell.

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
    cd mslearn-ai-language/Labfiles/04-text-classification/Python/classify-text
    ```

## Configurar tu aplicación

1. En el panel de línea de comandos, ejecuta el siguiente comando para ver los archivos de código en la carpeta **classify-text**:

    ```bash
    ls -a -l
    ```

    Los archivos incluyen un archivo de configuración (**.env**) y un archivo de código (**classify-text.py**). El texto que tu aplicación analizará está en la subcarpeta **articles**.

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

1. Actualiza los valores de configuración para incluir el **endpoint** y una **key** del recurso de Azure Language que creaste (disponibles en la página **Keys and Endpoint** de tu recurso de Azure AI Language en Azure Portal). El archivo ya debería contener los nombres del proyecto y del despliegue para tu modelo de clasificación de texto.
1. Después de que hayas reemplazado los marcadores de posición, dentro del editor de código, usa el comando **CTRL+S** o **Clic derecho > Save** para guardar tus cambios y luego usa el comando **CTRL+Q** o **Clic derecho > Quit** para cerrar el editor de código mientras mantienes abierta la línea de comandos del cloud shell.

## Agregar código para clasificar documentos

1. Ingresa el siguiente comando para editar el archivo de código de la aplicación:

    ```bash
    code classify-text.py
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

1. Nota que el código existente lee todos los archivos en la carpeta **articles** y crea una lista que contiene sus contenidos. Luego encuentra el comentario **Get Classifications** y agrega el siguiente código:

     ```Python
   # Get Classifications
   operation = ai_client.begin_single_label_classify(
        batchedDocuments,
        project_name=project_name,
        deployment_name=deployment_name
   )

   document_results = operation.result()

   for doc, classification_result in zip(files, document_results):
        if classification_result.kind == "CustomDocumentClassification":
            classification = classification_result.classifications[0]
            print("{} was classified as '{}' with confidence score {}.".format(
                doc, classification.category, classification.confidence_score)
            )
        elif classification_result.is_error is True:
            print("{} has an error with code '{}' and message '{}'".format(
                doc, classification_result.error.code, classification_result.error.message)
            )
    ```

1. Guarda tus cambios (CTRL+S), luego ingresa el siguiente comando para ejecutar el programa (puedes maximizar el panel del cloud shell y redimensionar los paneles para ver más texto en el panel de línea de comandos):

    ```bash
    python classify-text.py
    ```

1. Observa la salida. La aplicación debería listar una clasificación y una puntuación de confianza para cada archivo de texto.

## Limpiar

Cuando ya no necesites tu proyecto, puedes eliminarlo desde tu página **Projects** en Language Studio. También puedes eliminar el servicio Azure AI Language y la cuenta de almacenamiento asociada en el [Azure portal](https://portal.azure.com).
