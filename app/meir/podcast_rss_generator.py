from feedgen.feed import FeedGenerator

class MeirPodcastRSSGenerator:

    def __init__(self, podcast_title, podcast_link):
        self.title = podcast_title
        self.link = podcast_link
        self.description = "eqw"

    def generate_lessons_podcast_rss(self, lessons_set):
        feed_generator = self.__init_feed_generator()
        for lesson in lessons_set:
            feed_entry = feed_generator.add_entry()
            self.__edit_podcast_feed_entry(feed_entry, lesson)

        return feed_generator.rss_str()

    def __init_feed_generator(self):
        feed_generator = FeedGenerator()
        feed_generator.load_extension('podcast')
        feed_generator.title(self.title)
        feed_generator.link(self.__generate_podcast_link(self.link))
        feed_generator.description(self.description)
        feed_generator.podcast.itunes_category('Religion & Spirituality', 'Judaism')
        return feed_generator

    def __generate_podcast_link(self, link):
        return {"href": link}

    def __edit_podcast_feed_entry(self, feed_entry, lesson):
        feed_entry.id(str(lesson.code))
        feed_entry.link(self.__generate_podcast_link(lesson.audio_url))
        feed_entry.description(lesson.series_title)
        feed_entry.title(lesson.title)
        feed_entry.description(lesson.rabbi)
        feed_entry.enclosure(lesson.audio_url, 0, 'audio/mpeg')
