---
lab:
    title: "Crear una aplicación de chat de IA generativa"
    description: "Aprenda a utilizar el SDK de Azure AI Foundry para construir una aplicación que se conecte a su proyecto y converse con un modelo de lenguaje."
---

# Crear una aplicación de chat de IA generativa

En este ejercicio, utilizará el SDK de Python de Azure AI Foundry para crear una aplicación de chat simple que se conecte a un proyecto y converse con un modelo de lenguaje.

> **Nota**: Este ejercicio está basado en software de SDK en versión preliminar, que puede estar sujeto a cambios. Donde sea necesario, hemos utilizado versiones específicas de paquetes, que pueden no reflejar las últimas versiones disponibles. Puede experimentar comportamientos inesperados, advertencias o errores.

Aunque este ejercicio se basa en el SDK de Python de Azure AI Foundry, puede desarrollar aplicaciones de chat de IA utilizando múltiples SDK específicos de lenguaje, incluyendo:

-   [Azure AI Projects para Python](https://pypi.org/project/azure-ai-projects)
-   [Azure AI Projects para Microsoft .NET](https://www.nuget.org/packages/Azure.AI.Projects)
-   [Azure AI Projects para JavaScript](https://www.npmjs.com/package/@azure/ai-projects)

Este ejercicio toma aproximadamente **40** minutos.

## Implementar un modelo en un proyecto de Azure AI Foundry

Comencemos implementando un modelo en un proyecto de Azure AI Foundry.

1. En un navegador web, abra el [portal de Azure AI Foundry](https://ai.azure.com) en `https://ai.azure.com` e inicie sesión con sus credenciales de Azure. Cierre cualquier sugerencia o panel de inicio rápido que aparezca la primera vez que inicie sesión y, si es necesario, utilice el logotipo de **Azure AI Foundry** en la parte superior izquierda para navegar a la página de inicio, que se verá similar a la siguiente imagen (cierre el panel **Help** si está abierto):

    ![Captura de pantalla del portal de Azure AI Foundry.](./media/ai-foundry-home.png)

1. En la página de inicio, en la sección **Explore models and capabilities**, busque el modelo `gpt-4o`, que utilizaremos en nuestro proyecto.
1. En los resultados de búsqueda, seleccione el modelo **gpt-4o** para ver sus detalles y luego, en la parte superior de la página del modelo, seleccione **Use this model**.
1. Cuando se le solicite crear un proyecto, ingrese un nombre válido para su proyecto y expanda **Advanced options**.
1. Seleccione **Customize** y especifique las siguientes configuraciones para su proyecto:

    - **Azure AI Foundry resource**: _Un nombre válido para su recurso de Azure AI Foundry_
    - **Subscription**: _Su suscripción de Azure_
    - **Resource group**: _Cree o seleccione un grupo de recursos_
    - **Region**: \*Seleccione cualquier **ubicación admitida por AI Services\***\*

    > \* Algunos recursos de Azure AI están limitados por cuotas regionales de modelos. En caso de que se exceda un límite de cuota más adelante en el ejercicio, es posible que necesite crear otro recurso en una región diferente.

1. Seleccione **Create** y espere a que se cree su proyecto. Si se le solicita, implemente el modelo gpt-4o utilizando el tipo de implementación **Global standard** y personalice los detalles de la implementación para establecer un **Tokens per minute rate limit** de 50K (o el máximo disponible si es menor que 50K).

    > **Nota**: Reducir el TPM ayuda a evitar el uso excesivo de la cuota disponible en la suscripción que está utilizando. 50,000 TPM deberían ser suficientes para los datos utilizados en este ejercicio. Si su cuota disponible es menor, podrá completar el ejercicio, pero puede experimentar errores si se excede el límite de tasa.

1. Cuando se cree su proyecto, el playground de chat se abrirá automáticamente para que pueda probar su modelo.
1. En el panel **Setup**, observe el nombre de su implementación de modelo, que debería ser **gpt-4o**. Puede confirmarlo viendo la implementación en la página **Models and endpoints** (abra esa página en el panel de navegación izquierdo).
1. En el panel de navegación izquierdo, seleccione **Overview** para ver la página principal de su proyecto, que se verá así:

    ![Captura de pantalla de la página de resumen de un proyecto de Azure AI Foundry.](./media/ai-foundry-project.png)

## Crear una aplicación cliente para conversar con el modelo

Ahora que ha implementado un modelo, puede utilizar los SDKs de Azure AI Foundry y Azure OpenAI para desarrollar una aplicación que converse con él.

### Preparar la configuración de la aplicación

1. En el portal de Azure AI Foundry, vea la página **Overview** de su proyecto.
1. En el área **Endpoints and keys**, asegúrese de que la biblioteca **Azure AI Foundry** esté seleccionada y vea el **Azure AI Foundry project endpoint**. Utilizará este endpoint para conectarse a su proyecto y modelo en una aplicación cliente.

    > **Nota**: ¡También puede utilizar el endpoint de Azure OpenAI!

1. Abra una nueva pestaña del navegador (manteniendo el portal de Azure AI Foundry abierto en la pestaña existente). Luego, en la nueva pestaña, navegue al [portal de Azure](https://portal.azure.com) en `https://portal.azure.com`; iniciando sesión con sus credenciales de Azure si se le solicita.

    Cierre cualquier notificación de bienvenida para ver la página de inicio del portal de Azure.

1. Utilice el botón **[\>_]** a la derecha de la barra de búsqueda en la parte superior de la página para crear un nuevo Cloud Shell en el portal de Azure, seleccionando un entorno **_PowerShell_** sin almacenamiento en su suscripción.

    El cloud shell proporciona una interfaz de línea de comandos en un panel en la parte inferior del portal de Azure. Puede redimensionar o maximizar este panel para facilitar su uso.

    > **Nota**: Si ha creado previamente un cloud shell que utiliza un entorno _Bash_, cámbielo a **_PowerShell_**.

1. En la barra de herramientas del cloud shell, en el menú **Settings**, seleccione **Go to Classic version** (esto es necesario para utilizar el editor de código).

    **<font color="red">Asegúrese de haber cambiado a la versión clásica del cloud shell antes de continuar.</font>**

1. En el panel del cloud shell, ingrese los siguientes comandos para clonar el repositorio de GitHub que contiene los archivos de código para este ejercicio (escriba el comando o cópielo al portapapeles y luego haga clic derecho en la línea de comandos y pegue como texto sin formato):

    ```bash
    rm -r mslearn-ai-foundry -f
    git clone https://github.com/microsoftlearning/mslearn-ai-studio mslearn-ai-foundry
    ```

    > **Consejo**: A medida que ingresa comandos en el cloud shell, la salida puede ocupar una gran cantidad del búfer de pantalla. Puede limpiar la pantalla ingresando el comando `cls` para facilitar el enfoque en cada tarea.

1. Después de clonar el repositorio, navegue a la carpeta que contiene los archivos de código de la aplicación de chat y visualícelos:

    ```bash
    cd mslearn-ai-foundry/labfiles/chat-app/python
    ls -a -l
    ```

    La carpeta contiene un archivo de código, un archivo de configuración para los ajustes de la aplicación y un archivo que define el tiempo de ejecución del proyecto y los requisitos de paquetes.

1. En el panel de línea de comandos del cloud shell, ingrese el siguiente comando para instalar las bibliotecas que utilizará:

    ```bash
    python -m venv labenv
    ./labenv/bin/Activate.ps1
    pip install -r requirements.txt azure-identity azure-ai-projects openai
    ```

1. Ingrese el siguiente comando para editar el archivo de configuración proporcionado:

    ```bash
    code .env
    ```

    El archivo se abrirá en un editor de código.

1. En el archivo de código, reemplace el marcador de posición **your_project_endpoint** con el **Azure AI Foundry project endpoint** de su proyecto (copiado de la página **Overview** en el portal de Azure AI Foundry); y el marcador de posición **your_model_deployment** con el nombre de su implementación del modelo gpt-4.
1. Después de reemplazar los marcadores de posición, dentro del editor de código, utilice el comando **CTRL+S** o **Clic derecho > Guardar** para guardar los cambios y luego utilice el comando **CTRL+Q** o **Clic derecho > Salir** para cerrar el editor de código mientras mantiene abierta la línea de comandos del cloud shell.

### Escribir código para conectarse a su proyecto y conversar con su modelo

> **Consejo**: A medida que agrega código, asegúrese de mantener la indentación correcta.

1. Ingrese el siguiente comando para editar el archivo de código proporcionado:

    ```bash
    code chat-app.py
    ```

1. En el archivo de código, observe las declaraciones existentes que se han agregado en la parte superior del archivo para importar los espacios de nombres necesarios del SDK. Luego, encuentre el comentario **Add references** y agregue el siguiente código para hacer referencia a los espacios de nombres en las bibliotecas que instaló previamente:

    ```python
    # Add references
    from azure.identity import DefaultAzureCredential
    from azure.ai.projects import AIProjectClient
    from openai import AzureOpenAI
    ```

1. En la función **main**, bajo el comentario **Get configuration settings**, observe que el código carga los valores de la cadena de conexión del proyecto y el nombre de la implementación del modelo que definió en el archivo de configuración.
1. Encuentre el comentario **Initialize the project client** y agregue el siguiente código para conectarse a su proyecto de Azure AI Foundry:

    > **Consejo**: Tenga cuidado de mantener el nivel de indentación correcto para su código.

    ```python
    # Initialize the project client
    project_client = AIProjectClient(
            credential=DefaultAzureCredential(
                exclude_environment_credential=True,
                exclude_managed_identity_credential=True
            ),
            endpoint=project_endpoint,
        )
    ```

1. Encuentre el comentario **Get a chat client** y agregue el siguiente código para crear un objeto cliente para conversar con un modelo:

    ```python
    # Get a chat client
    openai_client = project_client.get_openai_client(api_version="2024-10-21")
    ```

1. Encuentre el comentario **Initialize prompt with system message** y agregue el siguiente código para inicializar una colección de mensajes con un prompt del sistema.

    ```python
    # Initialize prompt with system message
    prompt = [
            {"role": "system", "content": "You are a helpful AI assistant that answers questions."}
        ]
    ```

1. Observe que el código incluye un bucle para permitir que un usuario ingrese un prompt hasta que ingrese "quit". Luego, en la sección del bucle, encuentre el comentario **Get a chat completion** y agregue el siguiente código para agregar la entrada del usuario al prompt, recuperar la finalización de su modelo y agregar la finalización al prompt (para retener el historial de chat para futuras iteraciones):

    ```python
    # Get a chat completion
    prompt.append({"role": "user", "content": input_text})
    response = openai_client.chat.completions.create(
            model=model_deployment,
            messages=prompt)
    completion = response.choices[0].message.content
    print(completion)
    prompt.append({"role": "assistant", "content": completion})
    ```

1. Utilice el comando **CTRL+S** para guardar los cambios en el archivo de código.

### Iniciar sesión en Azure y ejecutar la aplicación

1. En el panel de línea de comandos del cloud shell, ingrese el siguiente comando para iniciar sesión en Azure.

    ```bash
    az login
    ```

    **<font color="red">Debe iniciar sesión en Azure, incluso si la sesión del cloud shell ya está autenticada.</font>**

    > **Nota**: En la mayoría de los escenarios, solo usar _az login_ será suficiente. Sin embargo, si tiene suscripciones en múltiples inquilinos, es posible que deba especificar el inquilino utilizando el parámetro _--tenant_. Consulte [Iniciar sesión en Azure interactivamente usando la CLI de Azure](https://learn.microsoft.com/cli/azure/authenticate-azure-cli-interactively) para más detalles.

1. Cuando se le solicite, siga las instrucciones para abrir la página de inicio de sesión en una nueva pestaña e ingrese el código de autenticación proporcionado y sus credenciales de Azure. Luego complete el proceso de inicio de sesión en la línea de comandos, seleccionando la suscripción que contiene su hub de Azure AI Foundry si se le solicita.
1. Después de iniciar sesión, ingrese el siguiente comando para ejecutar la aplicación:

    ```bash
    python chat-app.py
    ```

1. Cuando se le solicite, ingrese una pregunta, como `¿Cuál es el animal más rápido de la Tierra?` y revise la respuesta de su modelo de IA generativa.
1. Pruebe algunas preguntas de seguimiento, como `¿Dónde puedo ver uno?` o `¿Están en peligro de extinción?`. La conversación debería continuar, utilizando el historial de chat como contexto para cada iteración.
1. Cuando termine, ingrese `quit` para salir del programa.

> **Consejo**: Si la aplicación falla porque se excede el límite de tasa, espere unos segundos e intente nuevamente. Si no hay suficiente cuota disponible en su suscripción, el modelo puede no responder.

## Resumen

En este ejercicio, utilizó el SDK de Azure AI Foundry para crear una aplicación cliente para un modelo de IA generativa que implementó en un proyecto de Azure AI Foundry.

## Limpieza

Si ha terminado de explorar el portal de Azure AI Foundry, debe eliminar los recursos que ha creado en este ejercicio para evitar incurrir en costos innecesarios de Azure.

1. Abra el [portal de Azure](https://portal.azure.com) y vea el contenido del grupo de recursos donde implementó los recursos utilizados en este ejercicio.
1. En la barra de herramientas, seleccione **Delete resource group**.
1. Ingrese el nombre del grupo de recursos y confirme que desea eliminarlo.
