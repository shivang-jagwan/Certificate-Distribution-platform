"""
Certificate Generator Module
Handles dynamic certificate generation using Pillow
"""

import os
from PIL import Image, ImageDraw, ImageFont
from typing import Tuple
from io import BytesIO


class CertificateGenerator:
    """Generate personalized certificates from template"""
    
    def __init__(self, template_path: str = "templates/certificate_template.jpg", 
                 output_dir: str = "certificates"):
        """
        Initialize certificate generator
        
        Args:
            template_path: Path to the certificate template image
            output_dir: Directory to save generated certificates
        """
        self.template_path = template_path
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
    def _get_font(self, size: int) -> ImageFont.FreeTypeFont:
        """
        Load font with fallback to default
        
        Args:
            size: Font size
            
        Returns:
            Font object
        """
        try:
            # Try to load a nice font (works on most systems)
            return ImageFont.truetype("arial.ttf", size)
        except:
            try:
                # Fallback for Linux systems
                return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
            except:
                # Ultimate fallback to default font
                return ImageFont.load_default()
    
    def _get_text_bbox(self, draw: ImageDraw.ImageDraw, text: str, 
                       font: ImageFont.FreeTypeFont) -> Tuple[int, int, int, int]:
        """
        Get bounding box for text
        
        Args:
            draw: ImageDraw object
            text: Text to measure
            font: Font to use
            
        Returns:
            Tuple of (left, top, right, bottom)
        """
        return draw.textbbox((0, 0), text, font=font)
    
    def _center_text(self, image_width: int, text: str, 
                     font: ImageFont.FreeTypeFont, draw: ImageDraw.ImageDraw) -> int:
        """
        Calculate x position to center text
        
        Args:
            image_width: Width of the image
            text: Text to center
            font: Font being used
            draw: ImageDraw object
            
        Returns:
            X position for centered text
        """
        bbox = self._get_text_bbox(draw, text, font)
        text_width = bbox[2] - bbox[0]
        return (image_width - text_width) // 2
    
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
        if not os.path.exists(self.template_path):
            raise FileNotFoundError(f"Template not found: {self.template_path}")
        
        # Load template
        template = Image.open(self.template_path)
        draw = ImageDraw.Draw(template)
        
        # Get image dimensions
        img_width, img_height = template.size
        
        # Define font - larger size for name
        name_font = self._get_font(120)  # Increased from 80 to 120
        
        # Calculate position for centered name
        name_x = self._center_text(img_width, student_name, name_font, draw)
        name_y = img_height // 2 - 20  # Centered vertically
        
        # Draw only the student name on certificate (no certificate ID)
        draw.text((name_x, name_y), student_name, fill='#1a1a1a', font=name_font)
        
        # Save as PDF
        output_filename = f"{certificate_id}.pdf"
        output_path = os.path.join(self.output_dir, output_filename)
        
        # Convert RGB if necessary (PDF requires RGB)
        if template.mode != 'RGB':
            template = template.convert('RGB')
        
        # Save directly as PDF using Pillow
        template.save(output_path, "PDF", resolution=100.0)
        
        return output_path

    def generate_certificate_bytes(self, student_name: str) -> bytes:
        """Generate a certificate PDF as bytes (no filesystem writes).

        This is useful for serverless deployments (e.g. Vercel) where local
        disk is ephemeral and should not be used as a cache.
        """
        if not os.path.exists(self.template_path):
            raise FileNotFoundError(f"Template not found: {self.template_path}")

        template = Image.open(self.template_path)
        draw = ImageDraw.Draw(template)

        img_width, img_height = template.size
        name_font = self._get_font(120)

        name_x = self._center_text(img_width, student_name, name_font, draw)
        name_y = img_height // 2 - 20

        draw.text((name_x, name_y), student_name, fill='#1a1a1a', font=name_font)

        if template.mode != 'RGB':
            template = template.convert('RGB')

        buf = BytesIO()
        template.save(buf, "PDF", resolution=100.0)
        return buf.getvalue()
    
    def certificate_exists(self, certificate_id: str) -> bool:
        """
        Check if certificate already exists
        
        Args:
            certificate_id: Certificate ID to check
            
        Returns:
            True if certificate exists, False otherwise
        """
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
        return os.path.join(self.output_dir, f"{certificate_id}.pdf")
