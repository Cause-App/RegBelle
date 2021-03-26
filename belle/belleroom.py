import os.path
import os
import cv2

class BelleRoom:
    def __init__(self, movie):
        self.movie = movie
        self.framerate = movie.framerate
        self.dt = 1.0/self.framerate
        self.frame_number = 0

    
    def render_frame(self, output_dir):
        directory = os.path.join(output_dir, self.movie.name, "frames")

        if not os.path.exists(directory):
            os.makedirs(directory)
        filename = os.path.join(directory, f"{str(self.frame_number).zfill(7)}.png")

        time = self.frame_number * self.dt
        
        image = self.movie.render_frame(time)
        if image is None:
            return None

        cv2.imwrite(filename, image)
        self.frame_number += 1
        return image