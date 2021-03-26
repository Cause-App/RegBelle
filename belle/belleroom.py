class BelleRoom:
    def __init__(self, movie):
        self.movie = movie
        self.title = movie.name
        self.width, self.height = movie.resolution
        self.framerate = movie.framerate
        self.dt = 1.0/self.framerate