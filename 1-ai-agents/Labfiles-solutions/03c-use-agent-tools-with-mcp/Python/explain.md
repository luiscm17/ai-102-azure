# Explicación Detallada del Script `client.py`

A continuación, te explico en detalle el script `client.py`, que pertenece al laboratorio **"Connect AI agents to tools using Model Context Protocol (MCP)"** de la certificación AI-102. Este script crea y ejecuta un agente de IA que se conecta a un servidor MCP remoto (Model Context Protocol) para buscar información en la documentación oficial de Microsoft. El agente usa una herramienta MCP para realizar búsquedas en tiempo real y responder preguntas técnicas. Explicaré la lógica general, las importaciones, la función principal (`main`), las variables, métodos, parámetros y sintaxis, paso a paso, enfocándome en cómo funciona el código.

## Lógica General

- **Propósito**: El script configura y ejecuta un agente de IA en Azure AI Agent Service que actúa como un asistente para búsquedas en documentación técnica de Microsoft. El agente se conecta a un servidor MCP remoto (e.g., el de Microsoft Learn) y usa una herramienta de búsqueda para recuperar información relevante. Al final, muestra el historial de la conversación y elimina el agente.
- **Flujo Principal**:
  1. Importar módulos y herramientas MCP.
  2. Cargar variables de entorno.
  3. Autenticarse y conectar al cliente de agentes.
  4. Configurar la herramienta MCP y registrarla en el conjunto de herramientas.
  5. Crear un agente con instrucciones para usar la herramienta MCP.
  6. Crear un hilo de conversación.
  7. Solicitar un prompt al usuario, enviarlo al agente y procesar la ejecución.
  8. Mostrar el estado de la ejecución, pasos y llamadas a herramientas.
  9. Mostrar el historial de la conversación.
  10. Eliminar el agente.
- **Por qué este diseño**: El script demuestra cómo integrar herramientas basadas en MCP en un agente conversacional de Azure AI Agent Service. Usa un enfoque interactivo para simular una conversación, mostrando cómo el agente invoca herramientas externas (e.g., búsqueda en documentación). Esto alinea con los objetivos de AI-102 para extender agentes con herramientas personalizadas o externas.

## Importaciones

El script comienza con las importaciones de módulos necesarios para el funcionamiento. Cada una se explica a continuación:

- **`import os`**: Importa el módulo estándar `os` para interactuar con el sistema operativo (e.g., acceder a variables de entorno).
  - **Propósito**: Se usa para cargar variables de entorno desde `.env`.
  - **Por qué**: Permite una configuración segura sin hardcodear valores.

- **`from dotenv import load_dotenv`**: Importa la función `load_dotenv` del módulo `dotenv` (instalado con `pip install python-dotenv`).
  - **Propósito**: Carga variables de entorno desde un archivo `.env` (e.g., endpoint del proyecto, nombre del despliegue).
  - **Por qué**: Facilita la configuración segura (e.g., credenciales) sin exponerlas en el código.

- **`from typing import Any`**: Importa el tipo `Any` del módulo estándar `typing`.
  - **Propósito**: Se usa para anotaciones de tipo en variables como `user_functions: Set[Callable[..., Any]]`, aunque en este script no se usa directamente (podría ser un remanente).
  - **Por qué**: Mejora la legibilidad y el mantenimiento del código.

- **`from pathlib import Path`**: Importa la clase `Path` del módulo estándar `pathlib`.
  - **Propósito**: Maneja rutas de archivos de forma portable, aunque en este script no se usa (podría ser para futuras expansiones).
  - **Por qué**: Proporciona una sintaxis limpia para trabajar con archivos/directorios.

- **`from azure.identity import DefaultAzureCredential`**: Importa la clase `DefaultAzureCredential` del módulo `azure.identity`.
  - **Propósito**: Proporciona autenticación automática para Azure (e.g., usa credenciales del entorno, CLI o identidad administrada).
  - **Por qué**: Se usa para autenticar el cliente de agentes (`AgentsClient`) sin exponer credenciales.

- **`from azure.ai.agents import AgentsClient`**: Importa la clase `AgentsClient` del módulo `azure.ai.agents`.
  - **Propósito**: Crea un cliente para interactuar con Azure AI Agent Service (e.g., crear agentes, hilos, mensajes).
  - **Por qué**: Es el núcleo para gestionar agentes de IA en Azure.

- **`from azure.ai.agents.models import McpTool, ToolSet, ListSortOrder`**: Importa clases del submódulo `models` de `azure.ai.agents`.
  - **Propósito**:
    - `McpTool`: Define una herramienta basada en Model Context Protocol (MCP) para conectar a servidores remotos.
    - `ToolSet`: Conjunto de herramientas para registrar en el agente.
    - `ListSortOrder`: Enum para ordenar listas (e.g., mensajes en orden ascendente).
  - **Por qué**: Permite configurar herramientas MCP, conjuntos de herramientas y ordenar historiales.

## Función Principal: `main`

Esta es la función principal del script, que se ejecuta cuando el script se corre (`if __name__ == '__main__': main()`). Explico línea por línea su lógica, variables, métodos y sintaxis.

- **Sintaxis**: `def main():`
  - `def`: Palabra clave para definir una función.
  - `main`: Nombre convencional para la función principal.
  - `()`: No recibe parámetros.

- **Lógica Interna (Línea por Línea)**:
  1. **`load_dotenv()`**:
     - `load_dotenv`: Carga variables de un archivo `.env` (e.g., `FOUNDRY_PROJECT_ENDPOINT`, `MODEL_DEPLOYMENT_NAME`).
     - **Propósito**: Accede a configuraciones seguras sin hardcodearlas.
     - **Por qué**: Evita exponer credenciales en el código.

  2. **`project_endpoint = os.getenv("FOUNDRY_PROJECT_ENDPOINT")`**:
     - `os.getenv`: Obtiene una variable de entorno, con valor por defecto None si no existe.
     - **Propósito**: Obtiene el endpoint del proyecto de Azure AI Foundry.
     - **Por qué**: El endpoint es necesario para conectar al cliente de agentes.

  3. **`model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")`**:
     - Similar a lo anterior, obtiene el nombre del despliegue del modelo (e.g., "gpt-4o").
     - **Propósito**: Especifica el modelo que el agente usará.
     - **Por qué**: Permite configurar el modelo desde el `.env` sin modificar el código.

  4. **`agents_client = AgentsClient(endpoint=project_endpoint, credential=DefaultAzureCredential(...))`**:
     - `AgentsClient`: Clase para interactuar con Azure AI Agent Service.
     - **Parámetros**:
       - `endpoint=project_endpoint`: URL del proyecto (de `.env`).
       - `credential=DefaultAzureCredential(...)`: Objeto de autenticación, excluyendo credenciales de entorno e identidad administrada para enfocarse en CLI o credenciales compartidas.
     - **Propósito**: Crea un cliente para gestionar agentes, hilos y mensajes.
     - **Por qué**: Es el punto de entrada para todas las operaciones del agente.

  5. **`mcp_server_url = "https://learn.microsoft.com/api/mcp"`**:
     - Variable con la URL del servidor MCP remoto (Model Context Protocol).
     - **Propósito**: Define la URL del servidor MCP para la herramienta.
     - **Por qué**: El agente usa este servidor para buscar documentación de Microsoft.

  6. **`mcp_server_label = "mslearn"`**:
     - Variable con una etiqueta para el servidor MCP.
     - **Propósito**: Identifica el servidor en la herramienta MCP.
     - **Por qué**: Permite diferenciar múltiples servidores MCP si se usan.

  7. **`mcp_tool = McpTool(server_label=mcp_server_label, server_url=mcp_server_url)`**:
     - `McpTool`: Clase para definir una herramienta MCP.
     - **Parámetros**:
       - `server_label=mcp_server_label`: Etiqueta del servidor.
       - `server_url=mcp_server_url`: URL del servidor.
     - **Propósito**: Crea una herramienta basada en MCP para buscar en la documentación.
     - **Por qué**: Permite al agente usar el protocolo MCP para herramientas remotas.

  8. **`mcp_tool.set_approval_mode("never")`**:
     - `set_approval_mode`: Método para configurar el modo de aprobación de la herramienta.
     - **Parámetros**: `"never"`: No requiere aprobación para ejecutar la herramienta.
     - **Propósito**: Configura la herramienta para que se ejecute automáticamente sin intervención del usuario.
     - **Por qué**: Facilita el flujo automatizado en el laboratorio, evitando pausas para aprobación.

  9. **`toolset = ToolSet()`**:
     - `ToolSet`: Clase para un conjunto de herramientas.
     - **Propósito**: Crea un conjunto vacío de herramientas.
     - **Por qué**: El agente necesita un conjunto para registrar herramientas.

  10. **`toolset.add(mcp_tool)`**:
      - `add`: Método para agregar herramientas al conjunto.
      - **Parámetros**: `mcp_tool`: La herramienta MCP creada.
      - **Propósito**: Registra la herramienta MCP en el conjunto.
      - **Por qué**: Hace que la herramienta esté disponible para el agente.

  11. **`with agents_client:`**:
      - `with`: Gestor de contexto para abrir y cerrar recursos automáticamente (e.g., conexiones).
      - **Propósito**: Asegura que el cliente se cierre correctamente al final del bloque.
      - **Por qué**: Evita fugas de recursos.

  12. **`agent = agents_client.create_agent(...)`**:
      - `create_agent`: Método para crear un agente.
      - **Parámetros**:
        - `model = model_deployment`: Nombre del despliegue del modelo (de `.env`).
        - `name = "my-mcp-agent"`: Nombre único del agente.
        - `instructions`: Cadena con instrucciones para el agente (e.g., "You have access to an MCP server...").
      - **Propósito**: Crea el agente con instrucciones para usar la herramienta MCP.
      - **Por qué**: Define el comportamiento del agente para búsquedas en documentación.

  13. **`print(f"Created agent, ID: {agent.id}")`**:
      - `print`: Imprime un mensaje en la consola.
      - **Propósito**: Informa el ID del agente creado.
      - **Por qué**: Útil para depuración y seguimiento.

  14. **`print(f"MCP Server: {mcp_tool.server_label} at {mcp_tool.server_url}")`**:
      - Imprime detalles del servidor MCP.
      - **Propósito**: Confirma la configuración de la herramienta MCP.
      - **Por qué**: Ayuda a verificar que la herramienta está configurada correctamente.

  15. **`thread = agents_client.threads.create()`**:
      - `threads.create`: Método para crear un hilo de conversación.
      - **Propósito**: Crea un hilo nuevo para la conversación.
      - **Por qué**: Los hilos mantienen el estado de la conversación (historial).

  16. **`print(f"Created thread, ID: {thread.id}")`**:
      - Imprime el ID del hilo.
      - **Propósito**: Informa el ID del hilo creado.

  17. **`prompt = input("\nHow can I help?: ")`**:
      - `input`: Lee entrada del usuario desde la consola.
      - **Propósito**: Obtiene el prompt del usuario.
      - **Por qué**: Permite interacción dinámica.

  18. **`message = agents_client.messages.create(thread_id=thread.id, role="user", content=prompt)`**:
      - `messages.create`: Crea un mensaje en el hilo.
      - **Parámetros**:
        - `thread_id=thread.id`: ID del hilo.
        - `role="user"`: Rol del mensaje (del usuario).
        - `content=prompt`: Contenido del prompt.
      - **Propósito**: Agrega el mensaje del usuario al hilo.
      - **Por qué**: El agente necesita el mensaje para procesar la solicitud.

  19. **`print(f"Created message, ID: {message.id}")`**:
      - Imprime el ID del mensaje.
      - **Propósito**: Confirma la creación del mensaje.

  20. **`run = agents_client.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)`**:
      - `runs.create_and_process`: Crea y procesa una ejecución del agente.
      - **Parámetros**:
        - `thread_id=thread.id`: ID del hilo.
        - `agent_id=agent.id`: ID del agente.
      - **Propósito**: Ejecuta el agente en el hilo, invocando herramientas como MCP si es necesario.
      - **Por qué**: Procesa el mensaje del usuario y genera una respuesta.

  21. **`print(f"Created run, ID: {run.id}")`**:
      - Imprime el ID de la ejecución.
      - **Propósito**: Confirma la creación de la ejecución.

  22. **`print(f"Run completed with status: {run.status}")`**:
      - Imprime el estado de la ejecución.
      - **Propósito**: Verifica si la ejecución se completó.

  23. **`run_steps = agents_client.run_steps.list(thread_id=thread.id, run_id=run.id)`**:
      - `run_steps.list`: Lista los pasos de la ejecución.
      - **Parámetros**:
        - `thread_id=thread.id`: ID del hilo.
        - `run_id=run.id`: ID de la ejecución.
      - **Propósito**: Recupera los pasos detallados de la ejecución.
      - **Por qué**: Muestra qué acciones realizó el agente (e.g., llamadas a herramientas).

  24. **`for step in run_steps: print(f"Step {step['id']} status: {step['status']}")`**:
      - Bucle sobre los pasos: Imprime el ID y estado de cada paso.
      - **Propósito**: Muestra el progreso de la ejecución.

  25. **`step_details = step.get("step_details", {})`**:
      - `get`: Método de diccionario para obtener un valor con por defecto `{}` si no existe.
      - **Propósito**: Obtiene los detalles del paso.
      - **Por qué**: Accede a información adicional como llamadas a herramientas.

  26. **`tool_calls = step_details.get("tool_calls", [])`**:
      - Similar, obtiene las llamadas a herramientas con por defecto `[]`.
      - **Propósito**: Recupera las llamadas a herramientas en el paso.

  27. **`if tool_calls: print("  MCP Tool calls:")`**:
      - Verifica si hay llamadas a herramientas.
      - **Propósito**: Muestra si se usaron herramientas MCP.

  28. **`for call in tool_calls: print(f"    Tool Call ID: {call.get('id')}")`**:
      - Bucle sobre llamadas a herramientas: Imprime detalles como ID, tipo y nombre.
      - **Propósito**: Muestra información sobre las llamadas a herramientas MCP (e.g., "microsoft_docs_search").
      - **Por qué**: Ayuda a depurar qué herramientas usó el agente.

  29. **`print("\nConversation:")`**:
      - Imprime un encabezado para el historial.
      - **Propósito**: Separa el historial de la ejecución.

  30. **`messages = agents_client.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)`**:
      - `messages.list`: Lista todos los mensajes en el hilo.
      - **Parámetros**:
        - `thread_id=thread.id`: ID del hilo.
        - `order=ListSortOrder.ASCENDING`: Orden ascendente (del más viejo al más nuevo).
      - **Propósito**: Recupera el historial completo de la conversación.
      - **Por qué**: Muestra el registro completo al final.

  31. **`for msg in messages: if msg.text_messages: last_text = msg.text_messages[-1]; print(f"{msg.role.upper()}: {last_text.text.value}")`**:
      - Bucle sobre mensajes: Obtiene el último mensaje de texto de cada uno y lo imprime con el rol en mayúsculas.
      - **Propósito**: Muestra el historial de la conversación.
      - **Por qué**: Permite revisar la interacción completa.

  32. **`agents_client.delete_agent(agent.id)`**:
      - `delete_agent`: Elimina el agente.
      - **Parámetros**: `agent.id`: ID del agente.
      - **Propósito**: Limpia recursos al finalizar.
      - **Por qué**: Evita costos innecesarios y mantiene el entorno limpio.

  33. **`print("Deleted agent")`**:
      - Imprime un mensaje de confirmación.
      - **Propósito**: Indica que la limpieza se completó.

## Conjunto de Variables

- **`project_endpoint`**: Endpoint del proyecto de Azure AI Foundry, cargado de `.env`.
- **`model_deployment`**: Nombre del despliegue del modelo, cargado de `.env`.
- **`agents_client`**: Objeto cliente para gestionar agentes.
- **`mcp_server_url`**: URL del servidor MCP remoto.
- **`mcp_server_label`**: Etiqueta del servidor MCP.
- **`mcp_tool`**: Objeto herramienta MCP.
- **`toolset`**: Conjunto de herramientas registrado.
- **`agent`**: Objeto agente creado.
- **`thread`**: Objeto hilo de conversación.
- **`prompt`**: Prompt ingresado por el usuario.
- **`message`**: Mensaje agregado al hilo.
- **`run`**: Objeto de ejecución del agente.
- **`run_steps`**: Lista de pasos de la ejecución.
- **`step_details`**: Detalles de un paso.
- **`tool_calls`**: Lista de llamadas a herramientas en un paso.
- **`messages`**: Lista de mensajes del historial.
- **`msg`**: Mensaje individual del historial.

## Sintaxis y Métodos Clave

- **Gestor de Contexto (`with agents_client:`)**: Asegura que el cliente se cierre automáticamente.
- **Bucle `while True`**: Crea un chat interactivo infinito hasta "quit".
- **Condicionales (`if`, `elif`)**: Manejan entradas inválidas o comandos de salida.
- **Métodos del SDK**:
  - `AgentsClient(...)`: Crea el cliente con endpoint y credenciales.
  - `create_agent(...)`: Crea el agente con modelo, nombre e instrucciones.
  - `threads.create()`: Crea un hilo de conversación.
  - `messages.create(...)`: Agrega un mensaje al hilo.
  - `runs.create_and_process(...)`: Ejecuta el agente en el hilo.
  - `get_run(...)`: Obtiene el estado de la ejecución.
  - `run_steps.list(...)`: Lista los pasos de la ejecución.
  - `messages.list(...)`: Lista el historial de mensajes.
  - `delete_agent(...)`: Elimina el agente.

Este script demuestra un flujo completo de interacción con un agente de IA en Azure AI Agent Service, enfocándose en la integración con herramientas MCP para búsquedas en documentación externa.
