#!/bin/bash
# Script para automatizar la creación de un recurso Azure OpenAI, deployment y recuperación de endpoint y claves
# Cumple con el objetivo del laboratorio: 100% automatizable, sin pasos manuales en el portal

set -e

# Configura estos valores antes de ejecutar el script
group_name="rg-ai-foundry-lab2"               # Ejemplo: rg-ai-foundry-lab2
location="eastus"                             # Región compatible con OpenAI
openai_name="openai-lab-sdk"                  # Nombre único para el recurso
sku="S0"                                      # SKU estándar
model_name="gpt-4o"                           # Cambia por el modelo deseado
model_version="2024-05-13"                    # Cambia por la versión deseada
model_format="OpenAI"
deployment_name="gpt4o-deployment"            # Nombre del deployment
sku_name="Standard"
sku_capacity=1

# 1. Crear grupo de recursos si no existe
echo "Creando grupo de recursos..."
az group create --name "$group_name" --location "$location"

# 2. Crear recurso Azure OpenAI
echo "Creando recurso Azure OpenAI..."
az cognitiveservices account create \
  --name "$openai_name" \
  --resource-group "$group_name" \
  --kind OpenAI \
  --sku "$sku" \
  --location "$location"

# 3. Listar modelos disponibles para el recurso
echo "Modelos disponibles para despliegue en este recurso:"
az cognitiveservices account deployment model list \
  --name "$openai_name" \
  --resource-group "$group_name"

# 4. Crear deployment del modelo
echo "Creando deployment del modelo..."
az cognitiveservices account deployment create \
  --name "$openai_name" \
  --resource-group "$group_name" \
  --deployment-name "$deployment_name" \
  --model-name "$model_name" \
  --model-version "$model_version" \
  --model-format "$model_format" \
  --sku-name "$sku_name" \
  --sku-capacity $sku_capacity

# 5. Obtener endpoint y claves
echo "Recuperando endpoint y claves..."
endpoint=$(az cognitiveservices account show \
  --name "$openai_name" \
  --resource-group "$group_name" \
  --query "properties.endpoint" -o tsv)
key=$(az cognitiveservices account keys list \
  --name "$openai_name" \
  --resource-group "$group_name" \
  --query "key1" -o tsv)

# 6. Mostrar instrucciones para .env
echo "\nAgrega lo siguiente a tu archivo .env:"
echo "AZURE_OPENAI_ENDPOINT=$endpoint"
echo "AZURE_OPENAI_KEY=$key"
echo "\nDeployment creado: $deployment_name (modelo: $model_name, versión: $model_version)"

echo "\n¡Listo! Recurso, deployment y claves generados automáticamente."
