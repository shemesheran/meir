import unittest
import xml.etree.ElementTree

from app.meir.lesson import Lesson
from app.meir.podcast_rss_generator import MeirPodcastRSSGenerator

class MyTestCase(unittest.TestCase):

    test_podcast_title = "test title"
    test_podcast_title = "http://www.meir.co.il"

    def test_succesful_rss_generation(self):
        lessons_set = self.__create_lessons_set()
        rss_generator = MeirPodcastRSSGenerator(podcast_title=self.test_podcast_title,
                                                podcast_link=self.test_podcast_title)

        expected_rss = self.__get_expected_rss_file()
        expected_rss = self.__remove_last_buid_date_tag(expected_rss)

        actual_rss = rss_generator.generate_lessons_podcast_rss(lessons_set)
        actual_rss = self.__remove_last_buid_date_tag(actual_rss)
        self.assertEqual(expected_rss, actual_rss)

    def __create_lessons_set(self):
        lesson1 = Lesson(code=1234,
                         title="lesson1 title",
                         rabbi="harav noah",
                         series_title=self.test_podcast_title,
                         audio_url="www.merie.co.il/lesson1.mp3")
        lesson2 = Lesson(code=5678,
                         title="lesson1 title",
                         rabbi="harav sababa",
                         series_title=self.test_podcast_title,
                         audio_url="www.merie.co.il/lesson2.mp3")

        return (lesson1, lesson2)

    def __get_expected_rss_file(self):
        with open("rss_generation/expected_rss.xml", "r") as myfile:
            data = myfile.read()
        return data


    def __remove_last_buid_date_tag(self, data):
        parsed_rss = xml.etree.ElementTree.fromstring(data)
        channel_tag = parsed_rss.find("channel")
        last_buid_date_tag = channel_tag.find("lastBuildDate")
        channel_tag.remove(last_buid_date_tag)
        return xml.etree.ElementTree.tostring(parsed_rss, encoding="UTF-8")


if __name__ == '__main__':
    unittest.main()
