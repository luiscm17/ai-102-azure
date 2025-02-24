# Analyze Text
__Azure Language__ supports analysis of text, including language detection, sentiment analysis, key phrase extraction, and entity recognition.

For example, suppose a travel agency wants to process hotel reviews that have been submitted to the company’s web site. By using the Azure AI Language, they can determine the language each review is written in, the sentiment (positive, neutral, or negative) of the reviews, key phrases that might indicate the main topics discussed in the review, and named entities, such as places, landmarks, or people mentioned in the reviews.

## Provision an Azure AI Language resource
If you don’t already have one in your subscription, you’ll need to provision an __Azure AI Language service__ resource in your Azure subscription.

1. Open the Azure portal at [https://portal.azure.com](https://portal.azure.com), and sign in using the Microsoft account associated with your Azure subscription.
2. Select __Create a resource__.
3. In the search field, search for __Language service__. Then, in the results, select __Create__ under __Language Service__.
4. Select Continue to create your resource.
5. Provision the resource using the following settings:
    * __Subscription__: Your Azure subscription.
    * __Resource group__: Choose or create a resource group.
    * __Region__:Choose any available region
    * __Name__: Enter a unique name.
    * __Pricing tier__: Select F0 (free), or S (standard) if F is not available.
    * __Responsible AI Notice__: Agree.
6. Select __Review + create__, then select __Create__ to provision the resource.
7. Wait for deployment to complete, and then go to the deployed resource.
8. View the __Keys and Endpoint__ page in the __Resource Management__ section. You will need the information on this page later in the exercise.

## Prepare to develop an app in Visual Studio Code
You’ll develop your text analytics app using Visual Studio Code. The code files for your app have been provided in a GitHub repo.

> [!TIP]
>
> If you have already cloned the __mslearn-ai-language__ repo, open it in Visual Studio code. Otherwise, follow these steps to clone it to your development environment.

1. Start Visual Studio Code.
2. Open the palette (SHIFT+CTRL+P) and run a __Git__: __Clone__ command to clone the [https://github.com/MicrosoftLearning/mslearn-ai-language](https://github.com/MicrosoftLearning/mslearn-ai-language) repository to a local folder (it doesn’t matter which folder).
3. When the repository has been cloned, open the folder in Visual Studio Code.

>[!NOTE]
>If Visual Studio Code shows you a pop-up message to prompt you to trust the code you are opening, click on __Yes, I trust the authors__ option in the pop-up.

4. Wait while additional files are installed to support the C# code projects in the repo.

>[!NOTE]
>If you are prompted to add required assets to build and debug, select __Not Now__.

## Configure your application
Applications for both C# and Python have been provided, as well as a sample text file you’ll use to test the summarization. Both apps feature the same functionality. First, you’ll complete some key parts of the application to enable it to use your Azure AI Language resource.

1. In Visual Studio Code, in the __Explorer__ pane, browse to the __Labfiles/01-analyze-text__ folder and expand the __CSharp__ or __Python__ folder depending on your language preference and the __text-analysis__ folder it contains. Each folder contains the language-specific files for an app into which you’re you’re going to integrate Azure AI Language text analytics functionality.
2. Right-click the text-analysis folder containing your code files and open an integrated terminal. Then install the Azure AI Language Text Analytics SDK package by running the appropriate command for your language preference. For the Python exercise, also install the `dotenv` package:

__C#:__

```csharp
dotnet add package Azure.AI.TextAnalytics --version 5.3.0
```

__Python:__

```
 pip install azure-ai-textanalytics==5.3.0
 pip install python-dotenv
```
3. In the __Explorer__ pane, in the __text-analysis__ folder, open the configuration file for your preferred language

   * __C#__: appsettings.json
   * __Python__: .env
4. Update the configuration values to include the __endpoint__ and a __key__ from the Azure Language resource you created (available on the __Keys and Endpoint__ page for your Azure AI Language resource in the Azure portal)
5. Save the configuration file.

6. Note that the text-analysis folder contains a code file for the client application:

    * __C#__: Program.cs
    * __Python__: text-analysis.py

    Open the code file and at the top, under the existing namespace references, find the comment __Import namespaces__. Then, under this comment, add the following language-specific code to import the namespaces you will need to use the Text Analytics SDK:

    __C#__: Programs.cs
    
    ```csharp
     // import namespaces
     using Azure;
     using Azure.AI.TextAnalytics;
    ```
    __Python__: text-analysis.py

    ```python
     # import namespaces
     from azure.core.credentials import AzureKeyCredential
     from azure.ai.textanalytics import TextAnalyticsClient
    ```
7. In the __Main__ function, note that code to load the Azure AI Language service endpoint and key from the configuration file has already been provided. Then find the comment __Create client using endpoint and key__, and add the following code to create a client for the Text Analysis API:

    __C#__: Programs.cs
    ```cs
     // Create client using endpoint and key
     AzureKeyCredential credentials = new AzureKeyCredential(aiSvcKey);
     Uri endpoint = new Uri(aiSvcEndpoint);
     TextAnalyticsClient aiClient = new TextAnalyticsClient(endpoint, credentials);
    ```
    __Python__: text-analysis.py

    ```python
     # Create client using endpoint and key
     credential = AzureKeyCredential(ai_key)
     ai_client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)
    ```
8. Save your changes and return to the integrated terminal for the __text-analysis__ folder, and enter the following command to run the program:

    * __C#__: dotnet run
    * __Python__: python text-analysis.py

>[!TIP]
>You can use the __Maximize panel size (^)__ icon in the terminal toolbar to see more of the console text.

9. Observe the output as the code should run without error, displaying the contents of each review text file in the __reviews__ folder. The application successfully creates a client for the Text Analytics API but doesn’t make use of it. We’ll fix that in the next procedure.

## Add code to detect language

Now that you have created a client for the API, let’s use it to detect the language in which each review is written.

1. In the __Main__ function for your program, find the comment __Get language__. Then, under this comment, add the code necessary to detect the language in each review document:

    __C#__: Programs.cs
    ```csharp
     // Get language
     DetectedLanguage detectedLanguage = aiClient.DetectLanguage(text);
     Console.WriteLine($"\nLanguage: {detectedLanguage.Name}");
    ```
    __Python__: text-analysis.py

    ```python
     # Get language
     detectedLanguage = ai_client.detect_language(documents=[text])[0]
     print('\nLanguage: {}'.format(detectedLanguage.primary_language.name))
    ```

    > [!NOTE]
    > In this example, each review is analyzed individually, resulting in a separate call to the service for each file. An alternative approach is to create a collection of documents and pass them to the service in a single call. In both approaches, the response from the service consists of a collection of documents; which is why in the Python code above, the index of the first (and only) document in the response ([0]) is specified.

2. Save your changes. Then return to the integrated terminal for the __text-analysis__ folder, and re-run the program.

3. Observe the output, noting that this time the language for each review is identified.

## Add code to evaluate sentiment
___Sentiment analysis___ is a commonly used technique to classify text as _positive_ or _negative_ (or possible _neutral_ or _mixed_). It’s commonly used to analyze social media posts, product reviews, and other items where the sentiment of the text may provide useful insights.

1. In the __Main__ function for your program, find the comment __Get sentiment__. Then, under this comment, add the code necessary to detect the sentiment of each review document:

    __C#__: Program.cs

    ```csharp
     // Get sentiment
     DocumentSentiment sentimentAnalysis = aiClient.AnalyzeSentiment(text);
     Console.WriteLine($"\nSentiment: {sentimentAnalysis.Sentiment}");
    ```

    __Python__: text-analysis.py

    ```python
     # Get sentiment
     sentimentAnalysis = ai_client.analyze_sentiment(documents=[text])[0]
     print("\nSentiment: {}".format(sentimentAnalysis.sentiment))
    ```

2. Save your changes. Then return to the integrated terminal for the __text-analysis__ folder, and re-run the program.
3. Observe the output, noting that the sentiment of the reviews is detected.

## Add code to identify key phrases

It can be useful to identify key phrases in a body of text to help determine the main topics that it discusses.

1. In the __Main__ function for your program, find the comment __Get key phrases__. Then, under this comment, add the code necessary to detect the key phrases in each review document:

    __C#__: Program.cs

    ```csharp
     // Get key phrases
     KeyPhraseCollection phrases = aiClient.ExtractKeyPhrases(text);
     if (phrases.Count > 0)
     {
         Console.WriteLine("\nKey Phrases:");
         foreach(string phrase in phrases)
         {
             Console.WriteLine($"\t{phrase}");
         }
     }
    ```

    __Python__: text-analysis.py

    ```python
     # Get key phrases
     phrases = ai_client.extract_key_phrases(documents=[text])[0].key_phrases
     if len(phrases) > 0:
         print("\nKey Phrases:")
         for phrase in phrases:
             print('\t{}'.format(phrase))
    ```
2. Save your changes. Then return to the integrated terminal for the __text-analysis__ folder, and re-run the program.
3. Observe the output, noting that each document contains key phrases that give some insights into what the review is about.

## Add code to extract entities

Often, documents or other bodies of text mention people, places, time periods, or other entities. The text Analytics API can detect multiple categories (and subcategories) of entity in your text.

1. In the __Main__ function for your program, find the comment __Get entities__. Then, under this comment, add the code necessary to identify entities that are mentioned in each review:

    __C#__: Program.cs

    ```csharp
     // Get entities
     CategorizedEntityCollection entities = aiClient.RecognizeEntities(text);
     if (entities.Count > 0)
     {
         Console.WriteLine("\nEntities:");
         foreach(CategorizedEntity entity in entities)
         {
             Console.WriteLine($"\t{entity.Text} ({entity.Category})");
         }
     }
    ```
    __Python__: text-analysis.py

    ```python
     # Get entities
     entities = ai_client.recognize_entities(documents=[text])[0].entities
     if len(entities) > 0:
         print("\nEntities")
         for entity in entities:
             print('\t{} ({})'.format(entity.text, entity.category))
    ```

2. Save your changes. Then return to the integrated terminal for the __text-analysis__ folder, and re-run the program.
3. Observe the output, noting the entities that have been detected in the text.

## Add code to extract linked entities

In addition to categorized entities, the Text Analytics API can detect entities for which there are known links to data sources, such as Wikipedia.

1. In the __Main__ function for your program, find the comment __Get linked entities__. Then, under this comment, add the code necessary to identify linked entities that are mentioned in each review:

    __C#__: Program.cs
    
    ```csharp
     // Get linked entities
     LinkedEntityCollection linkedEntities = aiClient.RecognizeLinkedEntities(text);
     if (linkedEntities.Count > 0)
     {
         Console.WriteLine("\nLinks:");
         foreach(LinkedEntity linkedEntity in linkedEntities)
         {
             Console.WriteLine($"\t{linkedEntity.Name} ({linkedEntity.Url})");
         }
     }
    ```
    __Python__: text-analysis.py
    
    ```python
     # Get linked entities
     entities = ai_client.recognize_linked_entities(documents=[text])[0].entities
     if len(entities) > 0:
         print("\nLinks")
         for linked_entity in entities:
             print('\t{} ({})'.format(linked_entity.name, linked_entity.url))
    ```
2. Save your changes. Then return to the integrated terminal for the __text-analysis__ folder, and re-run the program.
3. Observe the output, noting the linked entities that are identified.

## Clean up resources
If you’re finished exploring the Azure AI Language service, you can delete the resources you created in this exercise. Here’s how:

1. Open the Azure portal at [https://portal.azure.com](https://portal.azure.com), and sign in using the Microsoft account associated with your Azure subscription.

2. Browse to the Azure AI Language resource you created in this lab.

3. On the resource page, select __Delete__ and follow the instructions to delete the resource.

### More information
For more information about using __Azure AI Language__, see the [documentation](https://learn.microsoft.com/azure/ai-services/language-service/).