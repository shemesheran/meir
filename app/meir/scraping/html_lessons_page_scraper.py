from bs4 import BeautifulSoup

from app.meir.lesson import Lesson

class LessonsPageScraper:

    def scrap_lessons_series_title(self, html_page_text):
        soup = BeautifulSoup(html_page_text, 'html.parser')
        series_title_select_query = ".pagekotret"
        series_title_tag = soup.select_one(series_title_select_query)
        series_title_tag.findChildren
        title_lines_text = map(lambda x: x.text, series_title_tag.children)
        title_lines_text_unicoded = map(unicode, title_lines_text)
        change_list_of_strings_to_paragraph = lambda x, y: u"{}\n{}".format(x, y)
        title_as_unicoded_paragraph = reduce(change_list_of_strings_to_paragraph, title_lines_text_unicoded)
        return title_as_unicoded_paragraph

    def scrap_lessons(self, html_page_text):
        soup = BeautifulSoup(html_page_text, 'html.parser')
        lessons_rows = self.__scrap_lessons_rows(soup)
        lessons = map(self.__create_lesson, lessons_rows)
        return lessons


    def __create_lesson(self, lesson_row):
        lesson_code = self.__scrap_lesson_code(lesson_row)
        lesson_title = self.__scrap_lesson_title(lesson_row)
        lesson_rabbi = self.__scrap_lesson_rabbi(lesson_row)
        lesson_series_title = self.__scrap_lesson_series_title(lesson_row)
        lesson_audio_url = self.__scrap_lesson_audio_url(lesson_row)
        return Lesson(code=lesson_code,
                      title=lesson_title,
                      rabbi=lesson_rabbi,
                      series_title=lesson_series_title,
                      audio_url=lesson_audio_url)

    def __scrap_lessons_rows(self, page_text):
        lessons_rows = page_text.select('#setsort .tableset')
        return lessons_rows

    def __scrap_lesson_code(self, lesson_row):
        lesson_code = lesson_row.select_one(".f-title + .dataOfLessonArchive").text
        return int(lesson_code)

    def __scrap_lesson_title(self, lesson_row):
        lesson_title = lesson_row.select_one(".titleArchive").text
        return lesson_title

    def __scrap_lesson_rabbi(self, lesson_row):
        lesson_rabbi = lesson_row.select_one(".rabbiNameArchive").text
        return lesson_rabbi

    def __scrap_lesson_series_title(self, lesson_row):
        lesson_series_title = lesson_row.select_one(".f-subtitle").text
        return lesson_series_title

    def __scrap_lesson_audio_url(self, lesson_row):
        lesson_audio_url = lesson_row.select_one(".durationOfLenssonArchive")['href']
        return lesson_audio_url