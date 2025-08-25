---
lab:
    title: 'Crear una solución de Question Answering'
    description: "Usa Azure AI Language para crear una solución personalizada de question answering."
---

# Crear una solución de Question Answering

Uno de los escenarios conversacionales más comunes es brindar soporte a través de una base de conocimiento de preguntas frecuentes (FAQs). Muchas organizaciones publican FAQs como documentos o páginas web, lo que funciona bien para un conjunto pequeño de pares de preguntas y respuestas, pero los documentos grandes pueden ser difíciles y llevar mucho tiempo buscar.

**Azure AI Language** incluye una capacidad de *question answering* que te permite crear una base de conocimiento de pares de preguntas y respuestas que pueden consultarse usando entrada de lenguaje natural, y se usa más comúnmente como un recurso que un bot puede usar para buscar respuestas a preguntas enviadas por usuarios. En este ejercicio, usarás el SDK de Python de Azure AI Language para text analytics para implementar una aplicación simple de question answering.

Si bien este ejercicio se basa en Python, puedes desarrollar aplicaciones de question answering usando múltiples SDKs específicos de lenguaje; incluyendo:

- [Biblioteca cliente de Question Answering de Azure AI Language Service para Python](https://pypi.org/project/azure-ai-language-questionanswering/)
- [Biblioteca cliente de Question Answering de Azure AI Language Service para .NET](https://www.nuget.org/packages/Azure.AI.Language.QuestionAnswering)

Este ejercicio toma aproximadamente **20** minutos.

## Aprovisionar un recurso de *Azure AI Language*

Si aún no tienes uno en tu suscripción, necesitarás aprovisionar un recurso de **servicio de Azure AI Language**. Adicionalmente, para crear y alojar una base de conocimiento para question answering, necesitas habilitar la característica **Question Answering**.

1. Abre el portal de Azure en `https://portal.azure.com` e inicia sesión usando la cuenta Microsoft asociada con tu suscripción de Azure.
1. Selecciona **Create a resource**.
1. En el campo de búsqueda, busca **Language service**. Luego, en los resultados, selecciona **Create** bajo **Language Service**.
1. Selecciona el bloque **Custom question answering**. Luego selecciona **Continue to create your resource**. Necesitarás ingresar la siguiente configuración:

    - **Subscription**: *Tu suscripción de Azure*
    - **Resource group**: *Elige o crea un grupo de recursos*.
    - **Region**: *Elige cualquier ubicación disponible*
    - **Name**: *Ingresa un nombre único*
    - **Pricing tier**: Selecciona **F0** (*gratuito*), o **S** (*estándar*) si F no está disponible.
    - **Azure Search region**: *Elige una ubicación en la misma región global que tu recurso de Language*
    - **Azure Search pricing tier**: Free (F) (*Si este nivel no está disponible, selecciona Basic (B)*)
    - **Responsible AI Notice**: *Acepta*

1. Selecciona **Create + review**, luego selecciona **Create**.

    > **NOTA**
    > Custom Question Answering usa Azure Search para indexar y consultar la base de conocimiento de preguntas y respuestas.

1. Espera a que la implementación se complete y luego ve al recurso implementado.
1. Visualiza la página **Keys and Endpoint** en la sección **Resource Management**. Necesitarás la información en esta página más adelante en el ejercicio.

## Crear un proyecto de question answering

Para crear una base de conocimiento para question answering en tu recurso de Azure AI Language, puedes usar el portal de Language Studio para crear un proyecto de question answering. En este caso, crearás una base de conocimiento que contiene preguntas y respuestas sobre [Microsoft Learn](https://docs.microsoft.com/learn).

1. En una nueva pestaña del navegador, ve al portal de Language Studio en [https://language.cognitive.azure.com/](https://language.cognitive.azure.com/) e inicia sesión usando la cuenta Microsoft asociada con tu suscripción de Azure.
1. Si se te solicita elegir un recurso de Language, selecciona la siguiente configuración:
    - **Azure Directory**: El directorio de Azure que contiene tu suscripción.
    - **Azure subscription**: Tu suscripción de Azure.
    - **Resource type**: Language
    - **Resource name**: El recurso de Azure AI Language que creaste anteriormente.

    Si <u>no</u> se te solicita elegir un recurso de lenguaje, puede ser porque tienes múltiples recursos de Language en tu suscripción; en cuyo caso:

    1. En la barra en la parte superior de la página, selecciona el botón **Settings (&#9881;)**.
    2. En la página **Settings**, visualiza la pestaña **Resources**.
    3. Selecciona el recurso de lenguaje que acabas de crear y haz clic en **Switch resource**.
    4. En la parte superior de la página, haz clic en **Language Studio** para regresar a la página de inicio de Language Studio.

1. En la parte superior del portal, en el menú **Create new**, selecciona **Custom question answering**.
1. En el asistente ***Create a project**, en la página **Choose language setting**, selecciona la opción para **Select the language for all projects**, y selecciona **English** como el idioma. Luego selecciona **Next**.
1. En la página **Enter basic information**, ingresa los siguientes detalles:
    - **Name** `LearnFAQ`
    - **Description**: `FAQ for Microsoft Learn`
    - **Default answer when no answer is returned**: `Lo siento, no entiendo la pregunta`
1. Selecciona **Next**.
1. En la página **Review and finish**, selecciona **Create project**.

## Agregar fuentes a la base de conocimiento

Puedes crear una base de conocimiento desde cero, pero es común comenzar importando preguntas y respuestas de una página FAQ existente o documento. En este caso, importarás datos de una página web FAQ existente para Microsoft Learn, y también importarás algunas preguntas y respuestas predefinidas de "chit chat" para soportar intercambios conversacionales comunes.

1. En la página **Manage sources** de tu proyecto de question answering, en la lista **&#9547; Add source**, selecciona **URLs**. Luego en el cuadro de diálogo **Add URLs**, selecciona **&#9547; Add url** y configura el siguiente nombre y URL antes de seleccionar **Add all** para agregarlo a la base de conocimiento:
    - **Name**: `Learn FAQ Page`
    - **URL**: `https://docs.microsoft.com/en-us/learn/support/faq`
1. En la página **Manage sources** de tu proyecto de question answering, en la lista **&#9547; Add source**, selecciona **Chitchat**. Luego en el cuadro de diálogo **Add chit chat**, selecciona **Friendly** y selecciona **Add chit chat**.

## Editar la base de conocimiento

Tu base de conocimiento ha sido poblada con pares de preguntas y respuestas del FAQ de Microsoft Learn, complementado con un conjunto de pares de preguntas y respuestas conversacionales de *chit-chat*. Puedes extender la base de conocimiento agregando pares adicionales de preguntas y respuestas.

1. En tu proyecto **LearnFAQ** en Language Studio, selecciona la página **Edit knowledge base** para ver los pares de preguntas y respuestas existentes (si se muestran algunos consejos, léelos y elige **Got it** para descartarlos, o selecciona **Skip all**)
1. En la base de conocimiento, en la pestaña **Question answer pairs**, selecciona **&#65291;**, y crea un nuevo par de pregunta respuesta con la siguiente configuración:
    - **Source**: `https://docs.microsoft.com/en-us/learn/support/faq`
    - **Question**: `What are Microsoft credentials?`
    - **Answer**: `Microsoft credentials enable you to validate and prove your skills with Microsoft technologies.`
1. Selecciona **Done**.
1. En la página para la pregunta **What are Microsoft credentials?** que se creó, expande **Alternate questions**. Luego agrega la pregunta alternativa `How can I demonstrate my Microsoft technology skills?`.

    En algunos casos, tiene sentido permitir al usuario hacer seguimiento a una respuesta creando una conversación *multi-turn* que permita al usuario refinar iterativamente la pregunta para llegar a la respuesta que necesita.

1. Debajo de la respuesta que ingresaste para la pregunta de certificación, expande **Follow-up prompts** y agrega el siguiente prompt de seguimiento:
    - **Text displayed in the prompt to the user**: `Learn more about credentials`.
    - Selecciona la pestaña **Create link to new pair**, e ingresa este texto: `You can learn more about credentials on the [Microsoft credentials page](https://docs.microsoft.com/learn/credentials/).`
    - Selecciona **Show in contextual flow only**. Esta opción asegura que la respuesta solo se devuelva en el contexto de una pregunta de seguimiento de la pregunta de certificación original.
1. Selecciona **Add prompt**.

## Entrenar y probar la base de conocimiento

Ahora que tienes una base de conocimiento, puedes probarla en Language Studio.

1. Guarda los cambios en tu base de conocimiento seleccionando el botón **Save** bajo la pestaña **Question answer pairs** a la izquierda.
1. Después de que se hayan guardado los cambios, selecciona el botón **Test** para abrir el panel de prueba.
1. En el panel de prueba, en la parte superior, deselecciona **Include short answer response** (si no está ya deseleccionado). Luego en la parte inferior ingresa el mensaje `Hello`. Debería devolverse una respuesta adecuada.
1. En el panel de prueba, en la parte inferior ingresa el mensaje `What is Microsoft Learn?`. Debería devolverse una respuesta apropiada del FAQ.
1. Ingresa el mensaje `Thanks!` Debería devolverse una respuesta apropiada de chit-chat.
1. Ingresa el mensaje `Tell me about Microsoft credentials`. Debería devolverse la respuesta que creaste junto con un enlace de prompt de seguimiento.
1. Selecciona el enlace de seguimiento **Learn more about credentials**. Debería devolverse la respuesta de seguimiento con un enlace a la página de certificación.
1. Cuando hayas terminado de probar la base de conocimiento, cierra el panel de prueba.

## Implementar la base de conocimiento

La base de conocimiento proporciona un servicio back-end que las aplicaciones cliente pueden usar para responder preguntas. Ahora estás listo para publicar tu base de conocimiento y acceder a su interfaz REST desde un cliente.

1. En el proyecto **LearnFAQ** en Language Studio, selecciona la página **Deploy knowledge base** desde el menú de navegación de la izquierda.
1. En la parte superior de la página, selecciona **Deploy**. Luego selecciona **Deploy** para confirmar que deseas implementar la base de conocimiento.
1. Cuando la implementación se complete, selecciona **Get prediction URL** para ver el endpoint REST para tu base de conocimiento y nota que la solicitud de ejemplo incluye parámetros para:
    - **projectName**: El nombre de tu proyecto (que debería ser *LearnFAQ*)
    - **deploymentName**: El nombre de tu implementación (que debería ser *production*)
1. Cierra el cuadro de diálogo de prediction URL.

## Prepararse para desarrollar una aplicación en Cloud Shell

Desarrollarás tu aplicación de question answering usando Cloud Shell en el portal de Azure. Los archivos de código para tu aplicación han sido proporcionados en un repositorio de GitHub.

1. En el Portal de Azure, usa el botón **[\>_]** a la derecha de la barra de búsqueda en la parte superior de la página para crear un nuevo Cloud Shell en el portal de Azure, seleccionando un entorno de ***PowerShell***. El cloud shell proporciona una interfaz de línea de comandos en un panel en la parte inferior del portal de Azure.

    > **Nota**: Si anteriormente creaste un cloud shell que usa un entorno *Bash*, cámbialo a ***PowerShell***.

1. En la barra de herramientas del cloud shell, en el menú **Settings**, selecciona **Go to Classic version** (esto es necesario para usar el editor de código).

    **<font color="red">Asegúrate de haber cambiado a la versión clásica del cloud shell antes de continuar.</font>**

1. En el panel de PowerShell, ingresa los siguientes comandos para clonar el repositorio de GitHub para este ejercicio:

    ```bash
    rm -r mslearn-ai-language -f
    git clone https://github.com/microsoftlearning/mslearn-ai-language
    ```

    > **Tip**: A medida que ingreses comandos en el cloudshell, la salida puede ocupar una gran parte del búfer de pantalla. Puedes limpiar la pantalla ingresando el comando `cls` para que sea más fácil enfocarse en cada tarea.

1. Después de que se haya clonado el repositorio, navega a la carpeta que contiene los archivos de código de la aplicación:  

    ```bash
    cd mslearn-ai-language/Labfiles/02-qna/Python/qna-app
    ```

## Configurar tu aplicación

1. En el panel de la línea de comandos, ejecuta el siguiente comando para ver los archivos de código en la carpeta **qna-app**:

    ```bash
   ls -a -l
    ```

    Los archivos incluyen un archivo de configuración (**.env**) y un archivo de código (**qna-app.py**).

1. Crea un entorno virtual de Python e instala el paquete del SDK de Question Answering de Azure AI Language y otros paquetes requeridos ejecutando el siguiente comando:

    ```bash
    python -m venv labenv
    ./labenv/bin/Activate.ps1
    pip install -r requirements.txt azure-ai-language-questionanswering
    ```

1. Ingresa el siguiente comando para editar el archivo de configuración:

    ```bash
    code .env
    ```

    El archivo se abre en un editor de código.

1. En el archivo de código, actualiza los valores de configuración que contiene para reflejar el **endpoint** y una **key** de autenticación para el recurso de Azure Language que creaste (disponible en la página **Keys and Endpoint** de tu recurso de Azure AI Language en el portal de Azure). El nombre del proyecto y el nombre de implementación para tu base de conocimiento implementada también deberían estar en este archivo.
1. Después de haber reemplazado los marcadores de posición, dentro del editor de código, usa el comando **CTRL+S** o **Clic derecho > Guardar** para guardar tus cambios y luego usa el comando **CTRL+Q** o **Clic derecho > Salir** para cerrar el editor de código mientras mantienes abierta la línea de comandos del cloud shell.

## Agregar código para usar tu base de conocimiento

1. Ingresa el siguiente comando para editar el archivo de código de la aplicación:

    ```bash
    code qna-app.py
    ```

1. Revisa el código existente. Agregarás código para trabajar con tu base de conocimiento.

    > **Tip**: A medida que agregues código al archivo de código, asegúrate de mantener la indentación correcta.

1. En el archivo de código, encuentra el comentario **Import namespaces**. Luego, debajo de este comentario, agrega el siguiente código específico del lenguaje para importar los espacios de nombres que necesitarás para usar el SDK de Question Answering:

    ```python
   # import namespaces
   from azure.core.credentials import AzureKeyCredential
   from azure.ai.language.questionanswering import QuestionAnsweringClient
    ```

1. En la función **main**, nota que el código para cargar el endpoint y la key del servicio Azure AI Language desde el archito de configuración ya ha sido proporcionado. Luego encuentra el comentario **Create client using endpoint and key**, y agrega el siguiente código para crear un cliente de question answering:

    ```Python
   # Create client using endpoint and key
   credential = AzureKeyCredential(ai_key)
   ai_client = QuestionAnsweringClient(endpoint=ai_endpoint, credential=credential)
    ```

1. En el archivo de código, encuentra el comentario **Submit a question and display the answer**, y agrega el siguiente código para leer repetidamente preguntas desde la línea de comandos, enviarlas al servicio y mostrar detalles de las respuestas:

    ```Python
   # Submit a question and display the answer
   user_question = ''
   while True:
        user_question = input('\nPregunta:\n')
        if user_question.lower() == "quit":                
            break
        response = ai_client.get_answers(question=user_question,
                                        project_name=ai_project_name,
                                        deployment_name=ai_deployment_name)
        for candidate in response.answers:
            print(candidate.answer)
            print("Confianza: {}".format(candidate.confidence))
            print("Fuente: {}".format(candidate.source))
    ```

1. Guarda tus cambios (CTRL+S), luego ingresa el siguiente comando para ejecutar el programa (puedes maximizar el panel del cloud shell y redimensionar los paneles para ver más texto en el panel de la línea de comandos):

    ```bash
    python qna-app.py
    ```

1. Cuando se te solicite, ingresa una pregunta para enviar a tu proyecto de question answering; por ejemplo `What is a learning path?`.
1. Revisa la respuesta que se devuelve.
1. Haz más preguntas. Cuando termines, ingresa `quit`.

## Limpiar recursos

Si has terminado de explorar el servicio Azure AI Language, puedes eliminar los recursos que creaste en este ejercicio. Así es cómo:

1. Cierra el panel de Azure cloud shell
1. En el portal de Azure, navega al recurso de Azure AI Language que creaste en este laboratorio.
1. En la página del recurso, selecciona **Delete** y sigue las instrucciones para eliminar el recurso.

## Más información

Para aprender más sobre question answering en Azure AI Language, consulta la [documentación de Azure AI Language](https://learn.microsoft.com/es-es/azure/ai-services/language-service/question-answering/overview).
