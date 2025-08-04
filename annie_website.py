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
        self.title = self.soup.title.string.strip()


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

class DialogueTabFetcher(Website):
    def get_dialogue_tab_html(self):
        """
        Returns the HTML content of the <div role="tabpanel" class="tab-pane" id="dialogue">
        """
        target_div = self.soup.find(
            "div",
            {
                "id": "dialogue"
            }
        )
        if target_div:
            for irrelevant in target_div(["script", "style", "img", "input", "audio", "source"]):
                irrelevant.decompose()
            all_spans = target_div.find_all("span")
            top_level_spans = [
                span for span in all_spans if not span.find_parent("span")
            ]

            lines = [span.get_text(strip=True, separator=" ") for span in top_level_spans if span.get_text(strip=True)]
            return "\n".join(lines)
        return None