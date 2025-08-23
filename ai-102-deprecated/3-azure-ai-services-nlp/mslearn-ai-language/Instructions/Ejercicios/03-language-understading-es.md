---
Laboratorio:
title: "Creación de un modelo de comprensión del lenguaje con el servicio Azure AI Language"
módulo: 'Módulo 5 - Crear soluciones de comprensión del lenguaje'
---

# Crear un modelo de comprensión del lenguaje con el servicio de lenguaje

> **NOTA**
> La característica de comprensión del lenguaje conversacional del servicio de lenguaje de Azure AI se encuentra actualmente en versión preliminar y está sujeta a cambios. En algunos casos, el entrenamiento del modelo puede fallar: si esto sucede, inténtelo de nuevo. 

El servicio Azure AI Language permite definir un  modelo de *comprensión del lenguaje conversacional* que las aplicaciones pueden usar para interpretar la entrada de lenguaje natural de los usuarios, predecir la *intención* de los usuarios  (lo que quieren lograr) e identificar las *entidades* a las que se debe aplicar la intención.

Por ejemplo, se podría esperar que un modelo de lenguaje conversacional para una aplicación de reloj procese entradas como:

*¿Qué hora es en Londres?*

Este tipo de entrada es un ejemplo de una *expresión* (algo que un usuario podría decir o escribir), para la cual la *intención* deseada  es obtener la hora en una ubicación específica (una *entidad*); en este caso, Londres.

> **NOTA**
> La tarea de un modelo de lenguaje conversacional es predecir la intención del usuario e identificar las entidades a las que se aplica la intención. Es <u>not</u> el trabajo de un modelo de lenguaje conversacional realizar realmente las acciones necesarias para satisfacer la intención. Por ejemplo, una aplicación de reloj puede usar un modelo de lenguaje conversacional para discernir que el usuario desea saber la hora en Londres; Sin embargo, la propia aplicación cliente debe implementar la lógica para determinar la hora correcta y presentarla al usuario.

## Aprovisionamiento de un  recurso de *Azure AI Language*

Si aún no tiene uno en su suscripción, deberá aprovisionar un  recurso **Azure AI Language Service** en su suscripción de Azure.

1. Abra Azure Portal en "https://portal.azure.com" e inicie sesión con la cuenta de Microsoft asociada a su suscripción de Azure.
1. En el campo de búsqueda de la parte superior, busque **Servicios de IA de Azure**. A continuación, en los resultados, seleccione **Crear** en **Servicio de idioma**.
1. Seleccione **Continuar para crear su recurso**.
1. Aprovisione el recurso con la siguiente configuración:
    - **Subscription**: *Su suscripción de Azure*.
    - **Resource group**: *Elija o cree un grupo de recursos*.
    - **Region**: *Elija una de las siguientes regiones*\*
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
    - **Name**: *Introduzca un nombre único*.
    - **Pricing tier**: seleccione **F0** (*gratis*) o **S** (*estándar*) si F no está disponible.
    - **responsible AI Notice**: De acuerdo.
2. Seleccione **Revisar + crear** y, a continuación, seleccione **Crear** para aprovisionar el recurso.
3. Espere a que se complete la implementación y, a continuación, vaya al recurso implementado.
4. Vea la  página **Claves y punto de conexión**. Necesitará la información de esta página más adelante en el ejercicio.

## Crear un proyecto de comprensión del lenguaje conversacional

Ahora que ha creado un recurso de creación, puede usarlo para crear un proyecto de comprensión del lenguaje conversacional.

1. En una nueva pestaña del navegador, abra el portal de Azure AI Language Studio en `https://language.cognitive.azure.com/` e inicie sesión con la cuenta de Microsoft asociada a su suscripción de Azure.

1. Si se le pide que elija un recurso de idioma, seleccione la siguiente configuración:

    - **Azure Directory**: el directorio de Azure que contiene su suscripción.
    - **Azure subscription**: Su suscripción de Azure.
    - **Resource type**: Idioma.
    - **Language resource**: el recurso de idioma de Azure AI que creó anteriormente.

    Si se le  solicita <u>not</u> que  elija un recurso de idioma, puede deberse a que tiene varios recursos de idioma en su suscripción; en cuyo caso:

    1. En la barra de la parte superior de la página, seleccione la opción **Configuración (&#9881;)Botón** .
    2. En la  página **Configuración**, vea la  pestaña **Recursos**.
    3. Seleccione el recurso de idioma que acaba de crear y haga clic en **Cambiar recurso**.
    4. En la parte superior de la página, haz clic en **Language Studio** para volver a la página de inicio de Language Studio

1. En la parte superior del portal, en el  menú **Crear nuevo**, seleccione **Conversational language understanding**.

1. En el  cuadro de diálogo **Crear un proyecto**, en la  página **Introducir información básica**, introduzca los siguientes detalles y, a continuación, seleccione **Siguiente**:
    - **Name**: `Clock`
    - **Utterances primary language**: English
    - **Enable multiple languages in project?**: *Unselected*
    - **Description**: `Natural language clock`

1. En la  página **Revisar y finalizar**, seleccione **Crear**.

### Crear intenciones

Lo primero que haremos en el nuevo proyecto es definir algunas intenciones. En última instancia, el modelo predecirá cuál de estas intenciones solicita un usuario al enviar una expresión de lenguaje natural.

> [!TIP]
> Cuando trabajes en tu proyecto, si se muestran algunos consejos, léelos y selecciona **Entendido** para descartarlos, o selecciona **Omitir todo**.

1. En la  página **Definición de esquema**, en la  pestaña **Intents**, seleccione **&#65291; Agregar** para agregar una nueva intención denominada 'GetTime'.
1. Verifica que la  intent **GetTime** aparezca en la lista (junto con la intent **None** predeterminada  ). A continuación, agregue las siguientes intenciones adicionales:
    - `GetDay`
    - `GetDate`

### Etiquete cada intención con expresiones de ejemplo

Para ayudar al modelo a predecir qué intención está solicitando un usuario, debe etiquetar cada intención con algunas expresiones de ejemplo.

1. En el panel de la izquierda, seleccione la  página **Etiquetado de datos**.

    > [!TIP]
    > Puede expandir el panel con el  icono **>>** para ver los nombres de las páginas y volver a ocultarlo con el  icono **<<**.

1. Seleccione la nueva  intención **GetTime** e introduzca la expresión `what is the time?`. Esto agrega la expresión como entrada de ejemplo para la intención.
1. Agregue las siguientes expresiones adicionales para el  intent **GetTime**:
    - `what's the time?`
    - `what time is it?`
    - `tell me the time`

    > [!NOTE]
    > Para agregar una nueva expresión, escriba la expresión en el cuadro de texto junto a la intención y, a continuación, presione ENTRAR. 

1. Seleccione la  intent **GetDay** y agregue las siguientes expresiones como entrada de ejemplo para esa intención:
    - `what day is it?`
    - `what's the day?`
    - `what is the day today?`
    - `what day of the week is it?`

1. Seleccione la  intent **GetDate** y agregue las siguientes expresiones para ella:
    - `what date is it?`
    - `what's the date?`
    - `what is the date today?`
    - `what's today's date?`

1. Una vez que hayas agregado expresiones para cada una de tus intenciones, selecciona **Guardar cambios**.

### Entrenar y probar el modelo

Ahora que ha agregado algunas intenciones, entrenemos el modelo de lenguaje y veamos si puede predecirlas correctamente a partir de la entrada del usuario.

1. En el panel de la izquierda, seleccione **Training jobs**. A continuación, seleccione **+ Start a training job**.

1. En el  cuadro de diálogo **Start a training job**, seleccione la opción para entrenar un nuevo modelo, asígnele el nombre 'Reloj'. Seleccione  el modo de **Standard training** y las opciones predeterminadas de **Data splitting**. 

1. Para comenzar el proceso de entrenamiento de su modelo, seleccione **Train**.

1. Cuando se complete la capacitación (lo que puede tardar varios minutos), el trabajo **Status** cambiará a **Training succeeded**.

1. Seleccione la  página **Model performance** y, a continuación, seleccione el  modelo **Clock**. Revise las métricas de evaluación general y por intención (*precisión*, *recuperación* y *puntuación F1*) y la *matriz de confusión* generada por la evaluación que se realizó durante el entrenamiento (tenga en cuenta que, debido al pequeño número de expresiones de muestra, es posible que no todas las intenciones se incluyan en los resultados).

    > [!NOTE]
    > Para obtener más información sobre las métricas de evaluación, consulte la [documentación](https://learn.microsoft.com/azure/ai-services/language-service/conversational-language-understanding/concepts/evaluation-metrics)

1. Vaya a la  página **Deploying a model** y, a continuación, seleccione **Add deployment**.

1. En el cuadro de  diálogo **Add deployment**, seleccione **Create a new deployment name** y, a continuación, escriba `production`.

1. Seleccione el  modelo de **Clock** en el  campo **Model** y luego seleccione **Deploy**. La implementación puede tardar algún tiempo.

1. Cuando se haya implementado el modelo, seleccione la  página **Testing deployments** y, a continuación, seleccione la  implementación de **production** en el  campo **Deployment name**.

1. Escriba el siguiente texto en el cuadro de texto vacío y, a continuación, seleccione **Run the test**:

    `what's the time now?`

    Revise el resultado que se devuelve, teniendo en cuenta que incluye la intención predicha (que debe ser **GetTime**) y una puntuación de confianza que indica la probabilidad que el modelo calculó para la intención predicha. La pestaña JSON muestra la confianza comparativa para cada intención potencial (la que tiene la puntuación de confianza más alta es la intención predicha)

1. Borre el cuadro de texto y, a continuación, ejecute otra prueba con el siguiente texto:

    `tell me the time`

    De nuevo, revise la intención predicha y la puntuación de confianza.

1. Pruebe con el siguiente texto:

    `what's the day today?`

    Con suerte, el modelo predice la  intención **GetDay**.

## Agregar entidades

Hasta ahora, ha definido algunas expresiones simples que se asignan a intenciones. La mayoría de las aplicaciones reales incluyen expresiones más complejas de las que se deben extraer entidades de datos específicas para obtener más contexto para la intención.

### Agregar una entidad aprendida

El tipo más común de entidad es una  entidad *aprendida*, en la que el modelo aprende a identificar los valores de la entidad basándose en ejemplos.

1. En Language Studio, vuelva a la  página **Definición de esquema** y, a continuación, en la  pestaña **Entidades**, seleccione **&#65291; Agregar** para agregar una nueva entidad.

1. En el cuadro de  diálogo **Agregar una entidad**, ingrese el nombre de la entidad 'Ubicación' y asegúrese de que la  pestaña **Aprendido** esté seleccionada. A continuación, seleccione **Agregar entidad**.

1. Una vez creada la  entidad **Ubicación**, vuelva a la  página **Etiquetado de datos**.
1. Seleccione la  intent **GetTime** e introduzca la siguiente expresión de ejemplo nueva:

    `what time is it in London?`

1. Cuando se haya agregado la expresión, seleccione la palabra **Londres** y, en la lista desplegable que aparece, seleccione **Ubicación** para indicar que "Londres" es un ejemplo de una ubicación.

1. Agregue otro ejemplo de expresión para la  intención **GetTime**:

    `Tell me the time in Paris?`

1. Cuando se haya agregado la expresión, seleccione la palabra **Paris** y asígnela a la  entidad **Location**.

1. Agregue otro ejemplo de expresión para la  intención **GetTime**:

    `what's the time in New York?`

1. Cuando se haya agregado la expresión, seleccione las palabras **Nueva York** y asígnelas a la  entidad **Location**.

1. Seleccione **Guardar cambios** para guardar las nuevas expresiones.

### Agregar una  entidad *lista*

En algunos casos, los valores válidos para una entidad pueden restringirse a una lista de términos y sinónimos específicos; lo que puede ayudar a la aplicación a identificar instancias de la entidad en las expresiones.

1. En Language Studio, vuelva a la  página **Definición de esquema** y, a continuación, en la  pestaña **Entidades**, seleccione **&#65291; Agregar** para agregar una nueva entidad.

1. En el  cuadro de diálogo **Agregar una entidad**, ingrese el nombre de la entidad `Weekday` y seleccione la pestaña de entidad **Lista**. A continuación, seleccione **Agregar entidad**.

1. En la página de la  entidad **Día de la semana**, en la  sección **Aprendido**, asegúrese de que  **No es necesario** esté seleccionado. A continuación, en la  sección **Lista**, seleccione **&#65291; Añadir nueva lista**. A continuación, introduzca el siguiente valor y sinónimo y seleccione **Guardar**:

    | List key | synonyms|
    |-------------------|---------|
    | `Sunday` | `Sun` |

    > [!NOTE]
    > Para ingresar a los campos de la nueva lista, inserte el valor `Sunday` en el campo de texto, luego haga clic en el campo donde `Escriba valor y presione enter...` , introduzca los sinónimos y pulse INTRO.

1. Repita el paso anterior para agregar los siguientes componentes de la lista:

    | Value | synonyms|
    |-------------------|---------|
    | `Monday` | `Mon` |
    | `Tuesday` | `Tue, Tues` |
    | `Wednesday` | `Wed, Weds` |
    | `Thursday` | `Thur, Thurs` |
    | `Friday` | `Fri` |
    | `Saturday` | `Sat` |

1. Después de agregar y guardar los valores de la lista, vuelva a la  página **Etiquetado de datos**.
1. Seleccione la  intención **GetDate** e introduzca la siguiente expresión de ejemplo nueva:

    `what date was it on Saturday?`

1. Cuando se haya agregado la expresión, seleccione la palabra ***Sábado*** y, en la lista desplegable que aparece, seleccione **Día de la semana**.

1. Agregue otro ejemplo de expresión para la  intención **GetDate**:

    `what date will it be on Friday?`

1. Cuando se haya agregado la expresión, asigne **Friday** a la  entidad **Weekday**.

1. Agregue otro ejemplo de expresión para la  intención **GetDate**:

    `what will the date be on Thurs?`

1. Cuando se haya agregado la expresión, asigne **Thurs** a la  entidad **Weekday**.

1. Seleccione **Guardar cambios** para guardar las nuevas expresiones.

### Agregar una  entidad *preconstruida*

El servicio Azure AI Language proporciona un conjunto de  entidades *prebuilt* que se usan normalmente en aplicaciones conversacionales.

1. En Language Studio, vuelva a la  página **Definición de esquema** y, a continuación, en la  pestaña **Entidades**, seleccione **&#65291; Agregar** para agregar una nueva entidad.

1. En el cuadro de  diálogo **Agregar una entidad**, ingrese el nombre de la entidad `Date` y seleccione la pestaña de entidad **Preconstruida**. A continuación, seleccione **Agregar entidad**.

1. En la página de la  entidad **Fecha**, en la  sección **Aprendido**, asegúrese de que  **No es necesario** esté seleccionado. A continuación, en la  sección **Prefabricado**, seleccione **&#65291; Agregue nuevo precompilado**.

1. En la  lista **Seleccionar precompilado**, seleccione **DateTime** y luego seleccione **Guardar**.
1. Después de agregar la entidad precompilada, regrese a la  página **Etiquetado de datos**
1. Selecciona la  intent **GetDay** e ingresa la siguiente expresión de ejemplo nueva:

    `what day was 01/01/1901?`

1. Cuando se haya agregado la expresión, seleccione ***01/01/1901*** y, en la lista desplegable que aparece, seleccione **Fecha**.

1. Agregue otro ejemplo de expresión para la  intención **GetDay**:

    `what day will it be on Dec 31st 2099?`

1. Cuando se haya agregado la expresión, asigne **31 de diciembre de 2099** a la  entidad **Date**.

1. Seleccione **Guardar cambios** para guardar las nuevas expresiones.

### Volver a entrenar el modelo

Ahora que ha modificado el esquema, debe volver a entrenar y probar el modelo.

1. En la  página **Trabajos de formación**, seleccione **Iniciar un trabajo de formación**.

1. En el cuadro de  diálogo **Iniciar un trabajo de entrenamiento**, seleccione **sobrescribir un modelo existente** y especifique el  modelo **Reloj**. Seleccione **Entrenar** para entrenar el modelo. Si se le solicita, confirme que desea sobrescribir el modelo existente.

1. Cuando se complete la capacitación, el trabajo **Estado** se actualizará a **Capacitación exitosa**.

1. Seleccione la  página **Rendimiento del modelo** y luego seleccione el  modelo **Reloj**. Revise las métricas de evaluación (*precisión*, *recuperación* y *puntuación F1*) y la *matriz de confusión* generada por la evaluación que se realizó durante el entrenamiento (tenga en cuenta que, debido al pequeño número de expresiones de muestra, es posible que no todas las intenciones se incluyan en los resultados).

1. En la  página **Implementación de un modelo**, seleccione **Agregar implementación**.

1. En el  cuadro de diálogo **Agregar implementación**, seleccione **Reemplazar un nombre de implementación existente** y, a continuación, seleccione **producción**.

1. Seleccione el  modelo **Reloj** en el  campo **Modelo** y luego seleccione **Implementar** para implementarlo. Esto puede llevar algún tiempo.

1. Cuando se implemente el modelo, en la  página **Implementaciones de prueba**, seleccione la  implementación de **producción** en el  campo **Nombre de implementación** y, a continuación, pruébela con el siguiente texto:

    `what's the time in Edinburgh?`

1. Revise el resultado que se devuelve, que debería predecir la  intención **GetTime** y una  entidad **Location** con el valor de texto "Edimburgo".

1. Intente probar las siguientes expresiones:

    `what time is it in Tokyo?`

    `what date is it on Friday?`

    `what's the date on Weds?`

    `what day was 01/01/2020?`

    `what day will Mar 7th 2030 be?`

## Usar el modelo de una aplicación cliente

En un proyecto real, refinaría de forma iterativa las intenciones y las entidades, volvería a entrenar y volvería a probar hasta que esté satisfecho con el rendimiento predictivo. Luego, cuando lo hayas probado y estés satisfecho con su rendimiento predictivo, puedes usarlo en una aplicación cliente llamando a su interfaz REST o a un SDK específico del entorno de ejecución.

### Preparación para desarrollar una aplicación en Visual Studio Code

Desarrollará la aplicación de comprensión del lenguaje mediante Visual Studio Code. Los archivos de código de la aplicación se han proporcionado en un repositorio de GitHub.

> [!TIP]
> Si ya ha clonado el  repositorio **mslearn-ai-language**, ábralo en el código de Visual Studio. De lo contrario, siga estos pasos para clonarlo en su entorno de desarrollo.

1. Inicie Visual Studio Code.
2. Abra la paleta (SHIFT+CTRL+P) y ejecute un  comando **Git: Clone** para clonar el  repositorio `https://github.com/MicrosoftLearning/mslearn-ai-language` en una carpeta local (no importa qué carpeta).
3. Cuando se haya clonado el repositorio, abra la carpeta en Visual Studio Code.

    > [!NOTE]
    > Si Visual Studio Code le muestra un mensaje emergente para pedirle que confíe en el código que está abriendo, haga clic en la opción **Sí, confío en los autores** en la ventana emergente.

4. Espere mientras se instalan archivos adicionales para admitir los proyectos de código de C# en el repositorio.

    > [!NOTE]
    > Si se le solicita que agregue los activos necesarios para compilar y depurar, seleccione **Ahora no**.

### Configura tu aplicación

Se han proporcionado aplicaciones para C# y Python, así como un archivo de texto de ejemplo que usará para probar el resumen. Ambas aplicaciones cuentan con la misma funcionalidad. En primer lugar, completará algunas partes clave de la aplicación para permitirle usar el recurso de Azure AI Language.

1. En Visual Studio Code, en el  panel **Explorer**, vaya a la  carpeta **Labfiles/03-language** y expanda la  carpeta **CSharp** o **Python** en función de su preferencia de idioma y de la  carpeta **clock-client** que contenga. Cada carpeta contiene los archivos específicos del idioma de una aplicación en la que va a integrar la funcionalidad de respuesta a preguntas del lenguaje de Azure AI.
2. Haga clic con el botón derecho en la  carpeta **clock-client** que contiene sus archivos de código y abra un terminal integrado. A continuación, instale el paquete del SDK de comprensión del lenguaje conversacional de Azure AI Language ejecutando el comando adecuado para su preferencia de idioma:

    **C#**:

    ```
    dotnet add package Azure.AI.Language.Conversations --version 1.1.0
    ```

    **Python**:

    ```
    pip install azure-ai-language-conversations
    ```

3. En el  panel **Explorer**, en la  carpeta **clock-client**,  abra el archivo de configuración de su idioma preferido

    - **C#**: appsettings.json
    - **Python**: .env

4. Actualice los valores de configuración para incluir el **punto de conexión** y una **clave** del recurso de lenguaje de Azure que creó (disponible en la  página **Claves y punto de conexión** del recurso de lenguaje de IA de Azure en Azure Portal).
5. Guarde el archivo de configuración.

### Agregar código a la aplicación

Ahora está listo para agregar el código necesario para importar las bibliotecas de SDK necesarias, establecer una conexión autenticada con el proyecto implementado y enviar preguntas.

1. Tenga en cuenta que la  carpeta **clock-client** contiene un archivo de código para la aplicación cliente:

    - **C#**: Program.cs
    - **Python**: clock-client.py

    Abra el archivo de código y en la parte superior, debajo de las referencias de espacio de nombres existentes, busque el comentario **Importar espacios de nombres**. A continuación, en este comentario, agregue el siguiente código específico del idioma para importar los espacios de nombres que necesitará para usar el SDK de Text Analytics:

    **C#**: Programs.cs

    ```c#
    // import namespaces
    using Azure;
    using Azure.AI.Language.Conversations;
    ```

    **Python**: clock-client.py

    ```python
    # Import namespaces
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.language.conversations import ConversationAnalysisClient
    ```

2. En la  función **Main**, tenga en cuenta que ya se ha proporcionado el código para cargar el punto final de predicción y la clave desde el archivo de configuración. A continuación, busque el comentario **Crear un cliente para el modelo de servicio de lenguaje** y agregue el siguiente código para crear un cliente de predicción para la aplicación de servicio de lenguaje:

    **C#**: Programs.cs

    ```c#
    // Create a client for the Language service model
    Uri endpoint = new Uri(predictionEndpoint);
    AzureKeyCredential credential = new AzureKeyCredential(predictionKey);

    ConversationAnalysisClient client = new ConversationAnalysisClient(endpoint, credential);
    ```

    **Python**: clock-client.py

    ```python
    # Create a client for the Language service model
    client = ConversationAnalysisClient(
        ls_prediction_endpoint, AzureKeyCredential(ls_prediction_key))
    ```
1. Tenga en cuenta que el código de la  función **Main** solicita la entrada del usuario hasta que el usuario ingresa "salir". Dentro de este bucle, busque el comentario **Llame al modelo de servicio de lenguaje para obtener la intención y las entidades** y agregue el código siguiente:

    **C#**: Programs.cs

    ```c#
    // Call the Language service model to get intent and entities
    var projectName = "Clock";
    var deploymentName = "production";
    var data = new
    {
        analysisInput = new
        {
            conversationItem = new
            {
                text = userText,
                id = "1",
                participantId = "1",
            }
        },
        parameters = new
        {
            projectName,
            deploymentName,
            // Use Utf16CodeUnit for strings in .NET.
            stringIndexType = "Utf16CodeUnit",
        },
        kind = "Conversation",
    };
    // Send request
    Response response = await client.AnalyzeConversationAsync(RequestContent.Create(data));
    dynamic conversationalTaskResult = response.Content.ToDynamicFromJson(JsonPropertyNames.CamelCase);
    dynamic conversationPrediction = conversationalTaskResult.Result.Prediction;   
    var options = new JsonSerializerOptions { WriteIndented = true };
    Console.WriteLine(JsonSerializer.Serialize(conversationalTaskResult, options));
    Console.WriteLine("--------------------\n");
    Console.WriteLine(userText);
    var topIntent = "";
    if (conversationPrediction.Intents[0].ConfidenceScore > 0.5)
    {
        topIntent = conversationPrediction.TopIntent;
    }
    ```

    **Python**: clock-client.py

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

La llamada al modelo de servicio de lenguaje devuelve una predicción o un resultado, que incluye la intención principal (más probable), así como las entidades que se detectaron en la expresión de entrada. La aplicación cliente ahora debe usar esa predicción para determinar y realizar la acción adecuada.

1. Busque el comentario **Aplicar la acción adecuada** y agregue el siguiente código, que comprueba las intenciones admitidas por la aplicación (**GetTime**, **GetDate** y **GetDay**) y determina si se han detectado entidades relevantes, antes de llamar a una función existente para producir una respuesta adecuada.

    **C#**: Programs.cs

    ```c#
    // Apply the appropriate action
    switch (topIntent)
    {
        case "GetTime":
            var location = "local";           
            // Check for a location entity
            foreach (dynamic entity in conversationPrediction.Entities)
            {
                if (entity.Category == "Location")
                {
                    //Console.WriteLine($"Location Confidence: {entity.ConfidenceScore}");
                    location = entity.Text;
                }
            }
            // Get the time for the specified location
            string timeResponse = GetTime(location);
            Console.WriteLine(timeResponse);
            break;
        case "GetDay":
            var date = DateTime.Today.ToShortDateString();            
            // Check for a Date entity
            foreach (dynamic entity in conversationPrediction.Entities)
            {
                if (entity.Category == "Date")
                {
                    //Console.WriteLine($"Location Confidence: {entity.ConfidenceScore}");
                    date = entity.Text;
                }
            }            
            // Get the day for the specified date
            string dayResponse = GetDay(date);
            Console.WriteLine(dayResponse);
            break;
        case "GetDate":
            var day = DateTime.Today.DayOfWeek.ToString();
            // Check for entities            
            // Check for a Weekday entity
            foreach (dynamic entity in conversationPrediction.Entities)
            {
                if (entity.Category == "Weekday")
                {
                    //Console.WriteLine($"Location Confidence: {entity.ConfidenceScore}");
                    day = entity.Text;
                }
            }          
            // Get the date for the specified day
            string dateResponse = GetDate(day);
            Console.WriteLine(dateResponse);
            break;
        default:
            // Some other intent (for example, "None") was predicted
            Console.WriteLine("Try asking me for the time, the day, or the date.");
            break;
    }
    ```

    **Python**: clock-client.py

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
        print('Try asking me for the time, the day, or the date.')
    ```

1. Guarde los cambios y regrese al terminal integrado para la  carpeta **clock-client**,  e ingrese el siguiente comando para ejecutar el programa:

    - **C#**: `dotnet run`
    - **Python**: `python clock-client.py`

    > [!TIP]
    > Puede usar el  icono **Maximizar tamaño del panel** (**^**) en la barra de herramientas del terminal para ver más texto de la consola.

1. Cuando se le solicite, escriba expresiones para probar la aplicación. Por ejemplo, pruebe lo siguiente:

    *Hello*

    *What time is it?*

    *What's the time in London?*

    *What's the date?*

    *What date is Sunday?*

    *What day is it?*

    *What day is 01/01/2025?*

    > [!NOTE]
    > La lógica de la aplicación es deliberadamente simple y tiene una serie de limitaciones. Por ejemplo, al obtener la hora, solo se admite un conjunto restringido de ciudades y se omite el horario de verano. El objetivo es ver un ejemplo de un patrón típico para usar Language Service en el que la aplicación debe:
    > 1. Conéctese a un punto de conexión de predicción.
    > 2. Envíe una expresión para obtener una predicción.
    > 3. Implemente la lógica para responder adecuadamente a la intención y las entidades predichas.

1. Cuando haya terminado la prueba, ingrese *quit*.

## Limpiar recursos

Si ha terminado de explorar el servicio de lenguaje de IA de Azure, puede eliminar los recursos que creó en este ejercicio. A continuación, te explicamos cómo hacerlo:

1. Abra Azure Portal en `https://portal.azure.com` e inicie sesión con la cuenta de Microsoft asociada a su suscripción de Azure.
2. Vaya al recurso de Azure AI Language que creó en este laboratorio.
3. En la página del recurso, seleccione **Eliminar** y siga las instrucciones para eliminar el recurso.

## Más información

Para obtener más información sobre la comprensión del lenguaje conversacional en Azure AI Language, consulte la [Documentación de Azure AI Language](https://learn.microsoft.com/azure/ai-services/language-service/conversational-language-understanding/overview).

