from . import tools
import random
import os.path


class Actor:
    def __init__(self, name, base_dir, speaking, graphics, mood, mouth_style, pos, scale):
        if not "body" in graphics:
            raise Exception(f"Actor '{name}' has no body graphics")
        if not "mouth" in graphics:
            raise Exception(f"Actor '{name}' has no mouth graphics")

        if not mood in graphics["body"]:
            raise Exception(f"Actor '{name}' does not have a mood '{mood}'")

        body_graphics = graphics["body"][mood]
        self.body_graphics = []
        for i in body_graphics:
            img = tools.load_image(
                os.path.join(base_dir, i["artwork"]),
                None,
                None,
                scale=scale
            )
            self.body_graphics.append({
                "img": img,
                "mouthX": i["mouthX"],
                "mouthY": i["mouthY"]
            })

        if not mouth_style in graphics["mouth"]:
            raise Exception(
                f"Actor '{name}' does not have a mouth style '{mouth_style}'")

        mouth_graphics = graphics["mouth"][mouth_style]
        self.mouth_graphics = {}
        for mouth_type in mouth_graphics:
            obj = {}
            for tween in mouth_graphics[mouth_type]:
                obj[tween] = tools.load_image(
                    os.path.join(base_dir, mouth_graphics[mouth_type][tween]),
                    None,
                    None,
                    scale=scale
                )
            self.mouth_graphics[mouth_type] = obj

        self.speaking = speaking
        self.pos = pos
        self.index = -1
        self.update_index()
    
    def update_index(self):
        choices = list(range(len(self.body_graphics)))
        choices = choices[:self.index] + choices[self.index+1:]
        if len(choices) == 0:
            return
        self.index = random.choice(choices)

    def get_graphic(self, phone, last_phone):

        body = self.body_graphics[self.index]
        body_img = body["img"]

        last_mouth_type = tools.phone_to_mouth_type(last_phone)
        mouth_type = tools.phone_to_mouth_type(phone)

        mouth_img = self.mouth_graphics[last_mouth_type][mouth_type]

        body_pos = [
            round(self.pos[0] - 0.5*body_img.shape[1]),
            round(self.pos[1] - 0.5*body_img.shape[0])
        ]

        mouth_pos = [
            round(self.pos[0] + body["mouthX"]*body_img.shape[1] -
                  0.5*mouth_img.shape[1] - 0.5*body_img.shape[1]),
            round(self.pos[1] + body["mouthY"]*body_img.shape[0] -
                  0.5*mouth_img.shape[0] - 0.5*body_img.shape[0])
        ]

        return body_img, mouth_img, body_pos, mouth_pos
