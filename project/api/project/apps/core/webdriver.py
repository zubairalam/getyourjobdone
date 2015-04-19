from subprocess import Popen, PIPE

from django.conf import settings

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support.ui import WebDriverWait


# determine the WebDriver module. default to Firefox
try:
    web_driver_module = settings.SELENIUM_WEBDRIVER
except AttributeError:
    from selenium.webdriver.firefox import webdriver as web_driver_module


class CygwinFirefoxProfile(FirefoxProfile):
    @property
    def path(self):

        path = '/cygdrive/c/Program\ Files\ \(x86\)/Mozilla\ Firefox/'

        # cygwin requires to manually specify Firefox path a below:
        # PATH=/cygdrive/c/Program\ Files\ \(x86\)/Mozilla\ Firefox/:$PATH
        try:
            proc = Popen(['cygpath', '-d', path], stdout=PIPE, stderr=PIPE)
            stdout, stderr = proc.communicate()
            path = stdout.split('\n', 1)[0]

        except OSError:
            print('No cygwin path found')

        return path


class CustomWebDriver(web_driver_module.WebDriver):
    """
    Our own WebDriver with some helpers added.
    """
    firefoxProfile = CygwinFirefoxProfile()

    ## Disable CSS
    firefoxProfile.set_preference('permissions.default.stylesheet', 2)
    ## Disable images
    firefoxProfile.set_preference('permissions.default.image', 2)
    ## Disable Flash
    firefoxProfile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')



    def find_css(self, css_selector):
        '''
        Shortcut to find elements by CSS. Returns either a list or singleton
        '''
        elems = self.find_elements_by_css_selector(css_selector)
        found = len(elems)
        if found == 1:
            return elems[0]
        elif not elems:
            raise NoSuchElementException(css_selector)
        return elems

    def wait_for_css(self, css_selector, timeout=7):
        '''
        Shortcut for WebDriverWait
        '''
        try:
            return WebDriverWait(self, timeout).until(lambda driver: driver.find_css(css_selector))
        except:
            self.quit()