# Capítulo 3: Monitoreo y Logging

En este capítulo, nos sumergimos en el monitoreo y logging de recursos de Azure AI utilizando el SDK de Python, específicamente con Azure Monitor y el paquete `azure-monitor-query` (v1.4.0). Este capítulo es esencial para la certificación AI-102, ya que cubre cómo rastrear el rendimiento, detectar errores y mantener un control detallado de los recursos de Azure AI (como Cognitive Services o Azure Machine Learning) sin depender del portal de Azure o interfaces como Azure AI Foundry. Todo se realizará mediante código, permitiendo automatización y análisis programático de métricas y logs. Construiremos sobre los capítulos anteriores (planificación y gestión de recursos) para implementar monitoreo en los recursos creados, como el servicio Text Analytics o el workspace de Azure Machine Learning.

Usaremos `azure-monitor-query` para consultar métricas y logs, junto con `azure-identity` (v1.24.0) para autenticación segura y `logging` estándar de Python para depuración local. Este capítulo equilibra teoría, configuración y ejemplos prácticos para monitorear recursos en escenarios reales.

## Objetivos del Capítulo

- Configurar Azure Monitor para recursos Azure AI mediante SDK.
- Consultar métricas (e.g., uso de API, latencia) de un recurso Cognitive Services.
- Recuperar y analizar logs de actividad con `azure-monitor-query`.
- Implementar logging local para depuración y monitoreo.

## Configuración de Azure Monitor

**Explicación**:  
Azure Monitor es una herramienta centralizada para recopilar métricas (e.g., número de llamadas API, errores) y logs (e.g., registros de actividad) de recursos Azure. En lugar de usar el portal, configuraremos el acceso a Azure Monitor vía el SDK de Python (`azure-monitor-query`) para consultar datos de recursos como Text Analytics o Azure Machine Learning. Esto es clave para escenarios de Azure AI Foundry, donde necesitas monitorear el rendimiento de agentes o modelos generativos.

**Paso a Paso**:  

1. Instala el paquete `azure-monitor-query`.
2. Autentica con `DefaultAzureCredential`.
3. Configura un cliente para consultar métricas y logs.

**Código Práctico** (instalación, ejecuta en terminal):

```bash
pip install azure-monitor-query==1.4.0 azure-identity==1.24.0
```

**Código de Configuración** (guarda como `monitor_setup.py`):

```python
from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsClient, LogsQueryClient
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Configura credenciales
credential = DefaultAzureCredential()
subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID", "tu-subscription-id")
resource_group = "my-resource-group"
resource_name = "mytextanalytics002"

# Crea clientes
metrics_client = MetricsClient(credential)
logs_client = LogsQueryClient(credential)

# Obtener ID del recurso
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
client = CognitiveServicesManagementClient(credential, subscription_id)
resource = client.accounts.get(resource_group, resource_name)
resource_id = resource.id

logger.info(f"Configurado Azure Monitor para recurso: {resource_id}")
```

**Explicación**:  

- `MetricsClient`: Para consultar métricas como uso de API o latencia.
- `LogsQueryClient`: Para consultar logs de actividad (e.g., operaciones en el recurso).
- `resource_id`: Identificador único del recurso (necesario para consultas).

**Práctica**:  

- Ejecuta el código y verifica que no hay errores de autenticación.
- Cambia `resource_name` a otro recurso (e.g., `myopenai001` del Módulo 2). Obtén su `resource_id`.

## Consultar Métricas con Azure Monitor

**Explicación**:  
Las métricas son datos numéricos que reflejan el rendimiento de un recurso, como el número de llamadas API exitosas o errores 429 (límite de cuota). Usaremos `MetricsClient` para consultar métricas del recurso Text Analytics creado en el Capítulo 2. Esto es útil para monitorear el uso en aplicaciones de Azure AI Foundry (e.g., un agente que usa Text Analytics).

**Paso a Paso**:  

1. Identifica métricas disponibles (e.g., `TotalCalls`, `SuccessfulCalls`).
2. Consulta métricas para un período reciente.
3. Analiza resultados.

**Código Práctico** (guarda como `query_metrics.py`):

```python
from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsClient
from datetime import datetime, timedelta
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Configura credenciales
credential = DefaultAzureCredential()
subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
resource_group = "my-resource-group"
resource_name = "mytextanalytics002"

# Obtener resource_id
client = CognitiveServicesManagementClient(credential, subscription_id)
resource = client.accounts.get(resource_group, resource_name)
resource_id = resource.id

# Configura cliente de métricas
metrics_client = MetricsClient(credential)

# Define período (últimas 24 horas)
end_time = datetime.utcnow()
start_time = end_time - timedelta(hours=24)

# Consulta métricas
try:
    metrics = metrics_client.query_resource(
        resource_id=resource_id,
        metric_names=["TotalCalls", "SuccessfulCalls", "Latency"],
        timespan=(start_time, end_time),
        interval=timedelta(hours=1)  # Agrupar por hora
    )
    for metric in metrics.metrics:
        logger.info(f"Métrica: {metric.name}")
        for timeseries in metric.timeseries:
            for data in timeseries.data:
                if data.total:  # Algunas métricas pueden ser None
                    logger.info(f"  {data.time_stamp}: {data.total}")
except Exception as e:
    logger.error(f"Error al consultar métricas: {e}")
```

**Explicación**:  

- `metric_names`: Métricas comunes para Cognitive Services incluyen `TotalCalls` (total de llamadas API), `SuccessfulCalls` (llamadas exitosas), y `Latency` (tiempo de respuesta).
- `timespan`: Define el rango de tiempo (24 horas en este caso).
- `interval`: Agrupa datos por hora para facilitar análisis.

**Práctica**:  

- Ejecuta el código y revisa las métricas. Si no ves datos (porque el recurso es nuevo), realiza una llamada al servicio Text Analytics (usa el código del Capítulo 3, Módulo 0) y reintenta.
- Agrega otra métrica (e.g., `BlockedCalls` para errores de cuota). Consulta docs.microsoft.com para métricas disponibles.

## Consultar Logs de Actividad

**Explicación**:  
Los logs de actividad registran eventos como creación, actualización o uso de recursos. Usaremos `LogsQueryClient` para consultar logs con Kusto Query Language (KQL), el lenguaje de Azure Monitor para análisis de datos. Esto es útil para auditar operaciones o depurar errores.

**Paso a Paso**:  

1. Escribe una consulta KQL para logs de actividad.
2. Ejecuta la consulta y analiza resultados.
3. Maneja errores comunes (e.g., logs no disponibles).

**Código Práctico** (guarda como `query_logs.py`):

```python
from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient
from datetime import datetime, timedelta
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Configura credenciales
credential = DefaultAzureCredential()
subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")

# Configura cliente
logs_client = LogsQueryClient(credential)

# Define consulta KQL (logs de actividad)
query = f"""
AzureActivity
| where ResourceId contains "{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.CognitiveServices/accounts/{resource_name}"
| where TimeGenerated > ago(7d)
| project TimeGenerated, OperationName, ResultType, Caller
"""

# Ejecuta consulta
try:
    response = logs_client.query_workspace(
        workspace_id=os.environ.get("LOG_ANALYTICS_WORKSPACE_ID", "tu-workspace-id"),
        query=query,
        timespan=(datetime.utcnow() - timedelta(days=7), datetime.utcnow())
    )
    logger.info("Logs encontrados:")
    for table in response.tables:
        for row in table.rows:
            logger.info(f"  {row[0]}: Operación={row[1]}, Resultado={row[2]}, Caller={row[3]}")
except Exception as e:
    logger.error(f"Error al consultar logs: {e}")
```

**Explicación**:  

- `workspace_id`: ID de un Log Analytics Workspace. Si no tienes uno, crea uno con `azure-mgmt-monitor` o usa el portal una vez para obtenerlo.
- `query`: Consulta KQL que filtra logs de actividad para el recurso específico. `AzureActivity` es la tabla para eventos de gestión.
- `timespan`: Últimos 7 días. Ajusta según necesidad.

**Práctica**:  

- Configura `LOG_ANALYTICS_WORKSPACE_ID` (obtén de un workspace existente o crea uno).
- Ejecuta el código y revisa los logs (e.g., creación del recurso en el Capítulo 2).
- Modifica la consulta KQL para filtrar solo operaciones exitosas (`ResultType == "Success"`).

## Logging Local para Depuración

**Explicación**:  
Además de Azure Monitor, el logging local con el módulo `logging` de Python es crucial para depurar scripts y rastrear operaciones en tiempo real. Lo integramos en todos los ejemplos para mantener un registro claro.

**Código Práctico** (integrado en ejemplos anteriores, pero aquí un caso aislado):

```python
import logging

# Configurar logging a archivo
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("monitor.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Ejemplo de uso
logger.info("Iniciando monitoreo de recurso")
try:
    # Simula una operación
    logger.info("Operación simulada exitosa")
except Exception as e:
    logger.error(f"Error en operación: {e}")
```

**Explicación**:  

- `handlers`: Escribe logs a un archivo (`monitor.log`) y a la consola.
- **Uso**: Agrega `logger.info`/`logger.error` en cada paso crítico de tus scripts.

**Práctica**:  

- Agrega logging a `query_metrics.py` para registrar cada métrica encontrada.
- Simula un error (e.g., métrica inválida como `FakeMetric`) y revisa `monitor.log`.

## Validación y Solución de Problemas

**Explicación**:  
Validar las consultas asegura que el monitoreo funciona. Errores comunes incluyen permisos insuficientes, métricas/logs no disponibles o workspace ID incorrecto.

**Paso a Paso**:  

1. Verifica que el recurso tiene actividad reciente (realiza una llamada API si es necesario).
2. Confirma permisos en el Log Analytics Workspace (usa RBAC del Capítulo 4, Módulo 0).
3. Revisa logs locales y de Azure Monitor para depurar.

**Código para Crear Workspace Log Analytics** (si no tienes uno):

```python
from azure.mgmt.monitor import MonitorManagementClient
credential = DefaultAzureCredential()
client = MonitorManagementClient(credential, subscription_id)
workspace_name = "myloganalytics001"
try:
    workspace = client.workspaces.begin_create_or_update(
        resource_group,
        workspace_name,
        {"location": "eastus"}
    ).result()
    logger.info(f"Workspace Log Analytics creado: {workspace.name}")
except Exception as e:
    logger.error(f"Error: {e}")
```

**Práctica**:  

- Crea un workspace Log Analytics si no tienes uno.
- Revisa logs en `monitor.log` tras ejecutar los scripts.

## Notas Adicionales

- **Azure AI Foundry**: El monitoreo es clave para agents en Foundry, que necesitan métricas como latencia para optimizar rendimiento.
- **Costos**: Monitorea el uso de Log Analytics, ya que puede generar cargos. Usa el tier gratuito para pruebas.
- **Seguridad**: Usa RBAC para limitar acceso a logs/métricas (revisa el Capítulo 4, Módulo 0).

## Práctica Final

1. Ejecuta `monitor_setup.py` para configurar Azure Monitor.
2. Usa `query_metrics.py` para consultar métricas de `mytextanalytics002`. Realiza una llamada API (e.g., `recognize_entities` del Capítulo 3, Módulo 0) para generar datos.
3. Ejecuta `query_logs.py` con un workspace válido y revisa logs de actividad.
4. Agrega logging a todos los scripts y guarda resultados en `monitor.log`.
5. Investiga en docs.microsoft.com otras métricas disponibles para `TextAnalytics` (e.g., `DataProcessed`).

```python
# monitor_setup.py
from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsClient, LogsQueryClient
import os
import logging

# Configurar logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(**name**)

# Configura credenciales

credential = DefaultAzureCredential()
subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID", "tu-subscription-id")
resource_group = "my-resource-group"
resource_name = "mytextanalytics002"

# Crea clientes

metrics_client = MetricsClient(credential)
logs_client = LogsQueryClient(credential)

# Obtener ID del recurso

from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
client = CognitiveServicesManagementClient(credential, subscription_id)
resource = client.accounts.get(resource_group, resource_name)
resource_id = resource.id

logger.info(f"Configurado Azure Monitor para recurso: {resource_id}")
```

```python
# query_metrics.py
from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsClient
from datetime import datetime, timedelta
import os
import logging

# Configurar logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(**name**)

# Configura credenciales

credential = DefaultAzureCredential()
subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
resource_group = "my-resource-group"
resource_name = "mytextanalytics002"

# Obtener resource_id

client = CognitiveServicesManagementClient(credential, subscription_id)
resource = client.accounts.get(resource_group, resource_name)
resource_id = resource.id

# Configura cliente de métricas

metrics_client = MetricsClient(credential)

# Define período (últimas 24 horas)

end_time = datetime.utcnow()
start_time = end_time - timedelta(hours=24)

# Consulta métricas

try:
    metrics = metrics_client.query_resource(
        resource_id=resource_id,
        metric_names=["TotalCalls", "SuccessfulCalls", "Latency"],
        timespan=(start_time, end_time),
        interval=timedelta(hours=1)
    )
    for metric in metrics.metrics:
        logger.info(f"Métrica: {metric.name}")
        for timeseries in metric.timeseries:
            for data in timeseries.data:
                if data.total:
                    logger.info(f"  {data.time_stamp}: {data.total}")
except Exception as e:
    logger.error(f"Error al consultar métricas: {e}")
```

```python
# query_logs.py
from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient
from datetime import datetime, timedelta
import os
import logging

# Configurar logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(**name**)

# Configura credenciales

credential = DefaultAzureCredential()
subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
resource_group = "my-resource-group"
resource_name = "mytextanalytics002"

# Define consulta KQL

query = f"""
AzureActivity
| where ResourceId contains "{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.CognitiveServices/accounts/{resource_name}"
| where TimeGenerated > ago(7d)
| project TimeGenerated, OperationName, ResultType, Caller
"""

# Configura cliente

logs_client = LogsQueryClient(credential)

# Ejecuta consulta

try:
    response = logs_client.query_workspace(
        workspace_id=os.environ.get("LOG_ANALYTICS_WORKSPACE_ID", "tu-workspace-id"),
        query=query,
        timespan=(datetime.utcnow() - timedelta(days=7), datetime.utcnow())
    )
    logger.info("Logs encontrados:")
    for table in response.tables:
        for row in table.rows:
            logger.info(f"  {row[0]}: Operación={row[1]}, Resultado={row[2]}, Caller={row[3]}")
except Exception as e:
    logger.error(f"Error al consultar logs: {e}")
```
