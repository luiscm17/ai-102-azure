# Explicación del script `agent.py`

## Explicación del Código de Conexión al Cliente de Agente

El fragmento de código que mencionas es fundamental para establecer la conexión con el servicio de Azure AI Agents. Vamos a desglosarlo:

```python
# Connect to the Agent client
agent_client = AgentsClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(
        exclude_enviroment_credential=True,
        exclude_managed_identity_credential=True
    )
)
```

### Componentes Explicados

**1. `AgentsClient`**

- **Qué es**: Es la clase principal del SDK de Azure AI Agents que permite interactuar con el servicio de agentes.
- **Para qué sirve**: Proporciona métodos para crear, gestionar y ejecutar agentes de IA.

**2. `endpoint=project_endpoint`**

- **project_endpoint**: Es la URL del punto de conexión de tu proyecto en Azure AI Foundry.
- **Ejemplo**: `"https://tu-proyecto.cognitiveservices.azure.com/"`
- **Importancia**: Especifica a qué instancia del servicio te estás conectando.

**3. `credential=DefaultAzureCredential(...)`**

- **DefaultAzureCredential**: Es una clase de autenticación que intenta varias formas de autenticación en orden.
- **Ventaja**: Permite diferentes formas de autenticación sin cambiar el código.

**4. `exclude_enviroment_credential=True`**

- **Propósito**: Desactiva la autenticación mediante variables de entorno.
- **Razón de uso**: Asegura que no se usen credenciales de variables de entorno, forzando otros métodos más seguros.

**5. `exclude_managed_identity_credential=True`**

- **Propósito**: Desactiva la autenticación mediante identidad administrada.
- **Razón de uso**: Si estás ejecutando el código localmente, probablemente no tengas una identidad administrada asignada, por lo que esta opción evita intentos de autenticación innecesarios.

### Flujo de Autenticación

Cuando se crea el `AgentsClient`, intentará autenticarse en este orden (a menos que se excluyan):

1. **Azure CLI** (si has hecho `az login`)
2. **Visual Studio Code** (si estás autenticado en la extensión de Azure)
3. **Visual Studio** (si estás autenticado)
4. **Azure PowerShell** (si estás autenticado)
5. **Interactive Browser** (abrirá una ventana del navegador para autenticación)

### Uso del Context Manager (`with`)

```python
with agent_client:
    # Código que usa el cliente
```

- **Propósito**: Asegura que los recursos de red se liberen correctamente.
- **Ventaja**: Cierra automáticamente la conexión cuando se sale del bloque `with`, incluso si ocurre un error.

Este patrón es esencial para trabajar con recursos que necesitan una limpieza adecuada, como conexiones de red.

## Explicación de la Creación del Agente

Este fragmento de código es donde se crea el agente de IA que analizará los datos. Vamos a desglosarlo:

```python
agent = agent_client.create_agent(
    model=model_deployment,  # Modelo de IA a utilizar
    name="data-agent-007",   # Nombre identificativo del agente
    instructions="You are an AI agent that analyzes the data in the file that has been uploaded. Use Python to calculate statistical metrics as necessary.",
    tools=code_interpreter.definitions,  # Definiciones de herramientas disponibles
    tool_resources=code_interpreter.resources,  # Recursos para las herramientas
)
```

### Parámetros Explicados

**1. `model=model_deployment`**

- **Qué es**: Especifica qué modelo de IA se utilizará.
- **Ejemplo**: Podría ser "gpt-4" o "gpt-5-mini".
- **Origen**: Se obtiene de la variable de entorno `MODEL_DEPLOYMENT_NAME`.

**2. `name="data-agent-007"`**

- **Propósito**: Identificador único para el agente.
- **Uso**: Útil para monitoreo y gestión de agentes.
- **Personalización**: Puedes cambiar este nombre según tus preferencias.

**3. `instructions=...`**

- **Contenido**: Instrucciones que definen el comportamiento del agente.
- **En este caso**:
  - Se define como un analista de datos.
  - Se le indica que use Python para cálculos estadísticos.
  - Se le recuerda que ya tiene acceso a un archivo cargado.

**4. `tools=code_interpreter.definitions`**

- **Qué es**: Define qué herramientas puede usar el agente.
- **En este caso**:
  - `code_interpreter` es una herramienta que permite ejecutar código Python.
  - `.definitions` contiene la especificación de cómo usar esta herramienta.

**5. `tool_resources=code_interpreter.resources`**

- **Qué es**: Recursos adicionales para las herramientas.
- **En este caso**:
  - Incluye el archivo de datos que se cargó previamente.
  - Permite al agente acceder y analizar estos datos.

### Flujo de Ejecución

1. **Creación**: El agente se crea con las especificaciones dadas.
2. **Configuración**: Se le asignan las herramientas y recursos necesarios.
3. **Preparación**: El agente está listo para recibir solicitudes y procesar datos.

### Uso Posterior

Una vez creado, el agente puede:

- Recibir preguntas o comandos.
- Usar Python para analizar los datos cargados.
- Proporcionar respuestas basadas en el análisis de los datos.

## Explicación de la Carga de Archivos y Creación de Hilos

### 1. Carga del Archivo y Creación del Intérprete de Código

```python
# Upload the data file and create a CodeInterpreterTool
file = agent_client.files.upload_and_poll(
    file_path=file_path, 
    purpose=FilePurpose.AGENTS
)
print(f"File uploaded: {file.filename}")
code_interpreter = CodeInterpreterTool(file_ids=[file.id])
```

**¿Qué hace?:**

1. **Sube el archivo**:
   - `upload_and_poll`: Sube el archivo al servicio y espera a que termine la carga.
   - `file_path`: Ruta local del archivo a subir.
   - `purpose=FilePurpose.AGENTS`: Indica que el archivo es para uso de agentes.

2. **Crea el intérprete de código**:
   - `CodeInterpreterTool`: Herramienta que permite ejecutar código Python.
   - `file_ids=[file.id]`: Asocia el archivo subido con el intérprete.

### 2. Creación del Hilo de Conversación

```python
# Create a thread for the conversation
thread = agent_client.threads.create()
```

**¿Qué hace?:**

- **Crea un hilo de conversación**:
  - `threads.create()`: Inicia una nueva conversación.
  - **Propósito**: Mantener el contexto de la conversación.
  - **Uso**: Todas las interacciones del usuario y respuestas del agente se almacenan aquí.

**Relación entre ambos:**

1. **Archivo**: Proporciona los datos para analizar.
2. **Hilo**: Mantiene el contexto de la conversación sobre esos datos.

## Explicación del Bucle de Conversación del Agente

Este fragmento de código maneja la interacción entre el usuario y el agente de IA. Vamos a desglosarlo:

### Estructura del Bucle

```python
while True:
    # 1. Obtener entrada del usuario
    user_prompt = input("Enter a prompt (or type 'quit' to exit): ")
    
    # 2. Condición de salida
    if user_prompt.lower() == "quit":
        break
        
    # 3. Validación de entrada vacía
    if len(user_prompt) == 0:
        print("Please enter a prompt.")
        continue

    # 4. Enviar mensaje al agente
    message = agent_client.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_prompt,
    )

    # 5. Procesar la solicitud
    run = agent_client.runs.create_and_process(
        thread_id=thread.id, 
        agent_id=agent.id
    )

    # 6. Manejar errores
    if run.status == "failed":
        print(f"Run failed: {run.last_error}")

    # 7. Obtener y mostrar respuesta
    last_msg = agent_client.messages.get_last_message_text_by_role(
        thread_id=thread.id,
        role=MessageRole.AGENT,
    )
    if last_msg:
        print(f"Last Message: {last_msg.text.value}")
```

### Explicación Detallada

**1. Entrada del Usuario:**

- **`input("Enter a prompt...")`**: Solicita al usuario que ingrese un mensaje.
- **Propósito**: Obtener la consulta o instrucción del usuario.

**2. Condición de Salida:**

- **`if user_prompt.lower() == "quit"`**: Verifica si el usuario quiere terminar.
- **Importante**: Permite salir del bucle infinito de manera controlada.

**3. Validación de Entrada:**

- **`if len(user_prompt) == 0`**: Verifica si el usuario no ingresó nada.
- **Propósito**: Evita procesar mensajes vacíos.

**4. Envío del Mensaje:**

- **`agent_client.messages.create()`**: Envía el mensaje al hilo de conversación.
- **Parámetros**:
  - `thread_id`: Identificador del hilo de conversación.
  - `role="user"`: Indica que el mensaje es del usuario.
  - `content`: El texto del mensaje.

**5. Procesamiento:**

- **`create_and_process()`**: Ejecuta el agente con el mensaje del usuario.
- **Parámetros**:
  - `thread_id`: El hilo donde está la conversación.
  - `agent_id`: El agente que procesará el mensaje.

**6. Manejo de Errores:**

- **`if run.status == "failed"`**: Verifica si hubo un error.
- **`run.last_error`**: Muestra detalles del error si ocurrió alguno.

**7. Obtención de Respuesta:**

- **`get_last_message_text_by_role()`**: Obtiene la última respuesta del agente.
- **Parámetros**:
  - `thread_id`: El hilo de la conversación.
  - `role=MessageRole.AGENT`: Filtra solo mensajes del agente.

### Flujo de la Conversación

1. El usuario escribe un mensaje.
2. El sistema verifica si debe terminar.
3. Si el mensaje no está vacío, lo envía al agente.
4. El agente procesa el mensaje.
5. Se verifica si hubo errores.
6. Se obtiene y muestra la respuesta del agente.
7. El ciclo se repite hasta que el usuario escriba "quit".

### Importancia de los Parámetros

- **`thread_id`**: Mantiene el contexto de la conversación.
- **`agent_id`**: Especifica qué agente procesará el mensaje.
- **`role`**: Define si el mensaje es del usuario o del agente.

## Explicación del Historial de Conversación

Este fragmento de código se encarga de recuperar y mostrar el historial completo de la conversación entre el usuario y el agente. Vamos a analizarlo:

```python
# Get the conversation history
print("\nConversation Log:\n")
messages = agent_client.messages.list(
    thread_id=thread.id,
    order=ListSortOrder.ASCENDING
)
for message in messages:
    if message.text_messages:
        last_msg = message.text_messages[-1]
        print(f"{message.role}: {last_msg.text.value}\n")
```

### Componentes Explicados del codigo del historial

**1. `agent_client.messages.list()`:**

- **Propósito**: Obtiene todos los mensajes de un hilo de conversación.
- **Parámetros**:
  - `thread_id`: Identificador único del hilo de conversación.
  - `order=ListSortOrder.ASCENDING`: Ordena los mensajes del más antiguo al más reciente.

**2. `for message in messages:`**

- **Propósito**: Itera sobre cada mensaje en el historial.
- **Importancia**: Permite procesar cada mensaje individualmente.

**3. `if message.text_messages:`**

- **Propósito**: Verifica si el mensaje contiene texto.
- **Por qué es necesario**: Algunos mensajes podrían ser de otro tipo (por ejemplo, archivos adjuntos).

**4. `last_msg = message.text_messages[-1]`**

- **Propósito**: Obtiene el último fragmento de texto del mensaje.
- **`[-1]`**: Accede al último elemento de la lista `text_messages`.

**5. `print(f"{message.role}: {last_msg.text.value}\n")`**

- **Formato**: Muestra el mensaje con el formato `ROL: TEXTO_DEL_MENSAJE`.
- **`message.role`**: Indica si el mensaje es del `user` o del `agent`.
- **`last_msg.text.value`**: Contenido del mensaje.

### Flujo de Ejecución del codigo del historial

1. Se imprime un encabezado "Conversation Log:".
2. Se obtienen todos los mensajes del hilo ordenados cronológicamente.
3. Para cada mensaje:
   - Se verifica que contenga texto.
   - Se extrae el último fragmento de texto.
   - Se imprime el rol del remitente y el contenido del mensaje.

**Ejemplo de Salida:**

```bash
Conversation Log:

user: ¿Cuál es la categoría con mayor costo?

agent: La categoría con mayor costo es Transporte con $2301.00.

user: Muestra un gráfico de los costos.

agent: Aquí tienes un gráfico de barras mostrando los costos por categoría...
```

### Importancia

- **Auditoría**: Permite revisar todo lo que se ha hablado.
- **Depuración**: Útil para entender el flujo de la conversación.
- **Registro**: Mantiene un historial de la interacción.
