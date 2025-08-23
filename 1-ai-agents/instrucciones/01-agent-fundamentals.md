---
## lab: title: 'Explorar el desarrollo de agentes de IA' description: 'Da tus primeros pasos en el desarrollo de agentes de IA explorando el servicio Azure AI Agent en el portal de Azure AI Foundry.'
---

# Explorar el desarrollo de agentes de IA

En este ejercicio, usarás el servicio Azure AI Agent en el portal de Azure AI Foundry para crear un agente de IA simple que asista a los empleados con las reclamaciones de gastos.

Este ejercicio dura aproximadamente **30** minutos.

> **Nota**: Algunas de las tecnologías utilizadas en este ejercicio están en versión preliminar o en desarrollo activo. Es posible que experimentes un comportamiento inesperado, advertencias o errores.

## Crear un proyecto y un agente de Azure AI Foundry

Comencemos creando un proyecto de Azure AI Foundry.

1. En un navegador web, abre el [portal de Azure AI Foundry](https://ai.azure.com) en `https://ai.azure.com` e inicia sesión con tus credenciales de Azure. Cierra cualquier sugerencia o panel de inicio rápido que se abra la primera vez que inicies sesión, y si es necesario usa el logo de **Azure AI Foundry** en la parte superior izquierda para navegar a la página de inicio, que se ve similar a la siguiente imagen (cierra el panel de **Help** si está abierto):

2. En la página de inicio, selecciona **Create an agent**.

3. Cuando se te pida que crees un proyecto, introduce un nombre válido para tu proyecto.

4. Expande **Advanced options** y especifica las siguientes configuraciones:

    - **Azure AI Foundry resource**: _Un nombre válido para tu recurso de Azure AI Foundry_
    - **Subscription**: _Tu suscripción de Azure_
    - **Resource group**: _Selecciona tu grupo de recursos, o crea uno nuevo_
    - **Region**: \*Selecciona cualquier **AI Services supported location\***\*

    > \* Algunos recursos de Azure AI están restringidos por cuotas de modelo regionales. En caso de que se supere un límite de cuota más adelante en el ejercicio, existe la posibilidad de que necesites crear otro recurso en una región diferente.

5. Selecciona **Create** y espera a que se cree tu proyecto.

6. Si se te solicita, implementa un modelo **gpt-4o** usando el tipo de implementación **Global standard** o **Standard** (dependiendo de la disponibilidad de cuota) y personaliza los detalles de la implementación para establecer un **Tokens per minute rate limit** de 50K (o el máximo disponible si es menos de 50K).

    > **Nota**: Reducir el TPM ayuda a evitar el uso excesivo de la cuota disponible en la suscripción que estás utilizando. 50,000 TPM deberían ser suficientes para los datos utilizados en este ejercicio. Si tu cuota disponible es menor, podrás completar el ejercicio pero podrías experimentar errores si se excede el límite de tasa.

7. Cuando tu proyecto se haya creado, el playground de Agentes se abrirá automáticamente para que puedas seleccionar o implementar un modelo:

    > **Nota**: Un modelo base GPT-4o se implementa automáticamente al crear tu Agente y proyecto.

Verás que se ha creado un agente con un nombre predeterminado para ti, junto con la implementación de tu modelo base.

## Crear tu agente

Ahora que tienes un modelo implementado, estás listo para construir un agente de IA. En este ejercicio, construirás un agente simple que responde preguntas basadas en una política de gastos corporativos. Descargarás el documento de la política de gastos y lo usarás como datos de _grounding_ para el agente.

1. Abre otra pestaña del navegador y descarga [Expenses_policy.docx](https://raw.githubusercontent.com/MicrosoftLearning/mslearn-ai-agents/main/Labfiles/01-agent-fundamentals/Expenses_Policy.docx) desde `https://raw.githubusercontent.com/MicrosoftLearning/mslearn-ai-agents/main/Labfiles/01-agent-fundamentals/Expenses_Policy.docx` y guárdalo localmente. Este documento contiene detalles de la política de gastos para la corporación ficticia Contoso.

1. Vuelve a la pestaña del navegador que contiene el Foundry Agents playground y encuentra el panel **Setup** (puede estar a un lado o debajo de la ventana de chat).

1. Establece el **Agent name** en `ExpensesAgent`, asegúrate de que la implementación del modelo gpt-4o que creaste previamente esté seleccionada y establece las **Instructions** en:

    ```prompt
    You are an AI assistant for corporate expenses.
    You answer questions about expenses based on the expenses policy data.
    If a user wants to submit an expense claim, you get their email address, a description of the claim, and the amount to be claimed and write the claim details to a text file that the user can download.
    ```

    ![Screenshot of the AI agent setup page in Azure AI Foundry portal.](./Media/ai-agent-setup.png)

1. Más abajo en el panel **Setup**, junto al encabezado **Knowledge**, selecciona **+ Add**. Luego, en el cuadro de diálogo **Add knowledge**, selecciona **Files**.

1. En el cuadro de diálogo **Adding files**, crea un nuevo vector store llamado `Expenses_Vector_Store`, subiendo y guardando el archivo local **Expenses_policy.docx** que descargaste previamente.

1. En el panel **Setup**, en la sección **Knowledge**, verifica que **Expenses_Vector_Store** esté listado y se muestre que contiene 1 archivo.

1. Debajo de la sección **Knowledge**, junto a **Actions**, selecciona **+ Add**. Luego, en el cuadro de diálogo **Add action**, selecciona **Code interpreter** y luego selecciona **Save** (no necesitas subir ningún archivo para el code interpreter).

    Tu agente usará el documento que subiste como su fuente de conocimiento para _ground_ sus respuestas (en otras palabras, responderá preguntas basándose en el contenido de este documento). Usará la herramienta code interpreter según sea necesario para realizar acciones generando y ejecutando su propio código Python.

## Probar tu agente

Ahora que has creado un agente, puedes probarlo en el playground chat.

1. En la entrada del playground chat, ingresa el prompt: `What's the maximum I can claim for meals?` y revisa la respuesta del agente, que debería basarse en la información del documento de política de gastos que agregaste como conocimiento al setup del agente.

    > **Nota**: Si el agente no responde porque se excede el rate limit. Espera unos segundos e inténtalo de nuevo. Si no hay suficiente cuota disponible en tu suscripción, es posible que el modelo no pueda responder. Si el problema persiste, intenta aumentar la cuota para tu modelo en la página **Models + endpoints**.

2. Prueba el siguiente prompt de seguimiento: `I'd like to submit a claim for a meal.` y revisa la respuesta. El agente te pedirá la información necesaria para enviar una reclamación.

3. Proporciona al agente una dirección de correo electrónico; por ejemplo, `fred@contoso.com`. El agente debería reconocer la respuesta y solicitar la información restante necesaria para la reclamación de gastos (descripción y cantidad).

4. Envía un prompt que describa la reclamación y la cantidad; por ejemplo, `Breakfast cost me $20`.

5. El agente debe usar el code interpreter para preparar el archivo de texto de la reclamación de gastos y proporcionar un enlace para que puedas descargarlo.

6. Descarga y abre el documento de texto para ver los detalles de la reclamación de gastos.

## Limpieza

Ahora que has terminado el ejercicio, debes eliminar los recursos en la nube que has creado para evitar un uso innecesario de recursos.

1. Abre el [portal de Azure](https://portal.azure.com) en `https://portal.azure.com` y visualiza el contenido del resource group donde implementaste los recursos del hub utilizados en este ejercicio.
2. En la barra de herramientas, selecciona **Delete resource group**.
3. Introduce el nombre del resource group y confirma que quieres eliminarlo.
