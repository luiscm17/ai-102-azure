# Curso  SDK Azure Python

## Módulo 0: Introducción y Fundamentos

- **Capítulo 1: Overview de Azure AI Services**  
  Conceptos: Servicios AI, SDK vs. otros. Incluir breve intro a generative AI y agentic solutions.

- **Capítulo 2: Setup del Entorno**  
  Creación de recursos vía SDK. Autenticación con `azure-identity`.

- **Capítulo 3: Instalación y Configuración Inicial**  
  Instalación de base SDKs, Jupyter setup.

- **Capítulo 4: Temas Avanzados en Fundamentos**  
  RBAC, multi-tenant vía código.

## Módulo 1: Plan and Manage an Azure AI Solution

- **Capítulo 1: Planificación de Soluciones AI**  
  Requisitos, costos, seguridad (incluyendo para generative y agentic).

- **Capítulo 2: Gestión de Recursos**  
  Deploy vía `azure-mgmt-cognitiveservices` (v13.7.0), `azure-ai-ml` (v1.28.1).

- **Capítulo 3: Monitoreo y Logging**  
  Azure Monitor en código.

- **Capítulo 4: Temas Avanzados**  
  CI/CD, compliance, costos optimizados para agents y generative.

## Módulo 2: Implement Generative AI Solutions

- **Capítulo 1: Introducción a Modelos Generativos**  
  Conceptos: GPT, DALL-E, prompts. Incluir overview de RAG como técnica clave.

- **Capítulo 2: Setup y Llamadas Básicas**  
  `openai` (v1.101.0) para Azure, completions, embeddings.

- **Capítulo 3: Uso Intermedio**  
  Chat, tool calling. Introducir basics de RAG (retrieval simple).

- **Capítulo 4: Temas Avanzados**  
  Fine-tuning, RAG completo (integración con search/indexes vía SDK como `azure-search-documents` v11.5.3 para retrieval). Evaluación con `azure-ai-evaluation` (v1.10.0). Seguridad en generative AI.

## Módulo 2.5: Implement an Agentic Solution (Nuevo, basado en outline oficial)

Este módulo cubre soluciones agentic, incluyendo MCP para integración con tools externos. Todo vía SDK Python.

- **Capítulo 1: Introducción a Agentic AI**  
  Conceptos: Agents AI, multi-turn interactions, tool integration. Overview de MCP como protocolo para context management y external connections.

- **Capítulo 2: Setup y Configuración Básica**  
  SDK: `azure-ai-generative` (v1.0.0b11), `openai` con extensions para agents, `azure-mcp-server` (v0.1.0 preview). Crear agents y conectar a Azure resources vía natural language commands.

- **Capítulo 3: Uso Intermedio**  
  Implementar agents con tool calling, multi-channel interactions (e.g., text/voice via MCP). Manejo de context protocol para data sources.

- **Capítulo 4: Temas Avanzados**  
  Integración RAG en agents (augmentar agents con retrieval). Custom tools con MCP, evaluación de agent performance. Seguridad y latency handling (e.g., usando Redis para context). Práctica: Agent que usa MCP para querying external APIs/Azure services.

## Módulo 3: Implement Computer Vision Solutions

- **Capítulo 1: Servicios de Visión Básicos**  
  Análisis, detección.

- **Capítulo 2: Análisis Básico**  
  `azure-ai-vision-imageanalysis` (v1.0.0).

- **Capítulo 3: Detección y Reconocimiento**  
  Facial, objetos.

- **Capítulo 4: Temas Avanzados**  
  Custom Vision, video.

## Módulo 4: Implement Natural Language Processing Solutions

- **Capítulo 1: Procesamiento de Texto Básico**  
  Sentiment, traducción.

- **Capítulo 2: Análisis y Traducción**  
  `azure-ai-textanalytics` (v5.3.0).

- **Capítulo 3: Conversational AI**  
  Bots con `botbuilder-core`.

- **Capítulo 4: Temas Avanzados**  
  CLU, anomaly detection. Incluir multi-turn patterns, enlazando a agentic.

## Módulo 5: Implement Content Moderation Solutions

- **Capítulo 1: Detección de Contenido Inapropiado**  
  Texto, imágenes.

- **Capítulo 2: Moderación Básica**  
  `azure-ai-contentsafety` (v1.0.0).

- **Capítulo 3: Uso Intermedio**  
  Multi-modal.

- **Capítulo 4: Temas Avanzados**  
  Custom policies, integración (e.g., con agents para moderación dinámica).

## Módulo 6: Implement Knowledge Mining and Document Intelligence Solutions

- **Capítulo 1: Extracción de Conocimiento**  
  Documentos, búsqueda.

- **Capítulo 2: Procesamiento de Documentos**  
  `azure-ai-documentintelligence` (v1.0.2).

- **Capítulo 3: Indexación y Búsqueda**  
  `azure-search-documents` (v11.5.3).

- **Capítulo 4: Temas Avanzados**  
  Knowledge bases, híbrida search. Enlazar a RAG para generative.
