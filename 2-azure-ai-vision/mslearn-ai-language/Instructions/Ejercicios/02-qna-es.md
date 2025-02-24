---
Laboratorio:
título: 'Crear una solución de respuesta a preguntas'
módulo: 'Módulo 6 - Creación de soluciones de respuesta a preguntas con Azure AI Language'
---

# Crear una solución de respuesta a preguntas

Uno de los escenarios conversacionales más comunes es proporcionar soporte a través de una base de conocimientos de preguntas frecuentes (FAQ). Muchas organizaciones publican preguntas frecuentes como documentos o páginas web, lo que funciona bien para un pequeño conjunto de pares de preguntas y respuestas, pero la búsqueda de documentos grandes puede ser difícil y llevar mucho tiempo.

**Azure AI Language** incluye una  funcionalidad de *respuesta a preguntas* que le permite crear una base de conocimiento de pares de preguntas y respuestas que se pueden consultar mediante la entrada de lenguaje natural, y se usa más comúnmente como un recurso que un bot puede usar para buscar respuestas a las preguntas enviadas por los usuarios.

## Aprovisionamiento de un  recurso de *Azure AI Language*

Si aún no tiene uno en su suscripción, deberá aprovisionar un  recurso **Azure AI Language Service**. Además, para crear y alojar una base de conocimientos para responder preguntas, debe habilitar la  función **Respuesta a preguntas**.

1. Abra Azure Portal en "https://portal.azure.com" e inicie sesión con la cuenta de Microsoft asociada a su suscripción de Azure.
1. Seleccione **Crear un recurso**.
1. En el campo de búsqueda, busque **Servicio lingüístico**. A continuación, en los resultados, seleccione **Crear** en **Servicio de idioma**.
1. Seleccione el  bloque **Respuesta a preguntas personalizadas**. A continuación, seleccione **Continuar para crear el recurso**. Deberá ingresar a los siguientes configurados:

- **Suscripción**: *Su suscripción de Azure*
- **Grupo de recursos**: *Elija o cree un grupo de recursos*.
- **Región**: *Elige cualquier ubicación disponible*
- **Nombre**: *Introduzca un nombre único*
- **Plan de tarifa**: seleccione **F0** (*gratis*) o **S** (*estándar*) si F no está disponible.
- **Región de Búsqueda de Azure**: *Elija una ubicación en la misma región global que su recurso de idioma*
- **Plan de tarifa de Búsqueda de Azure**: Gratis (F) (*Si este nivel no está disponible, seleccione Básico (B)*)
- **Aviso de IA responsable**: *De acuerdo*

1. Selecciona **Crear + revisar**, luego selecciona **Crear**.

> **NOTA**
> Respuesta a preguntas personalizadas usa Búsqueda de Azure para indexar y consultar la base de conocimiento de preguntas y respuestas.

1. Espere a que se complete la implementación y, a continuación, vaya al recurso implementado.
1. Vea la  página **Claves y punto de conexión**. Necesitará la información de esta página más adelante en el ejercicio.

## Crear un proyecto de respuesta a preguntas

Para crear una base de conocimiento para responder a preguntas en el recurso de Azure AI Language, puede usar el portal de Language Studio para crear un proyecto de respuesta a preguntas. En este caso, creará una base de conocimiento que contenga preguntas y respuestas sobre [Microsoft Learn](https://docs.microsoft.com/learn).

1. En una nueva pestaña del navegador, vaya al portal de Language Studio en [https://language.cognitive.azure.com/](https://language.cognitive.azure.com/) e inicie sesión con la cuenta de Microsoft asociada a su suscripción de Azure.
1. Si se le pide que elija un recurso de idioma, seleccione la siguiente configuración:
- **Directorio de Azure**: el directorio de Azure que contiene su suscripción.
- **Suscripción de Azure**: Su suscripción de Azure.
- **Tipo de recurso**: Idioma
- **Nombre del recurso**: el recurso de Azure AI Language que creó anteriormente.

Si se le  solicita <u>not</u> que  elija un recurso de idioma, puede deberse a que tiene varios recursos de idioma en su suscripción; en cuyo caso:

1. En la barra en la parte superior de la página, seleccione la **Configuración (&#9881;)Botón ** .
2. En la  página **Configuración**, vea la  pestaña **Recursos**.
3. Seleccione el recurso de idioma que acaba de crear y haga clic en **Cambiar recurso**.
4. En la parte superior de la página, haga clic en **Language Studio** para volver a la página de inicio de Language Studio.

1. En la parte superior del portal, en el  menú **Crear nuevo**, seleccione **Respuesta a preguntas personalizadas**.
1. En el  asistente Crear un proyecto**, en la  página **Elegir configuración de idioma**, seleccione la opción **Seleccionar el idioma para todos los proyectos** y seleccione **Inglés** como idioma. A continuación, seleccione **Siguiente**.
1. En la  página **Introducir información básica**, introduzca los siguientes datos:
- **Nombre** 'LearnFAQ'
- **Descripción**: 'Preguntas frecuentes sobre Microsoft Learn'
- **Respuesta predeterminada cuando no se devuelve ninguna respuesta**: 'Lo siento, no entiendo la pregunta'
1. Seleccione **Siguiente**.
1. En la  página **Revisar y finalizar**, seleccione **Crear proyecto**.

## Agregar fuentes a la base de conocimientos

Puede crear una base de conocimientos desde cero, pero es común comenzar importando preguntas y respuestas de una página o documento de preguntas frecuentes existente. En este caso, importará datos de una página web de preguntas más frecuentes existente para Microsoft Learn y también importará algunas preguntas y respuestas predefinidas de "charla" para admitir intercambios conversacionales comunes.

1. En la  página **Administrar fuentes** de su proyecto de respuesta a preguntas, en la página **&#9547; Agregue la lista de fuentes**, seleccione **URLs**. A continuación, en el  cuadro de diálogo **Agregar direcciones URL**, seleccione **&#9547; Agregue URL** y establezca el siguiente nombre y URL antes de seleccionar **Agregar todo** para agregarlo a la base de conocimiento:
- **Nombre**: 'Página de preguntas frecuentes sobre el aprendizaje'
- **URL**: 'https://docs.microsoft.com/en-us/learn/support/faq'
1. En la  página **Administrar fuentes** de su proyecto de respuesta a preguntas, en la página **&#9547; Agregue la lista de fuentes**, seleccione **Chitchat**. En el cuadro de  diálogo **Agregar charla**, seleccione **Amigable** y seleccione **Agregar charla**.

## Editar la base de conocimientos

La base de conocimientos se ha rellenado con pares de preguntas y respuestas de las preguntas más frecuentes de Microsoft Learn, complementados con un conjunto de pares de  preguntas y respuestas conversacionales. Puede ampliar la base de conocimientos agregando pares de preguntas y respuestas adicionales.

1. En tu  proyecto **LearnFAQ** en Language Studio, selecciona la  página **Editar base de conocimientos** para ver los pares de preguntas y respuestas existentes (si se muestran algunos consejos, léelos y elige **Entendido** para descartarlos, o selecciona **Omitir todo**)
1. En la base de conocimientos, en la  pestaña **Pares de preguntas y respuestas**, seleccione **&#65291;** y cree un nuevo par de preguntas y respuestas con la siguiente configuración:
- **Fuente**: 'https://docs.microsoft.com/en-us/learn/support/faq'
- **Pregunta**: '¿Qué son las credenciales de Microsoft?'
- **Respuesta**: "Las credenciales de Microsoft le permiten validar y demostrar sus habilidades con las tecnologías de Microsoft".
1. Seleccione **Listo**.
1. En la página de la  pregunta **¿Qué son las credenciales de Microsoft?** que se crea, expanda **Preguntas alternativas**. A continuación, agregue la pregunta alternativa "¿Cómo puedo demostrar mis habilidades tecnológicas de Microsoft?".

En algunos casos, tiene sentido permitir que el usuario haga un seguimiento de una respuesta mediante la creación de una  conversación *de varios turnos* que permita al usuario refinar iterativamente la pregunta para obtener la respuesta que necesita.

1. Debajo de la respuesta que ingresó para la pregunta de certificación, expanda **Indicaciones de seguimiento** y agregue la siguiente sugerencia de seguimiento:
- **Texto que se muestra en el mensaje al usuario**: 'Más información sobre las credenciales'.
- Seleccione la  pestaña **Crear enlace a un nuevo par** e introduzca este texto: 'Puede obtener más información sobre las credenciales en la [página de credenciales de Microsoft](https://docs.microsoft.com/learn/credentials/)".
- Seleccione **Mostrar solo en flujo contextual**. Esta opción garantiza que la respuesta solo se devuelva en el contexto de una pregunta de seguimiento de la pregunta de certificación original.
1. Seleccione **Agregar mensaje**.

## Entrenar y probar la base de conocimientos

Ahora que tiene una base de conocimientos, puede probarla en Language Studio.

1. Guarde los cambios en su base de conocimientos seleccionando el  botón **Guardar** en la  pestaña **Pares de preguntas y respuestas** a la izquierda.
1. Una vez que se hayan guardado los cambios, seleccione el  botón **Probar** para abrir el panel de prueba.
1. En el panel de prueba, en la parte superior, anule la selección  de **Incluir respuesta de respuesta corta** (si aún no está seleccionado). Luego, en la parte inferior, ingrese el mensaje 'Hola'. Se debe devolver una respuesta adecuada.
1. En el panel de pruebas, en la parte inferior, escriba el mensaje '¿Qué es Microsoft Learn?'. Se debe devolver una respuesta adecuada de las preguntas frecuentes.
1. Ingrese el mensaje '¡Gracias!' Se debe devolver una respuesta adecuada de charla.
1. Ingrese el mensaje 'Hábleme de las credenciales de Microsoft'. La respuesta que creaste debe devolverse junto con un enlace de solicitud de seguimiento.
1. Seleccione el  enlace de seguimiento **Más información sobre las credenciales**. Se debe devolver la respuesta de seguimiento con un enlace a la página de certificación.
1. Cuando haya terminado de probar la base de conocimientos, cierre el panel de pruebas.

## Desplegar la base de conocimientos

La base de conocimiento proporciona un servicio back-end que las aplicaciones cliente pueden usar para responder preguntas. Ahora está listo para publicar su base de conocimientos y acceder a su interfaz REST desde un cliente.

1. En el  proyecto **LearnFAQ** de Language Studio, seleccione la  página **Implementar base de conocimientos** en el menú de navegación de la izquierda.
1. En la parte superior de la página, seleccione **Implementar**. A continuación, seleccione **Implementar** para confirmar que desea implementar la base de conocimiento.
1. Una vez completada la implementación, seleccione **Obtener URL de predicción** para ver el punto de conexión de REST de la base de conocimientos y tenga en cuenta que la solicitud de ejemplo incluye parámetros para:
- **projectName**: El nombre de tu proyecto (que debería ser *LearnFAQ*)
- **deploymentName**: El nombre de tu implementación (que debe ser *production*)
1. Cierre el cuadro de diálogo URL de predicción.

## Preparación para desarrollar una aplicación en Visual Studio Code

Desarrollará la aplicación de respuesta a preguntas con Visual Studio Code. Los archivos de código de la aplicación se han proporcionado en un repositorio de GitHub.

> **Sugerencia**: Si ya ha clonado el  repositorio **mslearn-ai-language**, ábralo en el código de Visual Studio. De lo contrario, siga estos pasos para clonarlo en su entorno de desarrollo.

1. Inicie Visual Studio Code.
2. Abra la paleta (SHIFT+CTRL+P) y ejecute un  comando **Git: Clone** para clonar el  repositorio 'https://github.com/MicrosoftLearning/mslearn-ai-language' en una carpeta local (no importa qué carpeta).
3. Cuando se haya clonado el repositorio, abra la carpeta en Visual Studio Code.

> **Nota**: Si Visual Studio Code le muestra un mensaje emergente para pedirle que confíe en el código que está abriendo, haga clic en la opción **Sí, confío en los autores** en la ventana emergente.

4. Espere mientras se instalan archivos adicionales para admitir los proyectos de código de C# en el repositorio.

> **Nota**: Si se le solicita que agregue los activos necesarios para compilar y depurar, seleccione **Ahora no**.

## Configura tu aplicación

Se han proporcionado aplicaciones para C# y Python, así como un archivo de texto de ejemplo que usará para probar el resumen. Ambas aplicaciones cuentan con la misma funcionalidad. En primer lugar, completará algunas partes clave de la aplicación para permitirle usar el recurso de Azure AI Language.

1. En Visual Studio Code, en el  panel **Explorer**, vaya a la  carpeta **Labfiles/02-qna** y expanda la  carpeta **CSharp** o **Python** en función de su preferencia de idioma y de la  carpeta **qna-app** que contenga. Cada carpeta contiene los archivos específicos del idioma de una aplicación en la que va a integrar la funcionalidad de respuesta a preguntas del lenguaje de Azure AI.
2. Haga clic con el botón derecho en la  carpeta **qna-app** que contiene sus archivos de código y abra un terminal integrado. A continuación, instale el paquete del SDK de respuesta a preguntas de Azure AI Language ejecutando el comando adecuado para su preferencia de idioma:

**C#**:

```
dotnet add package Azure.AI.Language.QuestionAnswering
```

**Pitón**:

```
pip install azure-ai-language-questionanswering
```

3. En el  panel **Explorer**, en la  carpeta **qna-app**, abra el archivo de configuración de su idioma preferido

- **C#**: appsettings.json
- **Pitón**: .env
4. Actualice los valores de configuración para incluir el **punto de conexión** y una **clave** del recurso de lenguaje de Azure que creó (disponible en la  página **Claves y punto de conexión** del recurso de lenguaje de IA de Azure en Azure Portal). El nombre del proyecto y el nombre de implementación de la base de conocimiento implementada también deben estar en este archivo.
5. Guarde el archivo de configuración.

## Agregar código a la aplicación

Ahora está listo para agregar el código necesario para importar las bibliotecas de SDK necesarias, establecer una conexión autenticada con el proyecto implementado y enviar preguntas.

1. Tenga en cuenta que la  carpeta **qna-app** contiene un archivo de código para la aplicación cliente:

- **C#**: Program.cs
- **Pitón**: qna-app.py

Abra el archivo de código y en la parte superior, debajo de las referencias de espacio de nombres existentes, busque el comentario **Importar espacios de nombres**. A continuación, en este comentario, agregue el siguiente código específico del idioma para importar los espacios de nombres que necesitará para usar el SDK de Text Analytics:

**C#**: Programs.cs

'''csharp
Importar espacios de nombres
uso de Azure;
usando Azure.IA.Idioma.PreguntaRespuesta;
```

**Pitón**: qna-app.py

'''pitón
# importar espacios de nombres
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.questionanswering import QuestionAnsweringClient
```

1. En la  función **Main**, tenga en cuenta que ya se ha proporcionado el código para cargar el punto de conexión y la clave del servicio Azure AI Language desde el archivo de configuración. A continuación, busque el comentario **Crear cliente mediante punto de conexión y clave** y agregue el siguiente código para crear un cliente para la API de análisis de texto:

**C#**: Programs.cs

'''C#
Creación de un cliente mediante el punto de conexión y la clave
Credenciales AzureKeyCredential  = new AzureKeyCredential(aiSvcKey);
Punto de conexión de Uri  = nuevo Uri(aiSvcEndpoint);
QuestionAnsweringClient aiClient = nuevo QuestionAnsweringClient(endpoint, credenciales);
```

**Pitón**: qna-app.py

'''Pitón
# Crear cliente usando punto final y clave
credential = AzureKeyCredential(ai_key)
ai_client = QuestionAnsweringClient(endpoint=ai_endpoint, credential=credential)
```

1. En la  función **Principal**, busque el comentario **Enviar una pregunta y mostrar la respuesta**, y agregue el siguiente código para leer repetidamente las preguntas desde la línea de comandos, enviarlas al servicio y mostrar los detalles de las respuestas:

**C#**: Programs.cs

'''C#
Envíe una pregunta y muestre la respuesta
cadena user_question = "";
while (verdadero)
{
Consola.Escribir("Pregunta: ");
user_question = Consola.LeerLínea();
Si (user_question.ToLower() == "salir")
descanso;
QuestionAnsweringProject project = new QuestionAnsweringProject(projectName, deploymentName);
Response<AnswersResult> respuesta = aiClient.GetAnswers(user_question, proyecto);
foreach (KnowledgeBaseAnswer respuesta en respuesta.Valor.Respuestas)
{
Consola.WriteLine(respuesta.Respuesta);
Consola.WriteLine($"Confianza: {respuesta.Confianza:P2}");
Consola.WriteLine($"Fuente: {respuesta.Fuente}");
Consola.WriteLine();
}
}
```

**Pitón**: qna-app.py

'''Pitón
# Envíe una pregunta y muestre la respuesta
user_question = ''
mientras que True:
user_question = input('\nPregunta:\n')
if user_question.lower() == "salir": 
quebrar
respuesta = ai_client.obtener_respuestas(pregunta=user_question,
project_name=ai_project_name,
deployment_name=ai_deployment_name)
para el candidato en response.answers:
print(candidato.respuesta)
print("Confianza: {}".format(candidato.confianza))
print("Fuente: {}".format(candidato.fuente))
```

1. Guarde los cambios y regrese al terminal integrado para la  carpeta **qna-app**, e ingrese el siguiente comando para ejecutar el programa:

- **C#**: 'ejecución de dotnet'
- **Pitón**: 'pitón qna-app.py'

> **Consejo**: Puede usar el  icono **Maximizar tamaño del panel** (**^**) en la barra de herramientas del terminal para ver más texto de la consola.

1. Cuando se le solicite, ingrese una pregunta para enviarla a su proyecto de respuesta a preguntas; por ejemplo, "¿Qué es una ruta de aprendizaje?".
1. Revise la respuesta que se devuelve.
1. Haz más preguntas. Cuando hayas terminado, ingresa 'salir'.

## Limpiar recursos

Si ha terminado de explorar el servicio de lenguaje de IA de Azure, puede eliminar los recursos que creó en este ejercicio. A continuación, te explicamos cómo hacerlo:

1. Abra Azure Portal en "https://portal.azure.com" e inicie sesión con la cuenta de Microsoft asociada a su suscripción de Azure.
2. Vaya al recurso de Azure AI Language que creó en este laboratorio.
3. En la página del recurso, seleccione **Eliminar** y siga las instrucciones para eliminar el recurso.

## Más información

Para obtener más información sobre la respuesta a preguntas en Azure AI Language, consulte la [Documentación de Azure AI Language](https://learn.microsoft.com/azure/ai-services/language-service/question-answering/overview).

