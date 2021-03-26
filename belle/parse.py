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
    audio = os.path.join(movie_dir, movie_data["audio"])
    scenes = list(parse_scene(movie_dir, actors_dir, x) for x in movie_data["scenes"])

    return Movie([width, height], audio, scenes)

def parse_scene(movie_dir, actors_dir, scene):
    background_data = scene["background"]
    background_color = background_data["color"]
    background_image = os.path.join(movie_dir, background_data["image"])
    background_x = background_data["x"]
    background_y = background_data["y"]
    background_width = background_data["width"]
    background_height = background_data["height"]

    paragraphs = list(parse_paragraph(actors_dir, x) for x in scene["paragraphs"])
    
    return Scene(background_color, background_image, [background_x, background_y], [background_width, background_height], paragraphs)

def parse_paragraph(actors_dir, paragraph):
    actors = list(parse_actor(actors_dir, x) for x in paragraph["actors"])
    text = paragraph["text"]

    return Paragraph(actors, text)

def parse_actor(actors_dir, actor):
    name = actor["name"]
    speaking = actor["speaking"]
    mood = actor["mood"]
    mouth_style = actor["mouthStyle"]
    x = actor["x"]
    y = actor["y"]
    width = actor["width"]
    height = actor["height"]

    actor_json = os.path.join(actors_dir, name, "actor.json")
    with open(actor_json, "r") as file:
        actor_data = json.loads(file.read())
    
    graphics = actor_data["graphics"]

    return Actor(speaking, graphics, mood, mouth_style, [x, y], [width, height])