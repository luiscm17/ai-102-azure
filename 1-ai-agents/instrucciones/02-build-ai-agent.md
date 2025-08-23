---
lab:
    title: "Desarrollar un agente de IA"
    description: "Utiliza el servicio Azure AI Agent para desarrollar un agente que use herramientas integradas."
---

# Desarrollar un agente de IA

En este ejercicio, usarás el servicio Azure AI Agent para crear un agente simple que analice datos y cree gráficos. El agente puede usar la herramienta integrada _Code Interpreter_ para generar dinámicamente cualquier código necesario para analizar datos.

> **Sugerencia**: El código utilizado en este ejercicio se basa en el SDK para Python de Azure AI Foundry. Puedes desarrollar soluciones similares utilizando los SDK para Microsoft .NET, JavaScript y Java. Consulta [Bibliotecas cliente del SDK de Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/how-to/develop/sdk-overview) para obtener más detalles.

Este ejercicio debería tomar aproximadamente **30** minutos en completarse.

> **Nota**: Algunas de las tecnologías utilizadas en este ejercicio están en versión preliminar o en desarrollo activo. Es posible que experimentes un comportamiento inesperado, advertencias o errores.

---

## Crear un proyecto de Azure AI Foundry

Comencemos creando un proyecto de Azure AI Foundry.

1. En un navegador web, abre el [portal de Azure AI Foundry](https://ai.azure.com) en `https://ai.azure.com` e inicia sesión con tus credenciales de Azure. Cierra cualquier sugerencia o panel de inicio rápido que se abra la primera vez que inicies sesión, y si es necesario usa el logo de **Azure AI Foundry** en la parte superior izquierda para navegar a la página de inicio, que se ve similar a la siguiente imagen (cierra el panel de **Help** si está abierto):

2. En la página de inicio, selecciona **Create an agent**.

3. Cuando se te pida que crees un proyecto, introduce un nombre válido para tu proyecto y expande **Advanced options**.

4. Confirma las siguientes configuraciones para tu proyecto:

    - **Azure AI Foundry resource**: _Un nombre válido para tu recurso de Azure AI Foundry_
    - **Subscription**: _Tu suscripción de Azure_
    - **Resource group**: _Crea o selecciona un grupo de recursos_
    - **Region**: \*Selecciona cualquier **AI Services supported location\***\*

    > \* Algunos recursos de Azure AI están restringidos por cuotas de modelo regionales. En caso de que se supere un límite de cuota más adelante en el ejercicio, existe la posibilidad de que necesites crear otro recurso en una región diferente.

5. Selecciona **Create** y espera a que se cree tu proyecto.

6. Si se te solicita, implementa un modelo **gpt-4o** usando la opción de implementación _Global Standard_ o _Standard_ (dependiendo de la disponibilidad de tu cuota).

    > **Nota**: Si la cuota está disponible, un modelo base GPT-4o puede implementarse automáticamente al crear tu Agente y proyecto.

7. Cuando tu proyecto se haya creado, el playground de Agentes se abrirá.

8. En el panel de navegación de la izquierda, selecciona **Overview** para ver la página principal de tu proyecto; que se ve así:

9. Copia los valores de **Azure AI Foundry project endpoint** en un bloc de notas, ya que los usarás para conectarte a tu proyecto en una aplicación cliente.

---

## Crear una aplicación cliente de agente

Ahora estás listo para crear una aplicación cliente que use un agente. Se te ha proporcionado algo de código en un repositorio de GitHub.

### Clonar el repositorio que contiene el código de la aplicación

1. Abre una nueva pestaña del navegador (manteniendo el portal de Azure AI Foundry abierto en la pestaña existente). Luego, en la nueva pestaña, navega al [portal de Azure](https://portal.azure.com) en `https://portal.azure.com`; iniciando sesión con tus credenciales de Azure si se te solicita.

    Cierra cualquier notificación de bienvenida para ver la página de inicio del portal de Azure.

2. Usa el botón **[\>\_]** a la derecha de la barra de búsqueda en la parte superior de la página para crear un nuevo Cloud Shell en el portal de Azure, seleccionando un entorno **_PowerShell_** sin almacenamiento en tu suscripción.

    El cloud shell proporciona una interfaz de línea de comandos en un panel en la parte inferior del portal de Azure. Puedes cambiar el tamaño o maximizar este panel para que sea más fácil trabajar en él.

    > **Nota**: Si has creado previamente un cloud shell que usa un entorno _Bash_, cámbialo a **_PowerShell_**.

3. En la barra de herramientas del cloud shell, en el menú **Settings**, selecciona **Go to Classic version** (esto es necesario para usar el editor de código).

    **\<font color="red"\>Asegúrate de haber cambiado a la versión clásica del cloud shell antes de continuar.\</font\>**

4. En el panel del cloud shell, ingresa los siguientes comandos para clonar el repositorio de GitHub que contiene los archivos de código para este ejercicio (escribe el comando, o cópialo al portapapeles y luego haz clic derecho en la línea de comandos y pégalo como texto sin formato):

    ```bash
    rm -r ai-agents -f
    git clone <https://github.com/MicrosoftLearning/mslearn-ai-agents> ai-agents
    ```

> **Sugerencia**: A medida que ingresas comandos en el cloudshell, la salida puede ocupar una gran cantidad del búfer de la pantalla y el cursor en la línea actual puede quedar oscurecido. Puedes limpiar la pantalla ingresando el comando `cls` para que sea más fácil concentrarse en cada tarea.

1. Ingresa el siguiente comando para cambiar el directorio de trabajo a la carpeta que contiene los archivos de código y listarlos todos.

    ```bash
    cd ai-agents/Labfiles/02-build-ai-agent/Python
    ls -a -l
    ```

Los archivos proporcionados incluyen código de la aplicación, configuraciones y datos.

### Configurar las configuraciones de la aplicación

1. En el panel de línea de comandos del cloud shell, ingresa el siguiente comando para instalar las librerías que usarás:

    ```bash
    python -m venv labenv
    ./labenv/bin/Activate.ps1
    pip install -r requirements.txt azure-ai-projects
    ```

1. Ingresa el siguiente comando para editar el archivo de configuración que se ha proporcionado:

    ```bash
    code .env
    ```

El archivo se abre en un editor de código.

1. En el archivo de código, reemplaza el marcador de posición **your_project_endpoint** con el endpoint de tu proyecto (copiado de la página **Overview** del proyecto en el portal de Azure AI Foundry) y asegúrate de que la variable MODEL*DEPLOYMENT_NAME esté configurada con el nombre de tu implementación de modelo (que debería ser \_gpt-4o*).
2. Después de reemplazar el marcador de posición, usa el comando **CTRL+S** para guardar tus cambios y luego usa el comando **CTRL+Q** para cerrar el editor de código mientras mantienes la línea de comandos del cloud shell abierta.

### Escribir código para una aplicación de agente

> **Sugerencia**: A medida que agregas código, asegúrate de mantener la sangría correcta. Usa los niveles de sangría de los comentarios como guía.

1. Ingresa el siguiente comando para editar el archivo de código que se ha proporcionado:

    ```bash
    code agent.py
    ```

1. Revisa el código existente, que recupera las configuraciones de la aplicación y carga datos de _data.txt_ para ser analizados. El resto del archivo incluye comentarios donde agregarás el código necesario para implementar tu agente de análisis de datos.

1. Encuentra el comentario **Add references** y agrega el siguiente código para importar las clases que necesitarás para construir un agente de Azure AI que use la herramienta integrada code interpreter:

    ```python
    # Add references
    from azure.identity import DefaultAzureCredential
    from azure.ai.agents import AgentsClient
    from azure.ai.agents.models import FilePurpose, CodeInterpreterTool, ListSortOrder, MessageRole
    ```

1. Encuentra el comentario **Connect to the Agent client** y agrega el siguiente código para conectarte al proyecto de Azure AI.

    > **Sugerencia**: Ten cuidado de mantener el nivel de sangría correcto.

    ```python
    # Connect to the Agent client

    agent_client = AgentsClient(
        endpoint=project_endpoint,
        credential=DefaultAzureCredential
            (exclude_environment_credential=True,
             exclude_managed_identity_credential=True)
    )
    with agent_client:
    ```

    El código se conecta al proyecto de Azure AI Foundry usando las credenciales de Azure actuales. La declaración final _with agent_client_ inicia un bloque de código que define el ámbito del cliente, asegurando que se limpie cuando el código dentro del bloque termine.

1. Encuentra el comentario **Upload the data file and create a CodeInterpreterTool**, dentro del bloque _with agent_client_, y agrega el siguiente código para subir el archivo de datos al proyecto y crear una CodeInterpreterTool que pueda acceder a los datos en él:

    ```python
    # Upload the data file and create a CodeInterpreterTool

    file = agent_client.files.upload_and_poll(
        file_path=file_path, purpose=FilePurpose.AGENTS
    )
    print(f"Uploaded {file.filename}")

    code_interpreter = CodeInterpreterTool(file_ids=[file.id])
    ```

1. Encuentra el comentario **Define an agent that uses the CodeInterpreterTool** y agrega el siguiente código para definir un agente de IA que analice datos y pueda usar la herramienta code interpreter que definiste previamente:

    ```python
    # Define an agent that uses the CodeInterpreterTool

    agent = agent_client.create_agent(
    model=model_deployment,
    name="data-agent",
    instructions="You are an AI agent that analyzes the data in the file that has been uploaded. Use Python to calculate statistical metrics as necessary.",
    tools=code_interpreter.definitions,
    tool_resources=code_interpreter.resources,
    )
    print(f"Using agent: {agent.name}")
    ```

1. Encuentra el comentario **Create a thread for the conversation** y agrega el siguiente código para iniciar un thread en el que se ejecutará la sesión de chat con el agente:

    ```python
    # Create a thread for the conversation
    thread = agent_client.threads.create()
    ```

1. Ten en cuenta que la siguiente sección de código configura un bucle para que un usuario ingrese un prompt, terminando cuando el usuario ingresa "quit".

1. Encuentra el comentario **Send a prompt to the agent** y agrega el siguiente código para añadir un mensaje de usuario al prompt (junto con los datos del archivo que se cargó previamente), y luego ejecuta el thread con el agente.

    ```python

    # Send a prompt to the agent

    message = agent_client.messages.create(
    thread_id=thread.id,
    role="user",
    content=user_prompt,
    )

    run = agent_client.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
    ```

1. Encuentra el comentario **Check the run status for failures** y agrega el siguiente código para verificar si hay errores.

    ```python
    # Check the run status for failures

    if run.status == "failed":
        print(f"Run failed: {run.last_error}")
    ```

1. Encuentra el comentario **Show the latest response from the agent** y agrega el siguiente código para recuperar los mensajes del thread completado y mostrar el último que fue enviado por el agente.

    ```python
    # Show the latest response from the agent

    last_msg = agent_client.messages.get_last_message_text_by_role(
        thread_id=thread.id,
        role=MessageRole.AGENT,
    )
    if last_msg:
    print(f"Last Message: {last_msg.text.value}")
    ```

1. Encuentra el comentario **Get the conversation history**, que está después de que el bucle termina, y agrega el siguiente código para imprimir los mensajes del thread de conversación; invirtiendo el orden para mostrarlos en secuencia cronológica.

    ```python
    # Get the conversation history

    print("\\nConversation Log:\\n")
    messages = agent_client.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
    for message in messages:
    if message.text_messages:
        last_msg = message.text_messages[-1]
        print(f"{message.role}: {last_msg.text.value}\\n")
    ```

1. Encuentra el comentario **Clean up** y agrega el siguiente código para eliminar el agente y el thread cuando ya no sean necesarios.

    ```python
    # Clean up
    agent_client.delete_agent(agent.id)
    ```

1. Revisa el código, usando los comentarios para entender cómo:

    - Se conecta al proyecto de AI Foundry.
    - Sube el archivo de datos y crea una herramienta code interpreter que puede acceder a él.
    - Crea un nuevo agente que usa la herramienta code interpreter y tiene instrucciones explícitas para usar Python según sea necesario para el análisis estadístico.
    - Ejecuta un thread con un mensaje de prompt del usuario junto con los datos a ser analizados.
    - Verifica el estado de la ejecución en caso de que haya una falla.
    - Recupera los mensajes del thread completado y muestra el último enviado por el agente.
    - Muestra el historial de conversación.
    - Elimina el agente y el thread cuando ya no son necesarios.

1. Guarda el archivo de código (_CTRL+S_) cuando hayas terminado. También puedes cerrar el editor de código (_CTRL+Q_); aunque es posible que desees mantenerlo abierto en caso de que necesites hacer alguna edición al código que agregaste. En cualquier caso, mantén el panel de línea de comandos del cloud shell abierto.

### Iniciar sesión en Azure y ejecutar la aplicación

1. En el panel de línea de comandos del cloud shell, ingresa el siguiente comando para iniciar sesión en Azure.

    ```bash
    az login
    ```

    **\<font color="red"\>Debes iniciar sesión en Azure, incluso si la sesión del cloud shell ya está autenticada.\</font\>**

    > **Nota**: En la mayoría de los escenarios, solo usar _az login_ será suficiente. Sin embargo, si tienes suscripciones en múltiples tenants, es posible que necesites especificar el tenant usando el parámetro _--tenant_. Consulta [Iniciar sesión en Azure de forma interactiva usando la CLI de Azure](https://learn.microsoft.com/cli/azure/authenticate-azure-cli-interactively) para obtener más detalles.

2. Cuando se te solicite, sigue las instrucciones para abrir la página de inicio de sesión en una nueva pestaña e ingresa el código de autenticación proporcionado y tus credenciales de Azure. Luego completa el proceso de inicio de sesión en la línea de comandos, seleccionando la suscripción que contiene tu hub de Azure AI Foundry si se te solicita.

3. Después de haber iniciado sesión, ingresa el siguiente comando para ejecutar la aplicación:

    ```bash
    python agent.py
    ```

    La aplicación se ejecuta usando las credenciales de tu sesión de Azure autenticada para conectarse a tu proyecto y crear y ejecutar el agente.

4. Cuando se te solicite, visualiza los datos que la aplicación ha cargado del archivo de texto _data.txt_. Luego ingresa un prompt como:

    ```bash
    What's the category with the highest cost?
    ```

    > **Sugerencia**: Si la aplicación falla porque se excede el rate limit. Espera unos segundos e inténtalo de nuevo. Si no hay suficiente cuota disponible en tu suscripción, es posible que el modelo no pueda responder.

5. Visualiza la respuesta. Luego ingresa otro prompt, esta vez solicitando una visualización:

    ```prompt
    Create a text-based bar chart showing cost by category
    ```

6. Visualiza la respuesta. Luego ingresa otro prompt, esta vez solicitando una métrica estadística:

    ```prompt
    What's the standard deviation of cost?
    ```

    Visualiza la respuesta.

7. Puedes continuar la conversación si lo deseas. El thread es _stateful_, por lo que retiene el historial de la conversación, lo que significa que el agente tiene el contexto completo para cada respuesta. Ingresa `quit` cuando hayas terminado.

8. Revisa los mensajes de la conversación que se recuperaron del thread, que pueden incluir mensajes que el agente generó para explicar sus pasos al usar la herramienta code interpreter.

## Resumen

En este ejercicio, utilizaste el SDK de Azure AI Agent Service para crear una aplicación cliente que usa un agente de IA. El agente puede usar la herramienta integrada Code Interpreter para ejecutar código dinámico de Python para realizar análisis estadísticos.

## Limpieza

Si has terminado de explorar Azure AI Agent Service, debes eliminar los recursos que has creado en este ejercicio para evitar incurrir en costos innecesarios de Azure.

1. Regresa a la pestaña del navegador que contiene el portal de Azure (o vuelve a abrir el [portal de Azure](https://portal.azure.com) en `https://portal.azure.com` en una nueva pestaña del navegador) y visualiza el contenido del resource group donde implementaste los recursos utilizados en este ejercicio.
2. En la barra de herramientas, selecciona **Delete resource group**.
3. Ingresa el nombre del resource group y confirma que quieres eliminarlo.
