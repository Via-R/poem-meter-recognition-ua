import time
from typing import Optional
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

class TextStresser:
    '''Functionality to open selenium webdriver session.
    
    It loads the text stresser website and fetches the stressed version of input text.'''

    # Hides selenium dev browser
    SILENT: bool = True
    # There isn't any normal API for this, so rely on parsing this exact resource to have a stressed version of text
    # Obviously, if there was a normal API it would perform way better, but we have what we have
    STRESSER_SITE: str = "https://slovnyk.ua/nagolos.php"

    def __init__(self) -> None:
        '''Initiate selenium webdriver for further crawling.'''

        op = webdriver.ChromeOptions()
        if self.SILENT:
           op.add_argument('headless')
        self.driver = webdriver.Chrome(options=op)

    def cleanup(self) -> None:
        '''Close the webdriver session.'''

        self.driver.close()

    def wait_for_result(self, retries: int = 3, timeout: int = 1) -> Optional[str]:
        '''Wait for the page to process the input and load the result text holder.'''

        while retries > 0:
            try:
                return self.driver.find_element_by_id('emph').get_attribute('textContent').strip()
            except NoSuchElementException:
                time.sleep(timeout)
                retries -= 1

        return None

    def stress(self, text: str) -> Optional[str]:
        '''Load the text stresser website, load the text there and fetch the results.'''

        self.driver.get(self.STRESSER_SITE)
        input_area = self.driver.find_element_by_tag_name('textarea')
        input_area.send_keys(text)
        submit_button = self.driver.find_element_by_xpath('//button[@type="submit"]')
        submit_button.click()
        stressed_text = self.wait_for_result()
        self.cleanup()

        return stressed_text
