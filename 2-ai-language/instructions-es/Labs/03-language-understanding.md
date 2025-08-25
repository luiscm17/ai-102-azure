---
lab:
    title: 'Crear un modelo de comprensión de lenguaje con el servicio Azure AI Language'
    description: "Crear un modelo personalizado de comprensión de lenguaje para interpretar entrada, predecir intención e identificar entidades."
---

# Crear un modelo de comprensión de lenguaje con el servicio Language

El servicio Azure AI Language te permite definir un modelo de *comprensión de lenguaje conversacional* que las aplicaciones pueden usar para interpretar *expresiones* de lenguaje natural de los usuarios (entrada de texto o voz), predecir la *intención* de los usuarios (lo que quieren lograr) e identificar cualquier *entidad* a la que se deba aplicar la intención.

Por ejemplo, un modelo de lenguaje conversacional para una aplicación de reloj podría esperar procesar entrada como:

*¿Qué hora es en Londres?*

Este tipo de entrada es un ejemplo de una *expresión* (algo que un usuario podría decir o escribir), para la cual la *intención* deseada es obtener la hora en una ubicación específica (una *entidad*); en este caso, Londres.

> **NOTA**
> La tarea de un modelo de lenguaje conversacional es predecir la intención del usuario e identificar cualquier entidad a la que se aplique la intención. <u>No</u> es trabajo de un modelo de lenguaje conversacional realizar realmente las acciones requeridas para satisfacer la intención. Por ejemplo, una aplicación de reloj puede usar un modelo de lenguaje conversacional para discernir que el usuario quiere saber la hora en Londres; pero la aplicación cliente misma debe entonces implementar la lógica para determinar la hora correcta y presentarla al usuario.

En este ejercicio, usarás el servicio Azure AI Language para crear un modelo de comprensión de lenguaje conversacional y usarás el SDK de Python para implementar una aplicación cliente que lo use.

Si bien este ejercicio se basa en Python, puedes desarrollar aplicaciones de comprensión conversacional usando múltiples SDKs específicos de lenguaje; incluyendo:

- [Biblioteca cliente de Azure AI Conversations para Python](https://pypi.org/project/azure-ai-language-conversations/)
- [Biblioteca cliente de Azure AI Conversations para .NET](https://www.nuget.org/packages/Azure.AI.Language.Conversations)
- [Biblioteca cliente de Azure AI Conversations para JavaScript](https://www.npmjs.com/package/@azure/ai-language-conversations)

Este ejercicio toma aproximadamente **35** minutos.

## Aprovisionar un recurso de *Azure AI Language*

Si aún no tienes uno en tu suscripción, necesitarás aprovisionar un recurso de **servicio de Azure AI Language** en tu suscripción de Azure.

1. Abre el portal de Azure en `https://portal.azure.com` e inicia sesión usando la cuenta Microsoft asociada con tu suscripción de Azure.
1. Selecciona **Create a resource**.
1. En el campo de búsqueda, busca **Language service**. Luego, en los resultados, selecciona **Create** bajo **Language Service**.
1. Aprovisiona el recurso usando la siguiente configuración:
    - **Subscription**: *Tu suscripción de Azure*.
    - **Resource group**: *Elige o crea un grupo de recursos*.
    - **Region**: *Elige una de las siguientes regiones*\*
        - Australia East
        - Central India
        - China East 2
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
    - **Responsible AI Notice**: Acepta.
1. Selecciona **Review + create**, luego selecciona **Create** para aprovisionar el recurso.
1. Espera a que la implementación se complete y luego ve al recurso implementado.
1. Visualiza la página **Keys and Endpoint**. Necesitarás la información en esta página más adelante en el ejercicio.

## Crear un proyecto de comprensión de lenguaje conversacional

Ahora que has creado un recurso de autoría, puedes usarlo para crear un proyecto de comprensión de lenguaje conversacional.

1. En una nueva pestaña del navegador, abre el portal de Azure AI Language Studio en `https://language.cognitive.azure.com/` e inicia sesión usando la cuenta Microsoft asociada con tu suscripción de Azure.

1. Si se te solicita elegir un recurso de Language, selecciona la siguiente configuración:

    - **Azure Directory**: El directorio de Azure que contiene tu suscripción.
    - **Azure subscription**: Tu suscripción de Azure.
    - **Resource type**: Language.
    - **Language resource**: El recurso de Azure AI Language que creaste anteriormente.

    Si <u>no</u> se te solicita elegir un recurso de lenguaje, puede ser porque tienes múltiples recursos de Language en tu suscripción; en cuyo caso:

    1. En la barra en la parte superior de la página, selecciona el botón **Settings (&#9881;)**.
    2. En la página **Settings**, visualiza la pestaña **Resources**.
    3. Selecciona el recurso de lenguaje que acabas de crear y haz clic en **Switch resource**.
    4. En la parte superior de la página, haz clic en **Language Studio** para regresar a la página de inicio de Language Studio

1. En la parte superior del portal, en el menú **Create new**, selecciona **Conversational language understanding**.

1. En el cuadro de diálogo **Create a project**, en la página **Enter basic information**, ingresa los siguientes detalles y luego selecciona **Next**:
    - **Name**: `Clock`
    - **Utterances primary language**: English
    - **Enable multiple languages in project?**: *No seleccionado*
    - **Description**: `Natural language clock`

1. En la página **Review and finish**, selecciona **Create**.

### Crear intenciones

Lo primero que haremos en el nuevo proyecto es definir algunas intenciones. El modelo finalmente predecirá cuál de estas intenciones está solicitando un usuario cuando envía una expresión de lenguaje natural.

> **Tip**: Cuando trabajes en tu proyecto, si se muestran algunos consejos, léelos y selecciona **Got it** para descartarlos, o selecciona **Skip all**.

1. En la página **Schema definition**, en la pestaña **Intents**, selecciona **&#65291; Add** para agregar una nueva intención llamada `GetTime`.
1. Verifica que la intención **GetTime** esté listada (junto con la intención predeterminada **None**). Luego agrega las siguientes intenciones adicionales:
    - `GetDay`
    - `GetDate`

### Etiquetar cada intención con expresiones de ejemplo

Para ayudar al modelo a predecir qué intención está solicitando un usuario, debes etiquetar cada intención con algunas expresiones de ejemplo.

1. En el panel de la izquierda, selecciona la página **Data Labeling**.

> **Tip**: Puedes expandir el panel con el icono **>>** para ver los nombres de las páginas, y ocultarlo nuevamente con el icono **<<**.

1. Selecciona la nueva intención **GetTime** e ingresa la expresión `what is the time?`. Esto agrega la expresión como entrada de ejemplo para la intención.
1. Agrega las siguientes expresiones adicionales para la intención **GetTime**:
    - `what's the time?`
    - `what time is it?`
    - `tell me the time`

    > **NOTA**
    > Para agregar una nueva expresión, escribe la expresión en el cuadro de texto junto a la intención y luego presiona ENTER.

1. Selecciona la intención **GetDay** y agrega las siguientes expresiones como entrada de ejemplo para esa intención:
    - `what day is it?`
    - `what's the day?`
    - `what is the day today?`
    - `what day of the week is it?`

1. Selecciona la intención **GetDate** y agrega las siguientes expresiones para ella:
    - `what date is it?`
    - `what's the date?`
    - `what is the date today?`
    - `what's today's date?`

1. Después de que hayas agregado expresiones para cada una de tus intenciones, selecciona **Save changes**.

### Entrenar y probar el modelo

Ahora que has agregado algunas intenciones, entrenemos el modelo de lenguaje y veamos si puede predecirlas correctamente a partir de la entrada del usuario.

1. En el panel de la izquierda, selecciona **Training jobs**. Luego selecciona **+ Start a training job**.

1. En el cuadro de diálogo **Start a training job**, selecciona la opción para entrenar un nuevo modelo, nómbralo `Clock`. Selecciona el modo **Standard training** y las opciones predeterminadas de **Data splitting**.

1. Para comenzar el proceso de entrenar tu modelo, selecciona **Train**.

1. Cuando el entrenamiento se complete (lo que puede tomar varios minutos) el **Status** del trabajo cambiará a **Training succeeded**.

1. Selecciona la página **Model performance**, y luego selecciona el modelo **Clock**. Revisa las métricas de evaluación generales y por intención (*precisión*, *recall*, y *puntuación F1*) y la *matriz de confusión* generada por la evaluación que se realizó durante el entrenamiento (nota que debido al pequeño número de expresiones de ejemplo, es posible que no todas las intenciones estén incluidas en los resultados).

    > **NOTA**
    > Para aprender más sobre las métricas de evaluación, consulta la [documentación](https://learn.microsoft.com/es-es/azure/ai-services/language-service/conversational-language-understanding/concepts/evaluation-metrics)

1. Ve a la página **Deploying a model**, luego selecciona **Add deployment**.

1. En el cuadro de diálogo **Add deployment**, selecciona **Create a new deployment name**, y luego ingresa `production`.

1. Selecciona el modelo **Clock** en el campo **Model** luego selecciona **Deploy**. La implementación puede tomar algo de tiempo.

1. Cuando el modelo haya sido implementado, selecciona la página **Testing deployments**, luego selecciona la implementación **production** en el campo **Deployment name**.

1. Ingresa el siguiente texto en el cuadro de texto vacío, y luego selecciona **Run the test**:

    `what's the time now?`

    Revisa el resultado que se devuelve, notando que incluye la intención predicha (que debería ser **GetTime**) y una puntuación de confianza que indica la probabilidad que el modelo calculó para la intención predicha. La pestaña JSON muestra la confianza comparativa para cada intención potencial (la que tiene la puntuación de confianza más alta es la intención predicha)

1. Limpia el cuadro de texto, y luego ejecuta otra prueba con el siguiente texto:

    `tell me the time`

    Nuevamente, revisa la intención predicha y la puntuación de confianza.

1. Prueba el siguiente texto:

    `what's the day today?`

    Esperemos que el modelo prediga la intención **GetDay**.

## Agregar entidades

Hasta ahora has definido algunas expresiones simples que se mapean a intenciones. La mayoría de las aplicaciones reales incluyen expresiones más complejas de las cuales se deben extraer entidades de datos específicas para obtener más contexto para la intención.

### Agregar una entidad aprendida

El tipo más común de entidad es una entidad *aprendida*, en la que el modelo aprende a identificar valores de entidad basándose en ejemplos.

1. En Language Studio, regresa a la página **Schema definition** y luego en la pestaña **Entities**, selecciona **&#65291; Add** para agregar una nueva entidad.

1. En el cuadro de diálogo **Add an entity**, ingresa el nombre de entidad `Location` y asegúrate de que la pestaña **Learned** esté seleccionada. Luego selecciona **Add entity**.

1. Después de que se haya creado la entidad **Location**, regresa a la página **Data labeling**.
1. Selecciona la intención **GetTime** e ingresa la siguiente nueva expresión de ejemplo:

    `what time is it in London?`

1. Cuando se haya agregado la expresión, selecciona la palabra **London**, y en la lista desplegable que aparece, selecciona **Location** para indicar que "London" es un ejemplo de una ubicación.

1. Agrega otra expresión de ejemplo para la intención **GetTime**:

    `Tell me the time in Paris?`

1. Cuando se haya agregado la expresión, selecciona la palabra **Paris**, y mapeala a la entidad **Location**.

1. Agrega otra expresión de ejemplo para la intención **GetTime**:

    `what's the time in New York?`

1. Cuando se haya agregado la expresión, selecciona las palabras **New York**, y mapealas a la entidad **Location**.

1. Selecciona **Save changes** para guardar las nuevas expresiones.

### Agregar una entidad de *lista*

En algunos casos, los valores válidos para una entidad pueden restringirse a una lista de términos y sinónimos específicos; lo que puede ayudar a la aplicación a identificar instancias de la entidad en expresiones.

1. En Language Studio, regresa a la página **Schema definition** y luego en la pestaña **Entities**, selecciona **&#65291; Add** para agregar una nueva entidad.

1. En el cuadro de diálogo **Add an entity**, ingresa el nombre de entidad `Weekday` y selecciona la pestaña de entidad **List**. Luego selecciona **Add entity**.

1. En la página para la entidad **Weekday**, en la sección **Learned**, asegúrate de que **Not required** esté seleccionado. Luego, en la sección **List**, selecciona **&#65291; Add new list**. Luego ingresa el siguiente valor y sinónimo y selecciona **Save**:

    | List key | synonyms|
    |-------------------|---------|
    | `Sunday` | `Sun` |

    > **NOTA**
    > Para ingresar los campos de la nueva lista, inserta el valor `Sunday` en el campo de texto, luego haz clic en el campo donde se muestra 'Type in value and press enter...', ingresa los sinónimos y presiona ENTER.

1. Repite el paso anterior para agregar los siguientes componentes de lista:

    | Value | synonyms|
    |-------------------|---------|
    | `Monday` | `Mon` |
    | `Tuesday` | `Tue, Tues` |
    | `Wednesday` | `Wed, Weds` |
    | `Thursday` | `Thur, Thurs` |
    | `Friday` | `Fri` |
    | `Saturday` | `Sat` |

1. Después de agregar y guardar los valores de la lista, regresa a la página **Data labeling**.
1. Selecciona la intención **GetDate** e ingresa la siguiente nueva expresión de ejemplo:

    `what date was it on Saturday?`

1. Cuando se haya agregado la expresión, selecciona la palabra ***Saturday***, y en la lista desplegable que aparece, selecciona **Weekday**.

1. Agrega otra expresión de ejemplo para la intención **GetDate**:

    `what date will it be on Friday?`

1. Cuando se haya agregado la expresión, mapea **Friday** a la entidad **Weekday**.

1. Agrega otra expresión de ejemplo para la intención **GetDate**:

    `what will the date be on Thurs?`

1. Cuando se haya agregado la expresión, mapea **Thurs** a la entidad **Weekday**.

1. selecciona **Save changes** para guardar las nuevas expresiones.

### Agregar una entidad *prebuilt*

El servicio Azure AI Language proporciona un conjunto de entidades *prebuilt* que se usan comúnmente en aplicaciones conversacionales.

1. En Language Studio, regresa a la página **Schema definition** y luego en la pestaña **Entities**, selecciona **&#65291; Add** para agregar a una nueva entidad.

1. En el cuadro de diálogo **Add an entity**, ingresa el nombre de entidad `Date` y selecciona la pestaña de entidad **Prebuilt**. Luego selecciona **Add entity**.

1. En la página para la entidad **Date**, en la sección **Learned**, asegúrate de que **Not required** esté seleccionado. Luego, en la sección **Prebuilt**, selecciona **&#65291; Add new prebuilt**.

1. En la lista **Select prebuilt**, selecciona **DateTime** y luego selecciona **Save**.
1. Después de agregar la entidad prebuilt, regresa a la página **Data labeling**
1. Selecciona la intención **GetDay** e ingresa la siguiente nueva expresión de ejemplo:

    `what day was 01/01/1901?`

1. Cuando se haya agregado la expresión, selecciona ***01/01/1901***, y en la lista desplegable que aparece, selecciona **Date**.

1. Agrega otra expresión de ejemplo para la intención **GetDay**:

    `what day will it be on Dec 31st 2099?`

1. Cuando se haya agregado la expresión, mapea **Dec 31st 2099** a la entidad **Date**.

1. Selecciona **Save changes** para guardar las nuevas expresiones.

### Reentrenar el modelo

Ahora que has modificado el esquema, necesitas reentrenar y reprobar el modelo.

1. En la página **Training jobs**, selecciona **Start a training job**.

1. En el cuadro de diálogo **Start a training job**, selecciona **overwrite an existing model** y especifica el modelo **Clock**. Selecciona **Train** para entrenar el modelo. Si se solicita, confirma que deseas sobrescribir el modelo existente.

1. Cuando el entrenamiento se complete el **Status** del trabajo se actualizará a **Training succeeded**.

1. Selecciona la página **Model performance** y luego selecciona el modelo **Clock**. Revisa las métricas de evaluación (*precisión*, *recall*, y *puntuación F1*) y la *matriz de confusión* generada por la evaluación que se realizó durante el entrenamiento (nota que debido al pequeño número de expresiones de ejemplo, es posible que no todas las intenciones estén incluidas en los resultados).

1. En la página **Deploying a model**, selecciona **Add deployment**.

1. En el cuadro de diálogo **Add deployment**, selecciona **Override an existing deployment name**, y luego selecciona **production**.

1. Selecciona el modelo **Clock** en el campo **Model** y luego selecciona **Deploy** para implementarlo. Esto puede tomar algo de tiempo.

1. Cuando el modelo esté implementado, en la página **Testing deployments**, selecciona la implementación **production** bajo el campo **Deployment name**, y luego pruébalo con el siguiente texto:

    `what's the time in Edinburgh?`

1. Revisa el resultado que se devuelve, que debería predecir la intención **GetTime** y una entidad **Location** con el valor de texto "Edinburgh".

1. Intenta probar las siguientes expresiones:

    `what time is it in Tokyo?`

    `what date is it on Friday?`

    `what's the date on Weds?`

    `what day was 01/01/2020?`

    `what day will Mar 7th 2030 be?`

## Usar el modelo desde una aplicación cliente

En un proyecto real, refinarías iterativamente intenciones y entidades, reentrenarías y reprobarías hasta que estés satisfecho con el rendimiento predictivo. Luego, cuando lo hayas probado y estés satisfecho con su rendimiento predictivo, puedes usarlo en una aplicación cliente llamando a su interfaz REST o a un SDK específico del runtime.

### Prepararse para desarrollar una aplicación en Cloud Shell

Desarrollarás tu aplicación de comprensión de lenguaje usando Cloud Shell en el portal de Azure. Los archivos de código para tu aplicación han sido proporcionados en un repositorio de GitHub.

1. En el Portal de Azure, usa el botón **[\>_]** a la derecha de la barra de búsqueda en la parte superior de la página para crear un nuevo Cloud Shell en el portal de Azure, seleccionando un entorno de ***PowerShell***. El cloud shell proporciona una interfaz de línea de comandos en un panel en la parte inferior del portal de Azure.

    > **Nota**: Si anteriormente creaste un cloud shell que usa un entorno *Bash*, cámbialo a ***PowerShell***.

1. En la barra de herramientas del cloud shell, en el menú **Settings**, selecciona **Go to Classic version** (esto es necesario para usar el editor de código).

    **<font color="red">Asegúrate de haber cambiado a la versión clásica del cloud shell antes de continuar.</font>**

1. En el panel de PowerShell, ingresa los siguientes comandos para clonar el repositorio de GitHub para este ejercicio:

    ```bash
    rm -r mslearn-ai-language -f
    git clone https://github.com/microsoftlearning/mslearn-ai-language
    ```

    > **Tip**: A medida que pegues comandos en el cloudshell, la salida puede ocupar una gran parte del búfer de pantalla. Puedes limpiar la pantalla ingresando el comando `cls` para que sea más fácil enfocarse en cada tarea.

1. Después de que se haya clonado el repositorio, navega a la carpeta que contiene los archivos de código de la aplicación:  

    ```bash
    cd mslearn-ai-language/Labfiles/03-language/Python/clock-client
    ```

### Configurar tu aplicación

1. En el panel de la línea de comandos, ejecuta el siguiente comando para ver los archivos de código en la carpeta **clock-client**:

    ```bash
    ls -a -l
    ```

    Los archivos incluyen un archito de configuración (**.env**) y un archito de código (**clock-client.py**).

1. Crea un entorno virtual de Python e instala el paquete del SDK de Azure AI Conversations y otros paquetes requeridos ejecutando el siguiente comando:

    ```bash
    python -m venv labenv
    ./labenv/bin/Activate.ps1
    pip install -r requirements.txt azure-ai-language-conversations==1.1.0
    ```

1. Ingresa el siguiente comando para editar el archito de configuración:

    ```bash
    code .env
    ```

    El archito se abre en un editor de código.

1. Actualiza los valores de configuración para incluir el **endpoint** y una **key** del recurso de Azure Language que creaste (disponible en la página **Keys and Endpoint** de tu recurso de Azure AI Language en el portal de Azure).
1. Después de haber reemplazado los marcadores de posición, dentro del editor de código, usa el comando **CTRL+S** o **Clic derecho > Guardar** para guardar tus cambios y luego usa el comando **CTRL+Q** o **Clic derecho > Salir** para cerrar el editor de código mientras mantienes abierta la línea de comandos del cloud shell.

### Agregar código a la aplicación

1. Ingresa el siguiente comando para editar el archito de código de la aplicación:

    ```bash
    code clock-client.py
    ```

1. Revisa el código existente. Agregarás código para trabajar con el SDK de AI Language Conversations.

    > **Tip**: A medida que agregues código al archito de código, asegúrate de mantener la indentación correcta.

1. En la parte superior del archito de código, debajo de las referencias de espacios de nombres existentes, encuentra el comentario **Import namespaces** y agrega el siguiente código para importar los espacios de nombres que necesitarás para usar el SDK de AI Language Conversations:

    ```python
   # Import namespaces
   from azure.core.credentials import AzureKeyCredential
   from azure.ai.language.conversations import ConversationAnalysisClient
    ```

1. En la función **main**, nota que el código para cargar el endpoint de predicción y la key desde el archito de configuración ya ha sido proporcionado. Luego encuentra el comentario **Create a client for the Language service model** y agrega el siguiente código para crear un cliente de análisis de conversación para tu servicio de AI Language:

    ```python
   # Create a client for the Language service model
   client = ConversationAnalysisClient(
        ls_prediction_endpoint, AzureKeyCredential(ls_prediction_key))
    ```

1. Nota que el código en la función **main** solicita entrada del usuario hasta que el usuario ingresa "quit". Dentro de este bucle, encuentra el comentario **Call the Language service model to get intent and entities** y agrega el siguiente código:

    ```python
   # Call the Language service model to get intent and entities
   cls_project = 'Clock'
   deployment_slot = 'production'

   with client:
        query = userText
        result = client.analyze_conversation(
            task={
                "kind": "Conversation",
                "analysisInput": {
                    "conversationItem": {
                        "participantId": "1",
                        "id": "1",
                        "modality": "text",
                        "language": "en",
                        "text": query
                    },
                    "isLoggingEnabled": False
                },
                "parameters": {
                    "projectName": cls_project,
                    "deploymentName": deployment_slot,
                    "verbose": True
                }
            }
        )

   top_intent = result["result"]["prediction"]["topIntent"]
   entities = result["result"]["prediction"]["entities"]

   print("view top intent:")
   print("\ttop intent: {}".format(result["result"]["prediction"]["topIntent"]))
   print("\tcategory: {}".format(result["result"]["prediction"]["intents"][0]["category"]))
   print("\tconfidence score: {}\n".format(result["result"]["prediction"]["intents"][0]["confidenceScore"]))

   print("view entities:")
   for entity in entities:
        print("\tcategory: {}".format(entity["category"]))
        print("\ttext: {}".format(entity["text"]))
        print("\tconfidence score: {}".format(entity["confidenceScore"]))

   print("query: {}".format(result["result"]["query"]))
    ```

    La llamada al modelo de comprensión conversacional devuelve una predicción/resultado, que incluye la intención principal (más probable) así como cualquier entidad que se detectó en la expresión de entrada. Tu aplicación cliente debe ahora usar esa predicción para determinar y realizar la acción apropiada.

1. Encuentra el comentario **Apply the appropriate action**, y agrega el siguiente código, que verifica las intenciones soportadas por la aplicación (**GetTime**, **GetDate**, y **GetDay**) y determina si se han detectado entidades relevantes, antes de llamar a una función existente para producir una respuesta apropiada.

    ```python
   # Apply the appropriate action
   if top_intent == 'GetTime':
        location = 'local'
        # Check for entities
        if len(entities) > 0:
            # Check for a location entity
            for entity in entities:
                if 'Location' == entity["category"]:
                    # ML entities are strings, get the first one
                    location = entity["text"]
        # Get the time for the specified location
        print(GetTime(location))

   elif top_intent == 'GetDay':
        date_string = date.today().strftime("%m/%d/%Y")
        # Check for entities
        if len(entities) > 0:
            # Check for a Date entity
            for entity in entities:
                if 'Date' == entity["category"]:
                    # Regex entities are strings, get the first one
                    date_string = entity["text"]
        # Get the day for the specified date
        print(GetDay(date_string))

   elif top_intent == 'GetDate':
        day = 'today'
        # Check for entities
        if len(entities) > 0:
            # Check for a Weekday entity
            for entity in entities:
                if 'Weekday' == entity["category"]:
                # List entities are lists
                    day = entity["text"]
        # Get the date for the specified day
        print(GetDate(day))

   else:
        # Some other intent (for example, "None") was predicted
        print('Intenta preguntarme por la hora, el día o la fecha.')
    ```

1. Guarda tus cambios (CTRL+S), luego ingresa el siguiente comando para ejecutar el programa (puedes maximizar el panel del cloud shell y redimensionar los paneles para ver más texto en el panel de la línea de comandos):

    ```bash
    python clock-client.py
    ```

1. Cuando se te solicite, ingresa expresiones para probar la aplicación. Por ejemplo, intenta:

    *Hola*

    *¿Qué hora es?*

    *¿Qué hora es en Londres?*

    *¿Cuál es la fecha?*

    *¿Qué fecha es el domingo?*

    *¿Qué día es hoy?*

    *¿Qué día es 01/01/2025?*

    > **Nota**: La lógica en la aplicación es deliberadamente simple y tiene una serie de limitaciones. Por ejemplo, al obtener la hora, solo se admite un conjunto restringido de ciudades y se ignora el horario de verano. El objetivo es ver un ejemplo de un patrón típico para usar Language Service en el que tu aplicación debe:
    > 1. Conectarse a un endpoint de predicción.
    > 2. Enviar una expresión para obtener una predicción.
    > 3. Implementar lógica para responder apropiadamente a la intención predicha y las entidades.

1. Cuando hayas terminado de probar, ingresa *quit*.

## Limpiar recursos

Si has terminado de explorar el servicio Azure AI Language, puedes eliminar los recursos que creaste en este ejercicio. Así es cómo:

1. Cierra el panel de Azure cloud shell
1. En el portal de Azure, navega al recurso de Azure AI Language que creaste en este laboratorio.
1. En la página del recurso, selecciona **Delete** y sigue las instrucciones para eliminar el recurso.

## Más información

Para aprender más sobre comprensión de lenguaje conversacional en Azure AI Language, consulta la [documentación de Azure AI Language](https://learn.microsoft.com/es-es/azure/ai-services/language-service/conversational-language-understanding/overview).
