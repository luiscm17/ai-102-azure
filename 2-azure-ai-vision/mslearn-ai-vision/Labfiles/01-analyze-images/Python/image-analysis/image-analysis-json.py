# es una modificacion al codigo principal en la que los resultados se muestran en un archivo
# JSON en lugar de la consola

from dotenv import load_dotenv
import os
from PIL import Image, ImageDraw
import sys
from matplotlib import pyplot as plt
from azure.core.exceptions import HttpResponseError
import requests

# Import namespaces (REALIZADA)
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

import json # Modulo importado para el output en JSON


def main():
    global cv_client

    try:
        # Get Configuration Settings
        load_dotenv()
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')

        # Get image
        image_file = 'images/street.jpg'
        if len(sys.argv) > 1:
            image_file = sys.argv[1]

        with open(image_file, "rb") as f:
            image_data = f.read()

        # Authenticate Azure AI Vision client (REALIZADA)
        cv_client = ImageAnalysisClient(
            endpoint=ai_endpoint,
            credential=AzureKeyCredential(ai_key)
        )

        
        # Analyze image
        AnalyzeImage(image_file, image_data, cv_client)
        
    except Exception as ex:
        print(ex)


# ...existing code...

def AnalyzeImage(image_filename, image_data, cv_client):
    print('\nAnalyzing image...')

    try:
        # Get result with specified features to be retrieved (REALIZADA)
        result = cv_client.analyze(
            image_data=image_data,
            visual_features=[
                VisualFeatures.CAPTION,
                VisualFeatures.DENSE_CAPTIONS,
                VisualFeatures.TAGS,
                VisualFeatures.OBJECTS,
                VisualFeatures.PEOPLE
            ]
        )

    except HttpResponseError as e:
        print(f"Status code: {e.status_code}")
        print(f"Reason: {e.reason}")
        print(f"Message: {e.error.message}")
        return

    # Prepare the results dictionary
    analysis_results = {}

    # Get image captions
    if result.caption is not None:
        analysis_results["caption"] = {
            "text": result.caption.text,
            "confidence": result.caption.confidence
        }

    # Get image dense captions
    if result.dense_captions is not None:
        analysis_results["dense_captions"] = [
            {"text": caption.text, "confidence": caption.confidence}
            for caption in result.dense_captions.list
        ]

    # Get image tags
    if result.tags is not None:
        analysis_results["tags"] = [
            {"name": tag.name, "confidence": tag.confidence}
            for tag in result.tags.list
        ]

    # Get objects in the image
    if result.objects is not None:
        analysis_results["objects"] = [
            {
                "name": detected_object.tags[0].name,
                "confidence": detected_object.tags[0].confidence,
                "bounding_box": {
                    "x": detected_object.bounding_box.x,
                    "y": detected_object.bounding_box.y,
                    "width": detected_object.bounding_box.width,
                    "height": detected_object.bounding_box.height
                }
            }
            for detected_object in result.objects.list
        ]

    # Get people in the image
    if result.people is not None:
        analysis_results["people"] = [
            {
                "confidence": detected_people.confidence,
                "bounding_box": {
                    "x": detected_people.bounding_box.x,
                    "y": detected_people.bounding_box.y,
                    "width": detected_people.bounding_box.width,
                    "height": detected_people.bounding_box.height
                }
            }
            for detected_people in result.people.list
        ]

    # Create the lab-result directory if it doesn't exist
    os.makedirs("lab-result", exist_ok=True)

    # Save the results to a JSON file
    result_file = os.path.join("lab-result", f"{os.path.basename(image_filename)}_analysis.json")
    if os.path.exists(result_file):
        overwrite = input(f"The file {result_file} already exists. Do you want to overwrite it? (y/n): ")
        if overwrite.lower() != 'y':
            print("File not overwritten.")
            return

    with open(result_file, "w") as f:
        json.dump(analysis_results, f, indent=4)

    print(f"Analysis results saved to {result_file}")

# ...existing code...

if __name__ == "__main__":
    main()
