from dotenv import load_dotenv
import os
import json
from file_utils import slugify_basic
from annie_constants import *
from annie_website import CourseLinkScraper, DialogueTabFetcher

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

def save_podcast(title: str, content: str):
    safe_title = slugify_basic(title)
    filepath = os.path.join(PODCAST_DIR, f"{safe_title}.txt")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print ("wrote file: " + safe_title)

os.makedirs(PODCAST_DIR, exist_ok=True)

for i in range(1, ANNIE_EPISODE_LIST_LAST_PAGE):
    episode_links = get_episode_list(i)
    for episode in episode_links:
        dialogue = get_dialogue(episode)
        save_podcast(dialogue.title, dialogue.__str__())

