from . import tools
import random
import os.path

class Actor:
    def __init__(self, base_dir, speaking, graphics, mood, mouth_style, pos, size):
        # TODO
        # Instead of lazy-loading graphics
        # Load them all now
        # Or indeed memoize tools.load_image
        
        self.base_dir = base_dir
        self.speaking = speaking
        self.graphics = graphics
        self.mood = mood
        self.mouth_style = mouth_style
        self.pos = pos
        self.size = size
        self.index = random.randint(0, len(graphics["body"][mood])-1)
    
    def get_graphic(self, phone):
        body = self.graphics["body"][self.mood][self.index]

        body_img, scale = tools.load_image(
            os.path.join(self.base_dir, body["artwork"]),
            *self.size
        )

        # TODO
        # Handle tweens

        mouth_type = tools.phone_to_mouth_type(phone)

        mouth_img, _ = tools.load_image(
            os.path.join(self.base_dir, self.graphics["mouth"][mouth_type][self.mouth_style]["default"]),
            None,
            None,
            scale=scale
        )

        body_pos = [
            round(self.pos[0] - 0.5*body_img.shape[1]),
            round(self.pos[1] - 0.5*body_img.shape[0])
        ]

        mouth_pos = [
            round(self.pos[0] + body["mouthX"]*body_img.shape[1] - 0.5*mouth_img.shape[1] - 0.5*body_img.shape[1]),
            round(self.pos[1] + body["mouthY"]*body_img.shape[0] - 0.5*mouth_img.shape[0] - 0.5*body_img.shape[0])
        ]

        return body_img, mouth_img, body_pos, mouth_pos