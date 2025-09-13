import os
import customtkinter as ctk
from PIL import Image


CURRENT_PATH = os.getcwd()

rootWindow = ctk.CTk()
activeTab = None

pageManagers = {
    "forum": None,
    "gpa": None,
    "reminder": None,
}
forumAccount = None

imageCache = {}


def get_ctk_cache_image(tab, fileName, size=(100, 100)):
    global imageCache

    cacheString = tab + "_" + fileName + "_" + str(size)
    if cacheString not in imageCache:
        image = Image.open(os.path.join(CURRENT_PATH, tab, "img", fileName))
        imageCache[cacheString] = ctk.CTkImage(image, size=size)
    return imageCache[cacheString]


