---

lab: 
    title: 'Conectar agentes de IA a herramientas usando el Protocolo de Contexto de Modelo (MCP) local'
    description: 'Aprende a ejecutar un servidor local del Protocolo de Contexto de Modelo (MCP) para el desarrollo de agentes de IA'

---

# Conectar agentes de IA a herramientas usando el Protocolo de Contexto de Modelo (MCP)

En este ejercicio, crearás una solución de agente de IA que se conecta a un servidor local de MCP. Esto es útil para el desarrollo, ya que te permite trabajar con funciones personalizadas localmente antes de implementarlas en la nube. Construirás un agente simple de evaluación de inventario para un minorista de cosméticos. Usando el servidor MCP, el agente podrá recuperar información sobre el inventario y hacer sugerencias de reabastecimiento o liquidación.

> **Sugerencia**: El código utilizado en este ejercicio se basa en los SDK para Python de Azure AI Foundry y MCP. Puedes desarrollar soluciones similares usando los SDK para Microsoft .NET. Consulta [Bibliotecas cliente del SDK de Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/how-to/develop/sdk-overview) y [MCP C\# SDK](https://modelcontextprotocol.github.io/csharp-sdk/api/ModelContextProtocol.html) para más detalles.

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
    cd ai-agents/Labfiles/03d-use-local-mcp-server-tools/Python
    ls -a -l
    ```

    Los archivos proporcionados incluyen código de la aplicación y un archivo para las configuraciones.

### Configurar las configuraciones de la aplicación

1. En el panel de línea de comandos del cloud shell, ingresa el siguiente comando para instalar las librerías que usarás:

    ```bash
    python -m venv labenv
    ./labenv/bin/Activate.ps1
    pip install -r requirements.txt
    ```

2. Ingresa el siguiente comando para editar el archivo de configuración que se ha proporcionado:

    ```bash
    code .env
    ```

    El archivo se abre en un editor de código.

3. En el archivo de código, reemplaza el marcador de posición **your\_project\_endpoint** con el endpoint de tu proyecto (copiado de la página **Overview** del proyecto en el portal de Azure AI Foundry), y el marcador de posición **your\_model\_deployment** con el nombre que asignaste a tu implementación de modelo gpt-4o (que por defecto es `gpt-4o`).

4. Después de reemplazar los marcadores de posición, usa el comando **CTRL+S** para guardar tus cambios y luego usa el comando **CTRL+Q** para cerrar el editor de código mientras mantienes la línea de comandos del cloud shell abierta.

### Crear un servidor MCP y un agente de IA

Ahora estás listo para crear el agente para tu solución.

1. En el panel de línea de comandos del cloud shell, ingresa el siguiente comando para editar el archivo **mcp\_server.py**:

    ```bash
    code mcp_server.py
    ```

2. Revisa el código que ya existe en el archivo. Define una clase **InventoryManager** con algunas funciones que recuperan el inventario, identifican artículos que necesitan ser reabastecidos o liquidados y calculan las ventas promedio.

3. Encuentra el comentario **Create an MCP server** y agrega el siguiente código para inicializar un servidor MCP, registrar la clase **InventoryManager** para que sus métodos puedan ser llamados por un cliente MCP, y luego iniciar el servidor para que esté esperando solicitudes entrantes.

    ```python
    # Create an MCP server
    mcp_server = ModelContextProtocolServer(host="localhost", port=8000)
    mcp_server.register(InventoryManager)
    mcp_server.start()
    ```

4. Ahora estás listo para crear tu agente de IA. En una nueva pestaña de Cloud Shell (manten el Cloud Shell existente abierto), ingresa el siguiente comando para clonar el repositorio:

    ```bash
    rm -r ai-agents -f
    git clone https://github.com/MicrosoftLearning/mslearn-ai-agents ai-agents
    ```

    > **Sugerencia**: A medida que ingresas comandos en el cloud shell, la salida puede ocupar una gran cantidad del búfer de la pantalla y el cursor en la línea actual puede quedar oscurecido. Puedes limpiar la pantalla ingresando el comando `cls` para que sea más fácil concentrarse en cada tarea.

5. Cambia al directorio de trabajo correcto:

    ```bash
    cd ai-agents/Labfiles/03d-use-local-mcp-server-tools/Python
    ```

6. Ingresa el siguiente comando para instalar las librerías que usarás:

    ```bash
    python -m venv labenv
    ./labenv/bin/Activate.ps1
    pip install -r requirements.txt
    ```

7. Ingresa el siguiente comando para editar el archivo de configuración que se ha proporcionado:

    ```bash
    code .env
    ```

8. En el archivo de código, reemplaza el marcador de posición **your\_project\_endpoint** con el endpoint de tu proyecto (copiado de la página **Overview** del proyecto en el portal de Azure AI Foundry), y el marcador de posición **your\_model\_deployment** con el nombre que asignaste a tu implementación de modelo gpt-4o (que por defecto es `gpt-4o`).

9. Usa el comando **CTRL+S** para guardar tus cambios y luego usa el comando **CTRL+Q** para cerrar el editor de código.

10. Ingresa el siguiente comando para editar el archivo **client.py**:

    ```bash
    code client.py
    ```

11. Revisa el código en el archivo, notando que contiene strings para el nombre del agente y las instrucciones, así como un bucle simple para permitir un chat con el agente.

12. Encuentra el comentario **Add references** y agrega el siguiente código para importar las clases que necesitarás:

    ```python
    # Add references
    from azure.ai.agents import AgentsClient
    from azure.ai.agents.models import Tool, ListSortOrder, MessageRole, ToolSource, Tools
    from azure.identity import DefaultAzureCredential
    ```

13. Ten en cuenta que se ha proporcionado código para cargar el endpoint del proyecto y el nombre del modelo desde tus variables de entorno.

14. Encuentra el comentario **Connect to the agents client**, y agrega el siguiente código para crear un AgentsClient conectado a tu proyecto:

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

15. Ahora necesitas crear una conexión de herramienta que el agente pueda usar para conectarse a tu servidor MCP local. Encuentra el comentario **Create an MCP toolset** y agrega el siguiente código para conectarte a tu servidor local de MCP:

    ```python
    # Create an MCP toolset
    mcp_tools = Tools(source=ToolSource(uri="http://localhost:8000"))
    ```

    > **Nota**: El servidor MCP local aún no se está ejecutando, pero el código de tu agente necesitará el nombre de host y el número de puerto para conectarse a él cuando se inicie.

16. Ahora puedes crear tu agente de IA y conectarlo a las herramientas MCP que acabas de definir. Encuentra el comentario **Create an agent and an agent thread** y agrega el siguiente código:

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

17. Ahora es el momento de agregar el código para enviar un prompt a tu agente. Encuentra el comentario **Send a prompt to the agent** y agrega el siguiente código:

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

18. Una vez que la ejecución esté completa, puedes obtener y mostrar la respuesta. Encuentra el comentario **Fetch and display the conversation history** y agrega el siguiente código:

    ```python
    # Fetch and display the conversation history
    messages = agents_client.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
    for message in messages:
        if message.text_messages:
            last_msg = message.text_messages[-1]
            print(f"{message.role}: {last_msg.text.value}\n")
    ```

19. Finalmente, necesitas limpiar el agente para evitar costos continuos. Encuentra el comentario **Clean up** y agrega el siguiente código:

    ```python
    # Clean up
    agents_client.delete_agent(agent.id)
    print("Deleted agent")
    ```

20. Usa el comando **CTRL+S** para guardar tus cambios en el archivo de código. Puedes mantenerlo abierto (en caso de que necesites editar el código para corregir cualquier error) o usar el comando **CTRL+Q** para cerrar el editor de código.

### Iniciar sesión en Azure y ejecutar la aplicación

Ahora estás listo para ejecutar tu código y ver cómo tu agente de IA usa la herramienta MCP para encontrar información relevante.

1. En el panel de línea de comandos del cloud shell que contiene el servidor MCP, ingresa el siguiente comando para ejecutar el servidor.

    ```bash
    python mcp_server.py
    ```

    > **Sugerencia**: El servidor MCP se ejecutará hasta que presiones `Ctrl+C`.

2. En el otro panel de línea de comandos del cloud shell, ingresa el siguiente comando para iniciar sesión en Azure.

    ```bash
    az login
    ```

    **\<font color="red"\>Debes iniciar sesión en Azure, incluso si la sesión del cloud shell ya está autenticada.\</font\>**

    > **Nota**: En la mayoría de los escenarios, solo usar *az login* será suficiente. Sin embargo, si tienes suscripciones en múltiples tenants, es posible que necesites especificar el tenant usando el parámetro *--tenant*. Consulta [Iniciar sesión en Azure de forma interactiva usando la CLI de Azure](https://learn.microsoft.com/cli/azure/authenticate-azure-cli-interactively) para obtener más detalles.

3. Cuando se te solicite, sigue las instrucciones para abrir la página de inicio de sesión en una nueva pestaña e ingresa el código de autenticación proporcionado y tus credenciales de Azure. Luego completa el proceso de inicio de sesión en la línea de comandos, seleccionando la suscripción que contiene tu hub de Azure AI Foundry si se te solicita.

4. Después de haber iniciado sesión, ingresa el siguiente comando para ejecutar la aplicación:

    ```bash
    python client.py
    ```

5. Ingresa un prompt para el agente, como `What are the current inventory levels?`

    > **Sugerencia**: Si la aplicación falla porque se excede el rate limit. Espera unos segundos e inténtalo de nuevo. Si no hay suficiente cuota disponible en tu suscripción, el modelo puede no ser capaz de responder.

    Deberías ver una salida similar a la siguiente:

    ```yaml
    MessageRole.AGENT:
    Here are the current inventory levels:

    - Moisturizer: 6
    - Shampoo: 8
    - Body Spray: 28
    - Hair Gel: 5
    - Lip Balm: 12
    - Skin Serum: 9
    - Cleanser: 30
    - Conditioner: 3
    - Setting Powder: 17
    - Dry Shampoo: 45
    ```

6. Puedes continuar la conversación si lo deseas. El thread es *stateful*, por lo que retiene el historial de la conversación, lo que significa que el agente tiene el contexto completo para cada respuesta.

    Intenta ingresar prompts como:

    ```yaml
    Are there any products that should be restocked?
    ```

    ```yaml
    Which products would you recommend for clearance?
    ```

    ```yaml
    What are the best sellers this week?
    ```

    Ingresa `quit` cuando hayas terminado.

## Limpieza

Ahora que has terminado el ejercicio, debes eliminar los recursos en la nube que has creado para evitar un uso innecesario de recursos.

1. Abre el [portal de Azure](https://portal.azure.com) en `https://portal.azure.com` y visualiza el contenido del resource group donde implementaste los recursos del hub utilizados en este ejercicio.
2. En la barra de herramientas, selecciona **Delete resource group**.
3. Ingresa el nombre del resource group y confirma que quieres eliminarlo.
