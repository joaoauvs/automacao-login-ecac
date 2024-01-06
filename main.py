import asyncio
import json
import logging
import sys

from login_gov import Gov
from src.modules.common import attempts, time_execution, get_message
from src.modules.email import Email
from src.modules.log import Log
from src.web.webdriver import Browser, WebDriver


class Bot:

    PROCESS = "AUTOMACAO-LOGIN-ECAC"

    @time_execution
    @attempts(max_attempts=2)
    def main(self):
        """Executa o bot."""
        try:
            logging.info(f"📝 INICIANDO O PROCESSO ...")
            navegador = WebDriver.get_navegador(Browser.UNDETECTED_CHROME, headless=False)
            ecac = Gov(navegador)
            ecac.fazer_login_ecac()
            logging.info(f"[✔] PROCESSO FINALIZADO COM SUCESSO!")
        except RuntimeError as e:
            logging.warning(f"[FALHA START NAVEGADOR]: {type(e).__name__}, {e.args[0]}")
        finally:
            ecac.logout_gov()
            navegador.quit()


if __name__ == "__main__":
    try:
        Log()

        Bot().main()
        
    except Exception as e:
        logging.warning("Erro ao executar o bot: " + str(e))
        Email(process=Bot.PROCESS).send_email_fail()
