class Scene:
    def __init__(self, background_color, background_image, background_image_pos, background_image_size, paragraphs):
        self.background_color = background_color
        self.background_image = background_image
        self.background_pos = background_image_pos
        self.background_image_size = background_image_size
        self.paragraphs = paragraphs
        self.paragraph_end_times = [0]*len(paragraphs)
    
    def which_paragraph(self, time):
        if time < 0:
            return None
        for i, end_time in enumerate(self.paragraph_end_times):
            if end_time > time:
                return self.paragraphs[i]
        return None
