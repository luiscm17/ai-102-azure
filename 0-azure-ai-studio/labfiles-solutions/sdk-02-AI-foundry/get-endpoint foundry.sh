# Obtener el nombre del recurso
RESOURCE_NAME="opengpt41-foundry-rs"
RESOURCE_GROUP="rg-gpt41-sdk"

# Obtener el endpoint base
ENDPOINT=$(az cognitiveservices account show \
  -n $RESOURCE_NAME \
  -g $RESOURCE_GROUP \
  --query "properties.endpoints['Azure AI Model Inference API']" \
  -o tsv)

# Construir el endpoint completo
DEPLOYMENT_NAME="gpt41-deployment"  # Reemplaza con tu nombre de deployment
API_VERSION="2025-01-01-preview"    # Usa la versión de API más reciente

echo "${ENDPOINT}openai/deployments/${DEPLOYMENT_NAME}/chat/completions?api-version=${API_VERSION}"