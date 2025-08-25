---
lab:
    title: 'Desarrollar una app de chat con audio'
    description: 'Aprende cómo usar Azure AI Foundry para construir una app de IA generativa que soporte entrada de audio.'
---

# Desarrollar una app de chat con audio

En este ejercicio, usas el modelo de IA generativa *Phi-4-multimodal-instruct* para generar respuestas a prompts que incluyen archivos de audio. Desarrollarás una app que proporciona asistencia de IA para una empresa proveedora de productos usando Azure AI Foundry y el SDK de OpenAI para Python para resumir mensajes de voz dejados por clientes.

Si bien este ejercicio está basado en Python, puedes desarrollar aplicaciones similares usando múltiples SDKs específicos de lenguaje; incluyendo:

- [Azure AI Projects para Python](https://pypi.org/project/azure-ai-projects)
- [Biblioteca OpenAI para Python](https://pypi.org/project/openai/)
- [Azure AI Projects para Microsoft .NET](https://www.nuget.org/packages/Azure.AI.Projects)
- [Biblioteca cliente de Azure OpenAI para Microsoft .NET](https://www.nuget.org/packages/Azure.AI.OpenAI)
- [Azure AI Projects para JavaScript](https://www.npmjs.com/package/@azure/ai-projects)
- [Biblioteca de Azure OpenAI para TypeScript](https://www.npmjs.com/package/@azure/openai)

Este ejercicio toma aproximadamente **30** minutos.

## Crear un proyecto de Azure AI Foundry

Comencemos implementando un modelo en un proyecto de Azure AI Foundry.

1. En un navegador web, abre el [portal de Azure AI Foundry](https://ai.azure.com) en `https://ai.azure.com` e inicia sesión usando tus credenciales de Azure. Cierra cualquier consejo o paneles de inicio rápido que se abran la primera vez que inicies sesión, y si es necesario usa el logo **Azure AI Foundry** en la parte superior izquierda para navegar a la página de inicio, que se ve similar a la siguiente imagen:

    ![Captura de pantalla del portal de Azure AI Foundry.](../media/ai-foundry-home.png)

1. En la página de inicio, en la sección **Explore models and capabilities**, busca el modelo `Phi-4-multimodal-instruct`; que usaremos en nuestro proyecto.
1. En los resultados de búsqueda, selecciona el modelo **Phi-4-multimodal-instruct** para ver sus detalles, y luego en la parte superior de la página del modelo, selecciona **Use this model**.
1. Cuando se solicite crear un proyecto, ingresa un nombre válido para tu proyecto y expande **Advanced options**.
1. Selecciona **Customize** y especifica la siguiente configuración para tu hub:
    - **Azure AI Foundry resource**: *Un nombre válido para tu recurso de Azure AI Foundry*
    - **Subscription**: *Tu suscripción de Azure*
    - **Resource group**: *Crea o selecciona un grupo de recursos*
    - **Region**: *Selecciona cualquier **AI Services supported location***\*

    > \* Algunos recursos de Azure AI están limitados por cuotas regionales de modelos. En caso de que se exceda un límite de cuota más adelante en el ejercicio, existe la posibilidad de que necesites crear otro recurso en una región diferente. Puedes verificar la disponibilidad regional más reciente para modelos específicos en la [documentación de Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/how-to/deploy-models-serverless-availability#region-availability)

1. Selecciona **Create** y espera a que tu proyecto sea creado.

    Puede tomar unos momentos para que la operación se complete.

1. Selecciona **Agree and Proceed** para aceptar los términos del modelo, luego selecciona **Deploy** para completar la implementación del modelo Phi.

1. Cuando tu proyecto esté creado, los detalles del modelo se abrirán automáticamente. Nota el nombre de tu implementación de modelo; que debería ser **Phi-4-multimodal-instruct**

1. En el panel de navegación a la izquierda, selecciona **Overview** para ver la página principal de tu proyecto; que se ve así:

    > **Nota**: Si se muestra un error *Insufficient permissions**, usa el botón **Fix me** para resolverlo.

    ![Captura de pantalla de una página de overview de proyecto de Azure AI Foundry.](../media/ai-foundry-project.png)

## Crear una aplicación cliente

Ahora que implementaste un modelo, puedes usar los SDKs de Azure AI Foundry y Azure AI Model Inference para desarrollar una aplicación que converse con él.

> **Tip**: Puedes elegir desarrollar tu solución usando Python o Microsoft C#. Sigue las instrucciones en la sección apropiada para tu lenguaje elegido.

### Preparar la configuración de la aplicación

1. En el portal de Azure AI Foundry, ve la página **Overview** de tu proyecto.
1. En el área **Project details**, nota el **Azure AI Foundry project endpoint**. Usarás este endpoint para conectarte a tu proyecto en una aplicación cliente.
1. Abre una nueva pestaña del navegador (manteniendo el portal de Azure AI Foundry abierto en la pestaña existente). Luego en la nueva pestaña, navega al [Azure portal](https://portal.azure.com) en `https://portal.azure.com`; iniciando sesión con tus credenciales de Azure si se solicita.

    Cierra cualquier notificación de bienvenida para ver la página de inicio de Azure portal.

1. Usa el botón **[\>_]** a la derecha de la barra de búsqueda en la parte superior de la página para crear un nuevo Cloud Shell en Azure portal, seleccionando un entorno ***PowerShell*** sin almacenamiento en tu suscripción.

    El cloud shell proporciona una interfaz de línea de comandos en un panel en la parte inferior de Azure portal. Puedes redimensionar o maximizar este panel para facilitar el trabajo.

    > **Nota**: Si previamente creaste un cloud shell que usa un entorno *Bash*, cámbialo a ***PowerShell***.

1. En la barra de herramientas del cloud shell, en el menú **Settings**, selecciona **Go to Classic version** (esto es requerido para usar el editor de código).

    **<font color="red">Asegúrate de haber cambiado a la versión clásica del cloud shell antes de continuar.</font>**

1. En el panel del cloud shell, ingresa los siguientes comandos para clonar el repositorio GitHub que contiene los archivos de código para este ejercicio (escribe el comando, o cópialo al portapapeles y luego haz clic derecho en la línea de comandos y pega como texto plano):

    ```bash
    rm -r mslearn-ai-audio -f
    git clone https://github.com/MicrosoftLearning/mslearn-ai-language
    ```

    > **Tip**: Al pegar comandos en el cloudshell, la salida puede ocupar una gran parte del búfer de pantalla. Puedes limpiar la pantalla ingresando el comando `cls` para facilitar el enfoque en cada tarea.

1. Después de que el repositorio haya sido clonado, navega a la carpeta que contiene los archivos de código de la aplicación:

    ```bash
    cd mslearn-ai-language/Labfiles/09-audio-chat/Python
    ```

1. En el panel de línea de comandos del cloud shell, ingresa el siguiente comando para instalar las bibliotecas que usarás:

    ```bash
    python -m venv labenv
    ./labenv/bin/Activate.ps1
    pip install -r requirements.txt azure-identity azure-ai-projects openai
    ```

1. Ingresa el siguiente comando para editar el archivo de configuración que ha sido proporcionado:

    ```bash
    code .env
    ```

    El archivo debería abrirse en un editor de código.

1. En el archivo de código, reemplaza el marcador de posición **your_project_endpoint** con el endpoint para tu proyecto (copiado de la página **Overview** del proyecto en el portal de Azure AI Foundry), y el marcador de posición **your_model_deployment** con el nombre que asignaste a tu implementación del modelo Phi-4-multimodal-instruct.

1. Después de que reemplaces los marcadores de posición, en el editor de código, usa el comando **CTRL+S** o **Clic derecho > Save** para guardar tus cambios y luego usa el comando **CTRL+Q** o **Clic derecho > Quit** para cerrar el editor de código mientras mantienes abierta la línea de comandos del cloud shell.

### Escribir código para conectarse a tu proyecto y obtener un cliente de chat para tu modelo

> **Tip**: A medida que agregas código, asegúrate de mantener la sangría correcta.

1. Ingresa el siguiente comando para editar el archivo de código:

    ```bash
    code audio-chat.py
    ```

1. En el archivo de código, nota las declaraciones existentes que han sido agregadas en la parte superior del archivo para importar los espacios de nombres necesarios del SDK. Luego, encuentra el comentario **Add references**, agrega el siguiente código para referenciar los espacios de nombres en las bibliotecas que instalaste previamente:

    ```python
   # Add references
   from azure.identity import DefaultAzureCredential
   from azure.ai.projects import AIProjectClient
    ```

1. En la función **main**, bajo el comentario **Get configuration settings**, nota que el código carga los valores de cadena de conexión del proyecto y nombre de implementación del modelo que definiste en el archivo de configuración.

1. Encuentra el comentario **Initialize the project client** y agrega el siguiente código para conectarte a tu proyecto de Azure AI Foundry:

    > **Tip**: Ten cuidado de mantener el nivel de sangría correcto para tu código.

    ```python
   # Initialize the project client
   project_client = AIProjectClient(            
       credential=DefaultAzureCredential(
           exclude_environment_credential=True,
           exclude_managed_identity_credential=True
       ),
       endpoint=project_endpoint,
   )
    ```

1. Encuentra el comentario **Get a chat client**, agrega el siguiente código para crear un objeto cliente para chatear con tu modelo:

    ```python
   # Get a chat client
   openai_client = project_client.get_openai_client(api_version="2024-10-21")
    ```

### Escribir código para enviar un prompt basado en audio

Antes de enviar el prompt, necesitamos codificar el archivo de audio para la solicitud. Luego podemos adjuntar los datos de audio al mensaje del usuario con un prompt para el LLM. Nota que el código incluye un bucle para permitir al usuario ingresar un prompt hasta que ingrese "quit".

1. Bajo el comentario **Encode the audio file**, ingresa el siguiente código para preparar el siguiente archivo de audio:

    <video controls src="https://github.com/MicrosoftLearning/mslearn-ai-language/raw/refs/heads/main/Instructions/media/avocados.mp4" title="A request for avocados" width="150"></video>

    ```python
   # Encode the audio file
   file_path = "https://github.com/MicrosoftLearning/mslearn-ai-language/raw/refs/heads/main/Labfiles/09-audio-chat/data/avocados.mp3"
   response = requests.get(file_path)
   response.raise_for_status()
   audio_data = base64.b64encode(response.content).decode('utf-8')
    ```

1. Bajo el comentario **Get a response to audio input**, agrega el siguiente código para enviar un prompt:

    ```python
   # Get a response to audio input
   response = openai_client.chat.completions.create(
       model=model_deployment,
       messages=[
           {"role": "system", "content": system_message},
           { "role": "user",
               "content": [
               { 
                   "type": "text",
                   "text": prompt
               },
               {
                   "type": "input_audio",
                   "input_audio": {
                       "data": audio_data,
                       "format": "mp3"
                   }
               }
           ] }
       ]
   )
   print(response.choices[0].message.content)
    ```

1. Usa el comando **CTRL+S** para guardar tus cambios en el archivo de código. También puedes cerrar el editor de código (**CTRL+Q**) si lo deseas.

### Iniciar sesión en Azure y ejecutar la app

1. En el panel de línea de comandos del cloud shell, ingresa el siguiente comando para iniciar sesión en Azure.

    ```bash
    az login
    ```

    **<font color="red">Debes iniciar sesión en Azure - incluso though la sesión del cloud shell ya está autenticada.</font>**

    > **Nota**: En la mayoría de los escenarios, solo usar *az login* será suficiente. Sin embargo, si tienes suscripciones en múltiples inquilinos, puede que necesites especificar el inquilino usando el parámetro *--tenant*. Consulta [Iniciar sesión en Azure interactivamente usando la CLI de Azure](https://learn.microsoft.com/cli/azure/authenticate-azure-cli-interactively) para detalles.

1. Cuando se solicite, sigue las instrucciones para abrir la página de inicio de sesión en una nueva pestaña e ingresa el código de autenticación proporcionado y tus credenciales de Azure. Luego completa el proceso de inicio de sesión en la línea de comandos, seleccionando la suscripción que contiene tu hub de Azure AI Foundry si se solicita.

1. En el panel de línea de comandos del cloud shell, ingresa el siguiente comando para ejecutar la app:

    ```bash
    python audio-chat.py
    ```

1. Cuando se solicite, ingresa el prompt:

    ```bash
    Can you summarize this customer's voice message?
    ```

1. Revisa la respuesta.

### Usar un archivo de audio diferente

1. En el editor de código para tu código de app, encuentra el código que agregaste previamente bajo el comentario **Encode the audio file**. Luego modifica la url de la ruta del archivo como sigue para usar un archivo de audio diferente para la solicitud (dejando el código existente después de la ruta del archivo):

    ```python
   # Encode the audio file
   file_path = "https://github.com/MicrosoftLearning/mslearn-ai-language/raw/refs/heads/main/Labfiles/09-audio-chat/data/fresas.mp3"
    ```

    El nuevo archivo suena así:

    <video controls src="https://github.com/MicrosoftLearning/mslearn-ai-language/raw/refs/heads/main/Instructions/media/fresas.mp4" title="A request for strawberries" width="150"></video>

1. Usa el comando **CTRL+S** para guardar tus cambios en el archivo de código. También puedes cerrar el editor de código (**CTRL+Q**) si lo deseas.

1. En el panel de línea de comandos del cloud shell debajo del editor de código, ingresa el siguiente comando para ejecutar la app:

    ```bash
    python audio-chat.py
    ```

1. Cuando se solicite, ingresa el siguiente prompt:

    ```bash
    Can you summarize this customer's voice message? Is it time-sensitive?
    ```

1. Revisa la respuesta. Luego ingresa `quit` para salir del programa.

    > **Nota**: En esta app simple, no hemos implementado lógica para retener el historial de conversación; por lo que el modelo tratará cada prompt como una nueva solicitud sin contexto del prompt anterior.

1. Puedes continuar ejecutando la app, eligiendo diferentes tipos de prompt y probando diferentes prompts. Cuando hayas terminado, ingresa `quit` para salir del programa.

    Si tienes tiempo, puedes modificar el código para usar un system prompt diferente y tus propios archivos de audio accesibles por internet.

    > **Nota**: En esta app simple, no hemos implementado lógica para retener el historial de conversación; por lo que el modelo tratará cada prompt como una nueva solicitud sin contexto del prompt anterior.

## Resumen

En este ejercicio, usaste Azure AI Foundry y el SDK de Azure AI Inference para crear una aplicación cliente que usa un modelo multimodal para generar respuestas a audio.

## Limpiar

Si has terminado de explorar Azure AI Foundry, deberías eliminar los recursos que has creado en este ejercicio para evitar incurrir en costos de Azure innecesarios.

1. Regresa a la pestaña del navegador que contiene el Azure portal (o re-abre el [Azure portal](https://portal.azure.com) en `https://portal.azure.com` en una nueva pestaña del navegador) y ve el contenido del grupo de recursos donde implementaste los recursos usados en este ejercicio.
1. En la barra de herramientas, selecciona **Delete resource group**.
1. Ingresa el nombre del grupo de recursos y confirma que quieres eliminarlo.
