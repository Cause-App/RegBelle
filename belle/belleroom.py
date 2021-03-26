import os.path
import os
import cv2
import sys
import subprocess
from . import tools

class BelleRoom:
    def __init__(self, movie):
        self.movie = movie
        self.framerate = movie.framerate
        self.dt = 1.0/self.framerate
        self.frame_number = 0
        self.last_proportion = -1

    
    def render_frame(self, output_dir, show=False):
        directory = os.path.join(output_dir, self.movie.name, "frames")

        if not os.path.exists(directory):
            os.makedirs(directory)
        filename = os.path.join(directory, f"{str(self.frame_number).zfill(7)}.png")

        time = self.frame_number * self.dt
        
        image = self.movie.render_frame(time)
        if image is None:
            cv2.destroyAllWindows()
            return None

        cv2.imwrite(filename, image)

        if show:
            cv2.imshow(self.movie.name, image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                sys.exit()

        self.frame_number += 1

        proportion = int(100*(self.frame_number*self.dt)/self.movie.duration)
        if proportion != self.last_proportion:
            self.last_proportion = proportion
            print(f"{proportion}%")


        return image
    
    def stitch(self, output_dir, force_stitch=False):
        directory = os.path.join(output_dir, self.movie.name, "frames")
        output_file = os.path.join(output_dir, self.movie.name, "render.mp4")
        if (os.path.exists(output_file) and not force_stitch and (tools.confirm("Would you like to overwrite the stitched output video?") != "y")):
            return
        process = subprocess.Popen(
            [
                "ffmpeg",
                "-y",
                "-i",
                f"{directory}/%07d.png",
                "-c:v",
                "libx264",
                "-vf",
                f"fps={self.framerate}",
                "-pix_fmt",
                "yuv420p",
                output_file
            ]
        )
        process.communicate()
    
    def add_audio(self, output_dir, force_add_audio=False):
        input_file = os.path.join(output_dir, self.movie.name, "render.mp4")
        output_file = os.path.join(output_dir, self.movie.name, "render-with-audio.mp4")
        if (os.path.exists(output_file) and not force_add_audio and (tools.confirm("Would you like to overwrite the output video with audio overlay?") != "y")):
            return
        process = subprocess.Popen(
            [
                "ffmpeg",
                "-y",
                "-i",
                input_file,
                "-i",
                self.movie.audio,
                "-c:v",
                "copy",
                "-map",
                "0:v:0",
                "-map",
                "1:a:0",
                "-c:a",
                "aac",
                "-b:a",
                "192k",
                output_file
            ]
        )
        process.communicate()