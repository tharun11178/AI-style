from fastapi import HTTPException, UploadFile


async def read_valid_image(image: UploadFile) -> bytes:
    if image.content_type and not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Please upload an image file")

    contents = await image.read()
    if not contents:
        raise HTTPException(status_code=400, detail="The uploaded image is empty")
    return contents
