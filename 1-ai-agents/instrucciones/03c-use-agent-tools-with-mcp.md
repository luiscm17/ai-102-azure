---

lab: 
    title: 'Conectar agentes de IA a un servidor remoto de MCP' 
    description: 'Aprende a integrar herramientas del Protocolo de Contexto de Modelo con agentes de IA'
---

# Conectar agentes de IA a herramientas usando el Protocolo de Contexto de Modelo (MCP)

En este ejercicio, construirás un agente que se conecta a un servidor MCP alojado en la nube. El agente usará una búsqueda impulsada por IA para ayudar a los desarrolladores a encontrar respuestas precisas y en tiempo real de la documentación oficial de Microsoft. Esto es útil para construir asistentes que ayuden a los desarrolladores con orientación actualizada sobre herramientas como Azure, .NET y Microsoft 365. El agente usará la herramienta `microsoft_docs_search` proporcionada para consultar la documentación y devolver los resultados relevantes.

> **Sugerencia**: El código utilizado en este ejercicio se basa en el repositorio de ejemplo de soporte de MCP del servicio Azure AI Agent. Consulta [Demostraciones de Azure OpenAI](https://github.com/retkowsky/Azure-OpenAI-demos/blob/main/Azure%20Agent%20Service/9%20Azure%20AI%20Agent%20service%20-%20MCP%20support.ipynb) o visita [Conectarse a servidores del Protocolo de Contexto de Modelo](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/model-context-protocol) para más detalles.

Este ejercicio debería tomar aproximadamente **30** minutos en completarse.

> **Nota**: Algunas de las tecnologías utilizadas en este ejercicio están en versión preliminar o en desarrollo activo. Es posible que experimentes un comportamiento inesperado, advertencias o errores.

## Crear un proyecto de Azure AI Foundry

Comencemos creando un proyecto de Azure AI Foundry.

1. En un navegador web, abre el [portal de Azure AI Foundry](https://ai.azure.com) en `https://ai.azure.com` e inicia sesión con tus credenciales de Azure. Cierra cualquier sugerencia o panel de inicio rápido que se abra la primera vez que inicies sesión, y si es necesario usa el logo de **Azure AI Foundry** en la parte superior izquierda para navegar a la página de inicio, que se ve similar a la siguiente imagen (cierra el panel de **Help** si está abierto):

2. En la página de inicio, selecciona **Create an agent**.

3. Cuando se te pida que crees un proyecto, introduce un nombre válido para tu proyecto y expande **Advanced options**.

4. Confirma las siguientes configuraciones para tu proyecto:

      - **Azure AI Foundry resource**: *Un nombre válido para tu recurso de Azure AI Foundry*
      - **Subscription**: *Tu suscripción de Azure*
      - **Resource group**: *Crea o selecciona un grupo de recursos*
      - **Region**: *Selecciona cualquier **AI Services supported location***\*

    > \* Algunos recursos de Azure AI están restringidos por cuotas de modelo regionales. En caso de que se supere un límite de cuota más adelante en el ejercicio, existe la posibilidad de que necesites crear otro recurso en una región diferente.

5. Selecciona **Create** y espera a que se cree tu proyecto.

6. Si se te solicita, implementa un modelo **gpt-4o** usando la opción de implementación *Global Standard* o *Standard* (dependiendo de la disponibilidad de tu cuota).

    > **Nota**: Si la cuota está disponible, un modelo base GPT-4o puede implementarse automáticamente al crear tu Agente y proyecto.

7. Cuando tu proyecto se haya creado, el playground de Agentes se abrirá.

8. En el panel de navegación de la izquierda, selecciona **Overview** para ver la página principal de tu proyecto; que se ve así:

9. Copia los valores de **Azure AI Foundry project endpoint** en un bloc de notas, ya que los usarás para conectarte a tu proyecto en una aplicación cliente.

## Crear una aplicación cliente para agente de IA

Ahora estás listo para crear una aplicación cliente que defina el agente y las instrucciones. Se te ha proporcionado algo de código en un repositorio de GitHub.

### Preparar el entorno

1. Abre una nueva pestaña del navegador (manteniendo el portal de Azure AI Foundry abierto en la pestaña existente). Luego en la nueva pestaña, navega al [portal de Azure](https://portal.azure.com) en `https://portal.azure.com`; iniciando sesión con tus credenciales de Azure si se te solicita.

    Cierra cualquier notificación de bienvenida para ver la página de inicio del portal de Azure.

2. Usa el botón **[\>\_]** a la derecha de la barra de búsqueda en la parte superior de la página para crear un nuevo Cloud Shell en el portal de Azure, seleccionando un entorno ***PowerShell*** sin almacenamiento en tu suscripción.

    El cloud shell proporciona una interfaz de línea de comandos en un panel en la parte inferior del portal de Azure. Puedes cambiar el tamaño o maximizar este panel para que sea más fácil trabajar en él.

    > **Nota**: Si has creado previamente un cloud shell que usa un entorno *Bash*, cámbialo a ***PowerShell***.

3. En la barra de herramientas del cloud shell, en el menú **Settings**, selecciona **Go to Classic version** (esto es necesario para usar el editor de código).

    **\<font color="red"\>Asegúrate de haber cambiado a la versión clásica del cloud shell antes de continuar.\</font\>**

4. En el panel del cloud shell, ingresa los siguientes comandos para clonar el repositorio de GitHub que contiene los archivos de código para este ejercicio (escribe el comando, o cópialo al portapapeles y luego haz clic derecho en la línea de comandos y pégalo como texto sin formato):

    ```bash
    rm -r ai-agents -f
    git clone https://github.com/MicrosoftLearning/mslearn-ai-agents ai-agents
    ```

    > **Sugerencia**: A medida que ingresas comandos en el cloud shell, la salida puede ocupar una gran cantidad del búfer de la pantalla y el cursor en la línea actual puede quedar oscurecido. Puedes limpiar la pantalla ingresando el comando `cls` para que sea más fácil concentrarse en cada tarea.

5. Cuando el repositorio haya sido clonado, ingresa el siguiente comando para cambiar el directorio de trabajo a la carpeta que contiene los archivos de código y listarlos todos.

    ```bash
    cd ai-agents/Labfiles/03c-use-agent-tools-with-mcp/Python
    ls -a -l
    ```

    Los archivos proporcionados incluyen código de la aplicación y un archivo para las configuraciones.

### Configurar las configuraciones de la aplicación

1. En el panel de línea de comandos del cloud shell, ingresa el siguiente comando para instalar las librerías que usarás:

    ```bash
    python -m venv labenv
    ./labenv/bin/Activate.ps1
    pip install -r requirements.txt azure-ai-projects
    ```

2. Ingresa el siguiente comando para editar el archivo de configuración que se ha proporcionado:

    ```bash
    code .env
    ```

    El archivo se abre en un editor de código.

3. En el archivo de código, reemplaza el marcador de posición **your\_project\_endpoint** con el endpoint de tu proyecto (copiado de la página **Overview** del proyecto en el portal de Azure AI Foundry), y el marcador de posición **your\_model\_deployment** con el nombre que asignaste a tu implementación de modelo gpt-4o (que por defecto es `gpt-4o`).

4. Después de reemplazar los marcadores de posición, usa el comando **CTRL+S** para guardar tus cambios y luego usa el comando **CTRL+Q** para cerrar el editor de código mientras mantienes la línea de comandos del cloud shell abierta.

### Crear un agente de IA y conectarlo a un servidor MCP

Ahora estás listo para crear el agente para tu solución.

1. Ingresa el siguiente comando para editar el archivo **client.py**:

    ```bash
    code client.py
    ```

2. Revisa el código en el archivo, notando que contiene strings para el nombre del agente y las instrucciones, así como un bucle simple para permitir un chat con el agente.

3. Encuentra el comentario **Add references** y agrega el siguiente código para importar las clases que necesitarás:

    ```python
    # Add references
    from azure.ai.agents import AgentsClient
    from azure.ai.agents.models import Tool, ListSortOrder, MessageRole, ToolSource, Tools
    from azure.identity import DefaultAzureCredential
    ```

4. Ten en cuenta que se ha proporcionado código para cargar el endpoint del proyecto y el nombre del modelo desde tus variables de entorno.

5. Encuentra el comentario **Connect to the agents client**, y agrega el siguiente código para crear un AgentsClient conectado a tu proyecto:

    ```python
    # Connect to the agents client
    agents_client = AgentsClient(
        endpoint=project_endpoint,
        credential=DefaultAzureCredential(
            exclude_environment_credential=True,
            exclude_managed_identity_credential=True
        ),
    )
    ```

6. Ahora necesitas crear una conexión de herramienta que el agente pueda usar para conectarse a un servidor MCP remoto. Encuentra el comentario **Create an MCP toolset** y agrega el siguiente código para conectarte al servidor MCP:

    ```python
    # Create an MCP toolset
    mcp_tools = Tools(source=ToolSource(uri="https://mcp-docs-search-prod.azurewebsites.net/"))
    ```

7. Ahora puedes crear tu agente de IA y conectarlo a las herramientas MCP que acabas de definir. Encuentra el comentario **Create an agent and an agent thread** y agrega el siguiente código:

    ```python
    # Create an agent and an agent thread
    with agents_client:
        agent = agents_client.create_agent(
            model=model_deployment,
            name=agent_name,
            instructions=agent_instructions,
            tools=mcp_tools
        )
        thread = agents_client.threads.create()
        print(f"You're chatting with: {agent.name} ({agent.id})")
    ```

8. Ahora es el momento de agregar el código para enviar un prompt a tu agente. Encuentra el comentario **Send a prompt to the agent** y agrega el siguiente código:

    ```python
    # Send a prompt to the agent
    print("Sending message to agent. Please wait...")
    message = agents_client.messages.create(
        thread_id=thread.id,
        role=MessageRole.USER,
        content=user_prompt,
    )

    run = agents_client.runs.create_and_process(
        thread_id=thread.id,
        agent_id=agent.id,
    )

    if run.status == "failed":
        print(f"Run failed: {run.last_error}")
    ```

9. Una vez que la ejecución esté completa, puedes obtener y mostrar la respuesta. Encuentra el comentario **Fetch and display the conversation history** y agrega el siguiente código:

    ```python
    # Fetch and display the conversation history
    messages = agents_client.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
    for message in messages:
        if message.text_messages:
            last_msg = message.text_messages[-1]
            print(f"{message.role}: {last_msg.text.value}\n")
    ```

10. Finalmente, necesitas limpiar el agente para evitar costos continuos. Encuentra el comentario **Clean up** y agrega el siguiente código:

    ```python
    # Clean up
    agents_client.delete_agent(agent.id)
    print("Deleted agent")
    ```

11. Usa el comando **CTRL+S** para guardar tus cambios en el archivo de código. Puedes mantenerlo abierto (en caso de que necesites editar el código para corregir cualquier error) o usar el comando **CTRL+Q** para cerrar el editor de código mientras mantienes la línea de comandos del cloud shell abierta.

### Iniciar sesión en Azure y ejecutar la aplicación

Ahora estás listo para ejecutar tu código y ver cómo tu agente de IA usa la herramienta MCP para encontrar información relevante.

1. En el panel de línea de comandos del cloud shell, ingresa el siguiente comando para iniciar sesión en Azure.

    ```bash
    az login
    ```

    **\<font color="red"\>Debes iniciar sesión en Azure, incluso si la sesión del cloud shell ya está autenticada.\</font\>**

    > **Nota**: En la mayoría de los escenarios, solo usar *az login* será suficiente. Sin embargo, si tienes suscripciones en múltiples tenants, es posible que necesites especificar el tenant usando el parámetro *--tenant*. Consulta [Iniciar sesión en Azure de forma interactiva usando la CLI de Azure](https://learn.microsoft.com/cli/azure/authenticate-azure-cli-interactively) para obtener más detalles.

2. Cuando se te solicite, sigue las instrucciones para abrir la página de inicio de sesión en una nueva pestaña e ingresa el código de autenticación proporcionado y tus credenciales de Azure. Luego completa el proceso de inicio de sesión en la línea de comandos, seleccionando la suscripción que contiene tu hub de Azure AI Foundry si se te solicita.

3. Después de haber iniciado sesión, ingresa el siguiente comando para ejecutar la aplicación:

    ```bash
    python client.py
    ```

4. Ingresa un prompt para el agente, como `How can I create an Azure Container App with a managed identity?`

    Después de que el agente procese el prompt, deberías ver una salida similar a la siguiente:

    ```markdown
    You're chatting with: a-docs-search-agent (agt_xxxxxxxxxx)
    Sending message to agent. Please wait...

    USER: How can I create an Azure Container App with a managed identity?

    AGENT: To create an Azure Container App with a managed identity (either system-assigned or user-assigned). Below are the relevant commands and workflow:

    ---

    ### **1. Create a Resource Group**
    '''azurecli
    az group create --name myResourceGroup --location eastus
    '''


    {{continued...}}

    By following these steps, you can deploy an Azure Container App with either system-assigned or user-assigned managed identities to integrate seamlessly with other Azure services.
    --------------------------------------------------
    USER: Give me the Azure CLI commands to create an Azure Container App with a managed identity.
    --------------------------------------------------
    Deleted agent
    ```

    Observa que el agente pudo invocar automáticamente la herramienta MCP `microsoft_docs_search` para cumplir con la solicitud.

5. Puedes ejecutar la aplicación de nuevo (usando el comando `python client.py`) para pedir información diferente. En cada caso, el agente intentará encontrar documentación técnica usando la herramienta MCP.

## Limpieza

Ahora que has terminado el ejercicio, debes eliminar los recursos en la nube que has creado para evitar un uso innecesario de recursos.

1. Abre el [portal de Azure](https://portal.azure.com) en `https://portal.azure.com` y visualiza el contenido del resource group donde implementaste los recursos del hub utilizados en este ejercicio.
2. En la barra de herramientas, selecciona **Delete resource group**.
3. Ingresa el nombre del resource group y confirma que quieres eliminarlo.
