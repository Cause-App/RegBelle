#!/usr/bin/python3.9

from belle import parse

# TODO
# Read these from the command line
movies_dir = "./movies"
output_dir = "./output"
actors_dir = "./actors"
movie_name = "test"

movie = parse.parse_movie(movies_dir, actors_dir, movie_name)

mouth_data = movie.get_mouth_data(output_dir)

print(mouth_data)