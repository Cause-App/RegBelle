import os.path
import os
import json
import subprocess
import re
from . import tools


class Movie:
    def __init__(self, name, resolution, framerate, audio, scenes):
        self.name = name
        self.resolution = resolution
        self.framerate = framerate
        self.audio = audio
        self.scenes = scenes
        self.scene_end_times = [0] * len(scenes)

    def init(self, output_dir, force_overwrite_mouth_data=False, force_overwrite_transcript=False):
        mouth_data = self.get_mouth_data(
            output_dir,
            force_overwrite_mouth_data=force_overwrite_mouth_data,
            force_overwrite_transcript=force_overwrite_transcript
        )
        self.carve_mouth_data(mouth_data)

    def create_transcript(self, output_dir):
        text = []
        for scene in self.scenes:
            t = []
            for paragraph in scene.paragraphs:
                t.append(paragraph.text)
            text.append("\n".join(t))

        all_text = "\n\n".join(text)

        if output_dir is None:
            return all_text

        directory = os.path.join(output_dir, self.name)

        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(os.path.join(directory, "transcript.txt"), "w") as file:
            file.write(all_text)

        return all_text

    def get_mouth_data(self, output_dir, force_overwrite_mouth_data=False, force_overwrite_transcript=False):

        mouth_data_file = os.path.join(
            output_dir, self.name, "mouth_data.json")

        if os.path.exists(mouth_data_file):
            if not force_overwrite_transcript and (tools.confirm("Would you like to overwrite the mouth data file?") == "n"):
                with open(mouth_data_file, "r") as file:
                    mouth_data = json.loads(file.read())
                return mouth_data

        transcript_file = os.path.join(output_dir, self.name, "transcript.txt")

        if os.path.exists(transcript_file):
            if force_overwrite_transcript:
                self.create_transcript(output_dir)
            else:
                if (tools.confirm("Would you like to overwrite the transcript file?") == "y"):
                    self.create_transcript(output_dir)
        else:
            self.create_transcript(output_dir)

        process = subprocess.Popen(
            [
                'curl',
                '-F',
                f'audio=@{self.audio}',
                '-F',
                f'transcript=@{transcript_file}',
                'http://localhost:8765/transcriptions?async=false'
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        out, err = process.communicate()

        if (b"Failed to connect to" in err):
            raise Exception(
                "Failed to connect to GENTLE server. Perhaps it is not running.")

        mouth_data = json.loads(out)

        with open(mouth_data_file, "w") as file:
            file.write(json.dumps(mouth_data))

        return mouth_data

    def carve_mouth_data(self, mouth_data):

        word_index = 0
        words_data = mouth_data["words"]

        for i, scene in enumerate(self.scenes):
            end_time = 0
            for j, paragraph in enumerate(scene.paragraphs):
                paragraph_end_time = 0
                my_words = []
                words = paragraph.text
                words = re.sub(r"[^A-Za-z0-9]", " ", words)
                words = list(i for i in words.split(" ") if len(i))
                for word in words:
                    word_data = words_data[word_index]
                    assert word_data["word"] == word
                    my_words.append(word_data)
                    if word_data["end"] > end_time:
                        end_time = word_data["end"]
                    if word_data["end"] > paragraph_end_time:
                        paragraph_end_time = word_data["end"]
                    word_index += 1
                paragraph.words_data = my_words
                scene.paragraph_end_times[j] = paragraph_end_time
            self.scene_end_times[i] = end_time

    def which_scene(self, time):
        if time < 0:
            return None
        for i, end_time in enumerate(self.scene_end_times):
            if end_time > time:
                return self.scenes[i]
        return None

    def render_frame(self, time):
        scene = self.which_scene(time)
        if scene is None:
            return None
        
        return scene.render_frame(time, *self.resolution)