from fastapi import APIRouter, UploadFile, File

router = APIRouter()

# PUBLIC_INTERFACE
@router.post("/upload", summary="Upload receipt image for OCR (placeholder)")
async def upload_receipt(file: UploadFile = File(...)):
    """
    Simulate OCR by accepting an image upload and returning a static result.
    """
    # In a real implementation, OCR would happen here
    return {
        "vendor": "Sample Store",
        "total": 50.00,
        "date": "2024-02-28",
        "success": True,
        "details": "OCR not implemented, this is a placeholder."
    }
