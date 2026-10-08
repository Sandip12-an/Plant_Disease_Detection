from fastapi import HTTPException, status

class ModelInferenceError(HTTPException):
    def __init__(self, detail: str = "Error executing model inference pipeline"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

class InvalidImageError(HTTPException):
    def __init__(self, detail: str = "Uploaded file is not a valid or readable image"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class DiseaseNotFoundError(HTTPException):
    def __init__(self, detail: str = "Requested disease record not found in knowledge base"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
