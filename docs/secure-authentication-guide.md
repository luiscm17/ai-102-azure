# Guía de Autenticación Segura para Azure AI

## Introducción

Esta guía cubre las mejores prácticas para manejar credenciales de manera segura al trabajar con los servicios de Azure AI. El manejo adecuado de credenciales es crítico para la seguridad de tus aplicaciones.

## Tabla de Contenidos

- [Manejo Seguro de Credenciales](#manejo-seguro-de-credenciales)
- [Uso de Variables de Entorno](#uso-de-variables-de-entorno)
- [Autenticación con DefaultAzureCredential](#autenticación-con-defaultazurecredential)
- [Configuración para Desarrollo](#configuración-para-desarrollo)
- [Configuración para Producción](#configuración-para-producción)
- [Solución de Problemas](#solución-de-problemas)

## Manejo Seguro de Credenciales

Nunca incluyas credenciales directamente en tu código fuente. En su lugar:

1. Usa variables de entorno para desarrollo local
2. Emplea Azure Key Vault para producción
3. Utiliza identidades administradas cuando sea posible
4. Implementa el principio de menor privilegio

## Uso de Variables de Entorno

### Instalación

```bash
pip install python-dotenv
```

### Configuración del Entorno

1. Crea un archivo `.env` en la raíz de tu proyecto:

   ```env
   # Azure AI Services
   AZURE_AI_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
   AZURE_AI_KEY=your_ai_key_here
   
   # Azure OpenAI
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_KEY=your_openai_key_here
   
   # Azure Storage
   AZURE_STORAGE_CONNECTION_STRING=your_storage_connection_string
   ```

2. Agrega `.env` a tu `.gitignore`:

   ```gitignore
   # Archivos de entorno
   .env
   ```

3. Carga las variables en tu aplicación:

   ```python
   from dotenv import load_dotenv
   import os
   
   load_dotenv()
   
   endpoint = os.getenv("AZURE_AI_ENDPOINT")
   key = os.getenv("AZURE_AI_KEY")
   ```

## Autenticación con DefaultAzureCredential

### Instalación

```bash
pip install azure-identity
```

### Uso Básico

```python
from azure.identity import DefaultAzureCredential
from azure.ai.textanalytics import TextAnalyticsClient
import os

# Inicializar credenciales
credential = DefaultAzureCredential()

# Usar con servicios de Azure AI
endpoint = os.getenv("AZURE_AI_ENDPOINT")
client = TextAnalyticsClient(endpoint=endpoint, credential=credential)
```

### Métodos de Autenticación Soportados

`DefaultAzureCredential` intenta autenticarse en este orden:

1. **Variables de entorno**
2. **Azure CLI** (`az login`)
3. **Managed Identity**
4. **Visual Studio Code**
5. **Visual Studio**
6. **Azure PowerShell**
7. **Autenticación interactiva en navegador**

## Configuración para Desarrollo

### Usando Azure CLI (Recomendado)

```bash
# Iniciar sesión
az login

# Listar suscripciones
az account list --output table

# Establecer suscripción por defecto
az account set --subscription "nombre-o-id-de-tu-suscripción"
```

### Usando Variables de Entorno

```bash
# Linux/macOS
export AZURE_CLIENT_ID="tu-client-id"
export AZURE_TENANT_ID="tu-tenant-id"
export AZURE_CLIENT_SECRET="tu-client-secret"

# Windows (PowerShell)
$env:AZURE_CLIENT_ID = "tu-client-id"
$env:AZURE_TENANT_ID = "tu-tenant-id"
$env:AZURE_CLIENT_SECRET = "tu-client-secret"
```

## Configuración para Producción

### Usando Azure Key Vault

```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

def get_secret(secret_name):
    key_vault_url = "https://your-keyvault.vault.azure.net/"
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=key_vault_url, credential=credential)
    return client.get_secret(secret_name).value

# Usar el secreto
ai_endpoint = get_secret("AI-SERVICE-ENDPOINT")
```

### Usando Identidades Administradas

```python
# En un servicio de Azure (como App Service o VM)
credential = DefaultAzureCredential()

# El servicio usará automáticamente la identidad administrada
client = TextAnalyticsClient(endpoint=endpoint, credential=credential)
```

## Solución de Problemas

### Errores Comunes

1. **Credenciales no encontradas**

   ```yml
   DefaultAzureCredential failed to retrieve a token from the included credentials.
   ```

   **Solución**: Configura al menos un método de autenticación válido.

2. **Permisos insuficientes**

   ```yml
   The client '...' does not have authorization to perform action '...'
   ```

   **Solución**: Verifica los roles RBAC en el recurso de Azure.

3. **Suscripción no encontrada**

   ```yml
   No se puede encontrar la suscripción con nombre o id '...'
   ```

   **Solución**: Verifica que hayas iniciado sesión correctamente.

### Habilitar Logging

```python
import logging
import sys

# Configurar logging
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

# Obtener credenciales con logging habilitado
credential = DefaultAzureCredential(logging_enable=True)
```

## Recursos Adicionales

- [Documentación de Azure Identity](https://learn.microsoft.com/python/api/overview/azure/identity-readme)
- [Guía de seguridad de Azure](https://learn.microsoft.com/azure/security/)
- [Buenas prácticas de seguridad en la nube](https://learn.microsoft.com/azure/architecture/framework/security/security-baseline)
