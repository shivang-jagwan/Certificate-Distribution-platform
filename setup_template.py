"""
Setup Script - Generate Certificate Template
Run this once during initial setup to create the certificate template
"""

from PIL import Image, ImageDraw, ImageFont
import os


def create_certificate_template():
    """
    Create a professional certificate template
    Saves as templates/certificate_template.jpg
    """
    # Create templates directory if it doesn't exist
    os.makedirs("templates", exist_ok=True)
    
    # Image dimensions (1920x1080 - Full HD)
    width, height = 1920, 1080
    
    # Create image with elegant background
    img = Image.new('RGB', (width, height), color='#f5f5f0')
    draw = ImageDraw.Draw(img)
    
    # Draw outer border (gold color)
    border_color = '#d4af37'
    border_width = 20
    draw.rectangle(
        [(border_width, border_width), (width - border_width, height - border_width)],
        outline=border_color,
        width=border_width
    )
    
    # Draw inner border (darker gold)
    inner_border_color = '#b8941e'
    inner_offset = 50
    draw.rectangle(
        [(inner_offset, inner_offset), (width - inner_offset, height - inner_offset)],
        outline=inner_border_color,
        width=5
    )
    
    # Draw decorative corners
    corner_size = 100
    corner_color = '#d4af37'
    
    # Top-left corner
    draw.line([(inner_offset, inner_offset + corner_size), (inner_offset, inner_offset), 
               (inner_offset + corner_size, inner_offset)], fill=corner_color, width=8)
    
    # Top-right corner
    draw.line([(width - inner_offset - corner_size, inner_offset), 
               (width - inner_offset, inner_offset), 
               (width - inner_offset, inner_offset + corner_size)], fill=corner_color, width=8)
    
    # Bottom-left corner
    draw.line([(inner_offset, height - inner_offset - corner_size), 
               (inner_offset, height - inner_offset), 
               (inner_offset + corner_size, height - inner_offset)], fill=corner_color, width=8)
    
    # Bottom-right corner
    draw.line([(width - inner_offset - corner_size, height - inner_offset), 
               (width - inner_offset, height - inner_offset), 
               (width - inner_offset, height - inner_offset - corner_size)], fill=corner_color, width=8)
    
    # Try to load a nice font for the title
    try:
        title_font = ImageFont.truetype("arial.ttf", 100)
        subtitle_font = ImageFont.truetype("arial.ttf", 50)
    except:
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 100)
            subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 50)
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
    
    # Add header text
    header_text = "CERTIFICATE OF ACHIEVEMENT"
    header_bbox = draw.textbbox((0, 0), header_text, font=title_font)
    header_width = header_bbox[2] - header_bbox[0]
    header_x = (width - header_width) // 2
    header_y = 150
    
    draw.text((header_x, header_y), header_text, fill='#2c3e50', font=title_font)
    
    # Add subtitle
    subtitle_text = "This is to certify that"
    subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    subtitle_y = 320
    
    draw.text((subtitle_x, subtitle_y), subtitle_text, fill='#555555', font=subtitle_font)
    
    # Add decorative line for name (will be filled dynamically)
    line_y = height // 2 + 50
    draw.line([(400, line_y), (width - 400, line_y)], fill='#cccccc', width=2)
    
    # Add footer text
    footer_text = "has successfully completed the program"
    footer_bbox = draw.textbbox((0, 0), footer_text, font=subtitle_font)
    footer_width = footer_bbox[2] - footer_bbox[0]
    footer_x = (width - footer_width) // 2
    footer_y = height // 2 + 200
    
    draw.text((footer_x, footer_y), footer_text, fill='#555555', font=subtitle_font)
    
    # Save the template
    output_path = "templates/certificate_template.jpg"
    img.save(output_path, "JPEG", quality=95)
    
    print(f"✅ Certificate template created successfully!")
    print(f"📁 Saved to: {output_path}")
    print(f"📐 Dimensions: {width}x{height}")
    

if __name__ == "__main__":
    print("🎨 Generating certificate template...")
    create_certificate_template()
    print("\n✨ Setup complete! You can now run the FastAPI server.")
