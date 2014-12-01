__author__ = 'Dom Barnett'


import random
import string
from lib import get_or_create_driver


class Register_and_login():

    #def __init__(self):

    def register_and_login(self):

        first_name = ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
        surname = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
        username = first_name + '_' + surname
        password = "password01"

        self.browser = get_or_create_driver()

        # Navigate to Registration page
        self.browser.find_element_by_xpath("/html/body/header[2]/div/nav/ul[2]/li[2]/a").click()

        # Enter Username
        self.browser.find_element_by_id("field-username").clear()
        self.browser.find_element_by_id("field-username").send_keys(username)

        # Enter Full Name
        self.browser.find_element_by_id("field-fullname").clear()
        self.browser.find_element_by_id("field-fullname").send_keys(first_name + ' ' + surname)

        # Enter email address
        self.browser.find_element_by_id("field-email").clear()
        self.browser.find_element_by_id("field-email").send_keys(first_name + '.' + surname + "@test.com")

        # Enter password
        self.browser.find_element_by_id("field-password").clear()
        self.browser.find_element_by_id("field-password").send_keys(password)

        # Confirm password
        self.browser.find_element_by_id("field-confirm-password").clear()
        self.browser.find_element_by_id("field-confirm-password").send_keys(password)

        # Create Account
        self.browser.find_element_by_name("save").click()

        # Logout newly created user
        self.browser.find_element_by_xpath("/html/body/header[2]/div/nav/ul[2]/li[4]/a").click()

        # Login newly created user
        self.browser.find_element_by_xpath("/html/body/header[2]/div/nav/ul[2]/li[1]/a").click()
        self.browser.find_element_by_id("field-login").clear()
        self.browser.find_element_by_id("field-login").send_keys(username)
        self.browser.find_element_by_id("field-password").clear()
        self.browser.find_element_by_id("field-password").send_keys(password)
        self.browser.find_element_by_css_selector("button.btn.btn-primary").click()

        # Ensure user is logged in

        #self.browser.assertTrue("/html/body/header[2]/div/nav/ul[2]/li[1]/a/span", first_name + ' '
                        #+ surname)

        print username


        return self.browser
