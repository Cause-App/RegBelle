import json
import os.path

from .movie import Movie
from .scene import Scene
from .paragraph import Paragraph
from .actor import Actor

def parse_movie(movies_dir, actors_dir, movie_name):
    movie_dir = os.path.join(movies_dir, movie_name)
    movie_json = os.path.join(movie_dir, "movie.json")
    with open(movie_json, "r") as file:
        movie_data = json.loads(file.read())
    
    width = movie_data["width"]
    height = movie_data["height"]
    framerate = movie_data["framerate"]
    audio = os.path.join(movie_dir, movie_data["audio"])
    scenes = list(parse_scene(movie_dir, actors_dir, x, width, height) for x in movie_data["scenes"])
    phoneme_hacks = movie_data["phonemeHacks"]

    return Movie(movie_name, [width, height], framerate, audio, scenes, phoneme_hacks)

def parse_scene(movie_dir, actors_dir, scene, width, height):
    background_data = scene["background"]
    background_color = background_data["color"]
    background_image = os.path.join(movie_dir, background_data["image"])
    background_width = round(background_data["width"]*width) if background_data["width"] is not None else None
    background_height = round(background_data["height"]*height) if background_data["height"] is not None else None
    background_x = background_data["x"]*width
    background_y = background_data["y"]*height


    paragraphs = list(parse_paragraph(actors_dir, x, width, height) for x in scene["paragraphs"])
    
    return Scene(background_color, background_image, [background_x, background_y], [background_width, background_height], paragraphs)

def parse_paragraph(actors_dir, paragraph, width, height):
    actors = list(parse_actor(actors_dir, x, width, height) for x in paragraph["actors"])
    text = paragraph["text"]

    return Paragraph(actors, text)

def parse_actor(actors_dir, actor, width, height):
    name = actor["name"]
    speaking = actor["speaking"]
    mood = actor["mood"]
    mouth_style = actor["mouthStyle"]
    if "scale" in actor:
        scale_x = actor["scale"]
        scale_y = actor["scale"]
    else:
        scale_x = actor["scale_x"]
        scale_y = actor["scale_y"]

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

    return Actor(name, base_dir, speaking, graphics, mood, mouth_style, [x, y], [scale_x, scale_y])