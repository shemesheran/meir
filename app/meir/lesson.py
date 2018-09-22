class Lesson:
    def __init__(self,
                 code,
                 title,
                 rabbi,
                 series_title,
                 audio_url):
        self.code = code
        self.title = title
        self.rabbi = rabbi
        self.series_title = series_title
        self.audio_url = audio_url

    def __eq__(self, other):
        return isinstance(other, Lesson) and self.code == other.code

    def __hash__(self):
        return self.code