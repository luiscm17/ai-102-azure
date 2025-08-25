#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para crear recursos de Azure para el laboratorio de AI Agents
Este script utiliza el SDK de Azure para crear un grupo de recursos y un recurso de Azure AI Foundry
"""

import random
import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
from azure.mgmt.cognitiveservices.models import (
    CognitiveServicesAccount,
    Sku,
    Identity,
    ApiProperties
)

def main():
    # Configuración
    random_suffix = random.randint(1000, 9999)
    subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
    location = "eastus"  # Puedes cambiar la región según sea necesario
    resource_group_name = f"ai-agents-lab-rg-{random_suffix}"
    ai_foundry_name = f"ai-foundry-{random_suffix}"

    print("\n=== Configuración de recursos de Azure ===")
    print(f"Suscripción: {subscription_id}")
    print(f"Grupo de recursos: {resource_group_name}")
    print(f"Recurso AI Foundry: {ai_foundry_name}")
    print(f"Región: {location}")

    # Autenticación
    print("\nAutenticando con Azure...")
    credential = DefaultAzureCredential()
    
    # Crear cliente de Resource Management
    resource_client = ResourceManagementClient(credential, subscription_id)
    
    # Crear grupo de recursos
    print(f"\nCreando grupo de recursos '{resource_group_name}'...")
    resource_group = resource_client.resource_groups.create_or_update(
        resource_group_name,
        {"location": location}
    )
    print(f"Grupo de recursos creado: {resource_group.name}")

    # Crear cliente de Cognitive Services
    cognitiveservices_client = CognitiveServicesManagementClient(
        credential=credential,
        subscription_id=subscription_id
    )

    # Configuración del recurso de AI Foundry
    sku = Sku(name="S0")
    properties = {
        "custom_sub_domain_name": ai_foundry_name,
        "api_properties": {
            "features": {
                "enable_data_export": True,
                "enable_logging": True
            }
        }
    }

    # Crear recurso de Azure AI Foundry
    print(f"\nCreando recurso de Azure AI Foundry '{ai_foundry_name}'...")
    account = cognitiveservices_client.accounts.begin_create(
        resource_group_name=resource_group_name,
        account_name=ai_foundry_name,
        account=CognitiveServicesAccount(
            sku=sku,
            kind="OpenAI",
            location=location,
            properties=properties
        )
    ).result()

    # Obtener las claves de acceso
    keys = cognitiveservices_client.accounts.list_keys(
        resource_group_name=resource_group_name,
        account_name=ai_foundry_name
    )

    # Mostrar información de conexión
    print("\n=== Recursos creados exitosamente ===")
    print(f"\nInformación del recurso:")
    print(f"- Nombre: {account.name}")
    print(f"- Grupo de recursos: {resource_group_name}")
    print(f"- Región: {account.location}")
    print(f"- Punto de conexión: {account.properties.endpoint}")
    print("\n=== Credenciales de acceso ===")
    print(f"Clave 1: {keys.key1}")
    print(f"Clave 2: {keys.key2}")
    print("\n=== Instrucciones adicionales ===")
    print(f"\nPuedes acceder al portal de Azure AI Foundry en: https://ai.azure.com")
    print("\nPara eliminar estos recursos cuando termines, ejecuta:")
    print(f"az group delete --name {resource_group_name} --yes --no-wait")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nAsegúrate de que:")
        print("1. Tienes la CLI de Azure instalada y has iniciado sesión con 'az login'")
        print("2. Tienes los permisos necesarios en la suscripción")
        print("3. Has configurado la variable de entorno AZURE_SUBSCRIPTION_ID")
        print("   En Linux/Mac: export AZURE_SUBSCRIPTION_ID='tu-id-de-suscripcion'")
        print("   En Windows: set AZURE_SUBSCRIPTION_ID=tu-id-de-suscripcion")
        exit(1)
