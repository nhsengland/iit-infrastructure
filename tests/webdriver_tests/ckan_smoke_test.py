__author__ = 'Dom Barnett'

import unittest
from lib import get_or_create_driver
from register_user import RegisterUser
from register_and_login import Register_and_login


class SmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.browser = get_or_create_driver()
        cls.browser.get('http://ec2-54-77-144-171.eu-west-1.compute.amazonaws.com/')
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
        dataset_title = browser.find_element_by_xpath("/html/body/div[3]/div/div/div/section[1]/div/ul/li[1]/div/h3/a")\
            .text

        # Split title to retain first 3 words in order to prevent searching for ellipsis
        dataset_title_split = dataset_title.split(" ")
        dataset_search = dataset_title_split[0] + ' ' + dataset_title_split[1] + ' ' + dataset_title_split[2]

        # Use search bar to search for string
        browser.find_element_by_class_name("logo").click()
        browser.find_element_by_class_name('search').send_keys('"' + dataset_search + '"')
        browser.find_element_by_class_name("icon-search").click()
        self.assertIn('Datasets - CKAN', self.browser.title)
        browser.find_element_by_xpath("/html/body/div[3]/div/div/div/section[1]/div/ul/li/div/h3/a").click()
        self.assertTrue(self.browser.title.__contains__(dataset_search))

    def test_register_user(self):

        new_user = Register_and_login()
        new_user.register_and_login()

        # Logout user
        self.browser.find_element_by_xpath("/html/body/header[2]/div/nav/ul[2]/li[4]/a").click()
        # self.assertTrue("/html/body/header[2]/div/nav/ul[2]/li[1]/a/span", new_user.register_and_login().
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

        # Logout user
        self.browser.find_element_by_xpath("/html/body/header[2]/div/nav/ul[2]/li[4]/a").click()

    def test_dataset_download(self):

        new_user = RegisterUser()
        new_user.register()

        # navigate back to home page by clicking on NHS England logo
        self.browser.find_element_by_class_name("logo").click()

        # navigate to Dataset page and click on a dataset
        self.browser.find_element_by_link_text("Datasets").click()

        # select first dataset
        self.browser.find_element_by_xpath("/html/body/div[3]/div/div/div/section[1]/div/ul/li[1]/div/h3/a").click()

        # Retrieve file format
        file_format = self.browser.find_element_by_xpath("/html/body/div[3]/div/div/div/article/div/section[1]/ul/li"
                                                         "[1]/a/span").get_attribute("data-format")

        # Click on explore dropdown and select "More information"
        self.browser.find_element_by_class_name("icon-share-alt").click()
        self.browser.find_element_by_class_name("icon-info-sign").click()

        # If file format is pdf, file will open in current tab
        if file_format == u'pdf':
            self.browser.find_element_by_class_name("icon-external-link").click()
            self.assertIn("pdf", self.browser.current_url)
            #navigate back to CKAN and logout
            self.browser.back()
            self.browser.find_element_by_class_name("logo").click()
            self.browser.find_element_by_xpath("/html/body/header[2]/div/nav/ul[2]/li[4]/a/i").click()

        else:
            self.browser.find_element_by_class_name("icon-external-link").click()
            self.browser.find_element_by_class_name("logo").click()
            self.browser.find_element_by_xpath("/html/body/header[2]/div/nav/ul[2]/li[4]/a/i").click()


if __name__ == '__main__':
    unittest.main()
