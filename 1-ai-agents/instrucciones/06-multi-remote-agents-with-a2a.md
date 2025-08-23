---
lab: 
    title: 'Conectarse a agentes remotos con el protocolo A2A' 
    description: 'Utiliza el protocolo A2A para colaborar con agentes remotos.'
---

# Conectarse a agentes remotos con el protocolo A2A

En este ejercicio, usarás Azure AI Agent Service con el protocolo A2A para crear agentes remotos simples que interactúen entre sí. Estos agentes ayudarán a los redactores técnicos a preparar sus publicaciones de blog para desarrolladores. Un agente de títulos generará un titular, y un agente de esquemas usará el título para desarrollar un esquema conciso para el artículo. ¡Comencemos\!

> **Consejo**: El código utilizado en este ejercicio se basa en el **SDK** de Azure AI Foundry para Python. Puedes desarrollar soluciones similares usando los **SDKs** para Microsoft .NET, JavaScript y Java. Consulta [Azure AI Foundry SDK client libraries](https://learn.microsoft.com/azure/ai-foundry/how-to/develop/sdk-overview) para obtener más detalles.

Este ejercicio debería tomar aproximadamente **30** minutos en completarse.

> **Nota**: Algunas de las tecnologías utilizadas en este ejercicio están en versión preliminar o en desarrollo activo. Es posible que experimentes un comportamiento inesperado, advertencias o errores.

## Crear un proyecto de Azure AI Foundry

Comencemos creando un proyecto de Azure AI Foundry.

1. En un navegador web, abre el [Azure AI Foundry portal](https://ai.azure.com) en `https://ai.azure.com` e inicia sesión con tus credenciales de Azure. Cierra cualquier `tips` o `quick start panes` que se abra la primera vez que inicies sesión y, si es necesario, usa el logo de **Azure AI Foundry** en la parte superior izquierda para navegar a la página de `home`, que se parece a la siguiente imagen (cierra el panel de **Help** si está abierto):

    ![Screenshot of Azure AI Foundry portal.](./Media/ai-foundry-home.png)

2. En la página de `home`, selecciona **Create an agent**.

3. Cuando se te pida que crees un `project`, ingresa un nombre válido para tu proyecto y expande **Advanced options**.

4. Confirma la siguiente configuración para tu proyecto:

      - **Azure AI Foundry resource**: *Un nombre válido para tu recurso de Azure AI Foundry*
      - **Subscription**: *Tu suscripción de Azure*
      - **Resource group**: *Crea o selecciona un grupo de recursos*
      - **Region**: *Selecciona cualquier **AI Services supported location***\*

    > \* Algunos recursos de Azure AI están restringidos por cuotas de modelos regionales. En caso de que se exceda un límite de cuota más adelante en el ejercicio, es posible que debas crear otro recurso en una región diferente.

5. Selecciona **Create** y espera a que se cree tu proyecto.

6. Si se te solicita, implementa un modelo **gpt-4o** usando la opción de implementación *Global Standard* o *Standard* (dependiendo de la disponibilidad de tu cuota).

    > **Nota**: Si la cuota está disponible, un modelo base **GPT-4o** puede implementarse automáticamente al crear tu **Agent** y `project`.

7. Cuando se cree tu proyecto, se abrirá el **Agents playground**.

8. En el panel de navegación de la izquierda, selecciona **Overview** para ver la página principal de tu proyecto; que se ve así:

    ![Screenshot of a Azure AI Foundry project overview page.](./Media/ai-foundry-project.png)

9. Copia los valores del **Azure AI Foundry project endpoint** en un bloc de notas, ya que los usarás para conectarte a tu proyecto en una aplicación cliente.

## Crear una aplicación A2A

Ahora estás listo para crear una aplicación cliente que utilice un agente. Se te ha proporcionado algo de código en un repositorio de **GitHub**.

### Clonar el repositorio que contiene el código de la aplicación

1. Abre una nueva pestaña del navegador (manteniendo el `Azure AI Foundry portal` abierto en la pestaña existente). Luego, en la nueva pestaña, navega al [Azure portal](https://portal.azure.com) en `https://portal.azure.com`; iniciando sesión con tus credenciales de Azure si se te solicita.

    Cierra cualquier `welcome notifications` para ver la página de `home` del Azure portal.

2. Usa el botón **[\>_]** a la derecha de la barra de búsqueda en la parte superior de la página para crear un nuevo **Cloud Shell** en el Azure portal, seleccionando un entorno ***PowerShell*** sin almacenamiento en tu suscripción.

    El `cloud shell` proporciona una interfaz de línea de comandos en un panel en la parte inferior del Azure portal. Puedes cambiar el tamaño o maximizar este panel para que sea más fácil trabajar en él.

    > **Nota**: Si has creado previamente un `cloud shell` que usa un entorno *Bash*, cámbialo a ***PowerShell***.

3. En la barra de herramientas de `cloud shell`, en el menú de **Settings**, selecciona **Go to Classic version** (esto es necesario para usar el editor de código).

    **<font color="red">Asegúrate de haber cambiado a la versión clásica de `cloud shell` antes de continuar.</font>**

4. En el panel de `cloud shell`, ingresa los siguientes comandos para clonar el repositorio de **GitHub** que contiene los archivos de código para este ejercicio (escribe el comando, o cópialo al portapapeles y luego haz clic derecho en la línea de comandos y pégalo como texto sin formato):

    ```bash
    rm -r ai-agents -f
    git clone <https://github.com/MicrosoftLearning/mslearn-ai-agents> ai-agents
    ```

    > **Consejo**: Al ingresar comandos en el `cloudshell`, la salida puede ocupar una gran cantidad del `screen buffer` y el cursor en la línea actual puede quedar oculto. Puedes limpiar la pantalla ingresando el comando `cls` para que sea más fácil concentrarse en cada tarea.

5. Ingresa el siguiente comando para cambiar el directorio de trabajo a la carpeta que contiene los archivos de código y listarlos todos.

    ```bash
    cd ai-agents/Labfiles/06-build-remote-agents-with-a2a/python
    ls -a -l
    ```

    Los archivos proporcionados incluyen:

    ```yml
    python
    ├── outline_agent/
    │   ├── agent.py
    │   ├── agent_executor.py
    │   └── server.py
    ├── routing_agent/
    │   ├── agent.py
    │   └── server.py
    ├── title_agent/
    │   ├── agent.py
    │   ├── agent_executor.py
    │   └── server.py
    ├── client.py
    └── run_all.py
    ```

    Cada carpeta de agente contiene el código del agente de Azure AI y un servidor para alojar al agente. El **routing agent** es responsable de descubrir y comunicarse con los agentes de **title** y **outline**. El **client** permite a los usuarios enviar `prompts` al **routing agent**. `run_all.py` inicia todos los servidores y ejecuta el cliente.

### Configurar los ajustes de la aplicación

1. En el panel de la línea de comandos de `cloud shell`, ingresa el siguiente comando para instalar las bibliotecas que usarás:

    ```bash
    python -m venv labenv
    ./labenv/bin/Activate.ps1
    pip install -r requirements.txt azure-ai-projects a2a-sdk
    ```

2. Ingresa el siguiente comando para editar el archivo de configuración que se ha proporcionado:

    ```bash
    code .env
    ```

    El archivo se abre en un editor de código.

3. En el archivo de código, reemplaza el marcador de posición **your\_project\_endpoint** con el `endpoint` para tu proyecto (copiado de la página de **Overview** del proyecto en el Azure AI Foundry portal) y asegúrate de que la variable `MODEL_DEPLOYMENT_NAME` esté configurada con el nombre de tu `model deployment` (que debería ser *gpt-4o*).

4. Después de haber reemplazado el marcador de posición, usa el comando **CTRL+S** para guardar tus cambios y luego usa el comando **CTRL+Q** para cerrar el editor de código mientras mantienes la línea de comandos de `cloud shell` abierta.

### Crear un agente descubrible

En esta tarea, crearás el agente de títulos que ayuda a los escritores a crear `headlines` de moda para sus artículos. También definirás las `skills` y la `card` del agente requeridas por el protocolo **A2A** para que el agente sea descubrible.

1. Navega al directorio `title_agent`:

    ```bash
    cd title_agent
    ```

    > **Consejo**: A medida que agregues código, asegúrate de mantener la sangría correcta. Usa los niveles de sangría de los comentarios como guía.

2. Ingresa el siguiente comando para editar el archivo de código que se ha proporcionado:

    ```bash
    code agent.py
    ```

3. Encuentra el comentario **Create the agents client** y agrega el siguiente código para conectarte al proyecto de Azure AI:

    > **Consejo**: Ten cuidado de mantener el nivel de sangría correcto.

    ```python
    # Create the agents client
    self.client = AgentsClient(
        endpoint=os.environ['PROJECT_ENDPOINT'],
        credential=DefaultAzureCredential(
            exclude_environment_credential=True,
            exclude_managed_identity_credential=True
        )
    )
    ```

4. Encuentra el comentario **Create the title agent** y agrega el siguiente código para crear el agente:

    ```python
    # Create the title agent
    self.agent = self.client.create_agent(
        model=os.environ['MODEL_DEPLOYMENT_NAME'],
        name='title-agent',
        instructions="""
        You are a helpful writing assistant.
        Given a topic the user wants to write about, suggest a single clear and catchy blog post title.
        """,
    )
    ```

5. Encuentra el comentario **Create a thread for the chat session** y agrega el siguiente código para crear el `chat thread`:

    ```python
    # Create a thread for the chat session
    thread = self.client.threads.create()
    ```

6. Localiza el comentario **Send user message** y agrega este código para enviar el `prompt` del usuario:

    ```python
    # Send user message
    self.client.messages.create(thread_id=thread.id, role=MessageRole.USER, content=user_message)
    ```

7. Debajo del comentario **Create and run the agent**, agrega el siguiente código para iniciar la generación de la respuesta del agente:

    ```python
    # Create and run the agent
    run = self.client.runs.create_and_process(thread_id=thread.id, agent_id=self.agent.id)
    ```

    El código proporcionado en el resto del archivo procesará y devolverá la respuesta del agente.

8. Guarda el archivo de código (*CTRL+S*). Ahora estás listo para compartir las `skills` y la `card` del agente con el protocolo **A2A**.

9. Ingresa el siguiente comando para editar el archivo `server.py` del agente de títulos

    ```bash
    code server.py
    ```

10. Encuentra el comentario **Define agent skills** y agrega el siguiente código para especificar la funcionalidad del agente:

    ```python
    # Define agent skills
    skills = [
        AgentSkill(
            id='generate_blog_title',
            name='Generate Blog Title',
            description='Generates a blog title based on a topic',
            tags=['title'],
            examples=[
                'Can you give me a title for this article?',
            ],
        ),
    ]
    ```

11. Encuentra el comentario **Create agent card** y agrega este código para definir los metadatos que hacen que el agente sea descubrible:

    ```python
    # Create agent card
    agent_card = AgentCard(
        name='AI Foundry Title Agent',
        description='An intelligent title generator agent powered by Azure AI Foundry. '
        'I can help you generate catchy titles for your articles.',
        url=f'http://{host}:{port}/',
        version='1.0.0',
        default_input_modes=['text'],
        default_output_modes=['text'],
        capabilities=AgentCapabilities(),
        skills=skills,
    )
    ```

12. Localiza el comentario **Create agent executor** y agrega el siguiente código para inicializar el `agent executor` usando la `agent card`:

    ```python
    # Create agent executor
    agent_executor = create_foundry_agent_executor(agent_card)
    ```

    El `agent executor` actuará como un envoltorio para el agente de títulos que creaste.

13. Encuentra el comentario **Create request handler** y agrega lo siguiente para manejar las solicitudes entrantes usando el `executor`:

    ```python
    # Create request handler
    request_handler = DefaultRequestHandler(
        agent_executor=agent_executor, task_store=InMemoryTaskStore()
    )
    ```

14. Debajo del comentario **Create A2A application**, agrega este código para crear la instancia de la aplicación compatible con **A2A**:

    ```python
    # Create A2A application
    a2a_app = A2AStarletteApplication(
        agent_card=agent_card, http_handler=request_handler
    )
    ```

    Este código crea un servidor **A2A** que compartirá la información del agente de títulos y manejará las solicitudes entrantes para este agente usando el `title agent executor`.

15. Guarda el archivo de código (*CTRL+S*) cuando hayas terminado.

### Habilitar mensajes entre los agentes

En esta tarea, usarás el protocolo **A2A** para permitir que el **routing agent** envíe mensajes a los otros agentes. También permitirás que el agente de títulos reciba mensajes implementando la clase `agent_executor`.

1. Navega al directorio `routing_agent`:

    ```bash
    cd ../routing_agent
    ```

2. Ingresa el siguiente comando para editar el archivo de código que se ha proporcionado:

    ```bash
    code agent.py
    ```

    El **routing agent** actúa como un `orchestrator` que maneja los mensajes del usuario y determina qué agente remoto debe procesar la solicitud.

    Cuando se recibe un mensaje de usuario, el **routing agent**:
    - Inicia un `conversation thread`.
    - Usa el método `create_and_process` para evaluar el agente que mejor se adapta al mensaje del usuario.
    - El mensaje se enruta al agente apropiado a través de **HTTP** usando la función `send_message`.
    - El agente remoto procesa el mensaje y devuelve una respuesta.

    El **routing agent** finalmente captura la respuesta y la devuelve al usuario a través del `thread`.

    Observa que el método `send_message` es `async` y debe ser esperado para que la ejecución del agente se complete con éxito.

3. Agrega el siguiente código debajo del comentario **Retrieve the remote agent's A2A client using the agent name**:

    ```python
    # Retrieve the remote agent's A2A client using the agent name
    client = self.remote_agent_connections[agent_name]
    ```

4. Localiza el comentario **Construct the payload to send to the remote agent** y agrega el siguiente código:

    ```python
    # Construct the payload to send to the remote agent
    payload: dict[str, Any] = {
        'message': {
            'role': 'user',
            'parts': [{'kind': 'text', 'text': task}],
            'messageId': message_id,
        },
    }
    ```

5. Encuentra el comentario **Wrap the payload in a SendMessageRequest object** y agrega el siguiente código:

    ```python
    # Wrap the payload in a SendMessageRequest object
    message_request = SendMessageRequest(id=message_id, params=MessageSendParams.model_validate(payload))
    ```

6. Agrega el siguiente código debajo del comentario **Send the message to the remote agent client and await the response**:

    ```python
    # Send the message to the remote agent client and await the response
    send_response: SendMessageResponse = await client.send_message(message_request=message_request)
    ```

7. Guarda el archivo de código (*CTRL+S*) cuando hayas terminado. Ahora el **routing agent** puede descubrir y enviar mensajes al agente de títulos. Creemos el código del `agent executor` para manejar esos mensajes entrantes del **routing agent**.

8. Navega al directorio `title_agent`:

    ```bash
    cd ../title_agent
    ```

9. Ingresa el siguiente comando para editar el archivo de código que se ha proporcionado:

    ```bash
    code agent_executor.py
    ```

    La implementación de la clase `AgentExecutor` debe contener los métodos `execute` y `cancel`. El método `cancel` se te ha proporcionado. El método `execute` incluye un objeto `TaskUpdater` que gestiona eventos y señales al `caller` cuando la tarea está completa. Agreguemos la lógica para la ejecución de la tarea.

10. En el método `execute`, agrega el siguiente código debajo del comentario **Process the request**:

    ```python
    # Process the request
    await self._process_request(context.message.parts, context.context_id, updater)
    ```

11. En el método `_process_request`, agrega el siguiente código debajo del comentario **Get the title agent**:

    ```python
    # Get the title agent
    agent = await self._get_or_create_agent()
    ```

12. Agrega el siguiente código debajo del comentario **Update the task status**:

    ```python
    # Update the task status
    await task_updater.update_status(
        TaskState.working,
        message=new_agent_text_message('Title Agent is processing your request...', context_id=context_id),
    )
    ```

13. Encuentra el comentario **Run the agent conversation** y agrega el siguiente código:

    ```python
    # Run the agent conversation
    responses = await agent.run_conversation(user_message)
    ```

14. Encuentra el comentario **Update the task with the responses** y agrega el siguiente código:

    ```python
    # Update the task with the responses
    for response in responses:
        await task_updater.update_status(
            TaskState.working,
            message=new_agent_text_message(response, context_id=context_id),
        )
    ```

15. Encuentra el comentario **Mark the task as complete** y agrega el siguiente código:

    ```python
    # Mark the task as complete
    final_message = responses[-1] if responses else 'Task completed.'
    await task_updater.complete(
        message=new_agent_text_message(final_message, context_id=context_id)
    )
    ```

    Ahora tu agente de títulos ha sido envuelto con un `agent executor` que el protocolo **A2A** usará para manejar los mensajes. ¡Excelente trabajo!

### Iniciar sesión en Azure y ejecutar la aplicación

1. En el panel de la línea de comandos de `cloud shell`, ingresa el siguiente comando para iniciar sesión en Azure.

    ```bash
    az login
    ```

    **<font color="red">Debes iniciar sesión en Azure, incluso si la sesión de `cloud shell` ya está autenticada.</font>**

    > **Nota**: En la mayoría de los escenarios, solo usar *az login* será suficiente. Sin embargo, si tienes suscripciones en múltiples `tenants`, es posible que necesites especificar el `tenant` usando el parámetro *--tenant*. Consulta [Sign into Azure interactively using the Azure CLI](https://learn.microsoft.com/cli/azure/authenticate-azure-cli-interactively) para obtener detalles.

2. Cuando se te solicite, sigue las instrucciones para abrir la página de `sign-in` en una nueva pestaña e ingresa el `authentication code` proporcionado y tus credenciales de Azure. Luego completa el proceso de `sign in` en la línea de comandos, seleccionando la suscripción que contiene tu `Azure AI Foundry hub` si se te solicita.

3. Después de haber iniciado sesión, ingresa el siguiente comando para ejecutar la aplicación:

    ```bash
    cd ..
    python run_all.py
    ```

    La aplicación se ejecuta usando las credenciales de tu sesión de Azure autenticada para conectarte a tu proyecto y crear y ejecutar el agente. Deberías ver algunas salidas de cada servidor a medida que se inicia.

4. Espera hasta que aparezca el `prompt` para la entrada, luego ingresa un `prompt` como:

    ```yml
    Create a title and outline for an article about React programming.
    ```

    Después de unos momentos, deberías ver una respuesta del agente con los resultados.

5. Ingresa `quit` para salir del programa y detener los servidores.

## Resumen

En este ejercicio, usaste el **SDK** de Azure AI Agent Service y el **A2A** Python **SDK** para crear una solución `multi-agent` remota. Creaste un agente compatible con **A2A** y lo hiciste descubrible, y configuraste un `routing agent` para acceder a las `skills` del agente. También implementaste un `agent executor` para procesar los mensajes **A2A** entrantes y gestionar las tareas. ¡Excelente trabajo!

## Limpieza

Si has terminado de explorar Azure AI Agent Service, debes eliminar los recursos que has creado en este ejercicio para evitar incurrir en costos innecesarios de Azure.

1. Vuelve a la pestaña del navegador que contiene el Azure portal (o vuelve a abrir el [Azure portal](https://portal.azure.com) en `https://portal.azure.com` en una nueva pestaña del navegador) y visualiza el contenido del grupo de recursos donde implementaste los recursos utilizados en este ejercicio.
2. En la barra de herramientas, selecciona **Delete resource group**.
3. Ingresa el nombre del grupo de recursos y confirma que deseas eliminarlo.
