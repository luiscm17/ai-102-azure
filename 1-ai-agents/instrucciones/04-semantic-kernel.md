---
lab:
    title: 'Desarrollar un agente de Azure AI con el SDK de Semantic Kernel'
    description: 'Aprende a usar el SDK de Semantic Kernel para crear y usar un agente del Servicio de Agentes de IA de Azure.'
---

# Desarrollar un agente de Azure AI con el SDK de Semantic Kernel

En este ejercicio, usarás el Servicio de Agentes de IA de Azure y Semantic Kernel para crear un agente de IA que procese reclamos de gastos.

> **Tip**: El código utilizado en este ejercicio se basa en el SDK de Semantic Kernel para Python. Puedes desarrollar soluciones similares usando los SDKs para Microsoft .NET y Java. Consulta [Lenguajes admitidos por Semantic Kernel](https://learn.microsoft.com/es-es/semantic-kernel/get-started/supported-languages) para más detalles.

Este ejercicio debería tomar aproximadamente **30** minutos en completarse.

> **Nota**: Algunas de las tecnologías utilizadas en este ejercicio están en vista previa o en desarrollo activo. Puedes experimentar algún comportamiento inesperado, advertencias o errores.

## Implementar un modelo en un proyecto de Azure AI Foundry

Comencemos implementando un modelo en un proyecto de Azure AI Foundry.

1. En un navegador web, abre el [portal de Azure AI Foundry](https://ai.azure.com) en `https://ai.azure.com` e inicia sesión usando tus credenciales de Azure. Cierra cualquier panel de consejos o inicio rápido que se abra la primera vez que inicies sesión y, si es necesario, usa el logotipo de **Azure AI Foundry** en la parte superior izquierda para navegar a la página de inicio, que se ve similar a la siguiente imagen (cierra el panel **Help** si está abierto):

    ![Captura de pantalla del portal de Azure AI Foundry.](./Media/ai-foundry-home.png)

1. En la página de inicio, en la sección **Explore models and capabilities**, busca el modelo `gpt-4o`; que usaremos en nuestro proyecto.
1. En los resultados de búsqueda, selecciona el modelo **gpt-4o** para ver sus detalles, y luego en la parte superior de la página del modelo, selecciona **Use this model**.
1. Cuando se te solicite crear un proyecto, ingresa un nombre válido para tu proyecto y expande **Advanced options**.
1. Confirma la siguiente configuración para tu proyecto:
    - **Azure AI Foundry resource**: *Un nombre válido para tu recurso de Azure AI Foundry*
    - **Subscription**: *Tu suscripción de Azure*
    - **Resource group**: *Crea o selecciona un grupo de recursos*
    - **Region**: *Selecciona cualquier **ubicación admitida para AI Services***\*

    > \* Algunos recursos de Azure AI están limitados por cuotas regionales de modelos. En caso de que se exceda un límite de cuota más adelante en el ejercicio, existe la posibilidad de que necesites crear otro recurso en una región diferente.

1. Selecciona **Create** y espera a que se cree tu proyecto, incluyendo la implementación del modelo gpt-4 que seleccionaste.
1. Cuando se cree tu proyecto, el chat playground se abrirá automáticamente.
1. En el panel **Setup**, observa el nombre de tu implementación de modelo; que debería ser **gpt-4o**. Puedes confirmarlo viendo la implementación en la página **Models and endpoints** (solo abre esa página en el panel de navegación de la izquierda).
1. En el panel de navegación de la izquierda, selecciona **Overview** para ver la página principal de tu proyecto; que se ve así:

    ![Captura de pantalla de los detalles de un proyecto de Azure AI en el portal de Azure AI Foundry.](./Media/ai-foundry-project.png)

## Crear una aplicación cliente de agente

Ahora estás listo para crear una aplicación cliente que define un agente y una función personalizada. Se te ha proporcionado algo de código en un repositorio de GitHub.

### Preparar el entorno

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

1. Cuando se haya clonado el repositorio, ingresa el siguiente comando para cambiar el directorio de trabajo a la carpeta que contiene los archivos de código y listarlos todos.

    ```bash
   cd ai-agents/Labfiles/04-semantic-kernel/python
   ls -a -l
    ```

    Los archivos proporcionados incluyen código de aplicación, un archivo para configuraciones y un archivo que contiene datos de gastos.

### Configurar los ajustes de la aplicación

1. En el panel de la línea de comandos del cloud shell, ingresa el siguiente comando para instalar las bibliotecas que usarás:

    ```bash
   python -m venv labenv
   ./labenv/bin/Activate.ps1
   pip install python-dotenv azure-identity semantic-kernel --upgrade 
    ```

    > **Nota**: Instalar *semantic-kernel* instala automáticamente una versión compatible de semantic kernel de *azure-ai-projects*.

1. Ingresa el siguiente comando para editar el archivo de configuración que se ha proporcionado:

    ```bash
    code .env
    ```

    El archivo se abre en un editor de código.

1. En el archivo de código, reemplaza el marcador de posición **your_project_endpoint** con el endpoint de tu proyecto (copiado de la página **Overview** del proyecto en el portal de Azure AI Foundry), y el marcador de posición **your_model_deployment** con el nombre que asignaste a tu implementación del modelo gpt-4o.
1. Después de haber reemplazado los marcadores de posición, usa el comando **CTRL+S** para guardar tus cambios y luego usa el comando **CTRL+Q** para cerrar el editor de código mientras mantienes abierta la línea de comandos del cloud shell.

### Escribir código para una aplicación de agente

> **Tip**: A medida que agregues código, asegúrate de mantener la indentación correcta. Usa los comentarios existentes como guía, ingresando el nuevo código al mismo nivel de indentación.

1. Ingresa el siguiente comando para editar el archivo de código del agente que se ha proporcionado:

    ```bash
    code semantic-kernel.py
    ```

1. Revisa el código en el archivo. Contiene:
    - Algunas declaraciones **import** para agregar referencias a espacios de nombres comúnmente usados
    - Una función *main* que carga un archivo que contiene datos de gastos, pregunta al usuario por instrucciones, y luego llama...
    - Una función **process_expenses_data** en la que se debe agregar el código para crear y usar tu agente
    - Una clase **EmailPlugin** que incluye una función kernel llamada **send_email**; que será usada por tu agente para simular la funcionalidad utilizada para enviar un correo electrónico.

1. En la parte superior del archivo, después de la declaración **import** existente, encuentra el comentario **Add references**, y agrega el siguiente código para referenciar los espacios de nombres en las bibliotecas que necesitarás para implementar tu agente:

    ```python
   # Add references
   from dotenv import load_dotenv
   from azure.identity.aio import DefaultAzureCredential
   from semantic_kernel.agents import AzureAIAgent, AzureAIAgentSettings, AzureAIAgentThread
   from semantic_kernel.functions import kernel_function
   from typing import Annotated
    ```

1. Cerca de la parte inferior del archivo, encuentra el comentario **Create a Plugin for the email functionality**, y agrega el siguiente código para definir una clase para un plugin que contiene una función que tu agente usará para enviar correo electrónico (los plugins son una forma de agregar funcionalidad personalizada a los agentes de Semantic Kernel)

    ```python
   # Create a Plugin for the email functionality
   class EmailPlugin:
       """A Plugin to simulate email functionality."""
    
       @kernel_function(description="Sends an email.")
       def send_email(self,
                      to: Annotated[str, "Who to send the email to"],
                      subject: Annotated[str, "The subject of the email."],
                      body: Annotated[str, "The text body of the email."]):
           print("\nTo:", to)
           print("Subject:", subject)
           print(body, "\n")
    ```

    > **Nota**: ¡La función *simula* el envío de un correo electrónico imprimiéndolo en la consola. En una aplicación real, ¡usarías un servicio SMTP o similar para enviar realmente el correo electrónico!

1. Volviendo arriba del nuevo código de la clase **EmailPlugin**, en la función **process_expenses_data**, encuentra el comentario **Get configuration settings**, y agrega el siguiente código para cargar el archivo de configuración y crear un objeto **AzureAIAgentSettings** (que incluirá automáticamente la configuración del Agente de IA de Azure desde la configuración).

    (Asegúrate de mantener el nivel de indentación)

    ```python
   # Get configuration settings
   load_dotenv()
   ai_agent_settings = AzureAIAgentSettings()
    ```

1. Encuentra el comentario **Connect to the Azure AI Foundry project**, y agrega el siguiente código para conectarte a tu proyecto de Azure AI Foundry usando las credenciales de Azure con las que has iniciado sesión actualmente.

    (Asegúrate de mantener el nivel de indentación)

    ```python
   # Connect to the Azure AI Foundry project
   async with (
        DefaultAzureCredential(
            exclude_environment_credential=True,
            exclude_managed_identity_credential=True) as creds,
        AzureAIAgent.create_client(
            credential=creds
        ) as project_client,
   ):
    ```

1. Encuentra el comentario **Define an Azure AI agent that sends an expense claim email**, y agrega el siguiente código para crear una definición de Agente de IA de Azure para tu agente.

    (Asegúrate de mantener el nivel de indentación)

    ```python
   # Define an Azure AI agent that sends an expense claim email
   expenses_agent_def = await project_client.agents.create_agent(
        model= ai_agent_settings.model_deployment_name,
        name="expenses_agent",
        instructions="""Eres un asistente de IA para la presentación de reclamos de gastos.
                        Cuando un usuario envíe datos de gastos y solicite un reclamo de gastos, usa la función del plugin para enviar un correo electrónico a expenses@contoso.com con el asunto 'Expense Claim' y un cuerpo que contenga los gastos desglosados con un total.
                        Luego confirma al usuario que lo has hecho."""
   )
    ```

1. Encuentra el comentario **Create a semantic kernel agent**, y agrega el siguiente código para crear un objeto de agente de semantic kernel para tu agente de Azure AI, e incluye una referencia al plugin **EmailPlugin**.

    (Asegúrate de mantener el nivel de indentación)

    ```python
   # Create a semantic kernel agent
   expenses_agent = AzureAIAgent(
        client=project_client,
        definition=expenses_agent_def,
        plugins=[EmailPlugin()]
   )
    ```

1. Encuentra el comentario **Use the agent to process the expenses data**, y agrega el siguiente código para crear un hilo para que tu agente se ejecute, y luego invocarlo con un mensaje de chat.

    (Asegúrate de mantener el nivel de indentación):

    ```python
   # Use the agent to process the expenses data
   # If no thread is provided, a new thread will be
   # created and returned with the initial response
   thread: AzureAIAgentThread | None = None
   try:
        # Add the input prompt to a list of messages to be submitted
        prompt_messages = [f"{prompt}: {expenses_data}"]
        # Invoke the agent for the specified thread with the messages
        response = await expenses_agent.get_response(prompt_messages, thread=thread)
        # Display the response
        print(f"\n# {response.name}:\n{response}")
   except Exception as e:
        # Something went wrong
        print (e)
   finally:
        # Cleanup: Delete the thread and agent
        await thread.delete() if thread else None
        await project_client.agents.delete_agent(expenses_agent.id)
    ```

1. Revisa que el código completado para tu agente, usando los comentarios para ayudarte a entender lo que hace cada bloque de código, y luego guarda tus cambios de código (**CTRL+S**).
1. Mantén el editor de código abierto en caso de que necesites corregir algún error tipográfico en el código, pero redimensiona los panes para que puedas ver más de la línea de comandos de la consola.

### Iniciar sesión en Azure y ejecutar la aplicación

1. En el panel de la línea de comandos del cloud shell debajo del editor de código, ingresa el siguiente comando para iniciar sesión en Azure.

    ```bash
    az login
    ```

    **<font color="red">Debes iniciar sesión en Azure, incluso though la sesión del cloud shell ya está autenticada.</font>**

    > **Nota**: En la mayoría de los escenarios, solo usar *az login* será suficiente. Sin embargo, si tienes suscripciones en múltiples inquilinos, es posible que necesites especificar el inquilino usando el parámetro *--tenant*. Consulta [Iniciar sesión en Azure interactivamente usando la CLI de Azure](https://learn.microsoft.com/es-es/cli/azure/authenticate-azure-cli-interactively) para más detalles.

1. Cuando se te solicite, sigue las instrucciones para abrir la página de inicio de sesión en una nueva pestaña e ingresa el código de autenticación proporcionado y tus credenciales de Azure. Luego completa el proceso de inicio de sesión en la línea de comandos, seleccionando la suscripción que contiene tu hub de Azure AI Foundry si se te solicita.
1. Después de haber iniciado sesión, ingresa el siguiente comando para ejecutar la aplicación:

    ```bash
    python semantic-kernel.py
    ```

    La aplicación se ejecuta usando las credenciales de tu sesión autenticada de Azure para conectarse a tu proyecto y crear y ejecutar el agente.

1. Cuando se te pregunte qué hacer con los datos de gastos, ingresa el siguiente prompt:

    ```bash
    Enviar un reclamo de gastos
    ```

1. Cuando la aplicación haya terminado, revisa la salida. El agente debería haber compuesto un correo electrónico para un reclamo de gastos basado en los datos que se proporcionaron.

    > **Tip**: Si la aplicación falla porque se excede el límite de tasa. Espera unos segundos e intenta nuevamente. Si no hay suficiente cuota disponible en tu suscripción, el modelo podría no poder responder.

## Resumen

En este ejercicio, usaste el SDK del Servicio de Agentes de IA de Azure y Semantic Kernel para crear un agente.

## Limpieza

Si has terminado de explorar el Servicio de Agentes de IA de Azure, debes eliminar los recursos que has creado en este ejercicio para evitar incurrir en costos innecesarios de Azure.

1. Regresa a la pestaña del navegador que contiene el portal de Azure (o reabre el [portal de Azure](https://portal.azure.com) en `https://portal.azure.com` en una nueva pestaña del navegador) y visualiza el contenido del grupo de recursos donde desplegaste los recursos utilizados en este ejercicio.
1. En la barra de herramientas, selecciona **Delete resource group**.
1. Ingresa el nombre del grupo de recursos y confirma que deseas eliminarlo.
