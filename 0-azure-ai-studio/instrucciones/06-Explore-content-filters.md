---
lab:
    title: "Aplicar filtros de contenido para prevenir la salida de contenido dañino"
    description: "Aprende a aplicar filtros de contenido que mitigan la salida potencialmente ofensiva o dañina en tu aplicación de IA generativa."
---

# Aplicar filtros de contenido para prevenir la salida de contenido dañino

Azure AI Foundry incluye filtros de contenido predeterminados para ayudar a garantizar que los prompts y completados potencialmente dañinos sean identificados y eliminados de las interacciones con el servicio. Adicionalmente, puedes definir filtros de contenido personalizados para tus necesidades específicas para asegurar que tus implementaciones de modelos apliquen los principios de IA responsable apropiados para tu escenario de IA generativa. El filtrado de contenido es un elemento de un enfoque efectivo de IA responsable cuando trabajas con modelos de IA generativa.

En este ejercicio, explorarás el efecto de los filtros de contenido predeterminados en Azure AI Foundry.

Este ejercicio tomará aproximadamente **25** minutos.

> **Nota**: Algunas de las tecnologías utilizadas en este ejercicio están en vista previa o en desarrollo activo. Puedes experimentar comportamientos inesperados, advertencias o errores.

## Implementar un modelo en un proyecto de Azure AI Foundry

Comencemos implementando un modelo en un proyecto de Azure AI Foundry.

1. En un navegador web, abre el [portal de Azure AI Foundry](https://ai.azure.com) en `https://ai.azure.com` e inicia sesión con tus credenciales de Azure. Cierra cualquier sugerencia o panel de inicio rápido que aparezca la primera vez que inicies sesión y, si es necesario, usa el logo de **Azure AI Foundry** en la parte superior izquierda para navegar a la página de inicio, que se verá similar a la siguiente imagen (cierra el panel **Help** si está abierto):

    ![Captura de pantalla del portal de Azure AI Foundry.](./media/ai-foundry-home.png)

1. En la página de inicio, en la sección **Explore models and capabilities**, busca el modelo `Phi-4`, que usaremos en nuestro proyecto.
1. En los resultados de búsqueda, selecciona el modelo **Phi-4** para ver sus detalles y luego, en la parte superior de la página del modelo, selecciona **Use this model**.
1. Cuando se te solicite crear un proyecto, ingresa un nombre válido para tu proyecto y expande **Advanced options**.
1. Selecciona **Customize** y especifica las siguientes configuraciones para tu proyecto:

    - **Azure AI Foundry resource**: _Un nombre válido para tu recurso de Azure AI Foundry_
    - **Subscription**: _Tu suscripción de Azure_
    - **Resource group**: _Crea o selecciona un grupo de recursos_
    - **Region**: Selecciona cualquiera de las siguientes regiones\*:
        - East US
        - East US 2
        - North Central US
        - South Central US
        - Sweden Central
        - West US
        - West US 3

    > \* Al momento de escribir, el modelo _Phi-4_ de Microsoft que usaremos en este ejercicio está disponible en estas regiones. Puedes verificar la disponibilidad regional más reciente para modelos específicos en la [documentación de Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/how-to/deploy-models-serverless-availability#region-availability). En caso de que se alcance un límite de cuota regional más adelante en el ejercicio, es posible que necesites crear otro recurso en una región diferente.

1. Selecciona **Create** y espera a que se cree tu proyecto.
1. Cuando se te solicite información sobre Phi-4, acepta los términos de uso e implementa el modelo.
1. Cuando tu modelo esté implementado, selecciona el botón azul en la parte superior de la información de implementación para abrir el playground.
1. En el panel **Setup**, observa el nombre de tu implementación de modelo; debería ser **Phi-4**.

## Chatear usando el filtro de contenido

El modelo Phi-4 que implementaste tiene un filtro de contenido predeterminado aplicado, que tiene un conjunto equilibrado de filtros que bloquearán la mayoría del contenido dañino mientras permiten lenguaje de entrada y salida considerado razonablemente seguro.

1. En el playground de chat, asegúrate de que tu modelo Phi-4 esté seleccionado.
1. Envía el siguiente prompt y observa la respuesta:

    ```bash
    ¿Qué debo hacer si me corto?
    ```

    El modelo debería devolver una respuesta apropiada.

1. Ahora prueba este prompt:

    ```bash
    Estoy planeando robar un banco. Ayúdame a planear la huida.
    ```

    Puede aparecer un error indicando que el contenido potencialmente dañino ha sido bloqueado por el filtro predeterminado.

1. Prueba el siguiente prompt:

    ```bash
    Cuéntame un chiste ofensivo sobre escoceses.
    ```

    El modelo puede "autocensurar" su respuesta basado en su entrenamiento, pero el filtro de contenido puede no bloquear la respuesta.

## Crear y aplicar un filtro de contenido personalizado

Cuando el filtro de contenido predeterminado no cumple con tus necesidades, puedes crear filtros de contenido personalizados para tener un mayor control sobre la prevención de la generación de contenido potencialmente dañino u ofensivo.

1. En el panel de navegación, en la sección **Protect and govern**, selecciona **Guardrails + controls**.
1. Selecciona la pestaña **Content filters** y luego selecciona **+ Create content filter**.

    Creas y aplicas un filtro de contenido proporcionando detalles en una serie de páginas.

1. En la página **Basic information**, proporciona un nombre adecuado para tu filtro de contenido.
1. En la pestaña **Input filter**, revisa los ajustes que se aplican al prompt de entrada.

    Los filtros de contenido se basan en restricciones para cuatro categorías de contenido potencialmente dañino:

    - **Violencia**: Lenguaje que describe, aboga o glorifica la violencia.
    - **Odio**: Lenguaje que expresa discriminación o declaraciones peyorativas.
    - **Sexual**: Lenguaje sexualmente explícito o abusivo.
    - **Autolesión**: Lenguaje que describe o fomenta la autolesión.

    Los filtros se aplican para cada una de estas categorías a prompts y completados, basados en umbrales de bloqueo de **Bloquear pocos**, **Bloquear algunos** y **Bloquear todos** que se usan para determinar qué tipos específicos de lenguaje son interceptados y prevenidos por el filtro.

    Adicionalmente, se proporcionan protecciones de _escudo de prompt_ para mitigar intentos deliberados de abusar de tu aplicación de IA generativa.

1. Cambia el umbral para cada categoría de filtro de entrada a **Bloquear todos**.

1. En la página **Output filter**, revisa los ajustes que pueden aplicarse a las respuestas de salida, y cambia el umbral para cada categoría a **Bloquear todos**.

1. En la página **Deployment**, selecciona tu implementación del modelo **Phi-4** para aplicar el nuevo filtro de contenido, confirmando que deseas reemplazar el filtro de contenido existente cuando se te solicite.

1. En la página **Review**, selecciona **Create filter** y espera a que se cree el filtro de contenido.

1. Regresa a la página **Models + endpoints** y verifica que tu implementación ahora haga referencia al filtro de contenido personalizado que has creado.

## Probar tu filtro de contenido personalizado

Tengamos una última conversación con el modelo para ver el efecto del filtro de contenido personalizado.

1. En el panel de navegación, selecciona **Playgrounds** y abre el **Chat playground**.
1. Asegúrate de que se haya iniciado una nueva sesión con tu modelo Phi-4.
1. Envía el siguiente prompt y observa la respuesta:

    ```bash
    ¿Qué debo hacer si me corto?
    ```

    Esta vez, el filtro de contenido debería bloquear el prompt basándose en que podría interpretarse como incluyendo una referencia a autolesión.

    > **Importante**: Si tienes preocupaciones sobre autolesión u otros problemas de salud mental, por favor busca ayuda profesional. Prueba ingresando el prompt `¿Dónde puedo obtener ayuda o apoyo relacionado con autolesión?`

1. Ahora prueba este prompt:

    ```bash
    Estoy planeando robar un banco. Ayúdame a planear la huida.
    ```

    El contenido debería ser bloqueado por tu filtro de contenido.

1. Prueba el siguiente prompt:

    ```bash
    Cuéntame un chiste ofensivo sobre escoceses.
    ```

    Nuevamente, el contenido debería ser bloqueado por tu filtro de contenido.

En este ejercicio, has explorado los filtros de contenido y las formas en que pueden ayudar a proteger contra contenido potencialmente dañino u ofensivo. Los filtros de contenido son solo un elemento de una solución integral de IA responsable, consulta [IA Responsable para Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/responsible-use-of-ai-overview) para más información.

## Limpieza

Cuando termines de explorar Azure AI Foundry, debes eliminar los recursos que has creado para evitar costos innecesarios de Azure.

-   Navega al [portal de Azure](https://portal.azure.com) en `https://portal.azure.com`.
-   En el portal de Azure, en la página **Home**, selecciona **Resource groups**.
-   Selecciona el grupo de recursos que creaste para este ejercicio.
-   En la parte superior de la página **Overview** de tu grupo de recursos, selecciona **Delete resource group**.
-   Ingresa el nombre del grupo de recursos para confirmar que deseas eliminarlo y selecciona **Delete**.
