import requests
from bs4 import BeautifulSoup

# Some websites need you to use proper headers when fetching them:
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}


class Website:
    def __init__(self, url, cookies):
        """
        Create this Website object from the given url using the BeautifulSoup library
        """
        self.url = url
        response = requests.get(url, headers=headers, cookies=cookies)
        self.soup = BeautifulSoup(response.content, 'html.parser')


class CourseLinkScraper(Website):
    def get_course_links(self):
        """
        Returns a list of all href links inside <div class="course-item-content">
        """
        course_divs = self.soup.find_all("div", class_="course-item-content")
        links = set()
        for div in course_divs:
            for a_tag in div.find_all("a", href=True):
                href = a_tag["href"].strip()
                if href.startswith("http"):
                    links.add(href)
        return links
