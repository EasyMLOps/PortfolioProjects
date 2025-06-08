import schemas as _schemas
import os
from PIL import Image
from io import BytesIO
import uuid
import numpy as np
import base64
from enhancer.enhancer import Enhancer

TEMP_PATH = 'temp'
ENHANCE_METHOD = os.getenv('METHOD')
BACKGROUND_ENHANCEMENT = os.getenv('BACKGROUND_ENHANCEMENT')
if ENHANCE_METHOD is None:
    ENHANCE_METHOD = 'gfpgan'

if BACKGROUND_ENHANCEMENT is None:
    BACKGROUND_ENHANCEMENT = True
else:
    BACKGROUND_ENHANCEMENT = True if BACKGROUND_ENHANCEMENT == 'True' else False




async def enhance(enhanceBase: _schemas._EnhanceBase) -> str:
    enhancer = Enhancer(method=ENHANCE_METHOD, background_enhancement=BACKGROUND_ENHANCEMENT, upscale=2)
    
    # Decode base64 image and convert to numpy array
    init_image = np.array(Image.open(BytesIO(base64.b64decode(enhanceBase.encoded_base_img[0]))))
    print(f"Image shape: {init_image.shape}")
    
    # Check image dimensions
    if not enhancer.check_image_dimensions(init_image):
        raise ValueError("Image dimensions exceed 2048 pixels in either width or height.")
    
    processed_image = enhancer.enhance(init_image)
    
    
    # Face restoration
    # restored_result = enhancer.restorer.enhance(
    #     processed_image, has_aligned=False, only_center_face=False, paste_back=True
    # )
    
    if processed_image is None:
        raise ValueError("Image enhancement failed, no image returned.")
    else:
        print(f"Processed image shape: {processed_image.shape}")
    
    # Handle different return types from face restoration
    if isinstance(processed_image, tuple):
        processed_image = processed_image[0]
    else:
        processed_image = processed_image
    
    # If restored_image is still a list, get the first element
    if isinstance(processed_image, list):
        if len(processed_image) == 0:
            raise ValueError("Face restoration returned empty list.")
        processed_image = processed_image[0]

    # Debug: Print the type of processed_image
    print(f"Processed image type: {type(processed_image)}")

    # Ensure processed_image is a PIL Image
    if isinstance(processed_image, np.ndarray):
        processed_image = Image.fromarray(processed_image)
    elif not hasattr(processed_image, 'save'):
        raise ValueError(f"Unexpected processed image type: {type(processed_image)}")

    # Convert to base64
    buffered = BytesIO()
    processed_image.save(buffered, format="JPEG")
    encoded_img = base64.b64encode(buffered.getvalue()).decode('utf-8')
    print(f"Encoded image length: {len(encoded_img)}")
    
    # Clean up temporary files if needed
    if not os.path.exists(TEMP_PATH):
        os.makedirs(TEMP_PATH)
    
    temp_file_path = os.path.join(TEMP_PATH, f"{uuid.uuid4()}.jpg")

    # Save the processed image to a temporary file
    processed_image.save(temp_file_path, format="JPEG")
    print(f"Temporary file saved at: {temp_file_path}")
    
    print("Image enhancement completed successfully.")
    return encoded_img
        