#!/usr/bin/python3.9

from belle import parse, belleroom
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("movie_name", help="The name of the project inside the movies directory", type=str)
parser.add_argument("-m", "--movies-dir", help="The directory in which all of your projects are found", type=str, default="./movies")
parser.add_argument("-o", "--output-dir", help="The directory in which the output of all of your projects will be stored", type=str, default="./output")
parser.add_argument("-a", "--actors-dir", help="The directory in which all of your actors are found", type=str, default="./actors")
parser.add_argument("-p", "--gentle-port", help="The port on which the gentle server is running", type=int, default=8765)
parser.add_argument("-F", "--force", help="Forces overwriting to transcript, frames, etc.", action="store_true")
parser.add_argument("-G", "--launch-gentle", help="If the gentle server is not listening on the specified port, launch it", action="store_true")
parser.add_argument("-H", "--hide", help="Don't show the frames of the video while it is rendering", action="store_true")
parser.add_argument("-S", "--stitch", help="Stitch the frames together into an mp4 file after rendering", action="store_true")
parser.add_argument("-A", "--overlay-audio", help="Overlay the training audio on the rendered video. Use with --stitch", action="store_true")
parser.add_argument("-T", "--transcript-only", help="Only write a transcript and then exit. Do not render the video", action="store_true")

args = parser.parse_args()

movies_dir = args.movies_dir
output_dir = args.output_dir
actors_dir = args.actors_dir
movie_name = args.movie_name

gentle_port = args.gentle_port
launch_gentle = args.launch_gentle

force_overwrite_mouth_data = args.force
force_overwrite_transcript = args.force
force_overwrite_audio = args.force
force_delete_frames = args.force
force_stitch = args.force
force_add_audio = args.force

show = not args.hide

movie = parse.parse_movie(movies_dir, actors_dir, movie_name)

if args.transcript_only:
    movie.create_transcript(output_dir, hack=False, force_overwrite=force_overwrite_transcript)
else:
    movie.init(output_dir, gentle_port, force_overwrite_mouth_data=force_overwrite_mouth_data, force_overwrite_transcript=force_overwrite_transcript, force_overwrite_audio=force_overwrite_audio, force_delete_frames=force_delete_frames, launch_gentle=launch_gentle)

    room = belleroom.BelleRoom(movie)

    frame = 0
    while frame is not None:
        frame = room.render_frame(output_dir, show=show)

    if args.stitch:
        room.stitch(output_dir, force_stitch=force_stitch)

        if args.overlay_audio:
            room.add_audio(output_dir, force_add_audio=force_add_audio)