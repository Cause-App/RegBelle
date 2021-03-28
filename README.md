# RegBelle

A somewhat automated animation engine. Automatically lip sync an animated character to your voice.

The idea comes from [this YouTube video by carykh](https://www.youtube.com/watch?v=y3B8YqeLCpY).


## Usage

    usage: regbelle.py [-h] [-m MOVIES_DIR] [-o OUTPUT_DIR] [-a ACTORS_DIR] [-s START_SCENE] [-p GENTLE_PORT] [-F] [-G] [-H] [-S] [-A] [-R] movie_name

    positional arguments:
    movie_name            The name of the project inside the movies directory

    optional arguments:
    -h, --help            show this help message and exit
    -m MOVIES_DIR, --movies-dir MOVIES_DIR
                            The directory in which all of your projects are found
    -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                            The directory in which the output of all of your projects will be stored
    -a ACTORS_DIR, --actors-dir ACTORS_DIR
                            The directory in which all of your actors are found
    -s START_SCENE, --start-scene START_SCENE
                            The first scene to render. Can be helpful for testing (indexes from 0)
    -p GENTLE_PORT, --gentle-port GENTLE_PORT
                            The port on which the gentle server is running
    -F, --force           Forces overwriting to transcript, frames, etc.
    -G, --launch-gentle   If the gentle server is not listening on the specified port, launch it
    -H, --hide            Don't show the frames of the video while it is rendering
    -S, --stitch          Stitch the frames together into an mp4 file after rendering
    -A, --overlay-audio   Overlay the training audio on the rendered video. Use with --stitch
    -R, --rich-script-only
                            Only write a rich script and then exit. Do not render the video

## Creating an actor

An actor consists of three elements:
- Body art
- Mouth art
- An "actor.json" file.

The actor.json file must be in a subdirectory of the actors directory. This subdirectory must have the same name as your actor (which will be used to reference this actor in the script).

The JSON must contain a single key called `graphics` which has two sub-keys: `body` and `mouth`.

`body` can have as many sub-keys as you like &ndash; each referring to a different mood the character can express e.g. `happy`, `explainy`. Each of these subkeys must map to an array of objects, with each object corresponding to a different sprite which represents that mood.

These objects must have three keys: `artwork` must map to a string containing a relative path to the image (svg is recommended but most image formats will work). It must also contain `mouthX` and `mouthY` keys which are each floats representing the proportion of the way across the body image at which the mouth should appear. For example setting both to 0.5 will result in the centre of the mouth sprite being drawn in the centre of the body sprite.

In order to calculate `mouthX` and `mouthY`, you can use the tool located in `./mouth-pos-tool/` by running `ng serve` in that directory and then going to `localhost:4200/` in your browser.

The body sprites don't all need to be any specific size, but they all need to be to the same scale.

The `graphics` object needs to have another sub-key adject to `body` called `mouth`. The `mouth` object can have as many sub-keys as you like, one for each mouth style you want to be able to use, e.g. `smile`, `frown`.

Inside each of these objects must be 6 keys: `openVowels`, `y,l`, `oo,r`, `m,p,b`, `f,v`, and `d,g,k,th`. These represent the different shapes your mouth can make when making sounds. Each of these objects should have the exact same sub-keys, mapping to the path to the image to be used when going between those two mouth shapes.

For example, supposing the `actor.json` file was loaded into a JavaScript object `actor`,
```javascript
actor["mouth"]["smile"]["openVowels"]["openVowels"]
```
should map to the path of the image used to represent the shape the mouth makes when making an open vowel sound, and

```javascript
actor["mouth"]["smile"]["openVowels"]["y,l"]
```
should map to the path of the image used to represent the shape the mouth makes when moving from an open vowel sound, to a *y* or *l* sound.

As such there should be 36 paths in total. Note that these do not all have to be distinct images, i.e. you can use the path to the same image multiple times.

Once again svg is the recommended format but most image formats will work. Also the mouth images must be to the same scale as each other and to scale with the body images.

Once your actors are created you can go on to writing the movie script.

## Creating the movie script

In the movies directory, create a subdirectory whose name is the name of your movie. Inside this subdirectory, create a file called `script.regbelle`. You can edit this file in any plaintext editor.

This file contains the text which will be spoken in the movie by your actors. It also contains commands. Each command line starts with a colon (`:`) character.

### Commands

Here is a list of commands and the arguments they take

- `:audio [path]`

    specifies the relative path to the audio file of a human reading the transcript. Note that no file actually has to exist at that path if you are running the program in Rich Script Only mode.

- `:resolution [width] [height]`

    specifies the resolution of the output video

- `:framerate [fps]`

    specifies the framerate of the output video

- `:phoneme-hack [original] [hack]`

    sets a phoneme hack. If the lip syncing algorithm does not know the phoenemes for one of the words in your script, you can ask it to treat it as if some other word or combination of words was in its place. For example,

    `:phoneme hack "bourgeoisie" "boar jar sea"`

- `:background-image [path]`

    sets the path of the background image. This can be set multiple times to change the background image during the movie. Note that no file actually has to exist at that path if you are running the program in Rich Script Only mode, however if this is the case then the image will not appear in the rich script. This can also be set to `null` for no background image

- `:background-image-x [x]`

    sets the x coordinate of the centre of the background image as a proportion of the screen width.

- `:background-image-y [y]`

    sets the y coordinate of the centre of the background image as a proportion of the screen height

- `:background-image-pos [x] [y]`

    equivalent to writing both `:background-image-x [x]` and `:background-image-y [y]`

- `:background-image-width [width]`

    sets the width of the background image as a proportion of the screen width.

- `:background-image-height [height]`

    sets the height of the background image as a proportion of the screen height

- `:background-image-size [width] [height]`

    equivalent to writing both `:background-image-width [width]` and `:background-image-height [height]`

- `:background-color [r] [g] [b]`

    sets the colour of the background if/where it can be seen behind the background image. Values range from 0 to 255

- `:add-actor [name] [label]`

    adds an actor to the movie at this point in time. The `name` should be the name of the subdirectory of the actors directory in which the `actor.json` file should be found. The `label` is a string with which you can refer to the actor in later commands.

- `:remove-actor [label]`

    removes the specified actor from the movie at this point in time

- `:actor-speaking [label] [is_speaking]`

    sets whether the specified actor should be lip syncing to the words which are currently being spoken.

- `:actor-mouth-style [label] [style]`

    sets the specified actor's mouth style (e.g. `smile` or `frown`)

- `:actor-x [label] [x]`

    sets the x coordinate of the centre of the specified actor as a proportion of the screen width

- `:actor-y [label] [y]`

    sets the y coordinate of the centre of the specified actor as a proportion of the screen height

- `:actor-pos [label] [x] [y]`

    equivalent to writing both `:actor-x [label] [x]` and `:actor-y [label] [y]`

- `:actor-scale-x [label] [scale]`

    sets the horizontal scale factor of the specified actor, relative to the screen height (not width)

- `:actor-scale-x [label] [scale]`

    sets the vertical scale factor of the specified actor, relative to the screen height

- `:actor-scale [label] [scale]`

    equivalent to writing both `:actor-scale-x [label] [scale]` and `:actor-scale-y [label] [scale]`

- `:actor-mood [label] [mood]`

    sets the mood of the specified actor (e.g. `happy`, `explainy`)

The speaking character will pick a random one of the poses corresponding to the specified mood.

The other lines of the file should contain text to be spoken.

You can use a tilde (`~`) character to denote that the speaking actor/s should change pose at that point. Other than that, they will change pose when a punctuation mark is reached, and, of course, when their mood is changed.

## Generating a rich script

It can be difficult to record yourself reading straight from the `script.regbelle` file because of all the commands in the way, and because you can't see which background images are being displayed.

To combat this you can create a "rich script" for your movie before you have recorded the audio or have all the artwork in place. To do this, run

```bash
python3 regbelle.py [movie_name] -R
```

or

```bash
python3 regbelle.py [movie_name] --rich-script-only
```

which will generate a file called `rich-script.html` in the output directory of the movie. Opening this in a web-browser gives a much more reader-friendly and printable version of the script.

## Rendering

Once you have a `script.regbelle` file, all the artwork is made, and you have a recording of the full script being read by a human, you can run

```bash
python3 regbelle.py [movie_name]
```

to generate each frame as an individual bitmap in the `frames` subdirectory of your movie's output directory.

If you want the program to automatically stitch all of the frames together into a video file, run with the `-S` or `--stitch` flag, and you will then see a file named `render.mp4` in the movie's output directory.

If you also want the program to automatically overlay the audio of the transcript being read onto the rendered video, use the `-A` or `--overlay-audio` flag, and you will then see a file named `render-with-audio.mp4` in the movie's output directory.

## GENTLE server

[GENTLE](https://github.com/lowerquality/gentle) is the program used under the hood to sync up the audio with the transcript. It needs to be running on your localhost in order to use RegBelle. If you already have it running on your computer, but it is on a port other than 8765 (the default), then use the flag `-p [port]` or `--gentle-port [port]`.

If GENTLE is not already running, use the `-G` or `--launch-gentle` flag which will cause the program to try to launch gentle if it is not already running.