import json
import os

import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


class DriverOptions:
    DEFAULT_LANGUAGE_CODE = 'pt-BR'

    def __init__(self, download_folder_path=None):
        self.download_folder_path = download_folder_path

    def _default(self):
        if self.download_folder_path is not None:
            os.makedirs(self.download_folder_path, exist_ok=True)

    def _common_chrome_prefs(self):
        settings = {
            "recentDestinations": [{
                "id": "Save as PDF",
                "origin": "local",
                "account": "",
            }],
            "selectedDestinationId": "Save as PDF",
            "version": 2,
            "isHeaderFooterEnabled": False,
            "isInkEnabled": True,
            "isLandscapeEnabled": True,
            "scalingType": 2,
        }

        prefs = {
            "profile.default_content_settings.popups": 0,
            "printing.print_preview_sticky_settings.appState": json.dumps(settings),
            "savefile.default_directory": self.download_folder_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "download.default_directory": self.download_folder_path,
            "safebrowsing.enabled": True,
            "javascript.enabled": False,
            "privacy.trackingprotection.enabled": True,
            "privacy.trackingprotection.pbmode.enabled": True,
            "intl.accept_languages": self.DEFAULT_LANGUAGE_CODE,
            "profile.content_settings.exceptions.automatic_downloads.*.setting": 1,
            "profile.default_content_setting_values.geolocation": 2,
        }
        return prefs

    def _set_common_chrome_arguments(self, options):
        self._default()

        arguments = [
            '--disable-infobars',
            '--disable-popup-blocking',
            '--no-sandbox',
            '--disable-cache',
            '--ignore-certificate-errors',
            '--ignore-ssl-errors',
            '--disable-extensions',
            '--disable-notifications',
            '--force-dark-mode',
            '--lang=pt-BR',
            '--disable-cookies',
            '--remote-debugging-port=0',
            '--no-first-run',
            '--no-default-browser-check',
            '--disable-background-networking',
            '--disable-background-timer-throttling',
            '--disable-client-side-phishing-detection',
            '--disable-default-apps',
            '--disable-hang-monitor',
            '--disable-prompt-on-repost',
            '--disable-syncdisable-translate',
            '--metrics-recording-only',
            '--safebrowsing-disable-auto-update',
            '--disable-dev-shm-usage',
            '--disable-blink-features=AutomationControlled',
            '--enable-geolocation',
            '--disable-notifications',
        ]

        for arg in arguments:
            options.add_argument(arg)

        options.add_experimental_option('prefs', self._common_chrome_prefs())
        options.add_argument('--kiosk-printing')
        return options

    def chrome(self):
        options = ChromeOptions()
        options.add_argument('--log-level=3')
        options.add_argument('--silent')
        options.page_load_strategy = 'normal'
        return self._set_common_chrome_arguments(options)

    def undetectable_chrome(self):
        options = uc.ChromeOptions()
        return self._set_common_chrome_arguments(options)

    def firefox(self):
        options = FirefoxOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-infobars")
        options.add_argument("--window-position=1920,0")
        options.add_argument("--start-maximized")
        return options

    def edge(self):
        options = EdgeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-popup-blocking')
        options.add_argument("--start-maximized")
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-cookies')
        options.add_argument('--no-user-gestures')
        options.add_argument('--disable-sync')
        options.add_argument('--incognito')
        options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
        return options
