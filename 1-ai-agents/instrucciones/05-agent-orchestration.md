---
lab:
    title: 'Desarrollar una solución multiagente con Semantic Kernel'
    description: 'Aprende a configurar múltiples agentes para colaborar usando el SDK de Semantic Kernel'
---

# Desarrollar una solución multiagente

En este ejercicio, practicarás usando el patrón de orquestación secuencial en el SDK de Semantic Kernel. Crearás una canalización simple de tres agentes que trabajan juntos para procesar comentarios de clientes y sugerir próximos pasos. Crearás los siguientes agentes:

- El agente Resumidor condensará los comentarios crudos en una oración corta y neutral.
- El agente Clasificador categorizará los comentarios como Positivo, Negativo o Solicitud de función.
- Finalmente, el agente de Acción Recomendada recomendará un paso de seguimiento apropiado.

Aprenderás cómo usar el SDK de Semantic Kernel para desglosar un problema, enrutarlo a través de los agentes correctos y producir resultados accionables. ¡Comencemos!

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

1. En el panel de navegación de la izquierda, selecciona **Models and endpoints** y selecciona tu implementación **gpt-4o**.

1. En el panel **Setup**, observa el nombre de tu implementación de modelo; que debería ser **gpt-4o**. Puedes confirmarlo viendo la implementación en la página **Models and endpoints** (solo abre esa página en el panel de navegación de la izquierda).

1. En el panel de navegación de la izquierda, selecciona **Overview** para ver la página principal de tu proyecto; que se ve así:

    ![Captura de pantalla de los detalles de un proyecto de Azure AI en el portal de Azure AI Foundry.](./Media/ai-foundry-project.png)

## Crear una aplicación cliente de Agente de IA

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

    > **Tip**: A medida que ingreses comandos en el cloud shell, la salida puede ocupar una gran parte del búfer de pantalla y el cursor en la línea actual puede quedar oculto. Puedes limpiar la pantalla ingresando el comando `cls` para que sea más fácil enfocarse en cada tarea.

1. Cuando se haya clonado el repositorio, ingresa el siguiente comando para cambiar el directorio de trabajo a la carpeta que contiene los archivos de código y listarlos todos.

    ```bash
    cd ai-agents/Labfiles/05-agent-orchestration/Python
    ls -a -l
    ```

    Los archivos proporcionados incluyen código de aplicación y un archivo para configuraciones.

### Configurar los ajustes de la aplicación

1. En el panel de la línea de comandos del cloud shell, ingresa el siguiente comando para instalar las bibliotecas que usarás:

    ```bash
    python -m venv labenv
    ./labenv/bin/Activate.ps1
    pip install python-dotenv azure-identity semantic-kernel --upgrade
    ```

    > **Nota**: Instalar *semantic-kernel* instala automáticamente una versión compatible de semantic kernel de *azure-ai-projects*.

1. Ingresa el siguiente comando para editar el archivo de configuración que se proporciona:

    ```bash
    code .env
    ```

    El archivo se abre en un editor de código.

1. En el archivo de código, reemplaza el marcador de posición **your_openai_endpoint** con el endpoint de Azure Open AI de tu proyecto (copiado de la página **Overview** del proyecto en el portal de Azure AI Foundry bajo **Azure OpenAI**). Reemplaza el marcador de posición **your_openai_api_key** con la API Key de tu proyecto, y asegúrate de que la variable MODEL_DEPLOYMENT_NAME esté configurada con el nombre de tu implementación de modelo (que debería ser *gpt-4o*).

1. Después de haber reemplazado los marcadores de posición, usa el comando **CTRL+S** para guardar tus cambios y luego usa el comando **CTRL+Q** para cerrar el editor de código mientras mantienes abierta la línea de comandos del cloud shell.

### Crear agentes de IA

¡Ahora estás listo para crear los agentes para tu solución multiagente! ¡Comencemos!

1. Ingresa el siguiente comando para editar el archivo **agents.py**:

    ```bash
    code agents.py
    ```

1. En la parte superior del archivo debajo del comentario **Add references**, y agrega el siguiente código para referenciar los espacios de nombres en las bibliotecas que necesitarás para implementar tu agente:

    ```python
   # Add references
   import asyncio
   from semantic_kernel.agents import Agent, ChatCompletionAgent, SequentialOrchestration
   from semantic_kernel.agents.runtime import InProcessRuntime
   from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
   from semantic_kernel.contents import ChatMessageContent
    ```

1. En la función **get_agents**, agrega el siguiente código debajo del comentario **Create a summarizer agent**:

    ```python
   # Create a summarizer agent
   summarizer_agent = ChatCompletionAgent(
       name="SummarizerAgent",
       instructions="""
       Resume los comentarios del cliente en una oración corta. Manténlo neutral y conciso.
       Ejemplo de salida:
       La aplicación se bloquea durante la carga de fotos.
       El usuario elogia la función de modo oscuro.
       """,
       service=AzureChatCompletion(),
   )
    ```

1. Agrega el siguiente código debajo del comentario **Create a classifier agent**:

    ```python
   # Create a classifier agent
   classifier_agent = ChatCompletionAgent(
       name="ClassifierAgent",
       instructions="""
       Clasifica los comentarios como uno de los siguientes: Positivo, Negativo o Solicitud de función.
       """,
       service=AzureChatCompletion(),
   )
    ```

1. Agrega el siguiente código debajo del comentario **Create a recommended action agent**:

    ```python
   # Create a recommended action agent
   action_agent = ChatCompletionAgent(
       name="ActionAgent",
       instructions="""
       Basado en el resumen y la clasificación, sugiere la siguiente acción en una oración corta.
       Ejemplo de salida:
       Escalar como un error de alta prioridad para el equipo móvil.
       Registrar como comentario positivo para compartir con diseño y marketing.
       Registrar como solicitud de mejora para el backlog de producto.
       """,
       service=AzureChatCompletion(),
   )
    ```

1. Agrega el siguiente código debajo del comentario **Return a list of agents**:

    ```python
   # Return a list of agents
   return [summarizer_agent, classifier_agent, action_agent]
    ```

    El orden de los agentes en esta lista será el orden en que se seleccionen durante la orquestación.

## Crear una orquestación secuencial

1. En la función **main**, encuentra el comentario **Initialize the input task** y agrega el siguiente código:

    ```python
   # Initialize the input task
   task="""
   Intenté actualizar mi foto de perfil varias veces hoy, pero la aplicación seguía congelándose a mitad del proceso. 
   Tuve que reiniciarla tres veces, y al final, la foto aún no se cargaba. 
   Es realmente frustrante y hace que la aplicación se sienta poco confiable.
   """
    ```

1. Debajo del comentario **Create a sequential orchestration**, agrega el siguiente código para definir una orquestación secuencial con un callback de respuesta:

    ```python
   # Create a sequential orchestration
   sequential_orchestration = SequentialOrchestration(
       members=get_agents(),
       agent_response_callback=agent_response_callback,
   )
    ```

    El `agent_response_callback` te permitirá ver la respuesta de cada agente durante la orquestación.

1. Agrega el siguiente código debajo del comentario **Create a runtime and start it**:

    ```python
   # Create a runtime and start it
   runtime = InProcessRuntime()
   runtime.start()
    ```

1. Agrega el siguiente código debajo del comentario **Invoke the orchestration with a task and the runtime**:

    ```python
   # Invoke the orchestration with a task and the runtime
   orchestration_result = await sequential_orchestration.invoke(
       task=task,
       runtime=runtime,
   )
    ```

1. Agrega el siguiente código debajo del comentario **Wait for the results**:

    ```python
   # Wait for the results
   value = await orchestration_result.get(timeout=20)
   print(f"\n****** Entrada de Tarea ******{task}")
   print(f"***** Resultado Final *****\n{value}")
    ```

    En este código, recuperas y muestras el resultado de la orquestación. Si la orquestación no se completa dentro del timeout especificado, se lanzará una excepción de timeout.

1. Encuentra el comentario **Stop the runtime when idle**, y agrega el siguiente código:

    ```python
   # Stop the runtime when idle
   await runtime.stop_when_idle()
    ```

    Después de que el procesamiento esté completo, detén el runtime para limpiar recursos.

1. Usa el comando **CTRL+S** para guardar tus cambios en el archivo de código. Puedes mantenerlo abierto (en caso de que necesites editar el código para corregir algún error) o usar el comando **CTRL+Q** para cerrar el editor de código mientras mantienes abierta la línea de comandos del cloud shell.

### Iniciar sesión en Azure y ejecutar la aplicación

Ahora estás listo para ejecutar tu código y ver a tus agentes de IA colaborar.

1. En el panel de la línea de comandos del cloud shell, ingresa el siguiente comando para iniciar sesión en Azure.

    ```bash
    az login
    ```

    **<font color="red">Debes iniciar sesión en Azure, incluso though la sesión del cloud shell ya está autenticada.</font>**

    > **Nota**: En la mayoría de los escenarios, solo usar *az login* será suficiente. Sin embargo, si tienes suscripciones en múltiples inquilinos, es posible que necesites especificar el inquilino usando el parámetro *--tenant*. Consulta [Iniciar sesión en Azure interactivamente usando la CLI de Azure](https://learn.microsoft.com/es-es/cli/azure/authenticate-azure-cli-interactively) para más detalles.

1. Cuando se te solicite, sigue las instrucciones para abrir la página de inicio de sesión en una nueva pestaña e ingresa el código de autenticación proporcionado y tus credenciales de Azure. Luego completa el proceso de inicio de sesión en la línea de comandos, seleccionando la suscripción que contiene tu hub de Azure AI Foundry si se te solicita.

1. Después de haber iniciado sesión, ingresa el siguiente comando para ejecutar la aplicación:

    ```bash
    python agents.py
    ```

    Deberías ver una salida similar a la siguiente:

    ```output
    # SummarizerAgent
    La aplicación se congela durante la carga de la foto de perfil, impidiendo la finalización.
    # ClassifierAgent
    Negativo
    # ActionAgent
    Escalar como un error de alta prioridad para el equipo de desarrollo.

    ****** Entrada de Tarea ******
    Intenté actualizar mi foto de perfil varias veces hoy, pero la aplicación seguía congelándose a mitad del proceso.
    Tuve que reiniciarla tres veces, y al final, la foto aún no se cargaba.
    Es realmente frustrante y hace que la aplicación se sienta poco confiable.

    ***** Resultado Final *****
    Escalar como un error de alta prioridad para el equipo de desarrollo.
    ```

1. Opcionalmente, puedes intentar ejecutar el código usando diferentes entradas de tarea, como:

    ```output
    Uso el dashboard todos los días para monitorear métricas, y funciona bien en general. Pero cuando trabajo tarde en la noche, la pantalla brillante es muy dura para mis ojos. Si agregaran una opción de modo oscuro, haría la experiencia mucho más cómoda.
    ```

    ```output
    Me comuniqué con su soporte al cliente ayer porque no podía acceder a mi cuenta. El representante respondió casi inmediatamente, fue amable y profesional, y resolvió el problema en minutos. Honestamente, fue una de las mejores experiencias de soporte que he tenido.
    ```

## Resumen

En este ejercicio, practicaste la orquestación secuencial con el SDK de Semantic Kernel, combinando múltiples agentes en un único flujo de trabajo optimizado. ¡Buen trabajo!

## Limpieza

Si has terminado de explorar el Servicio de Agentes de IA de Azure, debes eliminar los recursos que has creado en este ejercicio para evitar incurrir en costos innecesarios de Azure.

1. Regresa a la pestaña del navegador que contiene el portal de Azure (o reabre el [portal de Azure](https://portal.azure.com) en `https://portal.azure.com` en una nueva pestaña del navegador) y visualiza el contenido del grupo de recursos donde desplegaste los recursos utilizados en este ejercicio.

1. En la barra de herramientas, selecciona **Delete resource group**.

1. Ingresa el nombre del grupo de recursos y confirma que deseas eliminarlo.
