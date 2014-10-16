__author__ = 'Dom Barnett'

import unittest
import pkg
from register_user import RegisterUser
from register_and_login import Register_and_login


class SmokeTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.browser = pkg.get_or_create_driver()
        cls.browser.get('http://ec2-54-171-89-128.eu-west-1.compute.amazonaws.com/')
        cls.browser.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()

    def test_anonymous_user_search_tag(self):
        browser = self.browser

        # Log out any user that may still be logged in.
        try:
            browser.find_element_by_xpath("/html/body/header[2]/div/nav/ul[2]/li[4]/a").is_displayed()
            browser.find_element_by_xpath("/html/body/header[2]/div/nav/ul[2]/li[4]/a").click()
            browser.find_element_by_link_text("Home").click()
        except Exception, e:
            browser.find_element_by_link_text("Home").click()

        # Retain tag name for manual search input
        search_tag = self.browser.find_element_by_xpath("/html/body/div[3]/div[2]/div/div/div/div/div/a[2]").text

        # Search by tag
        browser.find_element_by_xpath("/html/body/div[3]/div[2]/div/div/div/div/div/a[1]").click()
        browser.find_element_by_xpath("/html/body/div[3]/div/div/div/section[1]/div/ul/li[1]/div/h3/a").click()

        # navigate back to home page by clicking on NHS England logo
        browser.find_element_by_class_name("logo").click()

        # Use search bar to search for a tag
        browser.find_element_by_class_name('search').send_keys(search_tag)
        browser.find_element_by_class_name("icon-search").click()
        self.assertIn('Datasets - CKAN', self.browser.title)

    def test_anonymous_user_search_title(self):
        browser = self.browser

        # navigate back to home page by clicking on NHS England logo
        browser.find_element_by_class_name("logo").click()

        # Search all datasets
        browser.find_element_by_xpath("/html/body/div[3]/div[3]/div/div/div[2]/div/div/ul/li[1]/a").click()

        # Retain dataset title for manual search input
        search_title = browser.find_element_by_xpath("/html/body/div[3]/div/div/div/section[1]/div/ul/li[1]/div/h3/a")\
            .text

        # Use search bar to search for exact title
        browser.find_element_by_class_name("logo").click()
        browser.find_element_by_class_name('search').send_keys('"' + search_title + '"')
        browser.find_element_by_class_name("icon-search").click()
        self.assertIn('Datasets - CKAN', self.browser.title)
        browser.find_element_by_xpath("/html/body/div[3]/div/div/div/section[1]/div/ul/li/div/h3/a").click()
        self.assertIn(search_title, self.browser.title)

    def test_register_user(self):

        new_user = Register_and_login()
        new_user.register_and_login()

        #Logout user
        self.browser.find_element_by_xpath("/html/body/header[2]/div/nav/ul[2]/li[4]/a").click()
        #self.assertTrue("/html/body/header[2]/div/nav/ul[2]/li[1]/a/span", new_user.register_and_login().
                                #first_name + ' ' + new_user.register_and_login().surname)

    def test_logged_in_search(self):

        new_user = RegisterUser()
        new_user.register()

        # navigate back to home page by clicking on NHS England logo
        self.browser.find_element_by_class_name("logo").click()

        # Retain tag name for manual search input
        search_text = self.browser.find_element_by_xpath("/html/body/div[3]/div[2]/div/div/div/div/div/a[2]").text

        # Search by tag
        self.browser.find_element_by_xpath("/html/body/div[3]/div[2]/div/div/div/div/div/a[1]").click()
        self.browser.find_element_by_xpath("/html/body/div[3]/div/div/div/section[1]/div/ul/li[1]/div/h3/a").click()

        # navigate back to home page by clicking on NHS England logo
        self.browser.find_element_by_class_name("logo").click()

        # Use search bar to search for dataset
        self.browser.find_element_by_class_name('search').send_keys(search_text)
        self.browser.find_element_by_class_name("icon-search").click()
        self.assertIn('Datasets - CKAN', self.browser.title)

        # Click on dataset
        self.browser.find_element_by_xpath("/html/body/div[3]/div/div/div/section[1]/div/ul/li[1]/div/h3/a").click()

        #Logout user
        self.browser.find_element_by_xpath("/html/body/header[2]/div/nav/ul[2]/li[4]/a").click()

    def test_dataset_download(self):

        new_user = RegisterUser()
        new_user.register()

        # navigate back to home page by clicking on NHS England logo
        self.browser.find_element_by_class_name("logo").click()

        # navigate to Dataset page and click on a dataset
        self.browser.find_element_by_link_text("Datasets").click()
        self.browser.find_element_by_link_text(".xlsx").click()

        # Click on explore dropdown and select "More information"
        self.browser.find_element_by_class_name("icon-share-alt").click()
        self.browser.find_element_by_class_name("icon-info-sign").click()

        # Click Go to Resource
        self.browser.find_element_by_class_name("icon-external-link").click()

        #Logout user
        self.browser.find_element_by_xpath("/html/body/header[2]/div/nav/ul[2]/li[4]/a").click()

if __name__ == '__main__':
    unittest.main()

