def parse_args(line):
    args = []
    current_arg = ""
    in_string = None
    escaping = False
    for i in line:
        if in_string is not None:
            if i == in_string and not escaping:
                in_string = None
            elif i == "\\" and not escaping:
                escaping = True
            else:
                current_arg += i
                escaping = False
        elif i in ["\"", "'"] and not escaping:
            in_string = i
        elif i == " " and not escaping:
            args.append(current_arg)
            current_arg = ""
        elif i == "\\" and not escaping:
            escaping = True
        else:
            current_arg += i
            escaping = False

    if current_arg != "":
        args.append(current_arg)

    return args

def new_paragraph(movie, movie_data):
    new_paragraph = {
        "actors": [],
        "text": []
    }
    for actor in movie_data["actors"]:
        new_paragraph["actors"].append(actor.copy())
    
    movie_data["current-scene"]["paragraphs"].append(new_paragraph)
    movie_data["current-paragraph"] = new_paragraph


def new_scene(movie, movie_data):
    new_scene = {
        "background": {
            "color": movie_data["background-color"],
            "image": movie_data["background-image"],
            "x": movie_data["background-image-x"],
            "y": movie_data["background-image-y"],
            "width": movie_data["background-image-width"],
            "height": movie_data["background-image-height"]
        },
        "paragraphs": []
    }
    movie_data["current-scene"] = new_scene
    new_paragraph(movie, movie_data)
    movie["scenes"].append(new_scene)


def nullify(x):
    if type(x) == str and x.lower() == "null":
        return None
    if (type(x) == float or type(x) == int) and x < 0:
        return None
    return x

def audio(movie, movie_data, path):
    movie["audio"] = path

def resolution(movie, movie_data, width, height):
    movie["width"] = width
    movie["height"] = height

def framerate(movie, movie_data, fr):
    movie["framerate"] = fr

def phoneme_hack(movie, movie_data, original, hack):
    movie["phonemeHacks"][original] = hack

def background_image(movie, movie_data, path):
    path = nullify(path)
    movie_data["background-image"] = path
    new_scene(movie, movie_data)

def background_image_x(movie, movie_data, x):
    movie_data["background-image-x"] = x
    new_scene(movie, movie_data)

def background_image_y(movie, movie_data, y):
    movie_data["background-image-y"] = y
    new_scene(movie, movie_data)

def background_image_pos(movie, movie_data, x, y):
    movie_data["background-image-x"] = x
    movie_data["background-image-y"] = y
    new_scene(movie, movie_data)


def background_image_width(movie, movie_data, width):
    movie_data["background-image-width"] = nullify(width)
    new_scene(movie, movie_data)

def background_image_height(movie, movie_data, height):
    movie_data["background-image-height"] = nullify(height)
    new_scene(movie, movie_data)


def background_image_size(movie, movie_data, width, height):
    movie_data["background-image-width"] = nullify(width)
    movie_data["background-image-height"] = nullify(height)
    new_scene(movie, movie_data)

def background_color(movie, movie_data, r, g, b):
    movie_data["background-color"] = [r,g,b]
    new_scene(movie, movie_data)

def add_actor(movie, movie_data, name, label):
    new_actor = {
        "name": name,
    }
    movie_data["actor-labels"][label] = len(movie_data["actors"])
    movie_data["actors"].append(new_actor)
    new_paragraph(movie, movie_data)

def remove_actor(movie, movie_data, label):
    labels = movie_data["actor-labels"]
    index = labels[label]
    del labels[label]
    del movie_data["actors"][index]
    for l in labels:
        if labels[l] > index:
            labels[l] -= 1
    new_paragraph(movie, movie_data)


def actor_speaking(movie, movie_data, label, speaking):
    actor = movie_data["actors"][movie_data["actor-labels"][label]]
    actor["speaking"] = speaking
    new_paragraph(movie, movie_data)

def actor_mouth_style(movie, movie_data, label, style):
    actor = movie_data["actors"][movie_data["actor-labels"][label]]
    actor["mouthStyle"] = style
    new_paragraph(movie, movie_data)


def actor_x(movie, movie_data, label, x):
    actor = movie_data["actors"][movie_data["actor-labels"][label]]
    actor["x"] = x
    new_paragraph(movie, movie_data)

def actor_y(movie, movie_data, label, y):
    actor = movie_data["actors"][movie_data["actor-labels"][label]]
    actor["y"] = y
    new_paragraph(movie, movie_data)

def actor_pos(movie, movie_data, label, x, y):
    actor = movie_data["actors"][movie_data["actor-labels"][label]]
    actor["x"] = x
    actor["y"] = y
    new_paragraph(movie, movie_data)

def actor_scale_x(movie, movie_data, label, scale_x):
    actor = movie_data["actors"][movie_data["actor-labels"][label]]
    if "scale" in actor:
        actor["scaleY"] = actor["scale"]
        del actor["scale"]
    actor["scaleX"] = scale_x
    new_paragraph(movie, movie_data)

def actor_scale_y(movie, movie_data, label, scale_y):
    actor = movie_data["actors"][movie_data["actor-labels"][label]]
    if "scale" in actor:
        actor["scaleX"] = actor["scale"]
        del actor["scale"]
    actor["scaleY"] = scale_y
    new_paragraph(movie, movie_data)

def actor_scale(movie, movie_data, label, scale):
    actor = movie_data["actors"][movie_data["actor-labels"][label]]
    if "scaleX" in actor:
        del actor["scaleX"]
    if "scaleY" in actor:
        del actor["scaleY"]
    actor["scale"] = scale
    new_paragraph(movie, movie_data)

def actor_mood(movie, movie_data, label, mood):
    actor = movie_data["actors"][movie_data["actor-labels"][label]]
    actor["mood"] = mood
    new_paragraph(movie, movie_data)


def p_bool(x):
    x = x.lower()
    if x == "true":
        return True
    if x == "false":
        return False
    raise ValueError(f"'{x}' is not a valid boolean")

commands = {
    "audio": [[str], audio],
    "resolution": [[int, int], resolution],
    "framerate": [[int], framerate],
    "phoneme-hack": [[str, str], phoneme_hack],
    "background-image": [[str], background_image],
    "background-image-x": [[float], background_image_x],
    "background-image-y": [[float], background_image_y],
    "background-image-pos": [[float, float], background_image_pos],
    "background-image-width": [[float], background_image_width],
    "background-image-height": [[float], background_image_height],
    "background-image-size": [[float, float], background_image_size],
    "background-color": [[int, int, int], background_color],
    "add-actor": [[str, str], add_actor],
    "remove-actor": [[str], remove_actor],
    "actor-speaking": [[str, p_bool], actor_speaking],
    "actor-mouth-style": [[str, str], actor_mouth_style],
    "actor-x": [[str, float], actor_x],
    "actor-y": [[str, float], actor_y],
    "actor-pos": [[str, float, float], actor_pos],
    "actor-scale-x": [[str, float], actor_scale_x],
    "actor-scale-y": [[str, float], actor_scale_y],
    "actor-scale": [[str, float], actor_scale],
    "actor-mood": [[str, str], actor_mood]
}

def parse_script(lines):
    current_paragraph = {
        "actors": [],
        "text": []
    }
    current_scene = {
        "background": {},
        "paragraphs": [
            current_paragraph
        ]
    }
    movie = {
        "scenes": [
            current_scene
        ],
        "phonemeHacks": {}
    }
    movie_data = {
        "current-scene": current_scene,
        "current-paragraph": current_paragraph,
        "background-color": None,
        "background-image": None,
        "background-image-x": None,
        "background-image-y": None,
        "background-image-width": None,
        "background-image-height": None,
        "actors": [],
        "actor-labels": {}
    }
    
    for i, line in enumerate(lines):
        error_heading = f"Script error on line {i+1}:"
        if line.startswith(":"):
            args = parse_args(line[1:])
            if len(args) == 0:
                raise Exception(f"{error_heading} No command is specified")
            cmd, *args = args
            cmd = cmd.lower()
            if cmd not in commands:
                raise Exception(f"{error_heading} '{cmd}' is not a valid command")
            types, handler = commands[cmd]
            if len(types) != len(args):
                raise Exception(f"{error_heading} Command '{cmd}' takes {len(types)} arguments but {len(args)} {'was' if len(args) == 1 else 'were'} given")
            parsed_args = []
            for j, type in enumerate(types):
                try:
                    v = type(args[j])
                    parsed_args.append(v)
                except ValueError as e:
                    raise ValueError(f"{error_heading} {str(e)}")
            
            handler(movie, movie_data, *parsed_args)
        
        elif not line.startswith("//"):
            if line == "":
                new_paragraph(movie, movie_data)
            else:
                movie_data["current-paragraph"]["text"].append(line)

    for scene in movie["scenes"]:
        scene["paragraphs"] = [x for x in scene["paragraphs"] if len(x["text"]) > 0]

    movie["scenes"] = [x for x in movie["scenes"] if len(x["paragraphs"]) > 0]

    return movie