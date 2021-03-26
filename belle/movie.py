import os.path
import os
import json
import subprocess
import re
import wave
import contextlib
import shutil
from . import tools


class Movie:
    def __init__(self, name, resolution, framerate, audio, scenes, phoneme_hacks):
        self.name = name
        self.resolution = resolution
        self.framerate = framerate
        self.audio = audio
        self.scenes = scenes
        self.scene_end_times = [0] * len(scenes)
        self.phoneme_hacks = phoneme_hacks
        with contextlib.closing(wave.open(self.audio,'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            self.duration = frames / float(rate)


    def init(self, output_dir, force_overwrite_mouth_data=False, force_overwrite_transcript=False, force_overwrite_audio=False, force_delete_frames=False):
        self.create_transcript(output_dir, hack=False, force_overwrite=force_overwrite_transcript)
        mouth_data = self.get_mouth_data(
            output_dir,
            force_overwrite_mouth_data=force_overwrite_mouth_data,
            force_overwrite_transcript=force_overwrite_transcript
        )
        self.carve_mouth_data(mouth_data)
        self.copy_audio(output_dir, force_overwrite=force_overwrite_audio)
        self.delete_frames(output_dir, force_delete=force_delete_frames)

    def copy_audio(self, output_dir, force_overwrite=False):
        directory = os.path.join(output_dir, self.name)
        basename = os.path.basename(self.audio)
        filename = os.path.join(directory, basename)
        if os.path.exists(filename):
            if not force_overwrite and not (tools.confirm(f"'{basename}' already exists in the output directory. Would you like to overwrite it?") == "y"):
                return
        
        if not os.path.exists(directory):
            os.makedirs(directory)

        shutil.copyfile(self.audio, filename)


    def delete_frames(self, output_dir, force_delete=False):
        directory = os.path.join(output_dir, self.name, "frames")
        if os.path.exists(directory):
            contents = os.listdir(directory)
            if len(contents) > 0 and not force_delete and not (tools.confirm(f"The output frames directory is not empty. Would you like to empty it?") == "y"):
                return
            for filename in contents:
                filepath = os.path.join(directory, filename)
                if os.path.isfile(filepath) or os.path.islink(filepath):
                    os.unlink(filepath)
                elif os.path.isdir(filepath):
                    shutil.rmtree(filepath)
        else:
            os.makedirs(directory)

    def create_transcript(self, output_dir, hack=False, force_overwrite=False):
        directory = os.path.join(output_dir, self.name)
        filename = os.path.join(directory, "hacked-transcript.txt" if hack else "transcript.txt")
        if os.path.exists(filename):
            if not force_overwrite and not (tools.confirm(f"Would you like to overwrite the {'hacked ' if hack else ''}transcript file?") == "y"):
                with open(filename, "r") as file:
                    all_text = file.read()
                return all_text

        text = []
        for scene in self.scenes:
            t = []
            for paragraph in scene.paragraphs:
                t.append(paragraph.text)
            text.append("\n".join(t))

        all_text = "\n\n".join(text)

        if not os.path.exists(directory):
            os.makedirs(directory)
        
        if hack:
            for h in self.phoneme_hacks:
                all_text = all_text.replace(h, self.phoneme_hacks[h])

        with open(filename, "w") as file:
            file.write(all_text)

        return all_text

    def get_mouth_data(self, output_dir, force_overwrite_mouth_data=False, force_overwrite_transcript=False):

        mouth_data_file = os.path.join(
            output_dir, self.name, "mouth_data.json")

        if os.path.exists(mouth_data_file):
            if not force_overwrite_mouth_data and (tools.confirm("Would you like to overwrite the mouth data file?") == "n"):
                with open(mouth_data_file, "r") as file:
                    mouth_data = json.loads(file.read())
                return mouth_data

        transcript_file = os.path.join(output_dir, self.name, "hacked-transcript.txt")

        self.create_transcript(output_dir, hack=True, force_overwrite=force_overwrite_transcript)

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
                for h in self.phoneme_hacks:
                    words = words.replace(h, self.phoneme_hacks[h])
                words = re.sub(r"[^A-Za-z0-9]", " ", words)
                words = list(i for i in words.split(" ") if len(i))
                for word in words:
                    word_data = words_data[word_index]
                    assert word_data["word"] == word
                    if word_data["alignedWord"] == "<unk>":
                        print(f"Warning: Phonemes for word '{word}' unknown in scene {i+1} paragraph {j+1}")
                    if "phones" not in word_data:
                        print(f"Warning: Word '{word}' not found in audio in scene {i+1} paragraph {j+1}")
                    my_words.append(word_data)
                    if word_data["end"] > end_time:
                        end_time = word_data["end"]
                    if word_data["end"] > paragraph_end_time:
                        paragraph_end_time = word_data["end"]
                    word_index += 1
                paragraph.words_data = my_words
                scene.paragraph_end_times[j] = paragraph_end_time
            self.scene_end_times[i] = end_time
        
        self.scene_end_times[-1] = self.duration

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