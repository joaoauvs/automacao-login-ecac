import locale
import logging
import os
import time
from datetime import datetime, timedelta
from pathlib import Path


class Log():
    """
    Classe para criação e gerenciamento de arquivos de log.

    Attributes:
        path (str): Caminho do diretório onde o arquivo de log será armazenado.
        data_atual (str): Data atual no formato "dd-mm-yyyy".
        filename (str): Nome do arquivo de log, baseado na data atual.
    """
    
    def __init__(self):
        """
        Inicializa a instância da classe Log, define os atributos e gera o arquivo de log.

        Args:
            path (str): Caminho do diretório onde o arquivo de log será armazenado.
        """
        self.path = os.path.join(os.getcwd(), 'logs/')
        self.data_atual = datetime.now().strftime("%d-%m-%Y")
        self.filename = self.data_atual +'.log'
        self.generate_log()

    def generate_log(self):
        """
        Configura e gera o arquivo de log. Se o diretório especificado em 'path' não existir, ele será criado.
        """
        if self.path is not None:
            Path(self.path).mkdir(parents=True, exist_ok=True)
        logging.basicConfig(
            filename=self.path + self.filename, 
            filemode='w',
            encoding='utf-8',
            level=logging.INFO,
            format="{asctime} - {levelname} - {funcName}:{lineno} - {message}",
            datefmt="%d/%m/%Y %H:%M:%S",
            style='{'
        )

    def delete_log(self):
        """
        Exclui o arquivo de log.
        """
        os.remove(self.path + self.filename)