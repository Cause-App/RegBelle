import json
import os.path

from .movie import Movie
from .scene import Scene
from .paragraph import Paragraph
from .actor import Actor
from . import tools
from . import scriptparser

def parse_script(movies_dir, actors_dir, movie_name, start_scene=0, rich_script_only=False, force_overwrite_movie_json=False):
    movie_dir = os.path.join(movies_dir, movie_name)
    movie_json = os.path.join(movie_dir, "movie.json")
    if not os.path.exists(movie_json) or force_overwrite_movie_json or tools.confirm(f"'movie.json' already exists in the movie directory. Would you like to overwrite it?") == "y":
        print("Parsing script")
        script_file = os.path.join(movie_dir, "script.regbelle")
        with open(script_file, "r") as file:
            lines = [line.strip().replace("\t", "") for line in file.readlines()]
        movie_data = scriptparser.parse_script(lines)
        with open(movie_json, "w") as file:
            file.write(json.dumps(movie_data))
    
    return parse_movie(movies_dir, actors_dir, movie_name, start_scene, rich_script_only=rich_script_only)


def parse_movie(movies_dir, actors_dir, movie_name, start_scene=0, rich_script_only=False):
    print("Parsing movie...")
    movie_dir = os.path.join(movies_dir, movie_name)
    movie_json = os.path.join(movie_dir, "movie.json")
    with open(movie_json, "r") as file:
        movie_data = json.loads(file.read())
    
    width = movie_data["width"]
    height = movie_data["height"]
    framerate = movie_data["framerate"]
    audio = os.path.join(movie_dir, movie_data["audio"]) if not rich_script_only else None
    scenes = list(parse_scene(movie_dir, actors_dir, x, width, height, rich_script_only=rich_script_only) for x in movie_data["scenes"])
    phoneme_hacks = movie_data["phonemeHacks"]

    min_silence_length = movie_data["minSilenceLength"]
    silence_thresh = movie_data["silenceThresh"]

    movie = Movie(movie_name, [width, height], framerate, audio, scenes, phoneme_hacks, min_silence_length, silence_thresh, start_scene=start_scene)
    print("Done parsing movie")
    return movie

def parse_scene(movie_dir, actors_dir, scene, width, height, rich_script_only=False):
    background_data = scene["background"]
    background_color = background_data["color"] if "color" in background_data else [255, 255, 255]
    if "image" in background_data and background_data["image"] is not None:
        background_image = os.path.join(movie_dir, background_data["image"])
        if not os.path.exists(background_image):
            if rich_script_only:
                background_image = None
                background_width = None
                background_height = None
                background_x = None
                background_y = None
            else:
                raise Exception(f"Image {background_image} does not exist")
        else:
            background_width = round(background_data["width"]*width) if background_data["width"] is not None else None
            background_height = round(background_data["height"]*height) if background_data["height"] is not None else None
            background_x = background_data["x"]*width
            background_y = background_data["y"]*height
    else:
        background_image = None
        background_width = None
        background_height = None
        background_x = None
        background_y = None


    paragraphs = list(parse_paragraph(actors_dir, x, width, height) for x in scene["paragraphs"])
    
    return Scene(background_color, background_image, [background_x, background_y], [background_width, background_height], paragraphs)

def parse_paragraph(actors_dir, paragraph, width, height):
    actors = list(parse_actor(actors_dir, x, width, height) for x in paragraph["actors"])
    text = paragraph["text"]
    if type(text) == list:
        text = " ".join(text)

    return Paragraph(actors, text)

def parse_actor(actors_dir, actor, width, height):
    label = actor["label"]
    name = actor["name"]
    speaking = actor["speaking"]
    mood = actor["mood"]
    mouth_style = actor["mouthStyle"]
    if "scale" in actor:
        scale_x = actor["scale"]
        scale_y = actor["scale"]
    else:
        scale_x = actor["scaleX"]
        scale_y = actor["scaleY"]

    scale_x *= height/1000
    scale_y *= height/1000

    x = actor["x"]*width
    y = actor["y"]*height

    base_dir = os.path.join(actors_dir, name)
    actor_json = os.path.join(base_dir, "actor.json")
    if not os.path.exists(actor_json):
        raise Exception(f"Actor '{name}' cannot be found")
    with open(actor_json, "r") as file:
        actor_data = json.loads(file.read())
    
    graphics = actor_data["graphics"]

    return Actor(label, name, base_dir, speaking, graphics, mood, mouth_style, [x, y], [scale_x, scale_y])