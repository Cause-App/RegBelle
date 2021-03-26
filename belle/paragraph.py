import numpy as np
from . import tools

class Paragraph:
    def __init__(self, actors, text):
        self.actors = actors
        self.text = text
        self.words_data = None
    
    def which_phone(self, time):
        for word in self.words_data:
            if word["start"] <= time < word["end"]:
                offset = time - word["start"]
                total_offset = 0
                for phone in word["phones"]:
                    total_offset += phone["duration"]
                    if total_offset > offset:
                        return phone["phone"]
        return None

    
    def render_frame(self, image, time):

        # TODO
        # Handle updating the actor's index

        phone = self.which_phone(time)

        for actor in self.actors:
            body_img, mouth_img, body_pos, mouth_pos = actor.get_graphic(phone if actor.speaking else None)
            tools.overlay_image(image, body_img, *body_pos)
            tools.overlay_image(image, mouth_img, *mouth_pos)

        return image
