---
lab:
    title: 'Desarrollar una solución multiagente con Azure AI Foundry' 
    description: 'Aprende a configurar múltiples agentes para colaborar usando el servicio Azure AI Foundry Agent.'
---

# Desarrollar una solución multiagente

En este ejercicio, crearás un proyecto que orquesta múltiples agentes de IA usando el servicio Azure AI Foundry Agent. Diseñarás una solución de IA que asiste con el triaje de tickets. Los agentes conectados evaluarán la prioridad del ticket, sugerirán una asignación de equipo y determinarán el nivel de esfuerzo requerido para completar el ticket. ¡Comencemos\!

> **Sugerencia**: El código utilizado en este ejercicio se basa en el SDK para Python de Azure AI Foundry. Puedes desarrollar soluciones similares usando los SDK para Microsoft .NET, JavaScript y Java. Consulta [Bibliotecas cliente del SDK de Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/how-to/develop/sdk-overview) para obtener más detalles.

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

## Crear una aplicación cliente de agente de IA

Ahora estás listo para crear una aplicación cliente que defina los agentes y las instrucciones. Se te ha proporcionado algo de código en un repositorio de GitHub.

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
    cd ai-agents/Labfiles/03b-build-multi-agent-solution/Python
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

### Crear agentes de IA

¡Ahora estás listo para crear los agentes para tu solución multiagente\! ¡Comencemos\!

1. Ingresa el siguiente comando para editar el archivo **agent\_triage.py**:

    ```bash
    code agent_triage.py
    ```

2. Revisa el código en el archivo, notando que contiene strings para cada nombre de agente e instrucciones.

3. Encuentra el comentario **Add references** y agrega el siguiente código para importar las clases que necesitarás:

    ```python
    # Add references
    from azure.ai.agents import AgentsClient
    from azure.ai.agents.models import ConnectedAgentTool, MessageRole, ListSortOrder, ToolSet, FunctionTool
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

    Ahora agregarás código que usa el AgentsClient para crear múltiples agentes, cada uno con un rol específico en el procesamiento de un ticket de soporte.

    > **Sugerencia**: Al agregar código subsiguiente, asegúrate de mantener el nivel de sangría correcto bajo la declaración `using agents_client:`.

6. Encuentra el comentario **Create an agent to prioritize support tickets**, e ingresa el siguiente código (teniendo cuidado de mantener el nivel de sangría correcto):

    ```python
    # Create an agent to prioritize support tickets
    priority_agent_name = "priority_agent"
    priority_agent_instructions = """
    Assess how urgent a ticket is based on its description.

    Respond with one of the following levels:
    - High: User-facing or blocking issues
    - Medium: Time-sensitive but not breaking anything
    - Low: Cosmetic or non-urgent tasks

    Only output the urgency level and a very brief explanation.
    """

    priority_agent = agents_client.create_agent(
        model=model_deployment,
        name=priority_agent_name,
        instructions=priority_agent_instructions
    )
    ```

7. Encuentra el comentario **Create an agent to assign tickets to the appropriate team**, e ingresa el siguiente código:

    ```python
    # Create an agent to assign tickets to the appropriate team
    team_agent_name = "team_agent"
    team_agent_instructions = """
    Decide which team should own each ticket.

    Choose from the following teams:
    - Frontend
    - Backend
    - Infrastructure
    - Marketing

    Base your answer on the content of the ticket. Respond with the team name and a very brief explanation.
    """

    team_agent = agents_client.create_agent(
        model=model_deployment,
        name=team_agent_name,
        instructions=team_agent_instructions
    )
    ```

8. Encuentra el comentario **Create an agent to estimate effort for a support ticket**, e ingresa el siguiente código:

    ```python
    # Create an agent to estimate effort for a support ticket
    effort_agent_name = "effort_agent"
    effort_agent_instructions = """
    Estimate how much work each ticket will require.

    Use the following scale:
    - Small: Can be completed in a day
    - Medium: 2-3 days of work
    - Large: Multi-day or cross-team effort

    Base your estimate on the complexity implied by the ticket. Respond with the effort level and a brief justification.
    """

    effort_agent = agents_client.create_agent(
        model=model_deployment,
        name=effort_agent_name,
        instructions=effort_agent_instructions
    )
    ```

    Hasta ahora, has creado tres agentes; cada uno de los cuales tiene un rol específico en el triaje de un ticket de soporte. Ahora creemos objetos **ConnectedAgentTool** para cada uno de estos agentes para que puedan ser usados por otros agentes.

9. Encuentra el comentario **Create connected agent tools for the support agents**, e ingresa el siguiente código:

    ```python
    # Create connected agent tools for the support agents
    priority_agent_tool = ConnectedAgentTool(
        id=priority_agent.id, 
        name=priority_agent_name, 
        description="Assess the priority of a ticket"
    )

    team_agent_tool = ConnectedAgentTool(
        id=team_agent.id, 
        name=team_agent_name, 
        description="Determines which team should take the ticket"
    )

    effort_agent_tool = ConnectedAgentTool(
        id=effort_agent.id, 
        name=effort_agent_name, 
        description="Determines the effort required to complete the ticket"
    )
    ```

    Ahora estás listo para crear un agente principal que coordinará el proceso de triaje de tickets, usando los agentes conectados según sea necesario.

10. Encuentra el comentario **Create an agent to triage support ticket processing by using connected agents**, e ingresa el siguiente código:

    ```python
    # Create an agent to triage support ticket processing by using connected agents
    triage_agent_name = "triage-agent"
    triage_agent_instructions = """
    Triage the given ticket. Use the connected tools to determine the ticket's priority, 
    which team it should be assigned to, and how much effort it may take.
    """

    triage_agent = agents_client.create_agent(
        model=model_deployment,
        name=triage_agent_name,
        instructions=triage_agent_instructions,
        tools=[
            priority_agent_tool.definitions[0],
            team_agent_tool.definitions[0],
            effort_agent_tool.definitions[0]
        ]
    )
    ```

    Ahora que has definido un agente principal, puedes enviarle un prompt y hacer que use los otros agentes para triar un problema de soporte.

11. Encuentra el comentario **Use the agents to triage a support issue**, e ingresa el siguiente código:

    ```python
    # Use the agents to triage a support issue
    print("Creating agent thread.")
    thread = agents_client.threads.create()  

    # Create the ticket prompt
    prompt = input("\nWhat's the support problem you need to resolve?: ")

    # Send a prompt to the agent
    message = agents_client.messages.create(
        thread_id=thread.id,
        role=MessageRole.USER,
        content=prompt,
    )   

    # Run the thread usng the primary agent
    print("\nProcessing agent thread. Please wait.")
    run = agents_client.runs.create_and_process(thread_id=thread.id, agent_id=triage_agent.id)
        
    if run.status == "failed":
        print(f"Run failed: {run.last_error}")

    # Fetch and display messages
    messages = agents_client.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
    for message in messages:
        if message.text_messages:
            last_msg = message.text_messages[-1]
            print(f"{message.role}:\n{last_msg.text.value}\n")

    ```

12. Encuentra el comentario **Clean up**, e ingresa el siguiente código para eliminar los agentes cuando ya no sean necesarios:

    ```python
    # Clean up
    print("Cleaning up agents:")
    agents_client.delete_agent(triage_agent.id)
    print("Deleted triage agent.")
    agents_client.delete_agent(priority_agent.id)
    print("Deleted priority agent.")
    agents_client.delete_agent(team_agent.id)
    print("Deleted team agent.")
    agents_client.delete_agent(effort_agent.id)
    print("Deleted effort agent.")
    ```

13. Usa el comando **CTRL+S** para guardar tus cambios en el archivo de código. Puedes mantenerlo abierto (en caso de que necesites editar el código para corregir cualquier error) o usar el comando **CTRL+Q** para cerrar el editor de código mientras mantienes la línea de comandos del cloud shell abierta.

### Iniciar sesión en Azure y ejecutar la aplicación

Ahora estás listo para ejecutar tu código y ver cómo tus agentes de IA colaboran.

1. En el panel de línea de comandos del cloud shell, ingresa el siguiente comando para iniciar sesión en Azure.

    ```bash
    az login
    ```

    **\<font color="red"\>Debes iniciar sesión en Azure, incluso si la sesión del cloud shell ya está autenticada.\</font\>**

    > **Nota**: En la mayoría de los escenarios, solo usar *az login* será suficiente. Sin embargo, si tienes suscripciones en múltiples tenants, es posible que necesites especificar el tenant usando el parámetro *--tenant*. Consulta [Iniciar sesión en Azure de forma interactiva usando la CLI de Azure](https://learn.microsoft.com/cli/azure/authenticate-azure-cli-interactively) para obtener más detalles.

2. Cuando se te solicite, sigue las instrucciones para abrir la página de inicio de sesión en una nueva pestaña e ingresa el código de autenticación proporcionado y tus credenciales de Azure. Luego completa el proceso de inicio de sesión en la línea de comandos, seleccionando la suscripción que contiene tu hub de Azure AI Foundry si se te solicita.

3. Después de haber iniciado sesión, ingresa el siguiente comando para ejecutar la aplicación:

    ```bash
    python agent_triage.py
    ```

4. Ingresa un prompt, como `Users can't reset their password from the mobile app.`

    Después de que los agentes procesen el prompt, deberías ver una salida similar a la siguiente:

    ```yml
    Creating agent thread.
    Processing agent thread. Please wait.

    MessageRole.USER:
    Users can't reset their password from the mobile app.

    MessageRole.AGENT:
    ### Ticket Assessment

    - **Priority:** High — This issue blocks users from resetting their passwords, limiting access to their accounts.
    - **Assigned Team:** Frontend Team — The problem lies in the mobile app's user interface or functionality.
    - **Effort Required:** Medium — Resolving this problem involves identifying the root cause, potentially updating the mobile app functionality, reviewing API/backend integration, and testing to ensure compatibility across Android/iOS platforms.

    Cleaning up agents:
    Deleted triage agent.
    Deleted priority agent.
    Deleted team agent.
    Deleted effort agent.
    ```

    Puedes intentar modificar el prompt usando un escenario de ticket diferente para ver cómo colaboran los agentes. Por ejemplo, "Investigate occasional 502 errors from the search endpoint."

## Limpieza

Si has terminado de explorar el servicio Azure AI Agent, debes eliminar los recursos que has creado en este ejercicio para evitar incurrir en costos innecesarios de Azure.

1. Regresa a la pestaña del navegador que contiene el portal de Azure (o vuelve a abrir el [portal de Azure](https://portal.azure.com) en `https://portal.azure.com` en una nueva pestaña del navegador) y visualiza el contenido del resource group donde implementaste los recursos utilizados en este ejercicio.

2. En la barra de herramientas, selecciona **Delete resource group**.

3. Ingresa el nombre del resource group y confirma que quieres eliminarlo.
