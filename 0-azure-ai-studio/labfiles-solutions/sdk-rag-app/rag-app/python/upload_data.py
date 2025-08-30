from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import os
import glob

# Load environment variables
load_dotenv()

# Initialize credentials
credential = DefaultAzureCredential()
hub_name = os.getenv("AZURE_AI_HUB_NAME")

# Get storage account name
storage_account_name = f"{hub_name}storage"
blob_service_client = BlobServiceClient(
    account_url=f"https://{storage_account_name}.blob.core.windows.net",
    credential=credential
)

# Create container
container_name = "brochures"
container_client = blob_service_client.create_container(container_name, public_access="none")

# Upload brochures
brochure_files = glob.glob("brochures/*.pdf")
for file_path in brochure_files:
    blob_name = os.path.basename(file_path)
    blob_client = container_client.get_blob_client(blob_name)
    with open(file_path, "rb") as f:
        blob_client.upload_blob(f, overwrite=True)
    print(f"Uploaded: {blob_name}")