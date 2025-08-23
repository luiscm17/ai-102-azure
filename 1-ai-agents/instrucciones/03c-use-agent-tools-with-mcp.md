---
lab:
    title: 'Conectar agentes de IA a un servidor MCP remoto'
    description: 'Aprende a integrar herramientas del Protocolo de Contexto de Modelo (MCP) con agentes de IA'
---

# Conectar agentes de IA a herramientas usando el Protocolo de Contexto de Modelo (MCP)

En este ejercicio, construirás un agente que se conecta a un servidor MCP alojado en la nube. El agente utilizará búsqueda con tecnología de IA para ayudar a los desarrolladores a encontrar respuestas precisas y en tiempo real de la documentación oficial de Microsoft. Esto es útil para construir asistentes que brinden soporte a desarrolladores con orientación actualizada sobre herramientas como Azure, .NET y Microsoft 365. El agente utilizará la herramienta proporcionada `microsoft_docs_search` para consultar la documentación y devolver resultados relevantes.

> **Tip**: El código utilizado en este ejercicio se basa en el repositorio de ejemplo de soporte MCP del servicio Azure AI Agent. Consulta [Azure OpenAI demos](https://github.com/retkowsky/Azure-OpenAI-demos/blob/main/Azure%20Agent%20Service/9%20Azure%20AI%20Agent%20service%20-%20MCP%20support.ipynb) o visita [Conectarse a servidores del Protocolo de Contexto de Modelo](https://learn.microsoft.com/es-es/azure/ai-foundry/agents/how-to/tools/model-context-protocol) para más detalles.

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
    - **Region**: *Selecciona cualquiera de las siguientes ubicaciones admitidas:* \*
      - West US 2
      - West US
      - Norway East
      - Switzerland North
      - UAE North
      - South India

    > \* Algunos recursos de Azure AI están limitados por cuotas regionales de modelos. En caso de que se exceda un límite de cuota más adelante en el ejercicio, existe la posibilidad de que necesites crear otro recurso en una región diferente.

1. Selecciona **Create** y espera a que se cree tu proyecto.

1. Si se te solicita, implementa un modelo **gpt-4o** usando la opción de implementación *Global Standard* o *Standard* (dependiendo de la disponibilidad de tu cuota).

    >**Nota**: Si hay cuota disponible, un modelo base GPT-4o puede implementarse automáticamente al crear tu Agente y proyecto.

1. Cuando se cree tu proyecto, se abrirá el **Agents playground**.

1. En el panel de navegación de la izquierda, selecciona **Overview** para ver la página principal de tu proyecto; que se ve así:

    ![Captura de pantalla de la página de overview de un proyecto de Azure AI Foundry.](./Media/ai-foundry-project.png)

1. Copia el valor del **Azure AI Foundry project endpoint**. Lo usarás para conectarte a tu proyecto en una aplicación cliente.

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
   cd ai-agents/Labfiles/03c-use-agent-tools-with-mcp/Python
   ls -a -l
    ```

### Configurar los ajustes de la aplicación

1. En el panel de la línea de comandos del cloud shell, ingresa el siguiente comando para instalar las bibliotecas que usarás:

    ```bash
   python -m venv labenv
   ./labenv/bin/Activate.ps1
   pip install -r requirements.txt --pre azure-ai-projects mcp
    ```

    >**Nota:** Puedes ignorar cualquier mensaje de advertencia o error mostrado durante la instalación de la biblioteca.

1. Ingresa el siguiente comando para editar el archivo de configuración que se ha proporcionado:

    ```bash
   code .env
    ```

    El archivo se abre en un editor de código.

1. En el archivo de código, reemplaza el marcador de posición **your_project_endpoint** con el endpoint de tu proyecto (copiado de la página **Overview** del proyecto en el portal de Azure AI Foundry) y asegúrate de que la variable MODEL_DEPLOYMENT_NAME esté configurada con el nombre de tu implementación de modelo (que debería ser *gpt-4o*).

1. Después de haber reemplazado el marcador de posición, usa el comando **CTRL+S** para guardar tus cambios y luego usa el comando **CTRL+Q** para cerrar el editor de código mientras mantienes abierta la línea de comandos del cloud shell.

### Conectar un Agente de Azure AI a un servidor MCP remoto

En esta tarea, te conectarás a un servidor MCP remoto, prepararás el agente de IA y ejecutarás un prompt de usuario.

1. Ingresa el siguiente comando para editar el archivo de código que se ha proporcionado:

    ```bash
   code client.py
    ```

    El archivo se abre en el editor de código.

1. Encuentra el comentario **Add references** y agrega el siguiente código para importar las clases:

    ```python
   # Add references
   from azure.identity import DefaultAzureCredential
   from azure.ai.agents import AgentsClient
   from azure.ai.agents.models import McpTool, ToolSet, ListSortOrder
    ```

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

1. Debajo del comentario **Initialize agent MCP tool**, agrega el siguiente código:

    ```python
   # Initialize agent MCP tool
   mcp_tool = McpTool(
        server_label=mcp_server_label,
        server_url=mcp_server_url,
   )
    
   mcp_tool.set_approval_mode("never")
    
   toolset = ToolSet()
   toolset.add(mcp_tool)
    ```

    Este código se conectará al servidor MCP remoto de Microsoft Learn Docs. Este es un servicio alojado en la nube que permite a los clientes acceder a información confiable y actualizada directamente de la documentación oficial de Microsoft.

1. Debajo del comentario **Create a new agent** y agrega el siguiente código:

    ```python
   # Create a new agent
   agent = agents_client.create_agent(
        model=model_deployment,
        name="my-mcp-agent",
        instructions="""
        You have access to an MCP server called `microsoft.docs.mcp` - this tool allows you to 
        search through Microsoft's latest official documentation. Use the available MCP tools 
        to answer questions and perform tasks."""
   )
    ```

    En este código, proporcionas instrucciones para el agente y le das las definiciones de herramientas MCP.

1. Encuentra el comentario **Create thread for communication** y agrega el siguiente código:

    ```python
   # Create thread for communication
   thread = agents_client.threads.create()
   print(f"Created thread, ID: {thread.id}")
    ```

1. Encuentra el comentario **Create a message on the thread** y agrega el siguiente código:

    ```python
   # Create a message on the thread
   prompt = input("\nHow can I help?: ")
   message = agents_client.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt,
   )
   print(f"Created message, ID: {message.id}")
    ```

1. Encuentra el comentario **Create and process agent run in thread with MCP tools** y agrega el siguiente código:

    ```python
   # Create and process agent run in thread with MCP tools
   run = agents_client.runs.create_and_process(thread_id=thread.id, agent_id=agent.id, toolset=toolset)
   print(f"Created run, ID: {run.id}")
    ```

    El Agente de IA invoca automáticamente las herramientas MCP conectadas para procesar la solicitud del prompt. Para ilustrar este proceso, el código proporcionado debajo del comentario **Display run steps and tool calls** mostrará cualquier herramienta invocada desde el servidor MCP.

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

1. Cuando se te solicite, ingresa una solicitud de información técnica como:

    ```bash
    Dame los comandos de la CLI de Azure para crear una Azure Container App con una identidad administrada.
    ```

1. Espera a que el agente procese tu prompt, usando el servidor MCP para encontrar una herramienta adecuada para recuperar la información solicitada. Deberías ver una salida similar a la siguiente:

    ```md
    Created agent, ID: <<agent-id>>
    MCP Server: mslearn at https://learn.microsoft.com/api/mcp
    Created thread, ID: <<thread-id>>
    Created message, ID: <<message-id>>
    Created run, ID: <<run-id>>
    Run completed with status: RunStatus.COMPLETED
    Step <<step1-id>> status: completed

    Step <<step2-id>> status: completed
    MCP Tool calls:
        Tool Call ID: <<tool-call-id>>
        Type: mcp
        Type: microsoft_docs_search


    Conversation:
    --------------------------------------------------
    ASSISTANT: Puedes usar la CLI de Azure para crear una Azure Container App con una identidad administrada (ya sea asignada por el sistema o asignada por el usuario). A continuación se muestran los comandos y el flujo de trabajo relevantes:

    ---

    ### **1. Crear un Grupo de Recursos**
    '''azurecli
    az group create --name myResourceGroup --location eastus
    '''
    

    {{continuado...}}

    Siguiendo estos pasos, puedes implementar una Azure Container App con identidades administradas asignadas por el sistema o asignadas por el usuario para integrarte perfectamente con otros servicios de Azure.
    --------------------------------------------------
    USER: Dame los comandos de la CLI de Azure para crear una Azure Container App con una identidad administrada.
    --------------------------------------------------
    Deleted agent
    ```

    Observa que el agente pudo invocar automáticamente la herramienta MCP `microsoft_docs_search` para cumplir con la solicitud.

1. Puedes ejecutar la aplicación nuevamente (usando el comando `python client.py`) para solicitar información diferente. En cada caso, el agente intentará encontrar documentación técnica utilizando la herramienta MCP.

## Limpieza

Ahora que has terminado el ejercicio, debes eliminar los recursos en la nube que creaste para evitar un uso innecesario de recursos.

1. Abre el [portal de Azure](https://portal.azure.com) en `https://portal.azure.com` y visualiza el contenido del grupo de recursos donde desplegaste los recursos del hub utilizados en este ejercicio.
1. En la barra de herramientas, selecciona **Delete resource group**.
1. Ingresa el nombre del grupo de recursos y confirma que deseas eliminarlo.
