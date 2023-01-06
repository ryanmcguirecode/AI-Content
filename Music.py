class Music:
    def __init__(self, music_filepath: str, music_name: str, music_start: int = 0, music_duration: float = None, music_volume: float = 1.0):
        self.music_filepath = music_filepath
        self.music_name = music_name
        self.music_start = music_start
        self.music_duration = music_duration
        self.music_volume = music_volume