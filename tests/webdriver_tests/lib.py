from selenium import webdriver
DRIVER = None

def get_or_create_driver():
    global DRIVER
    DRIVER = DRIVER or webdriver.Firefox()
    return DRIVER
