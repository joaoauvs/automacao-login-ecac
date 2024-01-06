import logging
import os
import smtplib
import socket
from datetime import datetime
from email.message import EmailMessage
from fnmatch import fnmatch
from os import listdir
from os.path import basename, isfile, join


class Email:
    def __init__(self, process: str):
        self.process = process
        self.worker = socket.gethostbyname(socket.gethostname())
        self.dir_log = f'C:\\RPA\\{self.process}\\logs\\{datetime.now().strftime("%d-%m-%Y")}.log'
        self.emailRemetente = "emailremetente"
        self.emailPassword = "emailpassword"
        self.emailFalha = "emailfail"
        self.dataAtual = datetime.today().strftime("%d/%m/%Y")

    def send_email_fail(self):
        msg = EmailMessage()
        msg["Subject"] = "{}:{} (Apresentou Erro)".format(
            self.worker, self.process.upper()
        )

        corpo_email = f"""
        Bom dia,

        Segue o Log em anexo para análise.

        Att,

        """

        msg["From"] = self.emailRemetente
        msg["To"] = self.emailFalha

        msg.set_content(str(corpo_email))
        msg.add_attachment(open(self.dir_log, "r", encoding="utf-8").read(), filename="log.txt")
        with smtplib.SMTP_SSL("smtp.hostinger.com", 465) as smtp:
            smtp.login(self.emailRemetente, self.emailPassword)
            smtp.send_message(msg)
