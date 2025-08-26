
# Capítulo 1: Overview de Azure AI Services

En este módulo, exploraremos los conceptos esenciales de Azure AI y cómo el SDK de Python nos permite interactuar con ellos de manera programática. Imagina Azure AI como un ecosistema de servicios inteligentes (visión, lenguaje, generative, etc.) que normalmente se gestionan vía el portal de Azure o Azure AI Foundry (un hub para AI agents y modelos). Sin embargo, con el SDK, podemos crear, configurar y operar estos recursos directamente desde código Python, lo que facilita la automatización, integración en pipelines y escalabilidad. Esto es ideal para ingenieros AI que buscan eficiencia y reproducibilidad.

El SDK de Python para Azure es modular: cada servicio tiene su paquete (e.g., `azure-ai-vision-imageanalysis`), pero todos comparten bases como `azure-core` para HTTP y `azure-identity` para autenticación segura. Usaremos versiones estables al 25 de agosto de 2025, verificadas en PyPI y docs de Microsoft (e.g., `azure-identity` v1.24.0). Progresaremos de lo básico (qué es Azure AI) a avanzado (gestión de accesos).

**Contexto y Narrativa**:  
Azure AI es una suite de servicios en la nube que incluye Cognitive Services (para visión, lenguaje, etc.), Azure OpenAI (para modelos generativos como GPT), y herramientas emergentes como Azure AI Foundry para agents y MCP (Model Context Protocol). El SDK de Python actúa como puente: en lugar de navegar el portal para deployar un modelo, escribes código para crearlo y usarlo. Esto es clave para la certificación AI-102, donde se evalúa tu habilidad para implementar soluciones AI end-to-end vía código. Por ejemplo, en lugar de clicar en el portal para un recurso de visión, usas `azure-mgmt-cognitiveservices` para provisionarlo. Incluimos una breve intro a generative AI (e.g., prompts y RAG) y agentic solutions (e.g., agents que usan MCP para integrar tools), ya que son parte del outline oficial.

**Didáctica Paso a Paso**:  

1. **Entiende el Ecosistema**: Azure AI se divide en categorías: Vision, Language, Generative, etc. El SDK cubre todo sin UI.
2. **Diferencias Clave**: SDK vs. REST API (SDK es más Pythonic y maneja auth automáticamente) vs. CLI (SDK es programable para scripts complejos).
3. **Beneficios del SDK**: Automatización (e.g., CI/CD), integración con apps Python, y manejo de recursos como si fueran objetos Python.
4. **Intro a Generative y Agentic**: Generative usa modelos como GPT para crear texto/imágenes; agentic implica agents que razonan y usan tools vía protocolos como MCP.

**Ejemplo de Código Práctico**:  
Instalemos el paquete de gestión base y listemos servicios disponibles (asumiendo auth configurada). Esto te da un overview programático.

Primero, instala: `pip install azure-mgmt-cognitiveservices==13.7.0 azure-identity==1.24.0`

Código de ejemplo (guárdalo como `overview_azure_ai.py` y ejecútalo):

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
import os

# Configura credenciales (usa variables de entorno para seguridad)
credential = DefaultAzureCredential()

# ID de tu suscripción Azure (reemplaza con el tuyo)
subscription_id = os.environ.get('AZURE_SUBSCRIPTION_ID', 'tu-subscription-id-aquí')

# Crea cliente de gestión
client = CognitiveServicesManagementClient(credential, subscription_id)

# Lista todos los recursos Cognitive Services en tu suscripción
print("Recursos Azure AI disponibles:")
for account in client.accounts.list():
    print(f"- Nombre: {account.name}, Tipo: {account.kind}, Ubicación: {account.location}")

# Ejemplo: Verifica si un servicio específico existe (e.g., para generative AI via OpenAI)
# Nota: Para OpenAI, usa azure-mgmt-openai en módulos posteriores
```

**Explicación del Código**:  

- `DefaultAzureCredential`: Intenta auth vía environment vars, managed identity, etc., sin exponer keys.  
- `CognitiveServicesManagementClient`: Objeto para manejar recursos (list, create, delete).  
- Ejecuta esto para ver un overview real de tus recursos. Si no tienes ninguno, el output será vacío—lo crearemos en capítulos siguientes.  

**Práctica Sugerida**: Modifica el código para filtrar por ubicación (e.g., 'eastus'). Investiga en docs.microsoft.com qué significa 'kind' (e.g., 'ComputerVision'). Esto te familiariza con el SDK sin portal.
