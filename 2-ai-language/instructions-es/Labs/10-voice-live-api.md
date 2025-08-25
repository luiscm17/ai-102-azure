---
lab:
    title: 'Explorar la API de Voice Live'
    description: 'Aprende cómo usar, y personalizar, la API de Voice Live disponible en el Playground de Azure AI Foundry.'
---

# Explorar la API de Voice Live

En este ejercicio creas un agente en Azure AI Foundry y exploras la API de Voice Live en el Speech Playground.

Este ejercicio toma aproximadamente **30** minutos para completar.

> <span style="color:red">**Nota**:</span> Algunas de las tecnologías usadas en este ejercicio están actualmente en preview o en desarrollo activo. Puedes experimentar algún comportamiento inesperado, advertencias o errores.
> <span style="color:red">**Nota**:</span> Este ejercicio está diseñado para completarse en un entorno de navegador con acceso directo al micrófono de tu computadora. Si bien los conceptos pueden explorarse en Azure Cloud Shell, las características de voz interactivas requieren acceso a hardware de audio local.

## Crear un proyecto de Azure AI Foundry

Comencemos creando un proyecto de Azure AI Foundry.

1. En un navegador web, abre el [portal de Azure AI Foundry](https://ai.azure.com) en `https://ai.azure.com` e inicia sesión usando tus credenciales de Azure. Cierra cualquier consejo o paneles de inicio rápido que se abran la primera vez que inicies sesión, y si es necesario usa el logo **Azure AI Foundry** en la parte superior izquierda para navegar a la página de inicio, que se ve similar a la siguiente imagen (cierra el panel **Help** si está abierto):

    ![Captura de pantalla de la página de inicio de Azure AI Foundry con crear un agente seleccionado.](../media/ai-foundry-new-home-page.png)

1. En la página de inicio, selecciona **Create an agent**.

1. En el asistente **Create an agent**, ingresa un nombre válido para tu proyecto.

1. Selecciona **Advanced options** y especifica la siguiente configuración:
    - **Azure AI Foundry resource**: *Mantén el nombre predeterminado*
    - **Subscription**: *Tu suscripción de Azure*
    - **Resource group**: *Crea o selecciona un grupo de recursos*
    - **Region**: Selecciona aleatoriamente una región de las siguientes opciones:\*
        - East US 2
        - Sweden Central

    > \* Al momento de escribir, la API de Voice Live solo es compatible con las regiones listadas previamente. Seleccionar una ubicación aleatoriamente ayuda a asegurar que una sola región no se sature con tráfico, y te ayuda a tener una experiencia más fluida. En caso de que se alcancen los límites de servicio, existe la posibilidad de que necesites crear otro proyecto en una región diferente.

1. Selecciona **Create** y revisa tu configuración. Espera a que el proceso de configuración se complete.

    >**Nota**: Si recibes un error de permisos, selecciona el botón **Fix it** para agregar los permisos apropiados para continuar.

1. Cuando tu proyecto esté creado, serás llevado por defecto al Agents playground en el portal de Azure AI Foundry, que debería verse similar a la siguiente imagen:

    ![Captura de pantalla de los detalles de un proyecto de Azure AI en el portal de Azure AI Foundry.](../media/ai-foundry-project-2.png)

## Iniciar una muestra de Voice Live

 En esta sección del ejercicio interactúas con uno de los agentes.

1. Selecciona **Playgrounds** en el panel de navegación.

1. Localiza el grupo **Speech playground**, y selecciona el botón **Try the Speech playground**.

1. El Speech Playground ofrece muchas opciones preconstruidas. Usa la barra de desplazamiento horizontal para navegar al final de la lista y selecciona el tile **Voice Live**.

    ![Captura de pantalla del tile de Voice Live.](../media/voice-live-tile.png)

1. Selecciona la muestra de agente **Casual chat** en el panel **Try with samples**.

1. Asegúrate de que tu micrófono y altavoces estén funcionando y selecciona el botón **Start** en la parte inferior de la página.

    Mientras interactúas con el agente, nota que puedes interrumpir al agente y se pausará para escuchar. Intenta hablar con diferentes longitudes de pausas entre palabras y oraciones. Nota qué tan rápido el agente reconoce las pausas y llena la conversación. Cuando hayas terminado selecciona el botón **End**.

1. Inicia los otros agentes de muestra para explorar cómo se comportan.

    Mientras exploras los diferentes agentes, nota los cambios en la sección **Response instruction** en el panel **Configuration**.

## Configurar el agente

En esta sección cambias la voz del agente, y agregas un avatar al agente **Casual chat**. El panel **Configuration** está dividido en tres secciones: **GenAI**, **Speech**, y **Avatar**.

>**Nota:** Si cambias, o interactúas con, cualquiera de las opciones de configuración, necesitas seleccionar el botón **Apply** en la parte inferior del panel **Configuration** para habilitar el agente.

Selecciona el agente **Casual chat**. Luego, cambia la voz del agente, y agrega un avatar, con las siguientes instrucciones:

1. Selecciona **> Speech** para expandir la sección y acceder a las opciones.

1. Selecciona el menú desplegable en la opción **Voice** y elige una voz diferente.

1. Selecciona **Apply** para guardar tus cambios, y luego **Start** para lanzar el agente y escuchar tu cambio.

    Repite los pasos anteriores para probar algunas voces diferentes. Procede al siguiente paso cuando hayas terminado con la selección de voz.

1. Selecciona **> Avatar** para expandir la sección y acceder a las opciones.

1. Selecciona el botón de toggle para habilitar la característica y selecciona uno de los avatares.

1. Selecciona **Apply** para guardar tus cambios, y luego **Start** para lanzar el agente.

    Nota la animación del avatar y su sincronización con el audio.

1. Expande la sección **> GenAI** y establece el toggle **Proactive engagement** en la posición off. Luego, selecciona **Apply** para guardar tus cambios, y luego **Start** para lanzar el agente.

    Con el **Proactive engagement** apagado, el agente no inicia la conversación. Pregúntale al agente "¿Puedes decirme qué haces?" para iniciar la conversación.

>**Tip:** Puedes seleccionar **Reset to default** y luego **Apply** para devolver el agente a su comportamiento predeterminado.

Cuando hayas terminado, procede a la siguiente sección.

## Crear un agente de voz

En esta sección creas tu propio agente de voz desde cero.

1. Selecciona **Start from blank** en la sección **Try with your own** del panel.

1. Expande la sección **> GenAI** del panel **Configuration**.

1. Selecciona el menú desplegable **Generative AI model** y elige el modelo **GPT-4o Mini Realtime**.

1. Agrega el siguiente texto en la sección **Response instruction**.

    ```yml
    Eres un agente de voz llamado "Ava" que actúa como un agente amigable de alquiler de autos. 
    ```

1. Establece el slider **Response temperature** a un valor de **0.8**.

1. Establece el toggle **Proactive engagement** en la posición on.

1. Selecciona **Apply** para guardar tus cambios, y luego **Start** para lanzar el agente.

    El agente se presentará y preguntará cómo puede ayudarte hoy. Pregúntale al agente "¿Tienes algún sedán disponible para alquilar el jueves?" Nota cuánto tiempo tarda el agente en responder. Pregúntale al agente otras preguntas para ver cómo responde. Cuando hayas terminado, procede al siguiente paso.

1. Expande la sección **> Speech** del panel **Configuration**.

1. Establece el botón de toggle **End of utterance (EOU)** en la posición **on**.

1. Establece el botón de toggle **Audio enhancement** en la posición **on**.

1. Selecciona **Apply** para guardar tus cambios, y luego **Start** para lanzar el agente.

    Después de que el agente se presente, pregúntale "¿Tienes algún avión para alquilar?" Nota que el agente responde más rápidamente de lo que lo hizo anteriormente después de terminar tu pregunta. La configuración **End of utterance (EOU)** configura al agente para detectar pausas y tu fin de habla basado en contexto y semántica. Esto le permite tener una conversación más natural.

Cuando hayas terminado, procede a la siguiente sección.

## Limpiar recursos

Ahora que terminaste el ejercicio, elimina el proyecto que creaste para evitar uso innecesario de recursos.

1. Selecciona **Management center** en el menú de navegación de AI Foundry.
1. Selecciona **Delete project** en el panel de información derecho, y luego confirma la eliminación.
