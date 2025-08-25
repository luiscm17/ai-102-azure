#!/bin/bash

# Script para crear recursos de Azure para el laboratorio de AI Agents
# Este script crea un grupo de recursos y un recurso de Azure AI Foundry

# Configuración
RANDOM_SUFFIX=$((RANDOM % 10000))
LOCATION="eastus"  # Puedes cambiar la región según sea necesario
RESOURCE_GROUP_NAME="ai-agents-lab-rg-$RANDOM_SUFFIX"
AI_FOUNDRY_NAME="ai-foundry-$RANDOM_SUFFIX"

# Mostrar configuración
echo "Creando recursos de Azure con la siguiente configuración:"
echo "- Grupo de recursos: $RESOURCE_GROUP_NAME"
echo "- Recurso AI Foundry: $AI_FOUNDRY_NAME"
echo "- Región: $LOCATION"

# Crear grupo de recursos
echo "\nCreando grupo de recursos..."
az group create --name $RESOURCE_GROUP_NAME --location $LOCATION

# Crear recurso de Azure AI Foundry
echo "\nCreando recurso de Azure AI Foundry..."
az cognitiveservices account create \
    --name $AI_FOUNDRY_NAME \
    --resource-group $RESOURCE_GROUP_NAME \
    --location $LOCATION \
    --kind OpenAI \
    --sku s0 \
    --custom-domain $AI_FOUNDRY_NAME

# Mostrar información de conexión
echo "\nRecursos creados exitosamente:"
echo "- Grupo de recursos: $RESOURCE_GROUP_NAME"
echo "- Recurso AI Foundry: $AI_FOUNDRY_NAME"
echo "\nPuedes acceder al portal de Azure AI Foundry en: https://ai.azure.com"
echo "\nPara eliminar estos recursos cuando termines, ejecuta:"
echo "az group delete --name $RESOURCE_GROUP_NAME --yes --no-wait"