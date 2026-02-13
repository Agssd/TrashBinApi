from fastapi import APIRouter, UploadFile, File
import shutil
import os
from inference_sdk import InferenceHTTPClient

router = APIRouter()

client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="CQfRLTF1cPUpJskPF6en"
)

@router.post("/classify")
async def classify_image(image: UploadFile = File(...)):
    temp_path = "temp.jpg"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    result = client.run_workflow(
        workspace_name="kolka",
        workflow_id="small-object-detection-sahi-4",
        images={"image": temp_path},
        use_cache=True
    )

    os.remove(temp_path)
    return result
