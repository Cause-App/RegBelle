#!/usr/bin/python3.9

from belle import parse, belleroom
import cv2

# TODO
# Read these from the command line
movies_dir = "./movies"
output_dir = "./output"
actors_dir = "./actors"
movie_name = "test"

movie = parse.parse_movie(movies_dir, actors_dir, movie_name)
movie.init(output_dir)

room = belleroom.BelleRoom(movie)

frame = 0
while frame is not None:
    frame = room.render_frame(output_dir)
    if frame is not None:
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

