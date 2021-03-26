#!/usr/bin/python3.9

from belle import parse

movies_dir = "./movies"
actors_dir = "./actors"
movie_name = "test"

scene = parse.parse_movie(movies_dir, actors_dir, movie_name)