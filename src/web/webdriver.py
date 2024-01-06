import logging
import os
from enum import Enum
from functools import wraps

import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from .driveroptions import DriverOptions


class Browser(Enum):
    CHROME = "chrome"
    UNDETECTED_CHROME = "undetected_chrome"
    FIREFOX = "firefox"
    EDGE = "edge"


class WebDriver(DriverOptions):
    """
    Classe responsável por inicializar e encerrar os drivers da Web do Selenium para Chrome, Firefox e Edge.
    """

    def __init__(self, browser, headless=False, download_folder_path=None, **kwargs):
        super().__init__(download_folder_path=download_folder_path)
        self._headless = headless
        self.browser = Browser(browser)
        self._kwargs = kwargs

    @classmethod
    def get_navegador(cls, browser, headless=False, download_folder_path=None, **kwargs):
        try:
            instance = cls(browser, headless=headless, download_folder_path=download_folder_path, **kwargs)
            browser_methods = {
                Browser.CHROME: instance.get_chrome_driver,
                Browser.UNDETECTED_CHROME: instance.get_undetected_chrome,
                Browser.FIREFOX: instance.get_firefox_driver,
                Browser.EDGE: instance.get_edge_driver,
            }
            if instance.browser not in browser_methods:
                raise RuntimeError(f"Não foi possível iniciar o navegador {browser}.")
            return browser_methods[instance.browser]()
        except:
            raise RuntimeError(f"Não foi possível iniciar o navegador {browser}.")

    def configure_browser_options(self, browser_options):
        """
        Configura as opções do navegador.
        """
        browser_options.headless = self._headless
        for key, value in self._kwargs.items():
            setattr(browser_options, key, value)

    def get_chrome_driver(self):
        """
        Inicializa e retorna um driver Chrome com as opções configuradas.
        """
        chrome_options = self.chrome()
        self.configure_browser_options(chrome_options)
        chrome_service = ChromeService(executable_path=ChromeDriverManager().install(), log_path=os.path.devnull)
        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        driver.maximize_window()
        return driver

    def get_undetected_chrome(self):
        """
        Inicializa e retorna um driver Chrome não detectável com as opções configuradas.
        """
        chrome_options = self.undetectable_chrome()
        self.configure_browser_options(chrome_options)
        chrome_options.add_argument("--kiosk-printing")
        driver = uc.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)
        driver.maximize_window()
        return driver

    def get_firefox_driver(self):
        """
        Inicializa e retorna um driver do Firefox com as opções configuradas.
        """
        firefox_options = self.firefox()
        self.configure_browser_options(firefox_options)
        firefox_service = FirefoxService(executable_path=GeckoDriverManager().install())
        driver = webdriver.Firefox(service=firefox_service, options=firefox_options)
        driver.maximize_window()
        return driver

    def get_edge_driver(self):
        """
        Inicializa e retorna um driver Edge com as opções configuradas.
        """
        edge_options = self.edge()
        self.configure_browser_options(edge_options)
        driver = webdriver.Edge(service=EdgeService(), options=edge_options)
        driver.maximize_window()
        return driver
