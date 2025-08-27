---
lab:
    title: "Crear una aplicación de IA generativa que use tus propios datos"
    description: "Aprende a usar el modelo de Generación Aumentada por Recuperación (RAG) para construir una aplicación de chat que fundamenta prompts usando tus propios datos."
---

# Crear una aplicación de IA generativa que use tus propios datos

La Generación Aumentada por Recuperación (RAG) es una técnica utilizada para construir aplicaciones que integran datos de fuentes personalizadas en un prompt para un modelo de IA generativa. RAG es un patrón comúnmente usado para desarrollar aplicaciones de IA generativa - aplicaciones basadas en chat que usan un modelo de lenguaje para interpretar entradas y generar respuestas apropiadas.

En este ejercicio, usarás Azure AI Foundry para integrar datos personalizados en una solución de IA generativa.

> **Nota**: El código en este ejercicio está basado en software SDK en versión preliminar, que puede estar sujeto a cambios. Donde sea necesario, hemos usado versiones específicas de paquetes; que pueden no reflejar las últimas versiones disponibles. Puedes experimentar comportamientos inesperados, advertencias o errores.

Aunque este ejercicio está basado en el SDK de Python para Azure OpenAI, puedes desarrollar aplicaciones de chat de IA usando múltiples SDKs específicos de lenguaje, incluyendo:

-   [OpenAI para Python](https://pypi.org/project/openai/)
-   [Azure Open AI para Microsoft .NET](https://www.nuget.org/packages/Azure.AI.OpenAI)
-   [Azure OpenAI para TypeScript](https://www.npmjs.com/package/@azure/openai)

Este ejercicio toma aproximadamente **45** minutos.

## Crear un hub y proyecto de Azure AI Foundry

Las características de Azure AI Foundry que usaremos en este ejercicio requieren un proyecto basado en un recurso _hub_ de Azure AI Foundry.

1. En un navegador web, abre el [portal de Azure AI Foundry](https://ai.azure.com) en `https://ai.azure.com` e inicia sesión con tus credenciales de Azure. Cierra cualquier sugerencia o panel de inicio rápido que aparezca la primera vez que inicies sesión y, si es necesario, usa el logo de **Azure AI Foundry** en la parte superior izquierda para navegar a la página de inicio, que se verá similar a la siguiente imagen (cierra el panel **Help** si está abierto):

    ![Captura de pantalla del portal de Azure AI Foundry.](./media/ai-foundry-home.png)

1. En el navegador, navega a `https://ai.azure.com/managementCenter/allResources` y selecciona **Create new**. Luego elige la opción para crear un nuevo recurso **AI hub**.
1. En el asistente **Create a project**, ingresa un nombre válido para tu proyecto y selecciona la opción para crear un nuevo hub. Luego usa el enlace **Rename hub** para especificar un nombre válido para tu nuevo hub, expande **Advanced options** y especifica las siguientes configuraciones para tu proyecto:

    - **Subscription**: _Tu suscripción de Azure_
    - **Resource group**: _Crea o selecciona un grupo de recursos_
    - **Region**: East US 2 o Sweden Central (_En caso de que se exceda un límite de cuota más adelante en el ejercicio, es posible que necesites crear otro recurso en una región diferente._)

    > **Nota**: Si estás trabajando en una suscripción de Azure donde se usan políticas para restringir nombres de recursos permitidos, es posible que necesites usar el enlace en la parte inferior del cuadro de diálogo **Create a new project** para crear el hub usando el portal de Azure.
    > **Consejo**: Si el botón **Create** sigue deshabilitado, asegúrate de renombrar tu hub con un valor alfanumérico único.

1. Espera a que se cree tu proyecto y luego navega a tu proyecto.

## Implementar modelos

Necesitas dos modelos para implementar tu solución:

-   Un modelo de _embedding_ para vectorizar datos de texto para indexación y procesamiento eficiente.
-   Un modelo que pueda generar respuestas en lenguaje natural a preguntas basadas en tus datos.

1. En el portal de Azure AI Foundry, en tu proyecto, en el panel de navegación izquierdo, bajo **My assets**, selecciona la página **Models + endpoints**.
1. Crea una nueva implementación del modelo **text-embedding-ada-002** con las siguientes configuraciones seleccionando **Customize** en el asistente Deploy model:

    - **Deployment name**: _Un nombre válido para tu implementación de modelo_
    - **Deployment type**: Global Standard
    - **Model version**: _Selecciona la versión predeterminada_
    - **Connected AI resource**: _Selecciona el recurso creado previamente_
    - **Tokens per Minute Rate Limit (thousands)**: 50K _(o el máximo disponible en tu suscripción si es menor que 50K)_
    - **Content filter**: DefaultV2

    > **Nota**: Si la ubicación actual de tu recurso de IA no tiene cuota disponible para el modelo que deseas implementar, se te pedirá que elijas una ubicación diferente donde se creará un nuevo recurso de IA y se conectará a tu proyecto.

1. Regresa a la página **Models + endpoints** y repite los pasos anteriores para implementar un modelo **gpt-4o** usando una implementación **Global Standard** de la versión más reciente con un límite de tasa TPM de **50K** (o el máximo disponible en tu suscripción si es menor que 50K).

    > **Nota**: Reducir los Tokens Por Minuto (TPM) ayuda a evitar el uso excesivo de la cuota disponible en la suscripción que estás usando. 50,000 TPM es suficiente para los datos usados en este ejercicio.

## Agregar datos a tu proyecto

Los datos para tu aplicación consisten en un conjunto de folletos de viaje en formato PDF de la agencia de viajes ficticia _Margie's Travel_. Vamos a agregarlos al proyecto.

1. En una nueva pestaña del navegador, descarga el [archivo zip de folletos](https://github.com/MicrosoftLearning/mslearn-ai-studio/raw/main/data/brochures.zip) desde `https://github.com/MicrosoftLearning/mslearn-ai-studio/raw/main/data/brochures.zip` y extráelo a una carpeta llamada **brochures** en tu sistema de archivos local.
1. En el portal de Azure AI Foundry, en tu proyecto, en el panel de navegación izquierdo, bajo **My assets**, selecciona la página **Data + indexes**.
1. Selecciona **+ New data**.
1. En el asistente **Add your data**, expande el menú desplegable para seleccionar **Upload files/folders**.
1. Selecciona **Upload folder** y sube la carpeta **brochures**. Espera hasta que todos los archivos en la carpeta estén listados.
1. Selecciona **Next** y establece el nombre de los datos como `brochures`.
1. Espera a que la carpeta se suba y observa que contiene varios archivos .pdf.

## Crear un índice para tus datos

Ahora que has agregado una fuente de datos a tu proyecto, puedes usarla para crear un índice en tu recurso de Azure AI Search.

1. En el portal de Azure AI Foundry, en tu proyecto, en el panel de navegación izquierdo, bajo **My assets**, selecciona la página **Data + indexes**.
1. En la pestaña **Indexes**, agrega un nuevo índice con las siguientes configuraciones:

    - **Source location**:
        - **Data source**: Data in Azure AI Foundry
            - _Selecciona la fuente de datos **brochures**_
    - **Index configuration**:

        - **Select Azure AI Search service**: _Crea un nuevo recurso de Azure AI Search con las siguientes configuraciones_:

            - **Subscription**: _Tu suscripción de Azure_
            - **Resource group**: _El mismo grupo de recursos que tu hub de IA_
            - **Service name**: _Un nombre válido para tu recurso de AI Search_
            - **Location**: _La misma ubicación que tu hub de IA_
            - **Pricing tier**: Basic

            Espera a que se cree el recurso de AI Search. Luego regresa a Azure AI Foundry y termina de configurar el índice seleccionando **Connect other Azure AI Search resource** y agregando una conexión al recurso de AI Search que acabas de crear.

        - **Vector index**: `brochures-index`
        - **Virtual machine**: Auto select

    - **Search settings**:
        - **Vector settings**: Add vector search to this search resource
        - **Azure OpenAI connection**: _Selecciona el recurso predeterminado de Azure OpenAI para tu hub._
        - **Embedding model**: text-embedding-ada-002
        - **Embedding model deployment**: _Tu implementación del modelo_ text-embedding-ada-002

1. Crea el índice vectorial y espera a que se complete el proceso de indexación, lo que puede tardar un tiempo dependiendo de los recursos de computación disponibles en tu suscripción.

    La operación de creación de índice consiste en los siguientes trabajos:

    - Dividir, fragmentar y embeber los tokens de texto en tus datos de folletos.
    - Crear el índice de Azure AI Search.
    - Registrar el activo de índice.

    > **Consejo**: Mientras esperas que se cree el índice, ¿por qué no echas un vistazo a los folletos que descargaste para familiarizarte con su contenido?

## Probar el índice en el playground

Antes de usar tu índice en un prompt flow basado en RAG, verifiquemos que se puede usar para afectar las respuestas de IA generativa.

1. En el panel de navegación izquierdo, selecciona la página **Playgrounds** y abre el **Chat** playground.
1. En la página del Chat playground, en el panel Setup, asegúrate de que tu implementación del modelo **gpt-4o** esté seleccionada. Luego, en el panel principal de la sesión de chat, envía el prompt `¿Dónde puedo hospedarme en Nueva York?`
1. Revisa la respuesta, que debería ser una respuesta genérica del modelo sin datos del índice.
1. En el panel Setup, expande el campo **Add your data**, y luego agrega el índice de proyecto **brochures-index** y selecciona el tipo de búsqueda **hybrid (vector + keyword)**.

    > **Consejo**: En algunos casos, los índices recién creados pueden no estar disponibles de inmediato. Actualizar el navegador generalmente ayuda, pero si aún experimentas el problema de que no puede encontrar el índice, es posible que necesites esperar hasta que el índice sea reconocido.

1. Después de agregar el índice y reiniciar la sesión de chat, reenvía el prompt `¿Dónde puedo hospedarme en Nueva York?`
1. Revisa la respuesta, que debería basarse en datos del índice.

## Crear una aplicación cliente RAG

Ahora que tienes un índice funcional, puedes usar el SDK de Azure OpenAI para implementar el patrón RAG en una aplicación cliente. Exploremos el código para lograrlo en un ejemplo simple.

### Preparar la configuración de la aplicación

1. Regresa a la pestaña del navegador que contiene el portal de Azure (manteniendo el portal de Azure AI Foundry abierto en la pestaña existente).
1. Usa el botón **[\>_]** a la derecha de la barra de búsqueda en la parte superior de la página para crear un nuevo Cloud Shell en el portal de Azure, seleccionando un entorno **_PowerShell_** sin almacenamiento en tu suscripción.

    El cloud shell proporciona una interfaz de línea de comandos en un panel en la parte inferior del portal de Azure. Puedes redimensionar o maximizar este panel para facilitar su uso.

    > **Nota**: Si has creado previamente un cloud shell que usa un entorno _Bash_, cámbialo a **_PowerShell_**.

1. En la barra de herramientas del cloud shell, en el menú **Settings**, selecciona **Go to Classic version** (esto es necesario para usar el editor de código).

    **<font color="red">Asegúrate de haber cambiado a la versión clásica del cloud shell antes de continuar.</font>**

1. En el panel del cloud shell, ingresa los siguientes comandos para clonar el repositorio de GitHub que contiene los archivos de código para este ejercicio (escribe el comando o cópialo al portapapeles y luego haz clic derecho en la línea de comandos y pega como texto sin formato):

    ```bash
    rm -r mslearn-ai-foundry -f
    git clone https://github.com/microsoftlearning/mslearn-ai-studio mslearn-ai-foundry
    ```

    > **Consejo**: A medida que pegas comandos en el cloud shell, la salida puede ocupar una gran cantidad del búfer de pantalla. Puedes limpiar la pantalla ingresando el comando `cls` para facilitar el enfoque en cada tarea.

1. Después de clonar el repositorio, navega a la carpeta que contiene los archivos de código de la aplicación de chat:

    ```bash
    cd mslearn-ai-foundry/labfiles/rag-app/python
    ```

1. En el panel de línea de comandos del cloud shell, ingresa el siguiente comando para instalar la biblioteca del SDK de OpenAI:

    ```bash
    python -m venv labenv
    ./labenv/bin/Activate.ps1
    pip install -r requirements.txt openai
    ```

1. Ingresa el siguiente comando para editar el archivo de configuración proporcionado:

    ```bash
    code .env
    ```

    El archivo se abrirá en un editor de código.

1. En el archivo de configuración, reemplaza los siguientes marcadores de posición:
    - **your_openai_endpoint**: El endpoint de Open AI de la página **Overview** de tu proyecto en el portal de Azure AI Foundry (asegúrate de seleccionar la pestaña de capacidad **Azure OpenAI**, no la de Azure AI Inference o Azure AI Services).
    - **your_openai_api_key** La clave API de Open AI de la página **Overview** de tu proyecto en el portal de Azure AI Foundry (asegúrate de seleccionar la pestaña de capacidad **Azure OpenAI**, no la de Azure AI Inference o Azure AI Services).
    - **your_chat_model**: El nombre que asignaste a tu implementación del modelo **gpt-4o**, de la página **Models + endpoints** en el portal de Azure AI Foundry (el nombre predeterminado es `gpt-4o`).
    - **your_embedding_model**: El nombre que asignaste a tu implementación del modelo **text-embedding-ada-002**, de la página **Models + endpoints** en el portal de Azure AI Foundry (el nombre predeterminado es `text-embedding-ada-002`).
    - **your_search_endpoint**: La URL para tu recurso de Azure AI Search. La encontrarás en el **Management center** en el portal de Azure AI Foundry.
    - **your_search_api_key**: La clave API para tu recurso de Azure AI Search. La encontrarás en el **Management center** en el portal de Azure AI Foundry.
    - **your_index**: Reemplaza con el nombre de tu índice de la página **Data + indexes** para tu proyecto en el portal de Azure AI Foundry (debería ser `brochures-index`).
1. Después de reemplazar los marcadores de posición, en el editor de código, usa el comando **CTRL+S** o **Clic derecho > Guardar** para guardar tus cambios y luego usa el comando **CTRL+Q** o **Clic derecho > Salir** para cerrar el editor de código mientras mantienes abierta la línea de comandos del cloud shell.

### Explorar código para implementar el patrón RAG

1. Ingresa el siguiente comando para editar el archivo de código proporcionado:

    ```bash
    code rag-app.py
    ```

1. Revisa el código en el archivo, notando que:

    - Crea un cliente de Azure OpenAI usando el endpoint, clave y modelo de chat.
    - Crea un mensaje de sistema adecuado para una solución de chat relacionada con viajes.
    - Envía un prompt (incluyendo el mensaje de sistema y un mensaje de usuario basado en la entrada del usuario) al cliente de Azure OpenAI, agregando:
        - Detalles de conexión para el índice de Azure AI Search a consultar.
        - Detalles del modelo de embedding a usar para vectorizar la consulta\*.
    - Muestra la respuesta del prompt fundamentado.
    - Agrega la respuesta al historial de chat.

    \* _La consulta para el índice de búsqueda se basa en el prompt, y se usa para encontrar texto relevante en los documentos indexados. Puedes usar una búsqueda basada en palabras clave que envíe la consulta como texto, pero usar una búsqueda basada en vectores puede ser más eficiente - de ahí el uso de un modelo de embedding para vectorizar el texto de la consulta antes de enviarlo._

1. Usa el comando **CTRL+Q** para cerrar el editor de código sin guardar cambios, mientras mantienes abierta la línea de comandos del cloud shell.

### Ejecutar la aplicación de chat

1. En el panel de línea de comandos del cloud shell, ingresa el siguiente comando para ejecutar la aplicación:

    ```bash
    python rag-app.py
    ```

1. Cuando se te solicite, ingresa una pregunta, como `¿A dónde debería ir de vacaciones para ver arquitectura?` y revisa la respuesta de tu modelo de IA generativa.

    Nota que la respuesta incluye referencias de fuente para indicar los datos indexados en los que se encontró la respuesta.

1. Prueba una pregunta de seguimiento, por ejemplo `¿Dónde puedo hospedarme allí?`

1. Cuando hayas terminado, ingresa `quit` para salir del programa. Luego cierra el panel del cloud shell.

## Limpieza

Para evitar costos innecesarios de Azure y uso de recursos, debes eliminar los recursos que implementaste en este ejercicio.

1. Si has terminado de explorar Azure AI Foundry, regresa al [portal de Azure](https://portal.azure.com) en `https://portal.azure.com` e inicia sesión usando tus credenciales de Azure si es necesario. Luego elimina los recursos en el grupo de recursos donde provisionaste tus recursos de Azure AI Search y Azure AI.
