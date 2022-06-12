from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()
        
    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def wait_for_row_in_list_table(self, row_text):
        MAX_WAIT = 10
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except(AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
 
    def test_can_start_a_list_for_one_user(self):
        self.browser.get(self.live_server_url)
        
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
        
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock fethers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        self.wait_for_row_in_list_table('2: Use peacock fethers to make a fly')
        
        
    def test_mutiple_users_can_start_lists_at_different_url(self):
        self.browser.get(self.live_server_url)
            
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
    
        edith_list_url = self.browser.current_url
        
        self.assertRegex(edith_list_url, '/lists/.+')
        self.browser.quit()
        
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)
        
        page_text = self.browser.find_element_by_tag_name('body').text
    
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)
    
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy mulk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy mulk')
    
        francis_list_url = self.browser.current_url
        
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)
    
        page_text = self.browser.find_element_by_tag_name('body').text
        
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy mulk', page_text)
        self.browser.quit()

browser = webdriver.Firefox()
# Edith has heard about a cool new online to-do app. She goes to check out its homepage
browser.get('http://localhost:8000')

# She notices the page title and header mention to-do lists
assert 'To-Do' in browser.title

# She is invited to enter a to-do item straight away

# She types "Buy peacock feathers" into a text box (Edith's hobby is tying fly-fishing lures)

# When she hits enter, the page updates, and now the page lists "1: Buy peacock feathers" as an item in a to-do list

# There is still a text box inviting her to add another item. She enters "Use peacock feathers to make a fly" (Edith is very methodical)

# The page updates again, and now shows both items on her list

#Edith wonders whether the site will remember her list. Then she sees that the site has generated a unique URL for her -- there is some explanatory text to that effect.

# She vistis that URL - her to-do list is still there.

# Satisfied, she goes back to sleep

browser.quit()
