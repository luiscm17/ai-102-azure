---
Laboratorio:
title: 'Traducir texto'
módulo: 'Módulo 3 - Introducción al procesamiento del lenguaje natural'
---

# Traducir texto

**Azure AI Translator** es un servicio que permite traducir texto entre idiomas. En este ejercicio, lo usará para crear una aplicación sencilla que traduzca la entrada en cualquier idioma compatible al idioma de destino de su elección.

## Aprovisionamiento de un  recurso *Azure AI Translator*

Si aún no tiene uno en su suscripción, deberá aprovisionar un  recurso **Azure AI Translator**.

1. Abra Azure Portal en "https://portal.azure.com" e inicie sesión con la cuenta de Microsoft asociada a su suscripción de Azure.
1. En el campo de búsqueda de la parte superior, busque **Azure AI services** y pulse **Intro** y, a continuación, seleccione **Crear** en **Traductor** en los resultados.
1. Cree un recurso con la siguiente configuración:
- **Suscripción**: *Su suscripción de Azure*
- **Grupo de recursos**: *Elija o cree un grupo de recursos*
- **Región**: *Elige cualquier región disponible*
- **Nombre**: *Introduzca un nombre único*
- **Plan de tarifa**: seleccione **F0** (*gratis*) o **S** (*estándar*) si F no está disponible.
- **Aviso de IA responsable**: De acuerdo.
1. Seleccione **Revisar + crear** y, a continuación, seleccione **Crear** para aprovisionar el recurso.
1. Espere a que se complete la implementación y, a continuación, vaya al recurso implementado.
1. Vea la  página **Claves y punto de conexión**. Necesitará la información de esta página más adelante en el ejercicio.

## Preparación para desarrollar una aplicación en Visual Studio Code

Desarrollará la aplicación de traducción de texto con Visual Studio Code. Los archivos de código de la aplicación se han proporcionado en un repositorio de GitHub.

> **Sugerencia**: Si ya ha clonado el  repositorio **mslearn-ai-language**, ábralo en el código de Visual Studio. De lo contrario, siga estos pasos para clonarlo en su entorno de desarrollo.

1. Inicie Visual Studio Code.
2. Abra la paleta (SHIFT+CTRL+P) y ejecute un  comando **Git: Clone** para clonar el  repositorio 'https://github.com/MicrosoftLearning/mslearn-ai-language' en una carpeta local (no importa qué carpeta).
3. Cuando se haya clonado el repositorio, abra la carpeta en Visual Studio Code.

> **Nota**: Si Visual Studio Code le muestra un mensaje emergente para pedirle que confíe en el código que está abriendo, haga clic en la opción **Sí, confío en los autores** en la ventana emergente.

4. Espere mientras se instalan archivos adicionales para admitir los proyectos de código de C# en el repositorio.

> **Nota**: Si se le solicita que agregue los activos necesarios para compilar y depurar, seleccione **Ahora no**.

## Configura tu aplicación

Se han proporcionado aplicaciones para C# y Python. Ambas aplicaciones cuentan con la misma funcionalidad. En primer lugar, completará algunas partes clave de la aplicación para permitirle usar el recurso de Azure AI Translator.

1. En Visual Studio Code, en el  panel **Explorer**, vaya a la  carpeta **Labfiles/06b-translator-sdk** y expanda la  carpeta **CSharp** o **Python** en función de su preferencia de idioma y de la  carpeta **translate-text** que contenga. Cada carpeta contiene los archivos de código específicos del idioma de una aplicación en la que va a integrar la funcionalidad de Azure AI Translator.
2. Haga clic con el botón derecho en la  carpeta **translate-text** que contiene sus archivos de código y abra un terminal integrado. A continuación, instale el paquete del SDK de Azure AI Translator ejecutando el comando adecuado para su preferencia de idioma:

**C#**:

```
dotnet add package Azure.AI.Translation.Text --version 1.0.0-beta.1
```

**Pitón**:

```
pip install azure-ai-translation-text==1.0.0b1
```

3. En el  panel **Explorer**, en la  carpeta **translate-text**, abra el archivo de configuración de su idioma preferido

- **C#**: appsettings.json
- **Pitón**: .env
4. Actualice los valores de configuración para incluir la **región** y una **clave** del recurso de Azure AI Translator que creó (disponible en la  página **Claves y punto de conexión** del recurso de Azure AI Translator en Azure Portal).

> **NOTA**: Asegúrese de agregar la *región* para su recurso, <u>not</u> el punto de conexión!

5. Guarde el archivo de configuración.

## Agregar código para traducir texto

Ahora está listo para usar Azure AI Translator para traducir texto.

1. Tenga en cuenta que la  carpeta **translate-text** contiene un archivo de código para la aplicación cliente:

- **C#**: Program.cs
- **Pitón**: translate.py

Abra el archivo de código y en la parte superior, debajo de las referencias de espacio de nombres existentes, busque el comentario **Importar espacios de nombres**. A continuación, en este comentario, agregue el siguiente código específico del idioma para importar los espacios de nombres que necesitará para usar el SDK de Text Analytics:

**C#**: Programs.cs

'''csharp
Importar espacios de nombres
uso de Azure;
usando Azure.IA.Traducción.Texto;
```

**Pitón**: translate.py

'''pitón
# importar espacios de nombres
Importación de azure.ai.translation.text  *
from azure.ai.translation.text.models import InputTextItem
```

1. En la  función **Main**, tenga en cuenta que el código existente lee los ajustes de configuración.
1. Busque el comentario **Crear cliente usando punto final y clave** y agregue el siguiente código:

**C#**: Programs.cs

'''csharp
Creación de un cliente mediante el punto de conexión y la clave
Credencial AzureKeyCredential  = new(translatorKey);
TextTranslationClient cliente = new(credential, translatorRegion);
```

**Pitón**: translate.py

'''pitón
# Crear cliente usando punto final y clave
credential = TranslatorCredential(translatorKey, translatorRegion)
cliente = TextTranslationClient(credencial)
```

1. Busque el comentario **Elegir idioma de destino** y agregue el siguiente código, que utiliza el servicio Traductor de texto para devolver una lista de idiomas admitidos para la traducción y solicita al usuario que seleccione un código de idioma para el idioma de destino.

**C#**: Programs.cs

'''csharp
Elegir el idioma de destino
Response<GetLanguagesResult> languagesResponse = await client.GetLanguagesAsync(scope:"translation").ConfigureAwait(falso);
GetLanguagesResult languages = languagesResponse.Valor;
Consola.WriteLine($"{idiomas.Traducción.Count} idiomas disponibles.\n(Véase https://learn.microsoft.com/azure/ai-services/translator/language-support#translation)");
Consola.WriteLine("Introduzca un código de idioma de destino para la traducción (por ejemplo, 'en'):");
string targetLanguage = "xx";
bool languageSupported = falso;
mientras que (!languageSupported)
{
targetLanguage = Consola.LeerLínea();
if (idiomas.Traducción.ContainsKey(targetLanguage))
{
languageSupported = true;
}
más
{
Consola.WriteLine($"{targetLanguage} no es un lenguaje compatible.");
}

}
```

**Pitón**: translate.py

'''pitón
# Elegir el idioma de destino
languagesResponse = client.get_languages(scope="traducción")
print("{} idiomas compatibles.".format(len(languagesResponse.translation)))
print("(Ver https://learn.microsoft.com/azure/ai-services/translator/language-support#translation)")
print("Introduzca un código de idioma de destino para la traducción (por ejemplo, 'en'):")
targetLanguage = "xx"
supportedLanguage = Falso
while supportedLanguage == Falso:
targetLanguage = entrada()
if targetLanguage en languagesResponse.translation.keys():
supportedLanguage = True
De lo contrario:
print("{} no es un lenguaje compatible.".format(targetLanguage))
```

1. Busque el comentario **Traducir texto** y agregue el siguiente código, que solicita repetidamente al usuario que traduzca el texto, usa el servicio Azure AI Translator para traducirlo al idioma de destino (detectando el idioma de origen automáticamente) y muestra los resultados hasta que el usuario escribe *quit*.

**C#**: Programs.cs

'''csharp
Traducir texto
string inputText = "";
while (inputText.ToLower() != "salir")
{
Consola.WriteLine("Introducir texto para traducir ('salir' para salir)");
inputText = Consola.LeerLínea();
if (inputText.ToLower() != "salir")
{
Response<IReadOnlyList<TranslatedTextItem>> translationResponse = await client.TranslateAsync(targetLanguage, inputText).ConfigureAwait(falso);
IReadOnlyList<TranslatedTextItem> traducciones = translationResponse.Valor;
traducción de TranslatedTextItem  = traducciones[0];
string sourceLanguage = traducción?.DetectedLanguage?.Idioma;
Consola.WriteLine($"'{inputText}' traducido de {sourceLanguage} a {translation?.Traducciones[0].Para} como '{traducción?.¿Traducciones?[0]?.Texto}'.");
}
} 
```

**Pitón**: translate.py

'''pitón
# Traducir texto
inputText = ""
while inputText.lower() != "salir":
inputText = input("Introducir texto para traducir ('salir' para salir):")
if inputText != "salir":
input_text_elements = [InputTextItem(text=inputText)]
translationResponse = client.translate(content=input_text_elements, to=[targetLanguage])
translation = translationResponse[0] if translationResponse else None
Si la traducción:
fuenteIdioma = translation.detected_language
Para translated_text en translation.translations:
print(f"'{inputText}' fue traducido de {sourceLanguage.language} a {translated_text.to} como '{translated_text.text}'.")
```

1. Guarde los cambios en su archivo de código.

## Pruebe su aplicación

Ahora la aplicación está lista para probar.

1. En el terminal integrado para la  carpeta **Traducir texto**, e ingrese el siguiente comando para ejecutar el programa:

- **C#**: 'ejecución de dotnet'
- **Pitón**: 'pitón translate.py'

> **Consejo**: Puede usar el  icono **Maximizar tamaño del panel** (**^**) en la barra de herramientas del terminal para ver más texto de la consola.

1. Cuando se le solicite, ingrese un idioma de destino válido de la lista que se muestra.
1. Introduzca la frase que se va a traducir (por ejemplo, 'Esto es una prueba' o 'C'est un test') y vea los resultados, que deberían detectar el idioma de origen y traducir el texto al idioma de destino.
1. Cuando hayas terminado, ingresa 'salir'. Puede volver a ejecutar la aplicación y elegir un idioma de destino diferente.

## Limpiar

Cuando ya no necesite el proyecto, puede eliminar el recurso de Azure AI Translator en [Azure Portal](https://portal.azure.com).

