def confirm(prompt, default=0, options=["y","n"]):
    answer = None
    options = list(x.lower() for x in options)
    upperOptions = list(x.lower() for x in options)
    upperOptions[default] = upperOptions[default].upper()
    while not answer in options:
        answer = input(f"{prompt} ({'/'.join(upperOptions)}) ").lower()
        if answer == "":
            answer = options[default]
    
    return answer