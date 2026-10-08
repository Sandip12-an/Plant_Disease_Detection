from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.models.scan import Scan
from backend.app.models.disease import Disease
from backend.app.schemas.prediction import PredictionResponse, TreatmentPlan, TopClassPrediction
from backend.app.services.image_preprocessor import ImagePreprocessor
from backend.app.services.inference_service import inference_engine
from backend.app.services.gradcam_service import GradCamService
from backend.app.services.storage_service import StorageService
from backend.app.api.deps import get_current_user
from backend.app.utils.logger import logger

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse, status_code=status.HTTP_200_OK)
async def predict_plant_disease(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """
    Classifies uploaded plant leaf photo, generates visual Grad-CAM heatmap,
    retrieves biological & chemical remedies, and persists scan to history.
    """
    # 1. Read and validate image
    contents = await file.read()
    image = ImagePreprocessor.validate_and_load(contents)

    # 2. Plant leaf sanity check
    is_leaf_like, warning_msg = ImagePreprocessor.check_leaf_likeness(image)

    # 3. Preprocess to normalized NCHW tensor
    input_tensor = ImagePreprocessor.preprocess_for_inference(image)

    # 4. Model Inference
    prediction = inference_engine.predict(input_tensor)

    # 5. Generate Grad-CAM Heatmap & Store Images
    original_filename = StorageService.save_image(image, prefix="orig")
    heatmap_filename = GradCamService.generate_heatmap(image)

    original_url = f"/uploads/{original_filename}"
    heatmap_url = f"/uploads/{heatmap_filename}"

    # 6. Fetch Treatment from Database Knowledge Base
    disease_record = db.query(Disease).filter(Disease.id == prediction["disease_class"]).first()

    if disease_record:
        treatment_plan = TreatmentPlan(
            crop=disease_record.crop,
            disease_name=disease_record.name,
            is_healthy=disease_record.is_healthy,
            description=disease_record.description,
            symptoms=disease_record.symptoms,
            organic_treatment=disease_record.organic_treatment,
            chemical_treatment=disease_record.chemical_treatment,
            prevention=disease_record.prevention
        )
    else:
        treatment_plan = TreatmentPlan(
            crop=prediction["crop"],
            disease_name=prediction["disease_name"],
            is_healthy=prediction["is_healthy"],
            description=f"Diagnosed as {prediction['disease_name']}.",
            symptoms="Check leaf spots, discoloration, and lesion borders.",
            organic_treatment="Apply neem oil spray and prune infected leaves.",
            chemical_treatment="Consult local agricultural extension for registered fungicides.",
            prevention="Avoid overhead watering; ensure adequate spacing."
        )

    # 7. Persist to Scan History
    scan = Scan(
        user_id=current_user.id if current_user else None,
        image_url=original_url,
        heatmap_url=heatmap_url,
        crop_name=prediction["crop"],
        disease_name=prediction["disease_name"],
        disease_class=prediction["disease_class"],
        confidence=prediction["confidence"],
        is_healthy=prediction["is_healthy"],
        treatment_summary=treatment_plan.organic_treatment[:250]
    )
    db.add(scan)
    db.commit()
    db.refresh(scan)

    return PredictionResponse(
        scan_id=scan.id,
        crop=prediction["crop"],
        disease=prediction["disease_name"],
        disease_class=prediction["disease_class"],
        confidence=prediction["confidence"],
        is_healthy=prediction["is_healthy"],
        severity=prediction["severity"],
        original_image_url=original_url,
        heatmap_url=heatmap_url,
        treatment=treatment_plan,
        top_predictions=[TopClassPrediction(**p) for p in prediction["top_predictions"]],
        warning=warning_msg if not is_leaf_like else None
    )
