# Explicacion del codigo

## Explicación General del Script `user_function.py`

### Propósito

El script `user_functions.py` tiene como objetivo crear una función (`submit_support_ticket`) que el agente de IA pueda invocar para procesar solicitudes de soporte técnico. La función toma un correo electrónico y una descripción del problema, genera un número de ticket único, guarda los detalles en un archivo de texto y devuelve un mensaje en formato JSON confirmando la acción. Además, la función se agrega a un conjunto (`user_functions`) que permite registrar múltiples herramientas para el agente de IA.

### Flujo General

1. **Importar módulos**: Se importan las bibliotecas necesarias para manejar archivos, generar identificadores únicos, trabajar con JSON y usar anotaciones de tipo.
2. **Definir la función `submit_support_ticket`**: Procesa los parámetros (correo y descripción), crea un archivo con los detalles del ticket y devuelve un mensaje JSON.
3. **Crear un conjunto de funciones**: Se agrega la función a un conjunto (`user_functions`) para que el agente pueda registrarla como una herramienta.
4. **Uso en el contexto del laboratorio**: El script se importa en un programa principal (e.g., `agent.py`) donde el agente de IA usa la función como herramienta durante una conversación.

### Por qué este diseño

- **Modularidad**: La función es independiente y reutilizable, ideal para integrarse con agentes de IA en Azure AI Agent Service.
- **Formato JSON**: La salida en JSON asegura que el agente pueda interpretar fácilmente el resultado.
- **Conjunto de funciones**: Usar un `set` permite escalar el script para incluir más funciones en el futuro.
- **Alineación con AI-102**: El laboratorio enseña cómo integrar herramientas personalizadas en agentes conversacionales, un componente clave de la certificación AI-102.

### Estilo de Sintaxis

El script usa características modernas de Python (3.6+), como f-strings, anotaciones de tipo (`typing`), y la biblioteca `pathlib` para manejar rutas de archivos de forma portable. Sigue las convenciones de PEP 8 para nombres de variables y funciones.

---

## Análisis de los Componentes del Script

### Importaciones

El script comienza con las importaciones de módulos necesarios. A continuación, detallo cada una:

- **`import json`**:
  - **Qué es**: Módulo estándar de Python para trabajar con datos en formato JSON.
  - **Propósito**: Convierte un diccionario de Python a una cadena JSON usando `json.dumps`. Esto se usa para devolver un mensaje estructurado al agente (e.g., `{"message": "Ticket submitted"}`).
  - **Por qué**: Los agentes de IA esperan respuestas estructuradas en JSON para procesarlas y responder al usuario. Es un estándar en APIs y herramientas conversacionales.

- **`from pathlib import Path`**:
  - **Qué es**: Módulo estándar (desde Python 3.4) para manejar rutas de archivos de forma portátil.
  - **Propósito**: Crea un objeto `Path` para obtener el directorio del script (`Path(__file__).parent`) y construir rutas de archivo (e.g., para guardar el ticket).
  - **Por qué**: Es más robusto y portable que `os.path`, ya que funciona en Windows, Linux y macOS sin ajustes.

- **`import uuid`**:
  - **Qué es**: Módulo estándar para generar identificadores únicos universales (UUID).
  - **Propósito**: Genera un número de ticket único con `uuid.uuid4()` (e.g., un identificador como "123e4567-e89b-12d3-a456-426614174000").
  - **Por qué**: Garantiza que cada ticket tenga un identificador único, evitando colisiones en el sistema de soporte.

- **`from typing import Any, Callable, Set`**:
  - **Qué es**: Módulo estándar (desde Python 3.5) para anotaciones de tipo.
  - **Propósito**:
    - `Any`: Representa cualquier tipo de dato.
    - `Callable[..., Any]`: Representa una función que acepta cualquier número de argumentos (`...`) y devuelve cualquier tipo (`Any`).
    - `Set`: Representa un conjunto de elementos únicos.
  - **Por qué**: Proporciona anotaciones de tipo para el conjunto `user_functions` (e.g., `Set[Callable[..., Any]]`), mejorando la legibilidad, compatibilidad con IDEs y verificadores de tipos como mypy. Es una práctica recomendada en proyectos modernos.

### Definición de la Función: `submit_support_ticket`

Esta es la función principal del script, diseñada como una herramienta que el agente de IA puede invocar. A continuación, analizo su sintaxis, parámetros, lógica y métodos.

- **Sintaxis**: `def submit_support_ticket(email_address: str, description: str) -> str:`
  - `def`: Palabra clave para definir una función.
  - `submit_support_ticket`: Nombre descriptivo en formato snake_case (estándar PEP 8).
  - `(email_address: str, description: str)`: Parámetros con tipos explícitos (cadenas de texto).
  - `-> str`: Indica que la función devuelve una cadena (en este caso, JSON).
  - **Por qué**: La sintaxis clara y tipada facilita la integración con el agente y asegura que los parámetros sean correctos.

- **Parámetros**:
  - **`email_address: str`**: El correo electrónico del usuario que envía el ticket (e.g., "<user@example.com>").
    - **Propósito**: Identifica al remitente del ticket, necesario para el seguimiento del soporte.
    - **Por qué**: El agente recolecta este dato del usuario durante la conversación y lo pasa a la función.
  - **`description: str`**: Una descripción del problema o solicitud (e.g., "Mi computadora no enciende").
    - **Propósito**: Proporciona detalles sobre el problema para incluirlos en el ticket.
    - **Por qué**: Permite al agente registrar la información proporcionada por el usuario.

- **Lógica Interna (Línea por Línea)**:
  1. **`script_dir = Path(__file__).parent`**:
     - `__file__`: Variable especial que contiene la ruta del archivo del script actual.
     - `Path(__file__).parent`: Obtiene el directorio padre del script (e.g., `/ruta/al/script/`).
     - **Propósito**: Define dónde se guardará el archivo del ticket (en el mismo directorio que el script).
     - **Por qué**: Asegura que los archivos se guarden en un lugar predecible y accesible.

  2. **`ticket_number = str(uuid.uuid4()).replace('-', '')[:6]`**:
     - `uuid.uuid4()`: Genera un UUID aleatorio (e.g., "123e4567-e89b-12d3-a456-426614174000").
     - `str(...)`: Convierte el UUID a una cadena.
     - `.replace('-', '')`: Elimina los guiones (e.g., "123e4567e89b12d3a456426614174000").
     - `[:6]`: Toma los primeros 6 caracteres (e.g., "123e45").
     - **Propósito**: Crea un número de ticket único y corto.
     - **Por qué**: Facilita la identificación del ticket sin usar un UUID completo, que es largo.

  3. **`file_name = f"ticket_{ticket_number}.txt"`**:
     - Usa un f-string (Python 3.6+) para crear el nombre del archivo (e.g., "ticket_123e45.txt").
     - **Propósito**: Define un nombre de archivo único basado en el número de ticket.
     - **Por qué**: Evita sobrescribir archivos y hace que los tickets sean fáciles de identificar.

  4. **`file_path = script_dir / file_name`**:
     - `/`: Operador de `pathlib` para concatenar rutas (e.g., `/ruta/al/script/ticket_123e45.txt`).
     - **Propósito**: Construye la ruta completa del archivo.
     - **Por qué**: Garantiza compatibilidad multiplataforma (Windows, Linux, etc.).

  5. **`text = f"Support ticket: {ticket_number}\nSubmitted by: {email_address}\nDescription: {description}"`**:
     - Usa un f-string para formatear el contenido del ticket con saltos de línea (`\n`).
     - **Propósito**: Crea el texto que se escribirá en el archivo.
     - **Por qué**: Estructura el contenido del ticket para que sea legible y contenga toda la información necesaria.

  6. **`file_path.write_text(text)`**:
     - `write_text`: Método de `Path` que escribe una cadena en un archivo (codificación UTF-8).
     - **Propósito**: Guarda el contenido del ticket en el archivo especificado.
     - **Por qué**: Persiste los detalles del ticket en disco para referencia futura.

  7. **`message_json = json.dumps({"message": f"Support ticket {ticket_number} submitted. The ticket file is saved as {file_name}."})`**:
     - `json.dumps`: Convierte un diccionario a una cadena JSON.
     - **Propósito**: Genera un mensaje estructurado para que el agente lo devuelva al usuario.
     - **Por qué**: El agente espera una respuesta en JSON para procesarla y mostrar un mensaje al usuario (e.g., "Ticket submitted").

  8. **`return message_json`**:
     - Devuelve la cadena JSON como resultado de la función.
     - **Propósito**: Completa la ejecución de la herramienta, permitiendo al agente procesar el resultado.
     - **Por qué**: El agente usa esta respuesta para confirmar la acción al usuario.

- **Por qué esta función**: En el contexto del laboratorio, esta función actúa como una herramienta personalizada que el agente de IA invoca cuando el usuario solicita enviar un ticket. Esto demuestra cómo las funciones personalizadas pueden extender las capacidades de un agente conversacional en Azure AI Agent Service.

### Conjunto de Funciones: `user_functions`

- **`user_functions: Set[Callable[..., Any]] = {submit_support_ticket}`**:
  - `Set`: Tipo de colección para elementos únicos (de `typing`).
  - `Callable[..., Any]`: Anotación de tipo para funciones que aceptan cualquier número de argumentos y devuelven cualquier tipo.
  - `{submit_support_ticket}`: Inicializa el conjunto con la función como único elemento.
  - **Propósito**: Define un grupo de funciones que pueden registrarse como herramientas en el agente de IA.
  - **Por qué un conjunto**: Los conjuntos aseguran que no haya duplicados y permiten agregar más funciones fácilmente (e.g., `user_functions.add(otra_funcion)`). En el laboratorio, este conjunto se importa en el script principal para configurar el agente.
  - **Por qué anotaciones de tipo**: Mejoran la legibilidad, facilitan el mantenimiento y aseguran compatibilidad con herramientas de análisis estático.

---

## Contexto en el Laboratorio

### Resumen del Laboratorio

El laboratorio forma parte de la certificación AI-102 y se centra en el uso de funciones personalizadas como herramientas en agentes conversacionales de Azure AI Agent Service. En este caso, el agente actúa como un sistema de soporte técnico que recolecta información (correo y descripción) y usa la función `submit_support_ticket` para generar tickets.

#### Cómo se Usa

1. **Integración**:
   - En el script principal (e.g., `agent.py`), se importa el conjunto `user_functions` (`from user_functions import user_functions`).
   - Las funciones del conjunto se registran como herramientas en la configuración del agente (usando el SDK de Azure AI Foundry).
2. **Conversación**:
   - El usuario interactúa con el agente (e.g., diciendo "Tengo un problema técnico").
   - El agente solicita el correo y la descripción, luego invoca `submit_support_ticket` con esos datos.
   - La función genera el archivo y devuelve un mensaje JSON, que el agente usa para confirmar al usuario (e.g., "Ticket 123e45 enviado").
3. **Persistencia**:
   - Los tickets se guardan como archivos de texto en el directorio del script, accesibles con comandos como `ls` y `cat` en la terminal.

#### Relevancia para AI-102

- **Objetivo**: Demuestra cómo integrar herramientas personalizadas en agentes conversacionales, un concepto clave en IA conversacional y Azure AI Agent Service.
- **Habilidad**: Muestra cómo los agentes pueden realizar acciones del mundo real (e.g., guardar archivos) basándose en interacciones con el usuario, usando herramientas definidas por el desarrollador.

---

## Métodos y Parámetros Usados

### Métodos Relevantes

- **`Path(__file__).parent`** (de `pathlib`):
  - **Qué hace**: Obtiene el directorio padre del script actual.
  - **Parámetros**: `__file__` (ruta del script).
  - **Por qué**: Define un lugar consistente para guardar archivos.
- **`uuid.uuid4()`** (de `uuid`):
  - **Qué hace**: Genera un UUID version 4 (aleatorio).
  - **Parámetros**: Ninguno.
  - **Por qué**: Proporciona un identificador único para el ticket.
- **`str.replace('-', '')`** (de `str`):
  - **Qué hace**: Elimina guiones de una cadena.
  - **Parámetros**: Subcadena a reemplazar (`'-'`) y reemplazo (`''`).
  - **Por qué**: Limpia el UUID para un formato más legible.
- **`str[:6]`** (slicing de `str`):
  - **Qué hace**: Extrae los primeros 6 caracteres de una cadena.
  - **Parámetros**: Índices de inicio y fin (`[:6]`).
  - **Por qué**: Reduce el UUID a un número de ticket corto.
- **`Path.write_text(text)`** (de `pathlib`):
  - **Qué hace**: Escribe una cadena en un archivo.
  - **Parámetros**: `text` (contenido a escribir, tipo `str`).
  - **Por qué**: Guarda el ticket en disco de forma sencilla.
- **`json.dumps({...})`** (de `json`):
  - **Qué hace**: Convierte un diccionario a una cadena JSON.
  - **Parámetros**: Diccionario Python (e.g., `{"message": "..."}`).
  - **Por qué**: Proporciona una salida estructurada para el agente.

### Parámetros de la Función

- **`email_address: str`**:
  - **Tipo**: Cadena.
  - **Uso**: Identificador del usuario que envía el ticket.
- **`description: str`**:
  - **Tipo**: Cadena.
  - **Uso**: Detalles del problema o solicitud.

---

## Mejoras Potenciales

1. **Manejo de Errores**:
   - Agregar `try-except` para errores de escritura de archivos (e.g., permisos denegados).
   - Ejemplo:

     ```python
     try:
         file_path.write_text(text)
     except IOError as e:
         return json.dumps({"error": f"Failed to save ticket: {str(e)}"})
     ```

2. **Validación de Entrada**:
   - Verificar que `email_address` sea un correo válido (usando regex).
   - Asegurar que `description` no esté vacía.
3. **Más Funciones**:
   - Agregar otras funciones al conjunto `user_functions` (e.g., una para leer tickets existentes).
4. **Seguridad**:
   - Sanitizar `ticket_number` y `description` para evitar inyecciones de ruta o contenido malicioso.

---

## Conclusión

El script `user_functions.py` es un ejemplo claro de cómo crear herramientas personalizadas para agentes de IA en Azure AI Agent Service. La función `submit_support_ticket` demuestra cómo procesar entradas del usuario, realizar acciones (guardar un archivo) y devolver una respuesta estructurada (JSON). Su integración en un conjunto (`user_functions`) permite escalabilidad, y el uso de módulos modernos como `pathlib` y `typing` refleja buenas prácticas de Python. En el contexto del laboratorio AI-102, este script enseña cómo extender agentes conversacionales con funcionalidades personalizadas, un componente esencial para desarrollar soluciones de IA avanzadas.

## Explicación Detallada del Script `agent.py`

A continuación, te explico en detalle el script `agent.py`, que pertenece al laboratorio **"Use a custom function in an AI agent"** de la certificación AI-102. Este script crea y ejecuta un agente de IA conversacional que utiliza funciones personalizadas (importadas de `user_functions.py`) para manejar solicitudes de soporte técnico. El agente recolecta información del usuario y usa la función para generar tickets de soporte. Explicaré la lógica general, las importaciones, la función principal (`main`), las variables, métodos, parámetros y sintaxis, paso a paso, enfocándome en cómo funciona el código.

### Lógica General

- **Propósito**: El script configura y ejecuta un agente de IA en Azure AI Agent Service que actúa como un asistente de soporte técnico. El agente interactúa con el usuario a través de la consola, recolecta datos (como correo electrónico y descripción de problemas) y invoca funciones personalizadas para generar tickets de soporte. El agente es "stateful" (mantiene el estado de la conversación), por lo que recuerda mensajes previos. Al final, muestra el historial de la conversación y elimina el agente.
- **Flujo Principal**:
  1. Importar módulos y funciones personalizadas.
  2. Limpiar la consola y cargar variables de entorno.
  3. Autenticarse y conectar al cliente de agentes.
  4. Definir el agente con instrucciones y herramientas personalizadas.
  5. Crear un hilo de conversación.
  6. Iniciar un bucle para recibir prompts del usuario, enviarlos al agente, procesar respuestas y manejar fallos.
  7. Al salir del bucle, mostrar el historial de mensajes.
  8. Limpiar recursos (eliminar el agente).
- **Por qué este diseño**: El script demuestra cómo integrar herramientas personalizadas en un agente conversacional en Azure AI Agent Service. Usa un bucle para simular una conversación interactiva, y maneja estados para mantener el contexto. Esto alinea con los objetivos de AI-102 para crear agentes de IA que usan herramientas para acciones del mundo real.

### Importaciones

El script comienza con importaciones que traen módulos necesarios para el funcionamiento. Cada una se explica a continuación:

- **`import os`**: Importa el módulo estándar `os` para interactuar con el sistema operativo (e.g., limpiar la consola, acceder a variables de entorno).
  - **Propósito**: Se usa para limpiar la consola (`os.system`) y obtener el directorio de trabajo si es necesario.
  - **Por qué**: Permite una interfaz de consola limpia y portable entre sistemas operativos (Windows/Linux/macOS).

- **`from dotenv import load_dotenv`**: Importa la función `load_dotenv` del módulo `dotenv` (instalado con `pip install python-dotenv`).
  - **Propósito**: Carga variables de entorno desde un archivo `.env` (e.g., endpoint del proyecto, nombre del despliegue).
  - **Por qué**: Facilita la configuración segura (e.g., credenciales) sin hardcodearlas en el script, siguiendo mejores prácticas.

- **`from typing import Any`**: Importa el tipo `Any` del módulo estándar `typing`.
  - **Propósito**: Se usa para anotaciones de tipo en variables como `user_functions: Set[Callable[..., Any]]`.
  - **Por qué**: Mejora la legibilidad y el mantenimiento del código al indicar que una variable puede ser de cualquier tipo.

- **`from pathlib import Path`**: Importa la clase `Path` del módulo estándar `pathlib`.
  - **Propósito**: Maneja rutas de archivos de forma portable, aunque en este script no se usa directamente (podría ser un remanente o para futuras expansiones).
  - **Por qué**: Proporciona una sintaxis limpia para trabajar con archivos/directorios, aunque aquí no se aplica.

- **`from azure.identity import DefaultAzureCredential`**: Importa la clase `DefaultAzureCredential` del módulo `azure.identity`.
  - **Propósito**: Proporciona autenticación automática para Azure (e.g., usa credenciales del entorno, CLI o identidad administrada).
  - **Por qué**: Se usa para autenticar el cliente de agentes (`AgentsClient`) sin exponer credenciales.

- **`from azure.ai.agents import AgentsClient`**: Importa la clase `AgentsClient` del módulo `azure.ai.agents`.
  - **Propósito**: Crea un cliente para interactuar con Azure AI Agent Service (e.g., crear agentes, hilos, mensajes).
  - **Por qué**: Es el núcleo para gestionar agentes de IA en Azure.

- **`from azure.ai.agents.models import FunctionTool, ToolSet, ListSortOrder, MessageRole`**: Importa clases del submódulo `models` de `azure.ai.agents`.
  - **Propósito**:
    - `FunctionTool`: Define una herramienta basada en funciones personalizadas.
    - `ToolSet`: Conjunto de herramientas para registrar en el agente.
    - `ListSortOrder`: Enum para ordenar listas (e.g., mensajes en orden ascendente).
    - `MessageRole`: Enum para roles de mensajes (e.g., "user", "assistant").
  - **Por qué**: Permite configurar herramientas, ordenar historiales y definir roles en la conversación.

- **`from user_functions import user_functions`**: Importa el conjunto `user_functions` del archivo `user_functions.py`.
  - **Propósito**: Accede a las funciones personalizadas (e.g., `submit_support_ticket`) para registrarlas como herramientas.
  - **Por qué**: Integra las funciones del otro script con el agente.

### Función Principal: `main`

Esta es la función principal del script, que se ejecuta cuando el script se corre (`if __name__ == '__main__': main()`). Explico línea por línea su lógica, variables, métodos y sintaxis.

- **Sintaxis**: `def main():`
  - `def`: Define la función.
  - `main`: Nombre convencional para la función principal.
  - `()`: No recibe parámetros.

- **Lógica Interna (Línea por Línea)**:
  1. **`os.system('cls' if os.name == 'nt' else 'clear')`**:
     - `os.system`: Ejecuta un comando del sistema operativo.
     - `'cls' if os.name == 'nt' else 'clear'`: Condicional que usa 'cls' en Windows (`os.name == 'nt'`) o 'clear' en Linux/macOS.
     - **Propósito**: Limpia la consola para una interfaz limpia al inicio.
     - **Por qué**: Mejora la experiencia del usuario en la consola.

  2. **`load_dotenv()`**:
     - `load_dotenv`: Carga variables de un archivo `.env` (e.g., `FOUNDRY_PROJECT_ENDPOINT`, `MODEL_DEPLOYMENT_NAME`).
     - **Propósito**: Accede a configuraciones seguras sin hardcodearlas.
     - **Por qué**: Evita exponer credenciales en el código.

  3. **`project_endpoint = os.getenv("FOUNDRY_PROJECT_ENDPOINT")`**:
     - `os.getenv`: Obtiene una variable de entorno, con valor por defecto None si no existe.
     - **Propósito**: Obtiene el endpoint del proyecto de Azure AI Foundry.
     - **Por qué**: El endpoint es necesario para conectar al cliente de agentes.

  4. **`model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")`**:
     - Similar a lo anterior, obtiene el nombre del despliegue del modelo (e.g., "gpt-4o").
     - **Propósito**: Especifica el modelo que el agente usará.
     - **Por qué**: Permite configurar el modelo desde el `.env` sin modificar el código.

  5. **`agent_client = AgentsClient(endpoint=project_endpoint, credential=DefaultAzureCredential(...))`**:
     - `AgentsClient`: Clase para interactuar con Azure AI Agent Service.
     - **Parámetros**:
       - `endpoint=project_endpoint`: URL del proyecto (de `.env`).
       - `credential=DefaultAzureCredential(...)`: Objeto de autenticación, excluyendo credenciales de entorno e identidad administrada para enfocarse en CLI o credenciales compartidas.
     - **Propósito**: Crea un cliente para gestionar agentes, hilos y mensajes.
     - **Por qué**: Es el punto de entrada para todas las operaciones del agente.

  6. **`with agent_client:`**:
     - `with`: Gestor de contexto para abrir y cerrar recursos automáticamente (e.g., conexiones).
     - **Propósito**: Asegura que el cliente se cierre correctamente al final del bloque.
     - **Por qué**: Evita fugas de recursos.

  7. **`functions = FunctionTool(user_functions)`**:
     - `FunctionTool`: Clase para definir herramientas basadas en funciones.
     - **Parámetros**: `user_functions`: El conjunto de funciones del archivo `user_functions.py`.
     - **Propósito**: Convierte el conjunto de funciones en una herramienta usable por el agente.
     - **Por qué**: Permite al agente invocar las funciones personalizadas.

  8. **`toolset = ToolSet()`**:
     - `ToolSet`: Clase para un conjunto de herramientas.
     - **Propósito**: Crea un conjunto vacío de herramientas.
     - **Por qué**: El agente necesita un conjunto para registrar herramientas.

  9. **`toolset.add(functions)`**:
     - `add`: Método para agregar herramientas al conjunto.
     - **Parámetros**: `functions`: La herramienta creada a partir de `user_functions`.
     - **Propósito**: Registra las funciones en el conjunto de herramientas.
     - **Por qué**: Hace que las funciones estén disponibles para el agente.

  10. **`agent_client.enable_auto_function_calls(toolset)`**:
      - `enable_auto_function_calls`: Método para habilitar llamadas automáticas a funciones.
      - **Parámetros**: `toolset`: El conjunto de herramientas.
      - **Propósito**: Permite al agente invocar automáticamente las funciones basadas en el contexto.
      - **Por qué**: El agente decide cuándo usar las herramientas sin intervención manual.

  11. **`agent = agent_client.create_agent(...)`**:
      - `create_agent`: Método para crear un agente.
      - **Parámetros**:
        - `model = model_deployment`: Nombre del despliegue del modelo (de `.env`).
        - `name = "support-agent-007"`: Nombre único del agente.
        - `instructions`: Cadena con instrucciones para el agente (e.g., "You are a technical support agent").
        - `toolset = toolset`: El conjunto de herramientas.
      - **Propósito**: Crea el agente con instrucciones y herramientas.
      - **Por qué**: Define el comportamiento del agente para el soporte técnico.

  12. **`thread = agent_client.threads.create()`**:
      - `threads.create`: Método para crear un hilo de conversación.
      - **Propósito**: Crea un hilo nuevo para la conversación.
      - **Por qué**: Los hilos mantienen el estado de la conversación (historial).

  13. **`print(f"You're chatting with {agent.name} (ID: {agent.id})")`**:
      - `print`: Imprime un mensaje en la consola.
      - **Propósito**: Informa al usuario sobre el agente activo.
      - **Por qué**: Mejora la interacción del usuario.

  14. **`while True:`**:
      - Bucle infinito para la conversación.
      - **Propósito**: Mantiene la conversación hasta que el usuario escribe "quit".
      - **Por qué**: Simula un chat interactivo.

  15. **`user_prompt = input("Enter a prompt (or type 'quit' to exit): ")`**:
      - `input`: Lee entrada del usuario desde la consola.
      - **Propósito**: Obtiene el prompt del usuario.
      - **Por qué**: Permite interacción dinámica.

  16. **`if user_prompt.lower() == "quit": break`**:
      - `lower()`: Convierte a minúsculas para comparación insensible a mayúsculas.
      - `break`: Sale del bucle.
      - **Propósito**: Termina la conversación si el usuario escribe "quit".

  17. **`if len(user_prompt) == 0: print("Please enter a prompt."); continue`**:
      - `len`: Verifica si el prompt está vacío.
      - `continue`: Salta a la siguiente iteración.
      - **Propósito**: Evita procesar prompts vacíos.

  18. **`message = agent_client.messages.create(thread_id=thread.id, role="user", content=user_prompt)`**:
      - `messages.create`: Crea un mensaje en el hilo.
      - **Parámetros**:
        - `thread_id=thread.id`: ID del hilo.
        - `role="user"`: Rol del mensaje (del usuario).
        - `content=user_prompt`: Contenido del prompt.
      - **Propósito**: Agrega el mensaje del usuario al hilo.
      - **Por qué**: El agente necesita el mensaje para procesar la solicitud.

  19. **`run = agent_client.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)`**:
      - `runs.create_and_process`: Crea y procesa una ejecución del agente.
      - **Parámetros**:
        - `thread_id=thread.id`: ID del hilo.
        - `agent_id=agent.id`: ID del agente.
      - **Propósito**: Ejecuta el agente en el hilo, invocando herramientas si es necesario.
      - **Por qué**: Procesa el mensaje del usuario y genera una respuesta.

  20. **`if run.status == "failed": print(f"Run failed: {run.last_error}")`**:
      - Verifica si la ejecución falló.
      - **Propósito**: Maneja errores en la ejecución.
      - **Por qué**: Asegura que se notifiquen fallos (e.g., rate limits).

  21. **`last_msg = agent_client.messages.get_last_message_text_by_role(thread_id=thread.id, role=MessageRole.AGENT)`**:
      - `messages.get_last_message_text_by_role`: Obtiene el último mensaje de texto del agente en el hilo.
      - **Parámetros**:
        - `thread_id=thread.id`: ID del hilo.
        - `role=MessageRole.AGENT`: Rol del agente.
      - **Propósito**: Recupera la respuesta del agente.
      - **Por qué**: Muestra la última respuesta al usuario.

  22. **`if last_msg: print(f"Assistant: {last_msg.text.value}")`**:
      - Imprime la respuesta si existe.
      - **Propósito**: Muestra la respuesta del agente en la consola.
      - **Por qué**: Completa la interacción del usuario.

  23. **`print("\nConversation Log:\n")`**:
      - Imprime un encabezado para el historial.
      - **Propósito**: Separa el historial de la conversación actual.

  24. **`messages = agent_client.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)`**:
      - `messages.list`: Lista todos los mensajes en el hilo.
      - **Parámetros**:
        - `thread_id=thread.id`: ID del hilo.
        - `order=ListSortOrder.ASCENDING`: Orden ascendente (del más viejo al más nuevo).
      - **Propósito**: Recupera el historial completo de la conversación.
      - **Por qué**: Muestra el registro completo al final.

  25. **`for message in messages: last_msg = message.text_messages[-1]; print(f"{message.role}: {last_msg.text.value}\n")`**:
      - Bucle sobre mensajes: Obtiene el último mensaje de texto de cada uno y lo imprime con el rol.
      - **Propósito**: Muestra el historial de la conversación.
      - **Por qué**: Permite revisar la interacción completa.

  26. **`agent_client.delete_agent(agent.id)`**:
      - `delete_agent`: Elimina el agente.
      - **Parámetros**: `agent.id`: ID del agente.
      - **Propósito**: Limpia recursos al finalizar.
      - **Por qué**: Evita costos innecesarios y mantiene el entorno limpio.

### Conjunto de Variables

- **`project_endpoint`**: Endpoint del proyecto de Azure AI Foundry, cargado de `.env`.
- **`model_deployment`**: Nombre del despliegue del modelo, cargado de `.env`.
- **`agent_client`**: Objeto cliente para gestionar agentes.
- **`functions`**: Herramienta basada en funciones personalizadas.
- **`toolset`**: Conjunto de herramientas registrado en el agente.
- **`agent`**: Objeto agente creado.
- **`thread`**: Objeto hilo de conversación.
- **`user_prompt`**: Prompt ingresado por el usuario.
- **`message`**: Mensaje agregado al hilo.
- **`run`**: Objeto de ejecución del agente.
- **`last_msg`**: Último mensaje del agente.
- **`messages`**: Lista de mensajes del historial.

### Sintaxis y Métodos Clave

- **Gestor de Contexto (`with agent_client:`)**: Asegura que el cliente se cierre automáticamente, liberando recursos.
- **Bucle `while True`**: Crea un chat interactivo infinito hasta "quit".
- **Condicionales (`if`, `elif`)**: Manejan entradas inválidas o comandos de salida.
- **Métodos del SDK**:
  - `AgentsClient(...)`: Crea el cliente con endpoint y credenciales.
  - `enable_auto_function_calls(toolset)`: Habilita llamadas automáticas a funciones.
  - `create_agent(...)`: Crea el agente con modelo, nombre, instrucciones y herramientas.
  - `threads.create()`: Crea un hilo de conversación.
  - `messages.create(...)`: Agrega un mensaje al hilo.
  - `runs.create_and_process(...)`: Ejecuta el agente en el hilo.
  - `get_run(...)`: Obtiene el estado de la ejecución.
  - `messages.get_last_message_text_by_role(...)`: Obtiene el último mensaje del agente.
  - `messages.list(...)`: Lista el historial de mensajes.
  - `delete_agent(...)`: Elimina el agente.

### Contexto en el Laboratorio

El script `agent.py` es el componente principal del laboratorio, donde se integra la función personalizada de `user_functions.py` para extender el agente con capacidades reales (e.g., generar tickets). El agente, configurado como un asistente de soporte técnico, usa herramientas para procesar entradas del usuario y mantener el estado de la conversación. Al final, muestra el historial y limpia recursos, demostrando un flujo completo de IA conversacional en Azure AI Agent Service. Esto alinea con AI-102 para implementar agentes que usan herramientas personalizadas en soluciones de IA.

El script asume un archivo `.env` con credenciales y un despliegue de modelo existente, enfocándose en la integración de herramientas y la interacción conversacional.
