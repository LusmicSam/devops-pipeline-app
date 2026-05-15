import os
from PIL import Image, ImageDraw, ImageFont

def create_placeholder(filename, text, width=800, height=400, bg_color=(240, 248, 255), text_color=(0, 51, 102)):
    # Create a new image
    img = Image.new('RGB', (width, height), color=bg_color)
    d = ImageDraw.Draw(img)
    
    # Try to use a default font
    try:
        # On Windows
        font = ImageFont.truetype("arial.ttf", 36)
    except IOError:
        try:
            # Fallback
            font = ImageFont.load_default()
        except Exception:
            font = None
            
    # Calculate text bounding box
    if font:
        bbox = d.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    else:
        text_width = len(text) * 6
        text_height = 10
        
    position = ((width - text_width) / 2, (height - text_height) / 2)
    
    # Draw text
    if font:
        d.text(position, text, fill=text_color, font=font)
    else:
        d.text(position, text, fill=text_color)
        
    # Draw border
    d.rectangle([0, 0, width-1, height-1], outline=text_color, width=3)
    
    # Save the image
    img.save(filename)
    print(f"Generated {filename}")

if __name__ == "__main__":
    diagrams = {
        "lpu.png": ("LPU University Logo\n(Placeholder)", 300, 300),
        "pipeline_flow.png": ("CI/CD Pipeline Architecture Diagram\n(GitHub -> Jenkins -> Docker -> Deploy)", 1000, 500),
        "maven_lifecycle.png": ("Maven Build Lifecycle\n(Clean -> Compile -> Test -> Package)", 800, 400),
        "docker_arch.png": ("Docker Container Architecture\n(App + JRE in lightweight container)", 800, 400),
        "compose_services.png": ("Docker Compose Services Network\n(Spring Boot App <--> Jenkins)", 800, 400),
        "github_actions_flow.png": ("GitHub Actions CI Workflow\n(Build Job -> Test Job -> Publish Job)", 800, 400),
        "jenkins_stages.png": ("Jenkins Declarative Pipeline\n(Checkout -> Build -> Test -> Package -> Docker -> Deploy)", 1000, 400)
    }
    
    # Ensure we are in the correct directory
    # The script should be run from inside the 'report' directory
    for filename, (text, w, h) in diagrams.items():
        if not os.path.exists(filename):
            create_placeholder(filename, text, w, h)
        else:
            print(f"Skipping {filename}, already exists.")
