"""
FastAPI Certificate Distribution System
Main application with all API endpoints
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
from typing import Dict, Any
from pathlib import Path

from app.csv_handler import CSVHandler
from app.certificate_generator import CertificateGenerator


# Initialize FastAPI app
app = FastAPI(
    title="Certificate Distribution System",
    description="A system for generating and distributing certificates",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Vercel serverless deployments have an ephemeral filesystem.
IS_VERCEL = os.getenv("VERCEL") == "1"

# Admin key for protected endpoints (in production, use environment variables)
ADMIN_KEY = "ADMIN123"


# Project root (used to build stable absolute paths)
PROJECT_ROOT = Path(__file__).resolve().parents[1]


# Initialize handlers
csv_handler = CSVHandler(str(PROJECT_ROOT / "data" / "Workshop-I Attendance Form (Responses).csv"))
cert_generator = CertificateGenerator(
    template_path=str(PROJECT_ROOT / "templates" / "certificate_template.jpg"),
    # Avoid read-only filesystem issues on Vercel.
    output_dir=str(Path("/tmp") / "certificates") if IS_VERCEL else str(PROJECT_ROOT / "certificates"),
)


# Frontend (React) build support
FRONTEND_DIST_DIR = PROJECT_ROOT / "frontend" / "dist"
FRONTEND_INDEX_HTML = FRONTEND_DIST_DIR / "index.html"
FRONTEND_ASSETS_DIR = FRONTEND_DIST_DIR / "assets"

TEMPLATES_DIR = PROJECT_ROOT / "templates"

if FRONTEND_ASSETS_DIR.exists():
    app.mount("/assets", StaticFiles(directory=str(FRONTEND_ASSETS_DIR)), name="frontend-assets")

if TEMPLATES_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(TEMPLATES_DIR)), name="static")


@app.get("/", response_class=HTMLResponse)
async def home():
    """
    Serve the main HTML interface
    
    Returns:
        HTML page with certificate search form
    """
    # Prefer the built React SPA if present
    if FRONTEND_INDEX_HTML.exists():
        return FileResponse(str(FRONTEND_INDEX_HTML), media_type="text/html")

    # Fallback to legacy static HTML template
    html_path = TEMPLATES_DIR / "index.html"

    if not html_path.exists():
        raise HTTPException(status_code=500, detail="Template file not found")

    with open(html_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    return HTMLResponse(content=html_content)


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint for monitoring
    
    Returns:
        Status message
    """
    return {"status": "running"}


@app.get("/verify")
async def verify_certificate(name: str, student_id: str) -> Dict[str, Any]:
    """
    Verify a certificate and return student information
    
    Args:
        name: The student's name
        student_id: The student's ID
        
    Returns:
        Student information and validity status
        
    Raises:
        HTTPException: If student not found
    """
    student = csv_handler.find_student_by_name_and_id(name, student_id)
    
    if not student:
        raise HTTPException(
            status_code=404, 
            detail=f"Student not found with name: {name} and ID: {student_id}"
        )
    
    certificate_id = csv_handler.generate_certificate_id(student.get("Student_Id"))
    
    return {
        "name": student.get("Name"),
        "email": student.get("Email_id"),
        "student_id": student.get("Student_Id"),
        "course": student.get("Course"),
        "certificate_id": certificate_id,
        "valid": True
    }



@app.get("/certificate")
async def get_certificate(name: str, student_id: str):
    """
    Generate certificate if not exists and return as downloadable PDF
    
    Args:
        name: The student's name
        student_id: The student's ID
        
    Returns:
        PDF file as download
        
    Raises:
        HTTPException: If student not found in database
    """
    # Verify student exists
    student = csv_handler.find_student_by_name_and_id(name, student_id)
    
    if not student:
        raise HTTPException(
            status_code=404,
            detail=f"Student not found with name: {name} and ID: {student_id}"
        )
    
    # Generate certificate ID
    certificate_id = csv_handler.generate_certificate_id(student.get("Student_Id"))
    
    # Serverless (Vercel): generate in-memory PDF (no disk caching)
    if IS_VERCEL:
        try:
            pdf_bytes = cert_generator.generate_certificate_bytes(student_name=student.get("Name"))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating certificate: {str(e)}")

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=\"{certificate_id}.pdf\""},
        )

    # Local/dev: cache PDFs on disk
    if not cert_generator.certificate_exists(certificate_id):
        try:
            cert_generator.generate_certificate(
                student_name=student.get("Name"),
                certificate_id=certificate_id,
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating certificate: {str(e)}")

    cert_path = cert_generator.get_certificate_path(certificate_id)
    return FileResponse(path=cert_path, media_type="application/pdf", filename=f"{certificate_id}.pdf")


@app.get("/generate-all")
async def generate_all_certificates(admin_key: str = Query(..., description="Admin key for authorization")) -> Dict[str, Any]:
    """
    Admin endpoint to generate all certificates from CSV
    Protected by admin key
    
    Args:
        admin_key: Admin authorization key
        
    Returns:
        Summary of generated certificates
        
    Raises:
        HTTPException: If admin key is invalid or generation fails
    """
    # Verify admin key
    if admin_key != ADMIN_KEY:
        raise HTTPException(
            status_code=403,
            detail="Invalid admin key"
        )

    if IS_VERCEL:
        raise HTTPException(
            status_code=501,
            detail="Bulk generation is disabled on serverless deployments. Generate on-demand via /certificate instead.",
        )
    
    try:
        students = csv_handler.get_all_students()
        generated = []
        skipped = []
        
        for student in students:
            student_id = student.get("Student_Id")
            name = student.get("Name")
            
            # Generate certificate ID
            certificate_id = csv_handler.generate_certificate_id(student_id)
            
            # Skip if already exists
            if cert_generator.certificate_exists(certificate_id):
                skipped.append(certificate_id)
                continue
            
            # Generate certificate
            cert_generator.generate_certificate(
                student_name=name,
                certificate_id=certificate_id
            )
            generated.append(certificate_id)
        
        return {
            "success": True,
            "total_students": len(students),
            "generated": len(generated),
            "skipped": len(skipped),
            "generated_ids": generated,
            "skipped_ids": skipped
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating certificates: {str(e)}"
        )


@app.get("/{full_path:path}", include_in_schema=False)
async def spa_fallback(full_path: str):
    """Serve the React SPA for client-side routes when a frontend build is present."""
    if not FRONTEND_INDEX_HTML.exists():
        raise HTTPException(status_code=404)

    # Serve any real file from dist (e.g., favicon) if it exists.
    candidate = FRONTEND_DIST_DIR / full_path
    if candidate.exists() and candidate.is_file():
        return FileResponse(str(candidate))

    return FileResponse(str(FRONTEND_INDEX_HTML), media_type="text/html")


# Run with: uvicorn app.main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
