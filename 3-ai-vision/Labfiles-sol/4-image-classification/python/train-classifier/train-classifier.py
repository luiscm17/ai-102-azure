from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import time
import os

def main():
    from dotenv import load_dotenv
    global training_client
    global custom_vision_project

    # Clear the console
    os.system('cls' if os.name=='nt' else 'clear')

    try:
        # Get Configuration Settings
        load_dotenv()
        training_endpoint = os.getenv('TrainingEndpoint')
        training_key = os.getenv('TrainingKey')
        project_id = os.getenv('ProjectID')

        # Authenticate a client for the training API
        credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
        training_client = CustomVisionTrainingClient(training_endpoint, credentials)

        # Get the Custom Vision project
        custom_vision_project = training_client.get_project(project_id)

        # Get the directory where the script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        training_images_dir = os.path.join(script_dir, 'more-training-images')
        
        # Upload and tag images
        Upload_Images(training_images_dir)

        # Train the model
        Train_Model()
        
    except Exception as ex:
        print(ex)

def Upload_Images(folder):
    print("Uploading images...")
    tags = training_client.get_tags(custom_vision_project.id)
    for tag in tags:
        print(tag.name)
        tag_dir = os.path.join(folder, tag.name)
        if not os.path.exists(tag_dir):
            print(f"Warning: Directory not found: {tag_dir}")
            continue
            
        for image in os.listdir(tag_dir):
            image_path = os.path.join(tag_dir, image)
            try:
                with open(image_path, "rb") as image_file:
                    image_data = image_file.read()
                training_client.create_images_from_data(custom_vision_project.id, image_data, [tag.id])
            except Exception as e:
                print(f"Error processing {image_path}: {str(e)}")

def Train_Model():
    print("Training ...")
    iteration = training_client.train_project(custom_vision_project.id)
    while (iteration.status != "Completed"):
        iteration = training_client.get_iteration(custom_vision_project.id, iteration.id)
        print (iteration.status, '...')
        time.sleep(5)
    print ("Model trained!")


if __name__ == "__main__":
    main()


