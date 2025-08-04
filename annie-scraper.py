from dotenv import load_dotenv
import os
import json

from annie_website import CourseLinkScraper

ANNIE_EPISODE_LIST_URL = "https://learnvietnamesewithannie.com/podcast?page="
ANNIE_EPISODE_LIST_LAST_PAGE = 171

load_dotenv(override=True)

annie_cookie_str = os.getenv("ANNIE_COOKIE")
annie_cookie_dict = json.loads(annie_cookie_str)


def get_episode_list(page):
    episodes_website = CourseLinkScraper(f"{ANNIE_EPISODE_LIST_URL}{page}", annie_cookie_dict)
    all_links = episodes_website.get_course_links()

    return episodes_website.get_course_links()


for i in range(1, 10):
    print(get_episode_list(i))
