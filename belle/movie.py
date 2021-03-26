import os.path
import os
import json
import subprocess

class Movie:
    def __init__(self, name, resolution, audio, scenes):
        self.name = name
        self.resolution = resolution
        self.audio = audio
        self.scenes = scenes
    
    def create_transcript(self, output_dir):
        text = []
        for scene in self.scenes:
            t = []
            for paragraph in scene.paragraphs:
                t.append(paragraph.text)
            text.append("\n".join(t))

        directory = os.path.join(output_dir, self.name)

        if not os.path.exists(directory):
            os.makedirs(directory)

        
        with open(os.path.join(directory, "transcript.txt"), "w") as file:
            file.write("\n\n".join(text))
    
    def get_mouth_data(self, output_dir):
        # TODO
        # Save output of this function to a file
        # Add option to overwrite or not
        # Which can be forced from the command line

        transcript_file = os.path.join(output_dir, self.name, "transcript.txt")
        
        # TODO
        # Add option to overwrite or not
        # Which can be forced from the command line
        
        if os.path.exists(transcript_file):
            print("Warning. Overwriting transcript file")
        
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

        # TODO
        # Handle errors and the case in which gentle is not running

        mouth_data = json.loads(out)
        return mouth_data

