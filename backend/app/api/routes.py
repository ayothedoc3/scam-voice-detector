"""API routes and endpoints"""
from fastapi import APIRouter, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
import os
import tempfile
import uuid
from typing import List
from ..models import DetectionResult, BatchAnalysisResult
from ..services.analyzer import VoiceAnalyzer
from ..config import get_settings
from ..utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)
settings = get_settings()
analyzer = VoiceAnalyzer()

@router.post("/analyze", response_model=DetectionResult)
async def analyze_single_audio(
    file: UploadFile = File(..., description="Audio file to analyze")
):
    """Analyze a single audio file for deepfake detection"""

    # Validate file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in settings.allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format: {file_ext}. Allowed: {list(settings.allowed_extensions)}"
        )

    # Create temp file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=file_ext)

    try:
        # Save uploaded file
        content = await file.read()

        # Check file size
        if len(content) > settings.max_file_size:
            raise HTTPException(status_code=413, detail="File too large")

        temp_file.write(content)
        temp_file.close()

        # Analyze
        result = analyzer.analyze_audio(temp_file.name)

        logger.info(f"Analysis complete: {file.filename} - Risk: {result.risk_level}")
        return result

    except Exception as e:
        logger.error(f"Analysis failed for {file.filename}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

    finally:
        # Cleanup
        if os.path.exists(temp_file.name):
            os.remove(temp_file.name)

@router.post("/analyze/batch", response_model=BatchAnalysisResult)
async def analyze_batch(
    files: List[UploadFile] = File(..., description="Multiple audio files")
):
    """Analyze multiple audio files in batch"""

    if len(files) > 10:
        raise HTTPException(status_code=400, detail="Max 10 files per batch")

    batch_id = str(uuid.uuid4())
    results = []
    failed = 0

    import time
    start_time = time.time()

    for file in files:
        try:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1])
            content = await file.read()
            temp_file.write(content)
            temp_file.close()

            result = analyzer.analyze_audio(temp_file.name)
            results.append(result)

        except Exception as e:
            logger.error(f"Batch analysis failed for {file.filename}: {str(e)}")
            failed += 1
        finally:
            if os.path.exists(temp_file.name):
                os.remove(temp_file.name)

    total_time = (time.time() - start_time) * 1000

    return BatchAnalysisResult(
        total_files=len(files),
        processed=len(results),
        failed=failed,
        results=results,
        batch_id=batch_id,
        processing_time_total_ms=total_time
    )

@router.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version
    }
