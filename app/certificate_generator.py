"""
Certificate Generator Module
Handles dynamic certificate generation using ReportLab (production-friendly)
"""

import os
from pathlib import Path
from typing import Optional

from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


class CertificateGenerator:
    """Generate personalized certificates from template"""
    
    def __init__(self, template_path: str = "templates/certificate_template.jpg", 
                 output_dir: Optional[str] = "certificates"):
        """
        Initialize certificate generator
        
        Args:
            template_path: Path to the certificate template image
            output_dir: Directory to save generated certificates
        """
        project_root = Path(__file__).resolve().parents[1]

        template_candidate = Path(template_path)
        if not template_candidate.is_absolute():
            template_candidate = project_root / template_candidate
        self.template_path = str(template_candidate)

        if output_dir is None:
            self.output_dir = None
        else:
            output_candidate = Path(output_dir)
            if not output_candidate.is_absolute():
                output_candidate = project_root / output_candidate
            self.output_dir = str(output_candidate)
            os.makedirs(self.output_dir, exist_ok=True)
        
    def generate_certificate(self, student_name: str, certificate_id: str) -> str:
        """
        Generate a certificate for a student
        
        Args:
            student_name: Name of the student
            certificate_id: Unique certificate ID (used for filename only)
            
        Returns:
            Path to the generated certificate PDF
            
        Raises:
            FileNotFoundError: If template image doesn't exist
        """
        if not self.output_dir:
            raise RuntimeError("Output directory is not configured")

        output_filename = f"{certificate_id}.pdf"
        output_path = os.path.join(self.output_dir, output_filename)

        page_width, page_height = landscape(A4)
        c = canvas.Canvas(output_path, pagesize=(page_width, page_height))

        # Optional template background (if the image exists)
        if os.path.exists(self.template_path):
            try:
                img = ImageReader(self.template_path)
                c.drawImage(img, 0, 0, width=page_width, height=page_height, preserveAspectRatio=True, mask='auto')
            except Exception:
                # If template fails to load, still generate a valid PDF.
                pass
        else:
            # Simple background when no image is present
            c.setFillColorRGB(0.04, 0.06, 0.15)
            c.rect(0, 0, page_width, page_height, fill=1, stroke=0)

        # Student name
        c.setFillColorRGB(1, 1, 1)
        c.setFont("Helvetica-Bold", 36)
        c.drawCentredString(page_width / 2, page_height / 2, student_name)

        # Certificate ID (small)
        c.setFont("Helvetica", 10)
        c.setFillColorRGB(1, 1, 1)
        c.drawRightString(page_width - 24, 18, certificate_id)

        c.showPage()
        c.save()
        
        return output_path
    
    def certificate_exists(self, certificate_id: str) -> bool:
        """
        Check if certificate already exists
        
        Args:
            certificate_id: Certificate ID to check
            
        Returns:
            True if certificate exists, False otherwise
        """
        if not self.output_dir:
            return False

        output_path = os.path.join(self.output_dir, f"{certificate_id}.pdf")
        return os.path.exists(output_path)
    
    def get_certificate_path(self, certificate_id: str) -> str:
        """
        Get the path to a certificate
        
        Args:
            certificate_id: Certificate ID
            
        Returns:
            Path to the certificate PDF
        """
        if not self.output_dir:
            raise RuntimeError("Output directory is not configured")

        return os.path.join(self.output_dir, f"{certificate_id}.pdf")
