# Capítulo 4: Temas Avanzados

En este capítulo, abordamos temas avanzados para la gestión de soluciones Azure AI, enfocándonos en la integración con CI/CD, cumplimiento normativo (compliance) y optimización de costos, todo mediante el SDK de Python. Este capítulo es crucial para la certificación AI-102, ya que cubre habilidades avanzadas para automatizar despliegues, garantizar conformidad con regulaciones (como GDPR) y gestionar costos de recursos como Cognitive Services, Azure OpenAI o Azure Machine Learning, sin depender del portal de Azure o interfaces como Azure AI Foundry. Usaremos paquetes como `azure-mgmt-cognitiveservices` (v13.7.0), `azure-ai-ml` (v1.28.1), `azure-mgmt-costmanagement` (v3.0.0), y `azure-identity` (v1.24.0) para autenticación. También introduciremos `azure-ai-resources` (v1.0.0b9, beta) para provisioning automatizado, útil para agentes y soluciones generativas en Azure AI Foundry.

Construiremos sobre los capítulos anteriores (planificación, gestión de recursos, monitoreo) para implementar flujos de trabajo avanzados, con ejemplos prácticos y logging robusto para depuración.

## Objetivos del Capítulo

- Configurar pipelines CI/CD para automatizar despliegues de recursos Azure AI.
- Implementar medidas de cumplimiento normativo (e.g., GDPR) vía SDK.
- Optimizar costos de recursos para agentes y soluciones generativas.
- Usar `azure-ai-resources` para provisioning automatizado.

## Configuración de Pipelines CI/CD

**Explicación**:  
CI/CD (Continuous Integration/Continuous Deployment) permite automatizar el despliegue y actualización de recursos Azure AI, como un servicio Text Analytics o un modelo generativo en Azure OpenAI. En lugar de usar Azure DevOps UI, configuraremos un pipeline programático con Python, simulando tareas como crear recursos, actualizar configuraciones o desplegar modelos en Azure Machine Learning. Esto es clave para entornos escalables, como los agentes en Azure AI Foundry, que requieren despliegues automatizados.

**Paso a Paso**:  

1. Crear un script para automatizar el despliegue de un recurso Cognitive Services.
2. Simular un pipeline CI/CD ejecutando tareas secuenciales (crear, validar, actualizar).
3. Usar logging para rastrear el proceso.

**Código Práctico** (guarda como `cicd_pipeline.py`):

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
import os
import logging
import time

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", handlers=[logging.FileHandler("cicd.log"), logging.StreamHandler()])
logger = logging.getLogger(__name__)

# Configura credenciales
credential = DefaultAzureCredential()
subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID", "tu-subscription-id")
resource_group = "my-resource-group"
account_name = f"mytextanalytics-cicd-{int(time.time())}"  # Nombre único con timestamp
location = "eastus"
sku_name = "S0"

# Crea cliente
client = CognitiveServicesManagementClient(credential, subscription_id)

# Paso 1: Crear recurso
try:
    logger.info(f"CI/CD: Creando recurso {account_name}")
    parameters = {
        "kind": "TextAnalytics",
        "sku": {"name": sku_name},
        "location": location,
        "properties": {}
    }
    poller = client.accounts.begin_create(resource_group, account_name, parameters)
    result = poller.result()
    logger.info(f"CI/CD: Recurso creado: {result.name}, Tipo: {result.kind}")
except Exception as e:
    logger.error(f"CI/CD: Error al crear recurso: {e}")
    exit(1)

# Paso 2: Validar recurso
try:
    resource = client.accounts.get(resource_group, account_name)
    logger.info(f"CI/CD: Validación exitosa: {resource.name}, SKU: {resource.sku.name}")
except Exception as e:
    logger.error(f"CI/CD: Error al validar: {e}")
    exit(1)

# Paso 3: Actualizar recurso (e.g., cambiar SKU)
try:
    logger.info(f"CI/CD: Actualizando {account_name} a S1")
    parameters = {"sku": {"name": "S1"}, "properties": {}}
    poller = client.accounts.begin_update(resource_group, account_name, parameters)
    result = poller.result()
    logger.info(f"CI/CD: Recurso actualizado: {result.name}, SKU: {result.sku.name}")
except Exception as e:
    logger.error(f"CI/CD: Error al actualizar: {e}")
```

**Explicación**:  

- **Pipeline Simulado**: El script ejecuta tres tareas (crear, validar, actualizar), simulando un pipeline CI/CD. En un entorno real, lo integrarías con GitHub Actions o Azure Pipelines YAML, pero aquí usamos Python puro.
- `account_name`: Usa un timestamp para evitar conflictos de nombres.
- **Logging**: Registra cada paso en `cicd.log` y consola, útil para debugging en CI/CD.

**Práctica**:  

- Ejecuta el script y revisa `cicd.log`. Verifica que el recurso se crea y actualiza.
- Modifica para crear un recurso `OpenAI`. Cambia `kind` a "OpenAI" y valida.
- Integra con un repositorio Git y prueba en un entorno CI/CD local (e.g., GitHub Actions, configurando variables de entorno).

## Cumplimiento Normativo (Compliance)

**Explicación**:  
El cumplimiento normativo, como GDPR, requiere medidas como encriptación de datos, control de acceso y auditoría. Usaremos el SDK para configurar propiedades de cumplimiento (e.g., encriptación en Cognitive Services) y auditar accesos con RBAC (como en el Capítulo 4, Módulo 0). Esto es crítico para agentes generativos en Azure AI Foundry, que manejan datos sensibles.

**Paso a Paso**:  

1. Configurar encriptación para un recurso Cognitive Services.
2. Auditar accesos con Azure Monitor (reutilizando logs del Capítulo 3).
3. Implementar tags para cumplimiento (e.g., marcar recursos como GDPR-compliant).

**Código Práctico** (guarda como `compliance_setup.py`):

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
from azure.monitor.query import LogsQueryClient
from datetime import datetime, timedelta
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", handlers=[logging.FileHandler("compliance.log"), logging.StreamHandler()])
logger = logging.getLogger(__name__)

# Configura credenciales
credential = DefaultAzureCredential()
subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
resource_group = "my-resource-group"
account_name = "mytextanalytics-cicd-1695582600"  # Usa un recurso existente

# Crea cliente
client = CognitiveServicesManagementClient(credential, subscription_id)

# Configurar encriptación y tags
try:
    logger.info(f"Configurando cumplimiento para {account_name}")
    parameters = {
        "tags": {"Compliance": "GDPR", "Environment": "Production"},
        "properties": {
            "encryption": {
                "keySource": "Microsoft.KeyVault"  # Requiere Key Vault configurado
            }
        }
    }
    poller = client.accounts.begin_update(resource_group, account_name, parameters)
    result = poller.result()
    logger.info(f"Recurso actualizado: {result.name}, Tags: {result.tags}")
except Exception as e:
    logger.error(f"Error al configurar cumplimiento: {e}")

# Auditar accesos con logs
logs_client = LogsQueryClient(credential)
query = f"""
AzureActivity
| where ResourceId contains "{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.CognitiveServices/accounts/{account_name}"
| where OperationName contains "Write"
| project TimeGenerated, Caller, OperationName
"""
try:
    response = logs_client.query_workspace(
        workspace_id=os.environ.get("LOG_ANALYTICS_WORKSPACE_ID"),
        query=query,
        timespan=(datetime.utcnow() - timedelta(days=7), datetime.utcnow())
    )
    logger.info("Auditoría de accesos:")
    for table in response.tables:
        for row in table.rows:
            logger.info(f"  {row[0]}: Operación={row[2]}, Caller={row[1]}")
except Exception as e:
    logger.error(f"Error al auditar: {e}")
```

**Explicación**:  

- `encryption`: Configura encriptación con Key Vault (requiere un Key Vault preexistente; crea uno con `azure-mgmt-keyvault` si necesario).
- `tags`: Etiquetas para identificar recursos en auditorías (e.g., GDPR).
- `query`: Consulta KQL para auditar operaciones de escritura (e.g., cambios en el recurso).

**Práctica**:  

- Ejecuta el script con un recurso existente. Verifica los tags en el portal (solo para validar).
- Crea un Key Vault con `azure-mgmt-keyvault` y actualiza el script para usar su ID.
- Modifica la consulta KQL para buscar operaciones de lectura (`OperationName contains "Read"`).

## Optimización de Costos

**Explicación**:  
Optimizar costos es vital para agentes y soluciones generativas, que pueden consumir muchos recursos (e.g., tokens en Azure OpenAI). Usaremos `azure-mgmt-costmanagement` para consultar costos y establecer alertas, y ajustaremos recursos para minimizar gastos (e.g., usar tier F0 gratuito cuando sea posible).

**Paso a Paso**:  

1. Consultar costos de un recurso con `azure-mgmt-costmanagement`.
2. Configurar una alerta de presupuesto.
3. Ajustar el tier de un recurso para optimizar costos.

**Código Práctico** (guarda como `cost_optimization.py`):

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.costmanagement import CostManagementClient
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
import os
import logging
from datetime import datetime, timedelta

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", handlers=[logging.FileHandler("cost.log"), logging.StreamHandler()])
logger = logging.getLogger(__name__)

# Configura credenciales
credential = DefaultAzureCredential()
subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
resource_group = "my-resource-group"
account_name = "mytextanalytics-cicd-1695582600"

# Consultar costos
cost_client = CostManagementClient(credential)
query = {
    "type": "ActualCost",
    "timeframe": "Last7Days",
    "dataset": {
        "granularity": "Daily",
        "aggregation": {"totalCost": {"name": "Cost", "function": "Sum"}},
        "filter": {
            "dimensions": {
                "name": "ResourceGroupName",
                "operator": "In",
                "values": [resource_group]
            }
        }
    }
}
try:
    logger.info("Consultando costos...")
    result = cost_client.query.usage(
        scope=f"/subscriptions/{subscription_id}",
        parameters=query
    )
    for row in result.rows:
        logger.info(f"Fecha: {row[0]}, Costo: {row[1]} {row[2]}")
except Exception as e:
    logger.error(f"Error al consultar costos: {e}")

# Configurar alerta de presupuesto
from azure.mgmt.consumption import ConsumptionManagementClient
consumption_client = ConsumptionManagementClient(credential, subscription_id)
budget = {
    "category": "Cost",
    "amount": 100.0,  # Límite de $100
    "timeGrain": "Monthly",
    "timePeriod": {
        "startDate": datetime.utcnow().isoformat(),
        "endDate": (datetime.utcnow() + timedelta(days=365)).isoformat()
    },
    "notifications": {
        "BudgetAlert": {
            "enabled": True,
            "operator": "GreaterThan",
            "threshold": 80.0,
            "contactEmails": ["tu-email@ejemplo.com"]
        }
    }
}
try:
    logger.info("Creando alerta de presupuesto")
    consumption_client.budgets.create_or_update(
        scope=f"/subscriptions/{subscription_id}",
        budget_name="mybudget001",
        parameters=budget
    )
    logger.info("Alerta de presupuesto creada")
except Exception as e:
    logger.error(f"Error al crear alerta: {e}")

# Ajustar tier para optimización
client = CognitiveServicesManagementClient(credential, subscription_id)
try:
    logger.info(f"Cambiando {account_name} a tier F0 (gratuito)")
    parameters = {"sku": {"name": "F0"}, "properties": {}}
    poller = client.accounts.begin_update(resource_group, account_name, parameters)
    result = poller.result()
    logger.info(f"Recurso optimizado: {result.name}, SKU: {result.sku.name}")
except Exception as e:
    logger.error(f"Error al optimizar: {e}")
```

**Explicación**:  

- `query.usage`: Consulta costos por resource group en los últimos 7 días.
- `budgets.create_or_update`: Crea una alerta de presupuesto para notificar si el gasto supera el 80% de $100.
- `sku: "F0"`: Cambia a tier gratuito (si aplica; verifica en docs para `TextAnalytics`).

**Práctica**:  

- Ejecuta el script y revisa los costos en `cost.log`.
- Cambia el presupuesto a $50 y ajusta el threshold a 90%.
- Intenta usar `F0` en un recurso OpenAI (nota: no todos los servicios soportan F0).

## Provisioning Automatizado con `azure-ai-resources`

**Explicación**:  
El paquete `azure-ai-resources` (v1.0.0b9, beta) simplifica el provisioning de recursos para soluciones generativas y agentes. Aunque en beta, es útil para automatizar despliegues complejos, como los requeridos en Azure AI Foundry.

**Paso a Paso**:  

1. Instala `azure-ai-resources`.
2. Configura un recurso OpenAI con propiedades avanzadas.

**Código Práctico** (guarda como `auto_provision.py`):

```python
from azure.identity import DefaultAzureCredential
import os
import logging

# Instala azure-ai-resources (beta)
# pip install azure-ai-resources==1.0.0b9

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", handlers=[logging.FileHandler("provision.log"), logging.StreamHandler()])
logger = logging.getLogger(__name__)

# Configura credenciales
credential = DefaultAzureCredential()
subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
resource_group = "my-resource-group"
account_name = f"myopenai-auto-{int(time.time())}"
location = "eastus"

# Crea cliente (usamos azure-mgmt-cognitiveservices como fallback, ya que azure-ai-resources es beta)
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
client = CognitiveServicesManagementClient(credential, subscription_id)

try:
    logger.info(f"Provisionando recurso {account_name}")
    parameters = {
        "kind": "OpenAI",
        "sku": {"name": "S0"},
        "location": location,
        "properties": {"customSubDomainName": account_name}
    }
    poller = client.accounts.begin_create(resource_group, account_name, parameters)
    result = poller.result()
    logger.info(f"Recurso provisionado: {result.name}, Tipo: {result.kind}")
except Exception as e:
    logger.error(f"Error al provisionar: {e}")
```

**Explicación**:  

- `azure-ai-resources`: En beta, puede fallar. Usamos `azure-mgmt-cognitiveservices` como alternativa estable.
- `customSubDomainName`: Personaliza el endpoint para agentes en Foundry.

**Práctica**:  

- Ejecuta el script y verifica el recurso. Si usas `azure-ai-resources`, instala y prueba (nota: beta, consulta docs).
- Cambia `kind` a "ComputerVision" y agrega un tag personalizado.

## Validación y Solución de Problemas

**Explicación**:  
Validar CI/CD, compliance y costos asegura que las configuraciones son robustas. Errores comunes incluyen permisos insuficientes, recursos no soportados (e.g., F0 no disponible) o consultas KQL mal formadas.

**Paso a Paso**:  

1. Revisa logs (`cicd.log`, `compliance.log`, `cost.log`) para confirmar operaciones.
2. Valida costos y alertas con el portal (solo para confirmar).
3. Usa `client.accounts.get` para verificar recursos actualizados.

**Código para Validación**:

```python
try:
    resource = client.accounts.get(resource_group, account_name)
    logger.info(f"Validación: {resource.name}, SKU: {resource.sku.name}, Tags: {resource.tags}")
except Exception as e:
    logger.error(f"Error al validar: {e}")
```

**Práctica**:  

- Ejecuta cada script y revisa los logs.
- Simula un error (e.g., presupuesto con threshold inválido) y depura.

## Notas Adicionales

- **Azure AI Foundry**: CI/CD y compliance son esenciales para agentes generativos, que requieren despliegues automatizados y datos seguros.
- **Costos**: Usa tiers bajos (F0) y elimina recursos con `client.accounts.delete` para pruebas.
- **Seguridad**: Configura Key Vault para encriptación y credenciales (Módulo posterior).

## Práctica Final

1. Ejecuta `cicd_pipeline.py` y verifica el pipeline en `cicd.log`.
2. Usa `compliance_setup.py` para agregar tags y auditar un recurso.
3. Ejecuta `cost_optimization.py` y revisa costos. Configura una alerta de $50.
4. Prueba `auto_provision.py` con un recurso OpenAI. Investiga `azure-ai-resources` en docs.microsoft.com.
5. Simula un pipeline CI/CD local ejecutando los scripts en secuencia (crear, actualizar, monitorear costos).

```python
#cicd_pipeline.py
from azure.identity import DefaultAzureCredential
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
import os
import logging
import time

# Configurar logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", handlers=[logging.FileHandler("cicd.log"), logging.StreamHandler()])
logger = logging.getLogger(**name**)

# Configura credenciales

credential = DefaultAzureCredential()
subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID", "tu-subscription-id")
resource_group = "my-resource-group"
account_name = f"mytextanalytics-cicd-{int(time.time())}"
location = "eastus"
sku_name = "S0"

# Crea cliente

client = CognitiveServicesManagementClient(credential, subscription_id)

# Paso 1: Crear recurso

try:
    logger.info(f"CI/CD: Creando recurso {account_name}")
    parameters = {
        "kind": "TextAnalytics",
        "sku": {"name": sku_name},
        "location": location,
        "properties": {}
    }
    poller = client.accounts.begin_create(resource_group, account_name, parameters)
    result = poller.result()
    logger.info(f"CI/CD: Recurso creado: {result.name}, Tipo: {result.kind}")
except Exception as e:
    logger.error(f"CI/CD: Error al crear recurso: {e}")
    exit(1)

# Paso 2: Validar recurso

try:
    resource = client.accounts.get(resource_group, account_name)
    logger.info(f"CI/CD: Validación exitosa: {resource.name}, SKU: {resource.sku.name}")
except Exception as e:
    logger.error(f"CI/CD: Error al validar: {e}")
    exit(1)

# Paso 3: Actualizar recurso

try:
    logger.info(f"CI/CD: Actualizando {account_name} a S1")
    parameters = {"sku": {"name": "S1"}, "properties": {}}
    poller = client.accounts.begin_update(resource_group, account_name, parameters)
    result = poller.result()
    logger.info(f"CI/CD: Recurso actualizado: {result.name}, SKU: {result.sku.name}")
except Exception as e:
    logger.error(f"CI/CD: Error al actualizar: {e}")
```

```python
# compliance_setup.py
from azure.identity import DefaultAzureCredential
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
from azure.monitor.query import LogsQueryClient
from datetime import datetime, timedelta
import os
import logging

# Configurar logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", handlers=[logging.FileHandler("compliance.log"), logging.StreamHandler()])
logger = logging.getLogger(**name**)

# Configura credenciales

credential = DefaultAzureCredential()
subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
resource_group = "my-resource-group"
account_name = "mytextanalytics-cicd-1695582600"

# Crea cliente

client = CognitiveServicesManagementClient(credential, subscription_id)

# Configurar encriptación y tags

try:
    logger.info(f"Configurando cumplimiento para {account_name}")
    parameters = {
        "tags": {"Compliance": "GDPR", "Environment": "Production"},
        "properties": {
            "encryption": {
                "keySource": "Microsoft.KeyVault"
            }
        }
    }
    poller = client.accounts.begin_update(resource_group, account_name, parameters)
    result = poller.result()
    logger.info(f"Recurso actualizado: {result.name}, Tags: {result.tags}")
except Exception as e:
    logger.error(f"Error al configurar cumplimiento: {e}")

# Auditar accesos

logs_client = LogsQueryClient(credential)
query = f"""
AzureActivity
| where ResourceId contains "{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.CognitiveServices/accounts/{account_name}"
| where OperationName contains "Write"
| project TimeGenerated, Caller, OperationName
"""
try:
    response = logs_client.query_workspace(
        workspace_id=os.environ.get("LOG_ANALYTICS_WORKSPACE_ID"),
        query=query,
        timespan=(datetime.utcnow() - timedelta(days=7), datetime.utcnow())
    )
    logger.info("Auditoría de accesos:")
    for table in response.tables:
        for row in table.rows:
            logger.info(f"  {row[0]}: Operación={row[2]}, Caller={row[1]}")
except Exception as e:
    logger.error(f"Error al auditar: {e}")
```

```python
# cost_optimization.py
from azure.identity import DefaultAzureCredential
from azure.mgmt.costmanagement import CostManagementClient
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
import os
import logging
from datetime import datetime, timedelta

# Configurar logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", handlers=[logging.FileHandler("cost.log"), logging.StreamHandler()])
logger = logging.getLogger(**name**)

# Configura credenciales

credential = DefaultAzureCredential()
subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
resource_group = "my-resource-group"
account_name = "mytextanalytics-cicd-1695582600"

# Consultar costos

cost_client = CostManagementClient(credential)
query = {
    "type": "ActualCost",
    "timeframe": "Last7Days",
    "dataset": {
        "granularity": "Daily",
        "aggregation": {"totalCost": {"name": "Cost", "function": "Sum"}},
        "filter": {
            "dimensions": {
                "name": "ResourceGroupName",
                "operator": "In",
                "values": [resource_group]
            }
        }
    }
}
try:
    logger.info("Consultando costos...")
    result = cost_client.query.usage(
        scope=f"/subscriptions/{subscription_id}",
        parameters=query
    )
    for row in result.rows:
        logger.info(f"Fecha: {row[0]}, Costo: {row[1]} {row[2]}")
except Exception as e:
    logger.error(f"Error al consultar costos: {e}")

# Configurar alerta de presupuesto

from azure.mgmt.consumption import ConsumptionManagementClient
consumption_client = ConsumptionManagementClient(credential, subscription_id)
budget = {
    "category": "Cost",
    "amount": 100.0,
    "timeGrain": "Monthly",
    "timePeriod": {
        "startDate": datetime.utcnow().isoformat(),
        "endDate": (datetime.utcnow() + timedelta(days=365)).isoformat()
    },
    "notifications": {
        "BudgetAlert": {
            "enabled": True,
            "operator": "GreaterThan",
            "threshold": 80.0,
            "contactEmails": ["tu-email@ejemplo.com"]
        }
    }
}
try:
    logger.info("Creando alerta de presupuesto")
    consumption_client.budgets.create_or_update(
        scope=f"/subscriptions/{subscription_id}",
        budget_name="mybudget001",
        parameters=budget
    )
    logger.info("Alerta de presupuesto creada")
except Exception as e:
    logger.error(f"Error al crear alerta: {e}")

# Ajustar tier

client = CognitiveServicesManagementClient(credential, subscription_id)
try:
    logger.info(f"Cambiando {account_name} a tier F0 (gratuito)")
    parameters = {"sku": {"name": "F0"}, "properties": {}}
    poller = client.accounts.begin_update(resource_group, account_name, parameters)
    result = poller.result()
    logger.info(f"Recurso optimizado: {result.name}, SKU: {result.sku.name}")
except Exception as e:
    logger.error(f"Error al optimizar: {e}")
```

```python
# auto_provision.py
from azure.identity import DefaultAzureCredential
import os
import logging

# Configurar logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", handlers=[logging.FileHandler("provision.log"), logging.StreamHandler()])
logger = logging.getLogger(**name**)

# Configura credenciales

credential = DefaultAzureCredential()
subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
resource_group = "my-resource-group"
account_name = f"myopenai-auto-{int(time.time())}"
location = "eastus"

# Crea cliente

from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
client = CognitiveServicesManagementClient(credential, subscription_id)

try:
    logger.info(f"Provisionando recurso {account_name}")
    parameters = {
        "kind": "OpenAI",
        "sku": {"name": "S0"},
        "location": location,
        "properties": {"customSubDomainName": account_name}
    }
    poller = client.accounts.begin_create(resource_group, account_name, parameters)
    result = poller.result()
    logger.info(f"Recurso provisionado: {result.name}, Tipo: {result.kind}")
except Exception as e:
    logger.error(f"Error al provisionar: {e}")
```
