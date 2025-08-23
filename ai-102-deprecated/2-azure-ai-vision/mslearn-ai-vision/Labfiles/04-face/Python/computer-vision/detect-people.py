from dotenv import load_dotenv
import os
from PIL import Image, ImageDraw
import sys
from matplotlib import pyplot as plt
import numpy as np

# import namespaces (REALIZADA)
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential



def main():
    global cv_client

    try:
        # Get Configuration Settings
        load_dotenv()
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')

        # Get image
        image_file = 'images/people.jpg'
        if len(sys.argv) > 1:
            image_file = sys.argv[1]

        with open(image_file, "rb") as f:
            image_data = f.read()

        # Authenticate Azure AI Vision client (REALIZADA)
        cv_client = ImageAnalysisClient(
            endpoint= ai_endpoint,
            credential= AzureKeyCredential(ai_key)
        )
        
        
        # Analyze image
        AnalyzeImage(image_file, image_data, cv_client)

    except Exception as ex:
        print(ex)


import json
# ...existing code...

def AnalyzeImage(filename, image_data, cv_client):
    print('\nAnalyzing ', filename)

    # Get result with specified features to be retrieved (PEOPLE) (REALIZADA)
    result = cv_client.analyze(
        image_data = image_data,
        visual_features = [VisualFeatures.PEOPLE]
    )
    
    # Create a list to store people data
    people_data = []

    # Identify people in the image
    if result.people is not None:
        print("\nPeople in image:")

        # Prepare image for drawing
        image = Image.open(filename)
        fig = plt.figure(figsize=(image.width/100, image.height/100))
        plt.axis('off')
        draw = ImageDraw.Draw(image)
        color = 'cyan'

        # Draw bounding box around detected people
        for detected_people in result.people.list:
            if(detected_people.confidence > 0.5):
                # Draw object bounding box
                r = detected_people.bounding_box
                bounding_box = ((r.x, r.y), (r.x + r.width, r.y + r.height))
                draw.rectangle(bounding_box, outline=color, width=3)

                # Add person data to the list
                people_data.append({
                    'bounding_box': {
                        'x': r.x,
                        'y': r.y,
                        'width': r.width,
                        'height': r.height
                    },
                    'confidence': detected_people.confidence
                })

                # Return the confidence of the person detected
                print(" {} (confidence: {:.f}%)".format(detected_people.bounding_box, detected_people.confidence * 100))

        # Save annotated image
        plt.imshow(image)
        plt.tight_layout(pad=0)
        outputfile = 'people.jpg'
        fig.savefig(outputfile)
        print('  Results saved in', outputfile)

        # Save people data to a JSON file
        json_outputfile = 'people_data.json'
        with open(json_outputfile, 'w') as json_file:
            json.dump(people_data, json_file, indent=4)
        print('People data saved in', json_outputfile)

if __name__ == "__main__":
    main()