from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from config import urls, time_altered, user_agents
from seleniumbase import Driver
from urllib import error
import pyautogui as pg
import logging

class super_class:
    def __init__(self):
        self.driver = None
        
    def web_driver(self):
        self.driver = Driver(uc=True,incognito=True, no_sandbox=True,
        headless=False, 
        chromium_arg="--binary-location=/usr/local/bin/ublockdn,--block-new-web-contents,--disable-popup-blocking=false")

        self.driver.execute_cdp_cmd(
        f"Network.setUserAgentOverride", 
        {"userAgent":user_agents.useragent})
        return self.driver

class sub_class(super_class):
    def main(self):
        global val
        try:
            for i in urls.url_list_batbiz:
                val = i
                self.driver.get(val)
                print('indi url get request')
                try:
                    WDW(self.driver,10).until(EC.url_to_be(val))
                except (error.HTTPError):
                    pass
                print('url_match')
                time_altered.time_adjusted(0.5)
                pg.rightClick(x=687, y=293)
                time_altered.time_adjusted(0.5)
                pg.press('down')
                pg.press('down')
                pg.press('enter')
                time_altered.time_adjusted(1)
                pg.press('enter')
                time_altered.time_adjusted(1)
                pg.press('enter')
                print('download')
        except error.HTTPError as err:
            logging.error(err)

if __name__ == "__main__":
    try:
        instantiate = sub_class()
        instantiate.web_driver()
        instantiate.main()
    except KeyboardInterrupt:
        print('gracefully exiting...')