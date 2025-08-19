---
lab:
    title: "Afinar un modelo de lenguaje"
    description: "Aprende a usar tus propios datos de entrenamiento para afinar un modelo y personalizar su comportamiento."
---

# Afinar un modelo de lenguaje

Cuando deseas que un modelo de lenguaje se comporte de cierta manera, puedes usar ingeniería de prompts para definir el comportamiento deseado. Cuando quieres mejorar la consistencia del comportamiento deseado, puedes optar por afinar un modelo, comparándolo con tu enfoque de ingeniería de prompts para evaluar qué método se ajusta mejor a tus necesidades.

En este ejercicio, afinarás un modelo de lenguaje con Azure AI Foundry que deseas usar para un escenario de aplicación de chat personalizada. Compararás el modelo afinado con un modelo base para evaluar si el modelo afinado se ajusta mejor a tus necesidades.

Imagina que trabajas para una agencia de viajes y estás desarrollando una aplicación de chat para ayudar a las personas a planificar sus vacaciones. El objetivo es crear un chat simple e inspirador que sugiera destinos y actividades con un tono conversacional amigable y consistente.

Este ejercicio tomará aproximadamente **60** minutos\*.

> \* **Nota**: Este tiempo es una estimación basada en la experiencia promedio. El afinado depende de los recursos de infraestructura en la nube, que pueden tomar una cantidad variable de tiempo para provisionarse dependiendo de la capacidad del centro de datos y la demanda concurrente. Algunas actividades en este ejercicio pueden tomar <u>mucho</u> tiempo en completarse y requieren paciencia. Si las cosas están tardando, considera revisar la [documentación de afinado de Azure AI Foundry](https://learn.microsoft.com/azure/ai-studio/concepts/fine-tuning-overview) o tomar un descanso. Es posible que algunos procesos puedan agotar el tiempo de espera o parecer ejecutarse indefinidamente. Algunas de las tecnologías utilizadas en este ejercicio están en vista previa o en desarrollo activo. Puedes experimentar comportamientos inesperados, advertencias o errores.

## Implementar un modelo en un proyecto de Azure AI Foundry

Comencemos implementando un modelo en un proyecto de Azure AI Foundry.

1. En un navegador web, abre el [portal de Azure AI Foundry](https://ai.azure.com) en `https://ai.azure.com` e inicia sesión con tus credenciales de Azure. Cierra cualquier sugerencia o panel de inicio rápido que aparezca la primera vez que inicies sesión y, si es necesario, usa el logo de **Azure AI Foundry** en la parte superior izquierda para navegar a la página de inicio, que se verá similar a la siguiente imagen (cierra el panel **Help** si está abierto):

    ![Captura de pantalla del portal de Azure AI Foundry.](./media/ai-foundry-home.png)

1. En la página de inicio, en la sección **Explore models and capabilities**, busca el modelo `gpt-4o`, que usaremos en nuestro proyecto.
1. En los resultados de búsqueda, selecciona el modelo **gpt-4o** para ver sus detalles y luego, en la parte superior de la página del modelo, selecciona **Use this model**.
1. Cuando se te solicite crear un proyecto, ingresa un nombre válido para tu proyecto y expande **Advanced options**.
1. Selecciona **Customize** y especifica las siguientes configuraciones para tu proyecto:

    - **Azure AI Foundry resource**: _Un nombre válido para tu recurso de Azure AI Foundry_
    - **Subscription**: _Tu suscripción de Azure_
    - **Resource group**: _Crea o selecciona un grupo de recursos_
    - **Region**: _Selecciona una de las siguientes regiones_:\*
        - East US 2
        - North Central US
        - Sweden Central

    > \* Al momento de escribir, estas regiones admiten el afinado para modelos gpt-4o.

1. Selecciona **Create** y espera a que se cree tu proyecto. Si se te solicita, implementa el modelo gpt-4o usando el tipo de implementación **Global standard** y personaliza los detalles de la implementación para establecer un **Tokens per minute rate limit** de 50K (o el máximo disponible si es menor que 50K).

    > **Nota**: Reducir el TPM ayuda a evitar el uso excesivo de la cuota disponible en la suscripción que estás usando. 50,000 TPM deberían ser suficientes para los datos utilizados en este ejercicio. Si tu cuota disponible es menor, podrás completar el ejercicio pero puedes experimentar errores si se excede el límite de tasa.

1. Cuando se cree tu proyecto, el playground de chat se abrirá automáticamente para que puedas probar tu modelo.
1. En el panel **Setup**, observa el nombre de tu implementación de modelo; debería ser **gpt-4o**. Puedes confirmarlo viendo la implementación en la página **Models and endpoints** (solo abre esa página en el panel de navegación izquierdo).
1. En el panel de navegación izquierdo, selecciona **Overview** para ver la página principal de tu proyecto, que se verá así:

    ![Captura de pantalla de la página de resumen de un proyecto de Azure AI Foundry.](./media/ai-foundry-project.png)

## Afinar un modelo

Dado que afinar un modelo toma algo de tiempo para completarse, iniciarás el trabajo de afinado ahora y volverás a él después de explorar el modelo base gpt-4o que ya implementaste.

1. Descarga el [conjunto de datos de entrenamiento](https://raw.githubusercontent.com/MicrosoftLearning/mslearn-ai-studio/refs/heads/main/data/travel-finetune-hotel.jsonl) en `https://raw.githubusercontent.com/MicrosoftLearning/mslearn-ai-studio/refs/heads/main/data/travel-finetune-hotel.jsonl` y guárdalo como un archivo JSONL localmente.

    > **Nota**: Tu dispositivo podría guardar el archivo como .txt por defecto. Selecciona todos los archivos y elimina el sufijo .txt para asegurarte de que guardas el archivo como JSONL.

1. Navega a la página **Fine-tuning** bajo la sección **Build and customize**, usando el menú de la izquierda.
1. Selecciona el botón para agregar un nuevo modelo afinado, selecciona el modelo **gpt-4o** y luego selecciona **Next**.
1. **Afinar** el modelo usando la siguiente configuración:
    - **Method of customization**: Supervised
    - **Base model**: \*Selecciona la versión predeterminada de **gpt-4o\***
    - **Training data**: _Selecciona la opción **Add training data** y sube y aplica el archivo .jsonl que descargaste previamente_
    - **Model suffix**: `ft-travel`
    - **Seed**: \*Aleatorio
1. Envía los detalles del afinado y el trabajo comenzará. Puede tomar algo de tiempo en completarse. Puedes continuar con la siguiente sección del ejercicio mientras esperas.

> **Nota**: El afinado y la implementación pueden tomar una cantidad significativa de tiempo (30 minutos o más), por lo que es posible que necesites verificar periódicamente. Puedes ver más detalles del progreso hasta ahora seleccionando el trabajo de afinado del modelo y viendo su pestaña **Logs**.

## Chatear con un modelo base

Mientras esperas que se complete el trabajo de afinado, chateemos con un modelo base GPT 4o para evaluar su desempeño.

1. En el panel de navegación izquierdo, selecciona **Playgrounds** y abre el **Chat playground**.
1. Verifica que tu modelo base **gpt-4o** implementado esté seleccionado en el panel de configuración.
1. En la ventana de chat, ingresa la consulta `¿Qué puedes hacer?` y observa la respuesta.

    Las respuestas pueden ser bastante genéricas. Recuerda que queremos crear una aplicación de chat que inspire a las personas a viajar.

1. Actualiza el mensaje del sistema en el panel de configuración con el siguiente prompt:

    ```bash
    Eres un asistente de IA que ayuda a las personas a planificar sus viajes.
    ```

1. Selecciona **Apply changes** para actualizar el mensaje del sistema.
1. En la ventana de chat, ingresa la consulta `¿Qué puedes hacer?` nuevamente y observa la respuesta.

    Como respuesta, el asistente puede decirte que puede ayudarte a reservar vuelos, hoteles y autos de alquiler para tu viaje. Queremos evitar este comportamiento.

1. Actualiza el mensaje del sistema nuevamente con un nuevo prompt:

    ```bash
    Eres un asistente de viajes de IA que ayuda a las personas a planificar sus viajes. Tu objetivo es ofrecer soporte para consultas relacionadas con viajes, como requisitos de visa, pronósticos del tiempo, atracciones locales y normas culturales.
    No debes proporcionar recomendaciones de hoteles, vuelos, autos de alquiler o restaurantes.
    Haz preguntas atractivas para ayudar a alguien a planificar su viaje y pensar en lo que quiere hacer en sus vacaciones.
    ```

1. Continúa probando tu aplicación de chat para verificar que no proporcione información que no esté fundamentada en datos recuperados. Por ejemplo, haz las siguientes preguntas y revisa las respuestas del modelo, prestando especial atención al tono y estilo de escritura que el modelo usa para responder:

    `¿Dónde debería hospedarme en Roma?`

    `Principalmente voy por la comida. ¿Dónde debería hospedarme para estar a poca distancia de restaurantes asequibles?`

    `¿Cuáles son algunas delicias locales que debería probar?`

    `¿Cuál es la mejor época del año para visitar en términos del clima?`

    `¿Cuál es la mejor manera de moverse por la ciudad?`

## Revisar el archivo de entrenamiento

El modelo base parece funcionar lo suficientemente bien, pero es posible que busques un estilo conversacional particular para tu aplicación de IA generativa. Los datos de entrenamiento utilizados para el afinado te ofrecen la oportunidad de crear ejemplos explícitos de los tipos de respuesta que deseas.

1. Abre el archivo JSONL que descargaste previamente (puedes abrirlo en cualquier editor de texto).
1. Examina la lista de documentos JSON en el archivo de datos de entrenamiento. El primero debería ser similar a este (formateado para legibilidad):

    ```json
    {
        "messages": [
            {
                "role": "system",
                "content": "Eres un asistente de viajes de IA que ayuda a las personas a planificar sus viajes. Tu objetivo es ofrecer soporte para consultas relacionadas con viajes, como requisitos de visa, pronósticos del tiempo, atracciones locales y normas culturales. No debes proporcionar recomendaciones de hoteles, vuelos, autos de alquiler o restaurantes. Haz preguntas atractivas para ayudar a alguien a planificar su viaje y pensar en lo que quiere hacer en sus vacaciones."
            },
            { "role": "user", "content": "¿Qué es imprescindible ver en París?" },
            {
                "role": "assistant",
                "content": "¡Oh la la! ¡Simplemente debes girar alrededor de la Torre Eiffel y tomarte un selfie chic! Después de eso, considera visitar el Museo del Louvre para ver la Mona Lisa y otras obras maestras. ¿Qué tipo de atracciones te interesan más?"
            }
        ]
    }
    ```

    Cada ejemplo de interacción en la lista incluye el mismo mensaje del sistema que probaste con el modelo base, un prompt de usuario relacionado con una consulta de viaje y una respuesta. El estilo de las respuestas en los datos de entrenamiento ayudará al modelo afinado a aprender cómo debe responder.

## Implementar el modelo afinado

Cuando el afinado se haya completado con éxito, puedes implementar el modelo afinado.

1. Navega a la página **Fine-tuning** bajo **Build and customize** para encontrar tu trabajo de afinado y su estado. Si todavía está en ejecución, puedes optar por continuar chateando con tu modelo base implementado o tomar un descanso. Si se ha completado, puedes continuar.

    > **Consejo**: Usa el botón **Refresh** en la página de afinado para actualizar la vista. Si el trabajo de afinado desaparece por completo, actualiza la página en el navegador.

1. Selecciona el enlace del trabajo de afinado para abrir su página de detalles. Luego, selecciona la pestaña **Metrics** y explora las métricas del afinado.
1. Implementa el modelo afinado con las siguientes configuraciones:
    - **Deployment name**: _Un nombre válido para tu implementación de modelo_
    - **Deployment type**: Standard
    - **Tokens per Minute Rate Limit (thousands)**: 50K _(o el máximo disponible en tu suscripción si es menor que 50K)_
    - **Content filter**: Default
1. Espera a que la implementación se complete antes de poder probarlo, esto puede tomar un tiempo. Verifica el **Provisioning state** hasta que tenga éxito (es posible que necesites actualizar el navegador para ver el estado actualizado).

## Probar el modelo afinado

Ahora que implementaste tu modelo afinado, puedes probarlo como probaste tu modelo base implementado.

1. Cuando la implementación esté lista, navega al modelo afinado y selecciona **Open in playground**.
1. Asegúrate de que el mensaje del sistema incluya estas instrucciones:

    ```bash
    Eres un asistente de viajes de IA que ayuda a las personas a planificar sus viajes. Tu objetivo es ofrecer soporte para consultas relacionadas con viajes, como requisitos de visa, pronósticos del tiempo, atracciones locales y normas culturales.
    No debes proporcionar recomendaciones de hoteles, vuelos, autos de alquiler o restaurantes.
    Haz preguntas atractivas para ayudar a alguien a planificar su viaje y pensar en lo que quiere hacer en sus vacaciones.
    ```

1. Prueba tu modelo afinado para evaluar si su comportamiento es más consistente ahora. Por ejemplo, haz las siguientes preguntas nuevamente y explora las respuestas del modelo:

    `¿Dónde debería hospedarme en Roma?`

    `Principalmente voy por la comida. ¿Dónde debería hospedarme para estar a poca distancia de restaurantes asequibles?`

    `¿Cuáles son algunas delicias locales que debería probar?`

    `¿Cuál es la mejor época del año para visitar en términos del clima?`

    `¿Cuál es la mejor manera de moverse por la ciudad?`

1. Después de revisar las respuestas, ¿cómo se comparan con las del modelo base?

## Limpieza

Si has terminado de explorar Azure AI Foundry, debes eliminar los recursos que has creado para evitar costos innecesarios de Azure.

-   Navega al [portal de Azure](https://portal.azure.com) en `https://portal.azure.com`.
-   En el portal de Azure, en la página **Home**, selecciona **Resource groups**.
-   Selecciona el grupo de recursos que creaste para este ejercicio.
-   En la parte superior de la página **Overview** de tu grupo de recursos, selecciona **Delete resource group**.
-   Ingresa el nombre del grupo de recursos para confirmar que deseas eliminarlo y selecciona **Delete**.
