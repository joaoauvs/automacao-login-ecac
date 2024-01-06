import logging
import os
import random
import re
import threading
import time
import winreg
from os import listdir, path

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys

from locators import *
from src.base import Web
from src.modules.common import attempts, time_execution, get_message


class Gov(Web):
    """
    Classe responsável por fazer o download dos arquivos do ECAC
    """

    def __init__(self, driver) -> None:

        super().__init__(driver)

    def logout_gov(self) -> None:
        """
        Função para realizar o logout no sistema ECAC.

        Raises:
            Exception: Caso ocorra algum erro durante o processo de logout.
        """
        logging.info("-> INICIANDO O LOGOUT NO ECAC! <-")
        self.navigate(url=Locators.URL_LOGOUT)

    def fazer_login_ecac(self) -> None:
        """
        Realiza o login no ECAC com certificado A1.

        Args:
            self: O objeto da classe `LoginGov`.

        Raises:
            Exception: Se houver um erro ao realizar o login.
        """
        try:
            logging.info("[ FAZENDO O LOGIN NO ECAC COM CERTIFICADO A1 ]")

            logging.info(f"Navegando para a URL: {Locators.URL_ECAC}")
            self.navigate(url=Locators.URL_ECAC)
            self.click(by_locator=Locators.IMAGE_GOV)

            if not self.assert_element_exists(by_locator=Locators.FORM_LOGIN):
                raise logging.error("Não foi possível encontrar o formulário de login!")

            logging.info("Clicando no > SEU CERTIFICADO DIGITAL <")

            self.click(by_locator=Locators.BUTTON_CERTIFICADO_DIGITAL)

            self.click_pyautogui(image=r"C:\Users\Joao\Documents\automacao-login-ecac\src\images\select-certificate.png")

            logging.info("Clicando no BUTTON > OK <")

            self.click_pyautogui_list(directory=r"C:\Users\Joao\Documents\automacao-login-ecac\src\images\button ok")

            logging.info("[ LOGIN REALIZADO COM SUCESSO NO ECAC COM CERTIFICADO A1 ]")

        except Exception as e:
            raise Exception(f"Erro ao fazer login no ECAC: {type(e).__name__}, {e.args[0]}")
