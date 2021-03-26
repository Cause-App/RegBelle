import numpy as np
import cv2
from . import tools

class Scene:
    def __init__(self, background_color, background_image, background_image_pos, background_image_size, paragraphs):
        r,g,b = background_color
        self.background_color = [b, g, r]
        self.background_image = tools.load_image(background_image, *background_image_size)
        self.background_pos = background_image_pos
        self.paragraphs = paragraphs
        self.paragraph_end_times = [0]*len(paragraphs)
    
    def which_paragraph(self, time):
        if time < 0:
            return None
        for i, end_time in enumerate(self.paragraph_end_times):
            if end_time > time:
                return self.paragraphs[i]
        
        return self.paragraphs[-1]
    
    def render_frame(self, time, width, height):
        paragraph = self.which_paragraph(time)
        if paragraph is None:
            return None
        
        image = np.zeros((height, width, 3), dtype=np.uint8)

        im_height, im_width, _ = self.background_image.shape
        pos = [
            round(self.background_pos[0]-im_width/2),
            round(self.background_pos[1]-im_height/2)
        ]

        cv2.rectangle(image, (0, 0), (width, height), self.background_color, -1)
        tools.overlay_image(image, self.background_image, *pos)

        image = paragraph.render_frame(image, time)

        return image