import os
import os.path
import base64
import cv2
import html as h
from . import tools

template = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} script</title>
    <style>
        body {{
            font-family: Arial, Helvetica, sans-serif;
            font-size: 1.5em;
            padding: 50px;
        }}
        
        h1 {{
            text-decoration: underline;
            font-size: 1.5em;
        }}

        h1:not(:first-child) {{
            padding-top: 100px;
        }}

        img {{
            max-width: 300px;
            max-height: 300px;
            border: 1px solid black;
        }}
    </style>
</head>
<body>
    {content}
</body>
</html>
"""

scene_heading_template = "<h1>Scene {number}</h1>"
background_image_template = "<img src='{image}'>"

def generate_rich_script(movie, output_dir, force_overwrite=False):
    print(f"Creating rich script")
    directory = os.path.join(output_dir, movie.name)
    filename = os.path.join(
        directory, "rich-script.html")
    if not os.path.exists(directory):
        os.makedirs(directory)
    if os.path.exists(filename):
        if not force_overwrite and not (tools.confirm(f"Would you like to overwrite the rich script file?") == "y"):
            return
    
    content = ""
    for i, scene in enumerate(movie.scenes):
        content += scene_heading_template.format(number=i)
        if scene.background_image is not None:

            encoded_string = f"data:image/png;base64,{base64.b64encode(cv2.imencode('.png', scene.background_image)[1]).decode('utf-8').replace(' ','')}"

            content += background_image_template.format(image=encoded_string)
        
            content += "<br /><br/>"

        for p in scene.paragraphs:
            text = h.escape(p.text)
            
            content += text.replace("~", "") + "<br /><br />"
    
    html = template.format(title=movie.name, content=content)
    with open(filename, "w") as file:
        file.write(html)
    
