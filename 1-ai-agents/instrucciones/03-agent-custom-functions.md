---
lab: 
    title: 'Usar una función personalizada en un agente de IA' 
    description: 'Aprende a usar funciones para agregar capacidades personalizadas a tus agentes.'
---

# Usar una función personalizada en un agente de IA

En este ejercicio, explorarás cómo crear un agente que puede usar funciones personalizadas como una herramienta para completar tareas. Construirás un agente de soporte técnico simple que puede recopilar detalles de un problema técnico y generar un ticket de soporte.

> **Sugerencia**: El código utilizado en este ejercicio se basa en el SDK para Python de Azure AI Foundry. Puedes desarrollar soluciones similares usando los SDK para Microsoft .NET, JavaScript y Java. Consulta [Bibliotecas cliente del SDK de Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/how-to/develop/sdk-overview) para obtener más detalles.

Este ejercicio debería tomar aproximadamente **30** minutos en completarse.

> **Nota**: Algunas de las tecnologías utilizadas en este ejercicio están en versión preliminar o en desarrollo activo. Es posible que experimentes un comportamiento inesperado, advertencias o errores.

## Crear un proyecto de Azure AI Foundry

Comencemos creando un proyecto de Azure AI Foundry.

1. En un navegador web, abre el [portal de Azure AI Foundry](https://ai.azure.com) en `https://ai.azure.com` e inicia sesión con tus credenciales de Azure. Cierra cualquier sugerencia o panel de inicio rápido que se abra la primera vez que inicies sesión, y si es necesario usa el logo de **Azure AI Foundry** en la parte superior izquierda para navegar a la página de inicio, que se ve similar a la siguiente imagen (cierra el panel de **Help** si está abierto):

    ![Screenshot of Azure AI Foundry portal.](./Media/ai-foundry-home.png)

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

    ![Screenshot of a Azure AI Foundry project overview page.](./Media/ai-foundry-project.png)

9. Copia los valores de **Azure AI Foundry project endpoint** en un bloc de notas, ya que los usarás para conectarte a tu proyecto en una aplicación cliente.

## Desarrollar un agente que use herramientas de función

Ahora que has creado tu proyecto en AI Foundry, desarrollemos una aplicación que implemente un agente usando herramientas de función personalizadas.

### Clonar el repositorio que contiene el código de la aplicación

1. Abre una nueva pestaña del navegador (manteniendo el portal de Azure AI Foundry abierto en la pestaña existente). Luego, en la nueva pestaña, navega al [portal de Azure](https://portal.azure.com) en `https://portal.azure.com`; iniciando sesión con tus credenciales de Azure si se te solicita.

    Cierra cualquier notificación de bienvenida para ver la página de inicio del portal de Azure.

2. Usa el botón **[\>_]** a la derecha de la barra de búsqueda en la parte superior de la página para crear un nuevo Cloud Shell en el portal de Azure, seleccionando un entorno **_PowerShell_** sin almacenamiento en tu suscripción.

    El cloud shell proporciona una interfaz de línea de comandos en un panel en la parte inferior del portal de Azure. Puedes cambiar el tamaño o maximizar este panel para que sea más fácil trabajar en él.

    > **Nota**: Si has creado previamente un cloud shell que usa un entorno _Bash_, cámbialo a **_PowerShell_**.

3. En la barra de herramientas del cloud shell, en el menú **Settings**, selecciona **Go to Classic version** (esto es necesario para usar el editor de código).

    **<font color="red">Asegúrate de haber cambiado a la versión clásica del cloud shell antes de continuar.</font>**

4. En el panel del cloud shell, ingresa los siguientes comandos para clonar el repositorio de GitHub que contiene los archivos de código para este ejercicio (escribe el comando, o cópialo al portapapeles y luego haz clic derecho en la línea de comandos y pégalo como texto sin formato):

    ```bash
    rm -r ai-agents -f
    git clone https://github.com/MicrosoftLearning/mslearn-ai-agents> ai-agents
    ```

    > **Sugerencia**: A medida que ingresas comandos en el cloudshell, la salida puede ocupar una gran cantidad del búfer de la pantalla y el cursor en la línea actual puede quedar oscurecido. Puedes limpiar la pantalla ingresando el comando `cls` para que sea más fácil concentrarse en cada tarea.

5. Ingresa el siguiente comando para cambiar el directorio de trabajo a la carpeta que contiene los archivos de código y listarlos todos.

    ```bash
    cd ai-agents/Labfiles/03-ai-agent-functions/Python
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

    > **Nota:** Puedes ignorar cualquier mensaje de advertencia o error que se muestre durante la instalación de la librería.

2. Ingresa el siguiente comando para editar el archivo de configuración que se ha proporcionado:

    ```bash
    code .env
    ```

    El archivo se abre en un editor de código.

3. En el archivo de código, reemplaza el marcador de posición **your_project_endpoint** con el endpoint de tu proyecto (copiado de la página **Overview** del proyecto en el portal de Azure AI Foundry) y asegúrate de que la variable MODEL_DEPLOYMENT_NAME esté configurada con el nombre de tu implementación de modelo (que debería ser _gpt-4o_).

4. Después de reemplazar el marcador de posición, usa el comando **CTRL+S** para guardar tus cambios y luego usa el comando **CTRL+Q** para cerrar el editor de código mientras mantienes la línea de comandos del cloud shell abierta.

### Definir una función personalizada

1. Ingresa el siguiente comando para editar el archivo de código que se ha proporcionado para el código de tu función:

    ```bash
    code user_functions.py
    ```

2. Encuentra el comentario **Create a function to submit a support ticket** y agrega el siguiente código, que genera un número de ticket y guarda un ticket de soporte como un archivo de texto.

    ```python
    # Create a function to submit a support ticket
    def submit_support_ticket(email_address: str, description: str) -> str:
        script_dir = Path(**file**).parent # Get the directory of the script
        ticket_number = str(uuid.uuid4()).replace['-', ''](:6)
        file_name = f"ticket-{ticket_number}.txt"
        file_path = script_dir / file_name
        text = f"Support ticket: {ticket_number}\nSubmitted by: {email_address}\nDescription:\n{description}"
        file_path.write_text(text)

        message_json = json.dumps({"message": f"Support ticket {ticket_number} submitted. The ticket file is saved as {file_name}"})
        return message_json
    ```

3. Encuentra el comentario **Define a set of callable functions** y agrega el siguiente código, que define estáticamente un conjunto de funciones invocables en este archivo de código (en este caso, solo hay una, pero en una solución real podrías tener múltiples funciones que tu agente puede llamar):

    ```python
    # Define a set of callable functions
    user_functions: Set[Callable[..., Any]] = {
        submit_support_ticket
    }
    ```

4. Guarda el archivo (_CTRL+S_).

### Escribir código para implementar un agente que pueda usar tu función

1. Ingresa el siguiente comando para comenzar a editar el código del agente.

    ```bash
    code agent.py
    ```

    > **Sugerencia**: A medida que agregas código al archivo de código, asegúrate de mantener la sangría correcta.

2. Revisa el código existente, que recupera las configuraciones de la aplicación y configura un bucle en el que el usuario puede ingresar prompts para el agente. El resto del archivo incluye comentarios donde agregarás el código necesario para implementar tu agente de soporte técnico.

3. Encuentra el comentario **Add references** y agrega el siguiente código para importar las clases que necesitarás para construir un agente de Azure AI que use tu código de función como una herramienta:

    ```python
    # Add reference
    from azure.identity import DefaultAzureCredential
    from azure.ai.agents import AgentsClient
    from azure.ai.agents.models import FunctionTool, ToolSet, ListSortOrder, MessageRole
    from user_functions import user_functions
    ```

4. Encuentra el comentario **Connect to the Agent client** y agrega el siguiente código para conectarte al proyecto de Azure AI usando las credenciales de Azure actuales.

    > **Sugerencia**: Ten cuidado de mantener el nivel de sangría correcto.

    ```python
    # Connect to the Agent client
    agent_client = AgentsClient(
        endpoint=project_endpoint,
        credential=DefaultAzureCredential
        (exclude_environment_credential=True,
        exclude_managed_identity_credential=True)
    )
    ```

5. Encuentra la sección del comentario **Define an agent that can use the custom functions** y agrega el siguiente código para agregar tu código de función a un toolset, y luego crear un agente que pueda usar el toolset y un thread en el que ejecutar la sesión de chat.

    ```python
    # Define an agent that can use the custom functions
    with agent_client:

        functions = FunctionTool(user_functions)
        toolset = ToolSet()
        toolset.add(functions)
        agent_client.enable_auto_function_calls(toolset)

        agent = agent_client.create_agent(
            model=model_deployment,
            name="support-agent",
            instructions="""You are a technical support agent.
                        When a user has a technical issue, you get their email address and a description of the issue.
                        Then you use those values to submit a support ticket using the function available to you.
                        If a file is saved, tell the user the file name.
                     """,
            toolset=toolset
        )

        thread = agent_client.threads.create()
        print(f"You're chatting with: {agent.name} ({agent.id})")
    ```

6. Encuentra el comentario **Send a prompt to the agent** y agrega el siguiente código para agregar el prompt del usuario como un mensaje y ejecutar el thread.

    ```python
    # Send a prompt to the agent
    message = agent_client.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_prompt
    )
    run = agent_client.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
    ```

    > **Nota**: El uso del método **create_and_process** para ejecutar el thread permite que el agente encuentre automáticamente tus funciones y decida usarlas basándose en sus nombres y parámetros. Como alternativa, podrías usar el método **create_run**, en cuyo caso serías responsable de escribir código para sondear el estado de la ejecución para determinar cuándo se requiere una llamada de función, llamar a la función y devolver los resultados al agente.

7. Encuentra el comentario **Check the run status for failures** y agrega el siguiente código para mostrar cualquier error que ocurra.

    ```python
    # Check the run status for failures
    if run.status == "failed":
        print(f"Run failed: {run.last_error}")
    ```

8. Encuentra el comentario **Show the latest response from the agent** y agrega el siguiente código para recuperar los mensajes del thread completado y mostrar el último que fue enviado por el agente.

    ```python
    # Show the latest response from the agent
    last_msg = agent_client.messages.get_last_message_text_by_role(
        thread_id=thread.id,
        role=MessageRole.AGENT,
    )
    if last_msg:
        print(f"Last Message: {last_msg.text.value}")
    ```

9. Encuentra el comentario **Get the conversation history** y agrega el siguiente código para imprimir los mensajes del thread de conversación; ordenándolos en secuencia cronológica.

    ```python
    # Get the conversation history
    print("\nConversation Log:\n")
    messages = agent_client.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
    for message in messages:
        if message.text_messages:
            last_msg = message.text_messages[-1]
            print(f"{message.role}: {last_msg.text.value}\n")
    ```

10. Encuentra el comentario **Clean up** y agrega el siguiente código para eliminar el agente y el thread cuando ya no sean necesarios.

    ```python
    # Clean up
    agent_client.delete_agent(agent.id)
    print("Deleted agent")
    ```

11. Revisa el código, usando los comentarios para entender cómo:

    - Agrega tu conjunto de funciones personalizadas a un toolset.
    - Crea un agente que usa el toolset.
    - Ejecuta un thread con un mensaje de prompt del usuario.
    - Verifica el estado de la ejecución en caso de que haya una falla.
    - Recupera los mensajes del thread completado y muestra el último enviado por el agente.
    - Muestra el historial de conversación.
    - Elimina el agente y el thread cuando ya no son necesarios.

12. Guarda el archivo de código (_CTRL+S_) cuando hayas terminado. También puedes cerrar el editor de código (_CTRL+Q_); aunque es posible que desees mantenerlo abierto en caso de que necesites hacer alguna edición al código que agregaste. En cualquier caso, mantén el panel de línea de comandos del cloud shell abierto.

### Iniciar sesión en Azure y ejecutar la aplicación

1. En el panel de línea de comandos del cloud shell, ingresa el siguiente comando para iniciar sesión en Azure.

    ```bash
    az login
    ```

    **<font color="red">Debes iniciar sesión en Azure, incluso si la sesión del cloud shell ya está autenticada.</font>**

    > **Nota**: En la mayoría de los escenarios, solo usar _az login_ será suficiente. Sin embargo, si tienes suscripciones en múltiples tenants, es posible que necesites especificar el tenant usando el parámetro _--tenant_. Consulta [Iniciar sesión en Azure de forma interactiva usando la CLI de Azure](https://learn.microsoft.com/cli/azure/authenticate-azure-cli-interactively) para obtener más detalles.

2. Cuando se te solicite, sigue las instrucciones para abrir la página de inicio de sesión en una nueva pestaña e ingresa el código de autenticación proporcionado y tus credenciales de Azure. Luego completa el proceso de inicio de sesión en la línea de comandos, seleccionando la suscripción que contiene tu hub de Azure AI Foundry si se te solicita.

3. Después de haber iniciado sesión, ingresa el siguiente comando para ejecutar la aplicación:

    ```bash
    python agent.py
    ```

    La aplicación se ejecuta usando las credenciales de tu sesión de Azure autenticada para conectarse a tu proyecto y crear y ejecutar el agente.

4. Cuando se te solicite, ingresa un prompt como:

    ```yml
    I have a technical problem
    ```

    > **Sugerencia**: Si la aplicación falla porque se excede el rate limit. Espera unos segundos e inténtalo de nuevo. Si no hay suficiente cuota disponible en tu suscripción, el modelo puede no ser capaz de responder.

5. Visualiza la respuesta. El agente puede pedir tu dirección de correo electrónico y una descripción del problema. Puedes usar cualquier dirección de correo electrónico (por ejemplo, `alex@contoso.com`) y cualquier descripción del problema (por ejemplo `my computer won't start`)

    Cuando tenga suficiente información, el agente debería elegir usar tu función según sea necesario.

6. Puedes continuar la conversación si lo deseas. El thread es _stateful_, por lo que retiene el historial de la conversación, lo que significa que el agente tiene el contexto completo para cada respuesta. Ingresa `quit` cuando hayas terminado.

7. Revisa los mensajes de la conversación que se recuperaron del thread y los tickets que se generaron.

8. La herramienta debería haber guardado los tickets de soporte en la carpeta de la aplicación. Puedes usar el comando `ls` para verificar, y luego usar el comando `cat` para ver el contenido del archivo, así:

    ```bash
    ls
    cat ticket-\<ticket_num\>.txt
    ```

## Limpieza

Ahora que has terminado el ejercicio, debes eliminar los recursos en la nube que has creado para evitar incurrir en costos innecesarios de Azure.

1. Abre el [portal de Azure](https://portal.azure.com) en `https://portal.azure.com` y visualiza el contenido del resource group donde implementaste los recursos del hub utilizados en este ejercicio.
2. En la barra de herramientas, selecciona **Delete resource group**.
3. Ingresa el nombre del resource group y confirma que quieres eliminarlo.
