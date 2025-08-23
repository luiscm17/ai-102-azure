# Conectar agentes de IA a herramientas usando el Protocolo de Contexto de Modelo (MCP)

En este ejercicio, crearás un agente que puede conectarse a un servidor MCP y descubrir automáticamente funciones invocables.

Construirás un agente simple de evaluación de inventario para un minorista de cosméticos. Usando el servidor MCP, el agente podrá recuperar información sobre el inventario y hacer sugerencias de reabastecimiento o liquidación.

> **Tip**: El código utilizado en este ejercicio se basa en los SDKs de Azure AI Foundry y MCP para Python. Puedes desarrollar soluciones similares usando los SDKs para Microsoft .NET. Consulta [Bibliotecas cliente del SDK de Azure AI Foundry](https://learn.microsoft.com/es-es/azure/ai-foundry/how-to/develop/sdk-overview) y [SDK de MCP para C#](https://modelcontextprotocol.github.io/csharp-sdk/api/ModelContextProtocol.html) para más detalles.

Este ejercicio debería tomar aproximadamente **30** minutos en completarse.

> **Nota**: Algunas de las tecnologías utilizadas en este ejercicio están en vista previa o en desarrollo activo. Puedes experimentar algún comportamiento inesperado, advertencias o errores.

## Crear un proyecto de Azure AI Foundry

Comencemos creando un proyecto de Azure AI Foundry.

1. En un navegador web, abre el [portal de Azure AI Foundry](https://ai.azure.com) en `https://ai.azure.com` e inicia sesión usando tus credenciales de Azure. Cierra cualquier panel de consejos o inicio rápido que se abra la primera vez que inicies sesión y, si es necesario, usa el logotipo de **Azure AI Foundry** en la parte superior izquierda para navegar a la página de inicio, que se ve similar a la siguiente imagen (cierra el panel **Help** si está abierto):

    ![Captura de pantalla del portal de Azure AI Foundry.](./Media/ai-foundry-home.png)

1. En la página de inicio, selecciona **Create an agent**.
1. Cuando se te solicite crear un proyecto, ingresa un nombre válido para tu proyecto y expande **Advanced options**.
1. Confirma la siguiente configuración para tu proyecto:
    - **Azure AI Foundry resource**: *Un nombre válido para tu recurso de Azure AI Foundry*
    - **Subscription**: *Tu suscripción de Azure*
    - **Resource group**: *Crea o selecciona un grupo de recursos*
    - **Region**: *Selecciona cualquier **ubicación admitida para AI Services***\*

    > \* Algunos recursos de Azure AI están limitados por cuotas regionales de modelos. En caso de que se exceda un límite de cuota más adelante en el ejercicio, existe la posibilidad de que necesites crear otro recurso en una región diferente.

1. Selecciona **Create** y espera a que se cree tu proyecto.
1. Si se te solicita, implementa un modelo **gpt-4o** usando la opción de implementación *Global Standard* o *Standard* (dependiendo de la disponibilidad de tu cuota).

    >**Nota**: Si hay cuota disponible, un modelo base GPT-4o puede implementarse automáticamente al crear tu Agente y proyecto.

1. Cuando se cree tu proyecto, se abrirá el **Agents playground**.

1. En el panel de navegación de la izquierda, selecciona **Overview** para ver la página principal de tu proyecto; que se ve así:

    ![Captura de pantalla de la página de overview de un proyecto de Azure AI Foundry.](./Media/ai-foundry-project.png)

1. Copia el valor del **Azure AI Foundry project endpoint** a un bloc de notas, ya que lo usarás para conectarte a tu proyecto en una aplicación cliente.

## Desarrollar un agente que utilice herramientas de función MCP

Ahora que has creado tu proyecto en AI Foundry, desarrollemos una aplicación que integre un agente de IA con un servidor MCP.

### Clonar el repositorio que contiene el código de la aplicación

1. Abre una nueva pestaña del navegador (manteniendo el portal de Azure AI Foundry abierto en la pestaña existente). Luego, en la nueva pestaña, navega al [portal de Azure](https://portal.azure.com) en `https://portal.azure.com`; inicia sesión con tus credenciales de Azure si se te solicita.

    Cierra cualquier notificación de bienvenida para ver la página de inicio del portal de Azure.

1. Usa el botón **[\>_]** a la derecha de la barra de búsqueda en la parte superior de la página para crear un nuevo Cloud Shell en el portal de Azure, seleccionando un entorno de ***PowerShell*** sin almacenamiento en tu suscripción.

    El cloud shell proporciona una interfaz de línea de comandos en un panel en la parte inferior del portal de Azure. Puedes redimensionar o maximizar este panel para que sea más fácil trabajar en él.

    > **Nota**: Si anteriormente creaste un cloud shell que usa un entorno *Bash*, cámbialo a ***PowerShell***.

1. En la barra de herramientas del cloud shell, en el menú **Settings**, selecciona **Go to Classic version** (esto es necesario para usar el editor de código).

    **<font color="red">Asegúrate de haber cambiado a la versión clásica del cloud shell antes de continuar.</font>**

1. En el panel del cloud shell, ingresa los siguientes comandos para clonar el repositorio de GitHub que contiene los archivos de código para este ejercicio (escribe el comando, o cópialo al portapapeles y luego haz clic derecho en la línea de comandos y pega como texto sin formato):

    ```bash
   rm -r ai-agents -f
   git clone https://github.com/MicrosoftLearning/mslearn-ai-agents ai-agents
    ```

    > **Tip**: A medida que ingreses comandos en el cloudshell, la salida puede ocupar una gran parte del búfer de pantalla y el cursor en la línea actual puede quedar oculto. Puedes limpiar la pantalla ingresando el comando `cls` para que sea más fácil enfocarse en cada tarea.

1. Ingresa el siguiente comando para cambiar el directorio de trabajo a la carpeta que contiene los archivos de código y listarlos todos.

    ```bash
   cd ai-agents/Labfiles/03d-use-agent-tools-with-mcp/Python
   ls -a -l
    ```

    Los archivos proporcionados incluyen el código de la aplicación cliente y servidor. El Protocolo de Contexto de Modelo proporciona una forma estandarizada de conectar modelos de IA a diferentes fuentes de datos y herramientas. Separamos `client.py` y `server.py` para mantener la lógica del agente y las definiciones de herramientas modulares y simular una arquitectura del mundo real.

    `server.py` define las herramientas que el agente puede usar, simulando servicios backend o lógica de negocio.
    `client.py` maneja la configuración del agente de IA, los prompts del usuario y la invocación de las herramientas cuando sea necesario.

### Configurar los ajustes de la aplicación

1. En el panel de la línea de comandos del cloud shell, ingresa el siguiente comando para instalar las bibliotecas que usarás:

    ```bash
   python -m venv labenv
   ./labenv/bin/Activate.ps1
   pip install -r requirements.txt azure-ai-projects mcp
    ```

    >**Nota:** Puedes ignorar cualquier mensaje de advertencia o error mostrado durante la instalación de la biblioteca.

1. Ingresa el siguiente comando para editar el archito de configuración que se ha proporcionado:

    ```bash
   code .env
    ```

    El archivo se abre en un editor de código.

1. En el archivo de código, reemplaza el marcador de posición **your_project_endpoint** con el endpoint de tu proyecto (copiado de la página **Overview** del proyecto en el portal de Azure AI Foundry) y asegúrate de que la variable MODEL_DEPLOYMENT_NAME esté configurada con el nombre de tu implementación de modelo (que debería ser *gpt-4o*).

1. Después de haber reemplazado el marcador de posición, usa el comando **CTRL+S** para guardar tus cambios y luego usa el comando **CTRL+Q** para cerrar el editor de código mientras mantienes abierta la línea de comandos del cloud shell.

### Implementar un Servidor MCP

Un Servidor del Protocolo de Contexto de Modelo (MCP) es un componente que aloja herramientas invocables. Estas herramientas son funciones de Python que pueden ser expuestas a agentes de IA. Cuando las herramientas se anotan con `@mcp.tool()`, se vuelven descubribles para el cliente, permitiendo que un agente de IA las llame dinámicamente durante una conversación o tarea. En esta tarea, agregarás algunas herramientas que permitirán al agente realizar verificaciones de inventario.

1. Ingresa el siguiente comando para editar el archivo de código que se ha proporcionado para tu código de función:

    ```bash
   code server.py
    ```

    En este archivo de código, definirás las herramientas que el agente puede usar para simular un servicio backend para la tienda minorista. Observa el código de configuración del servidor en la parte superior del archivo. Utiliza `FastMCP` para levantar rápidamente una instancia de servidor MCP llamada "Inventory". Este servidor alojará las herramientas que defines y las hará accesibles al agente durante el laboratorio.

1. Encuentra el comentario **Add an inventory check tool** y agrega el siguiente código:

    ```python
   # Add an inventory check tool
   @mcp.tool()
   def get_inventory_levels() -> dict:
        """Returns current inventory for all products."""
        return {
            "Moisturizer": 6,
            "Shampoo": 8,
            "Body Spray": 28,
            "Hair Gel": 5, 
            "Lip Balm": 12,
            "Skin Serum": 9,
            "Cleanser": 30,
            "Conditioner": 3,
            "Setting Powder": 17,
            "Dry Shampoo": 45
        }
    ```

    Este diccionario representa un inventario de ejemplo. La anotación `@mcp.tool()` permitirá que el LLM descubra tu función.

1. Encuentra el comentario **Add a weekly sales tool** y agrega el siguiente código:

    ```python
   # Add a weekly sales tool
   @mcp.tool()
   def get_weekly_sales() -> dict:
        """Returns number of units sold last week."""
        return {
            "Moisturizer": 22,
            "Shampoo": 18,
            "Body Spray": 3,
            "Hair Gel": 2,
            "Lip Balm": 14,
            "Skin Serum": 19,
            "Cleanser": 4,
            "Conditioner": 1,
            "Setting Powder": 13,
            "Dry Shampoo": 17
        }
    ```

1. Guarda el archivo (*CTRL+S*).

### Implementar un Cliente MCP

Un cliente MCP es el componente que se conecta al servidor MCP para descubrir e invocar herramientas. Puedes pensarlo como el puente entre el agente y las funciones alojadas en el servidor, permitiendo el uso dinámico de herramientas en respuesta a prompts de usuario.

1. Ingresa el siguiente comando para comenzar a editar el código del cliente.

    ```bash
   code client.py
    ```

    > **Tip**: A medida que agregues código al archivo de código, asegúrate de mantener la indentación correcta.

1. Encuentra el comentario **Add references** y agrega el siguiente código para importar las clases:

    ```python
   # Add references
   from mcp import ClientSession, StdioServerParameters
   from mcp.client.stdio import stdio_client
   from azure.ai.agents import AgentsClient
   from azure.ai.agents.models import FunctionTool, MessageRole, ListSortOrder
   from azure.identity import DefaultAzureCredential
    ```

1. Encuentra el comentario **Start the MCP server** y agrega el siguiente código:

    ```python
   # Start the MCP server
   stdio_transport = await exit_stack.enter_async_context(stdio_client(server_params))
   stdio, write = stdio_transport
    ```

    En una configuración de producción estándar, el servidor se ejecutaría por separado del cliente. Pero por el bien de este laboratorio, el cliente es responsable de iniciar el servidor usando transporte de entrada/salida estándar. Esto crea un canal de comunicación ligero entre los dos componentes y simplifica la configuración de desarrollo local.

1. Encuentra el comentario **Create an MCP client session** y agrega el siguiente código:

    ```python
   # Create an MCP client session
   session = await exit_stack.enter_async_context(ClientSession(stdio, write))
   await session.initialize()
    ```

    Esto crea una nueva sesión de cliente usando los flujos de entrada y salida del paso anterior. Llamar a `session.initialize` prepara la sesión para descubrir e invocar herramientas que están registradas en el servidor MCP.

1. Debajo del comentario **List available tools**, agrega el siguiente código para verificar que el cliente se haya conectado al servidor:

    ```python
   # List available tools
   response = await session.list_tools()
   tools = response.tools
   print("\nConnected to server with tools:", [tool.name for tool in tools]) 
    ```

    Ahora tu sesión de cliente está lista para usar con tu Agente de Azure AI.

### Conectar las herramientas MCP a tu agente

En esta tarea, prepararás el agente de IA, aceptarás prompts de usuario e invocarás las herramientas de función.

1. Encuentra el comentario **Connect to the agents client** y agrega el siguiente código para conectarte al proyecto de Azure AI usando las credenciales actuales de Azure.

    ```python
   # Connect to the agents client
   agents_client = AgentsClient(
        endpoint=project_endpoint,
        credential=DefaultAzureCredential(
            exclude_environment_credential=True,
            exclude_managed_identity_credential=True
        )
   )
    ```

1. Debajo del comentario **List tools available on the server**, agrega el siguiente código:

    ```python
   # List tools available on the server
   response = await session.list_tools()
   tools = response.tools
    ```

1. Debajo del comentario **Build a function for each tool** y agrega el siguiente código:

    ```python
   # Build a function for each tool
   def make_tool_func(tool_name):
        async def tool_func(**kwargs):
            result = await session.call_tool(tool_name, kwargs)
            return result
        
        tool_func.__name__ = tool_name
        return tool_func

   functions_dict = {tool.name: make_tool_func(tool.name) for tool in tools}
   mcp_function_tool = FunctionTool(functions=list(functions_dict.values()))
    ```

    Este código envuelve dinámicamente las herramientas disponibles en el servidor MCP para que puedan ser llamadas por el agente de IA. Cada herramienta se convierte en una función async y luego se agrupa en un `FunctionTool` para que el agente la use.

1. Encuentra el comentario **Create the agent** y agrega el siguiente código:

    ```python
   # Create the agent
   agent = agents_client.create_agent(
        model=model_deployment,
        name="inventory-agent",
        instructions="""
        Eres un asistente de inventario. Aquí hay algunas pautas generales:
        - Recomienda reabastecer si el inventario del artículo < 10 y las ventas semanales > 15
        - Recomienda liquidación si el inventario del artículo > 20 y las ventas semanales < 5
        """,
        tools=mcp_function_tool.definitions
   )
    ```

1. Encuentra el comentario **Enable auto function calling** y agrega el siguiente código:

    ```python
   # Enable auto function calling
   agents_client.enable_auto_function_calls(tools=mcp_function_tool)
    ```

1. Debajo del comentario **Create a thread for the chat session**, agrega el siguiente código:

    ```python
   # Create a thread for the chat session
   thread = agents_client.threads.create()
    ```

1. Localiza el comentario **Invoke the prompt** y agrega el siguiente código:

    ```python
   # Invoke the prompt
   message = agents_client.messages.create(
        thread_id=thread.id,
        role=MessageRole.USER,
        content=user_input,
   )
   run = agents_client.runs.create(thread_id=thread.id, agent_id=agent.id)
    ```

1. Localiza el comentario **Retrieve the matching function tool** y agrega el siguiente código:

    ```python
   # Retrieve the matching function tool
   function_name = tool_call.function.name
   args_json = tool_call.function.arguments
   kwargs = json.loads(args_json)
   required_function = functions_dict.get(function_name)

   # Invoke the function
   output = await required_function(**kwargs)
    ```

    Este código utiliza la información de la llamada a herramienta del hilo del agente. El nombre de la función y los argumentos se recuperan y se usan para invocar la función coincidente.

1. Debajo del comentario **Append the output text**, agrega el siguiente código:

    ```python
   # Append the output text
   tool_outputs.append({
        "tool_call_id": tool_call.id,
        "output": output.content[0].text,
   })
    ```

1. Debajo del comentario **Submit the tool call output**, agrega el siguiente código:

    ```python
   # Submit the tool call output
   agents_client.runs.submit_tool_outputs(thread_id=thread.id, run_id=run.id, tool_outputs=tool_outputs)
    ```

    Este código señalará al hilo del agente que la acción requerida está completa y actualizará las salidas de la llamada a herramienta.

1. Encuentra el comentario **Display the response** y agrega el siguiente código:

    ```python
   # Display the response
   messages = agents_client.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
   for message in messages:
        if message.text_messages:
            last_msg = message.text_messages[-1]
            print(f"{message.role}:\n{last_msg.text.value}\n")
    ```

1. Guarda el archivo de código (*CTRL+S*) cuando hayas terminado. También puedes cerrar el editor de código (*CTRL+Q*); aunque quizás quieras mantenerlo abierto en caso de que necesites hacer alguna edición al código que agregaste. En cualquier caso, mantén abierto el panel de la línea de comandos del cloud shell.

### Iniciar sesión en Azure y ejecutar la aplicación

1. En el panel de la línea de comandos del cloud shell, ingresa el siguiente comando para iniciar sesión en Azure.

    ```bash
   az login
    ```

    **<font color="red">Debes iniciar sesión en Azure, incluso though la sesión del cloud shell ya está autenticada.</font>**

    > **Nota**: En la mayoría de los escenarios, solo usar *az login* será suficiente. Sin embargo, si tienes suscripciones en múltiples inquilinos, es posible que necesites especificar el inquilino usando el parámetro *--tenant*. Consulta [Iniciar sesión en Azure interactivamente usando la CLI de Azure](https://learn.microsoft.com/es-es/cli/azure/authenticate-azure-cli-interactively) para más detalles.

1. Cuando se te solicite, sigue las instrucciones para abrir la página de inicio de sesión en una nueva pestaña e ingresa el código de autenticación proporcionado y tus credenciales de Azure. Luego completa el proceso de inicio de sesión en la línea de comandos, seleccionando la suscripción que contiene tu hub de Azure AI Foundry si se te solicita.

1. Después de haber iniciado sesión, ingresa el siguiente comando para ejecutar la aplicación:

    ```bash
   python client.py
    ```

1. Cuando se te solicite, ingresa una consulta como:

    ```bash
   ¿Cuáles son los niveles de inventario actuales?
    ```

    > **Tip**: Si la aplicación falla porque se excede el límite de tasa. Espera unos segundos e intenta nuevamente. Si no hay suficiente cuota disponible en tu suscripción, el modelo podría no poder responder.

    Deberías ver una salida similar a la siguiente:

    ```yml
    MessageRole.AGENT:
    Aquí están los niveles de inventario actuales:

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

1. Puedes continuar la conversación si lo deseas. El hilo es *con estado*, por lo que retiene el historial de la conversación, lo que significa que el agente tiene el contexto completo para cada respuesta.

    Intenta ingresar prompts como:

    ```yml
   ¿Hay algún producto que deba reabastecerse?
    ```

    ```yml
   ¿Qué productos recomendarías para liquidación?
    ```

    ```yml
   ¿Cuáles son los mejores vendedores esta semana?
    ```

    Ingresa `quit` cuando hayas terminado.

## Limpieza

Ahora que has terminado el ejercicio, debes eliminar los recursos en la nube que creaste para evitar un uso innecesario de recursos.

1. Abre el [portal de Azure](https://portal.azure.com) en `https://portal.azure.com` y visualiza el contenido del grupo de recursos donde desplegaste los recursos del hub utilizados en este ejercicio.
1. En la barra de herramientas, selecciona **Delete resource group**.
1. Ingresa el nombre del grupo de recursos y confirma que deseas eliminarlo.
