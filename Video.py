class Video:
    def __init__(self, filepath: str, name: str, start_time: int = 0, 
                 duration: float = None, volume: float = 1.0):
        self.filepath = filepath
        self.name = name
        self.start_time = start_time
        self.duration = duration
        self.volume = volume