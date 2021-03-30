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

        .scene {{
            white-space: nowrap
        }}
        
        img {{
            max-width: 500px;
            max-height: 300px;
            border: 1px solid black;
            margin: 0 50px;
        }}

        .text {{
            vertical-align: text-top;
        }}
    </style>
</head>
<body>
    <table>
    {content}
    </table>
</body>
</html>
"""

scene_template = """
<tr>
    <td class='text scene'>
        <span>Scene {number}</span>
    </td>
    <td>
        {bg_image}
    </td>
    <td class='text'>
        {content}
    </td>
</tr>

"""
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
        scene_content = ""
        scene_bg_image = ""
        if scene.background_image is not None:

            encoded_string = f"data:image/png;base64,{base64.b64encode(cv2.imencode('.png', scene.background_image)[1]).decode('utf-8').replace(' ','')}"

            scene_bg_image = background_image_template.format(image=encoded_string)
        
        for p in scene.paragraphs:
            text = h.escape(p.text)
            
            scene_content += text.replace("~", "") + "<br /><br />"
        
        content += scene_template.format(number=i, bg_image=scene_bg_image, content=scene_content)
    
    html = template.format(title=movie.name, content=content)
    with open(filename, "w") as file:
        file.write(html)
    
