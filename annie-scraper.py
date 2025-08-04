from dotenv import load_dotenv
import os
import json

from annie_website import CourseLinkScraper, DialogueTabFetcher

ANNIE_EPISODE_LIST_URL = "https://learnvietnamesewithannie.com/podcast?page="
ANNIE_EPISODE_LIST_LAST_PAGE = 171

load_dotenv(override=True)

annie_cookie_str = os.getenv("ANNIE_COOKIE")
annie_cookie_dict = json.loads(annie_cookie_str)

class Dialogue():
    def __init__(self, title, dialogue):
        self.title = title
        self.dialogue = dialogue

    def __str__(self):
        return f"""Title:
        {self.title}
        
        Dialogue:
        {self.dialogue}
        """

def get_episode_list(page):
    episodes_website = CourseLinkScraper(f"{ANNIE_EPISODE_LIST_URL}{page}", annie_cookie_dict)
    all_links = episodes_website.get_course_links()

    return episodes_website.get_course_links()

def get_dialogue(podcast_url):
    podcast_website = DialogueTabFetcher(podcast_url, annie_cookie_dict)
    return Dialogue(podcast_website.title, podcast_website.get_dialogue_tab_html())

for i in range(1, 2):
    episode_links = get_episode_list(i)
    for episode in episode_links:
        dialogue = get_dialogue(episode)
        print(dialogue)
