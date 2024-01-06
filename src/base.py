import logging
import os
import shutil
import time
from typing import Optional, Tuple, Union

import pyautogui
import win32gui
from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,
                                        NoSuchFrameException, TimeoutException)
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Web:
    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(self.driver, self.timeout)

    def navigate(self, url: str):
        """
        Navega até a URL fornecida e maximiza a janela do navegador.

        Args:
            url (str): A URL para navegar.
        """
        self.driver.get(url)
        self.driver.maximize_window()

    def focus_window_app(self, app: str) -> bool:
        """
        Foca a janela do aplicativo com o título fornecido.

        Args:
            app (str): O título da janela do aplicativo.

        Returns:
            bool: Retorna True se a janela for encontrada e focada com sucesso, caso contrário, retorna False.
        """
        window = win32gui.FindWindow(None, app)
        if window:
            win32gui.BringWindowToTop(window)
            return True
        else:
            raise Exception(f"Janela não encontrada: {app}")

    ######## JAVA SCRIPT ########

    def assert_js_exists(self, selector: str, timeout: int = 15) -> bool:
        """
        Verifica a existência de um elemento utilizando um seletor CSS através de JavaScript.

        Args:
            selector (str): O seletor CSS do elemento a ser verificado.
            timeout (int, opcional): O tempo máximo (em segundos) para aguardar o elemento. Por padrão é 15.

        Returns:
            bool: Retorna True se o elemento for encontrado dentro do tempo limite.

        Raises:
            Exception: Se o elemento não for encontrado dentro do tempo limite.
        """
        for _ in range(timeout):
            js_expression = f"document.querySelector('{selector}')"
            result = self.driver.execute_script(f"return !!({js_expression});")
            if result:
                return True
            time.sleep(1)
        return False

    def execute_js(self, query: str) -> None:
        """
        Executa um comando JavaScript no navegador.

        Args:
            query (str): O comando JavaScript a ser executado.
        """
        self.driver.execute_script(query)

    def execute_js_return(self, query: str):
        """
        Executa um comando JavaScript no navegador e retorna o resultado.

        Args:
            query (str): O comando JavaScript a ser executado.

        Returns:
            O resultado da execução do comando JavaScript.
        """
        return self.driver.execute_script(query)

    def set_text_js(self, query: str, value: str) -> bool:
        """
        Define o texto de um elemento utilizando JavaScript.

        Args:
            query (str): A query do elemento a ser buscado.
            value (str): O valor a ser definido no elemento.

        Returns:
            bool: True se o texto foi definido com sucesso, False caso contrário.
        """
        self.driver.execute_script(f"document.querySelector('{query}').value = '{value}';")
        return True

    def get_text_js(self, query: str) -> str:
        """
        Obtém o texto de um elemento utilizando JavaScript.

        Args:
            query (str): A consulta do elemento a ser buscado.

        Returns:
            str: O texto do elemento.

        Raises:
            Exception: Se ocorrer um problema ao obter o texto do elemento.
        """
        try:
            return self.driver.execute_script(f"return document.querySelector('{query}').textContent")
        except Exception as e:
            raise Exception(f"Não foi possível obter o texto do elemento com a consulta: {query}. Erro: {e}")

    def click_js(self, query: str) -> None:
        """
        Clica em um elemento usando JavaScript.

        Args:
            query (str): O seletor CSS do elemento a ser clicado.

        Raises:
            Exception: Se ocorrer um problema ao clicar no elemento.
        """
        try:
            self.driver.execute_script(f"document.querySelector('{query}').click()")
        except Exception as e:
            raise Exception(f"Não foi possível clicar no elemento com a consulta: {query}. Erro: {e}")

    def click_wait_js(self, selector: str, timeout: int = 15) -> None:
        """
        Clica em um elemento utilizando um seletor CSS através de JavaScript e aguarda até que o elemento seja clicado com sucesso.

        Args:
            selector (str): O seletor CSS do elemento a ser clicado.
            timeout (int, opcional): O tempo máximo (em segundos) para aguardar o clique ser efetuado com sucesso. Por padrão é 15.

        Raises:
            Exception: Se o elemento não for clicado com sucesso dentro do tempo limite.
        """
        js_click = f"document.querySelector('{selector}').click();"
        for _ in range(timeout):
            try:
                self.driver.execute_script(js_click)
                return True
            except Exception as e:
                time.sleep(1)
        raise Exception(f"Não foi possível clicar no elemento com o seletor: {selector}.")

    ######## ELEMENTS XPATH ########

    def assert_element_exists(self, by_locator: Tuple[str, str], ensure_visible: bool = True) -> bool:
        """
        Verifica se o elemento existe e é visível (se especificado) na página.

        Args:
            by_locator (Tuple[str, str]): Uma tupla contendo o tipo de localizador e o valor do localizador.
            ensure_visible (bool, opcional): Se True, verifica a visibilidade do elemento. Por padrão é True.

        Returns:
            bool: Retorna True se o elemento for encontrado e visível (se especificado), caso contrário, retorna False.
        """
        try:
            condition = EC.visibility_of_element_located(by_locator) if ensure_visible else EC.presence_of_element_located(by_locator)
            return bool(self.wait.until(condition))
        except (NoSuchElementException, TimeoutException):
            return False

    def set_text(self, by_locator: Tuple[str, str], text: str) -> bool:
        """
        Envia o texto especificado para o elemento encontrado pelo localizador.

        Args:
            by_locator (Tuple[str, str]): O localizador do elemento que se deseja enviar o texto.
            text (str): O texto a ser enviado para o elemento.

        Returns:
            bool: Retorna True se o texto foi enviado com sucesso, caso contrário retorna False.

        Raises:
            Exception: Se ocorrer um problema ao enviar o texto para o elemento.
        """
        if self.assert_element_exists(by_locator):
            web_element = self.driver.find_element(*by_locator)
            web_element.clear()
            web_element.send_keys(text)
            return True
        else:
            raise Exception(f"Não foi possível digitar no elemento: {by_locator}")

    def set_text_with_action(self, by_locator: Tuple[str, str], text: str, key_action: str = 'enter') -> None:
        """
        Envia o texto especificado para o elemento encontrado pelo localizador e pressiona a tecla especificada (Enter ou Tab).

        Args:
            by_locator (Tuple[str, str]): O localizador do elemento que se deseja enviar o texto.
            text (str): O texto a ser enviado para o elemento.
            key_action (str, opcional): A tecla a ser pressionada após o envio do texto. Padrão é 'enter'.
        
        Raises:
            NoSuchElementException: Se o elemento não for encontrado.
            ValueError: Se a tecla especificada não for 'enter' ou 'tab'.
        """
        if self.assert_element_exists(by_locator):
            web_element = self.driver.find_element(*by_locator)
            web_element.clear()
            web_element.send_keys(text)

            if key_action == 'enter':
                web_element.send_keys(Keys.ENTER)
            elif key_action == 'tab':
                web_element.send_keys(Keys.TAB)
            else:
                raise ValueError(f"Ação de tecla inválida: {key_action}. Deve ser 'enter' ou 'tab'.")
        else:
            raise NoSuchElementException(f"Elemento com localizador: {by_locator} não foi encontrado.")

    def get_text(self, by_locator: Tuple[str, str]) -> str:
        """
        Obtém o texto de um elemento da página a partir de um localizador.

        Args:
            by_locator (Tuple[str, str]): Uma tupla contendo o tipo de localizador e o valor do localizador.

        Returns:
            str: O texto do elemento.
        
        Raises:
            NoSuchElementException: Se o elemento não for encontrado.
        """
        if self.assert_element_exists(by_locator):
            return self.driver.find_element(*by_locator).text
        raise NoSuchElementException(f"Elemento com localizador: {by_locator} não foi encontrado.")

    def is_clickable(self, by_locator: Tuple[str, str]) -> bool:
        """
        Verifica se o elemento é clicável.

        Args:
            by_locator (Tuple[str, str]): Uma tupla contendo o tipo de localizador e o valor do localizador.

        Returns:
            bool: Retorna True se o elemento for clicável, caso contrário retorna False.

        Raises:
            Exception: Se ocorrer um problema ao verificar se o elemento é clicável.
        """
        if self.wait.until(EC.element_to_be_clickable(by_locator)):
            return True
        raise Exception(f"Elemento não é clicável: {by_locator}")

    def click(self, by_locator: Tuple[str, str]) -> bool:
        """
        Clica em um elemento na página.

        Args:
            by_locator (Tuple[str, str]): Uma tupla contendo o tipo de localizador e o valor do localizador.

        Returns:
            bool: Retorna True se o clique for realizado com sucesso.
        
        Raises:
            Exception: Se ocorrer um problema ao clicar no elemento.
        """
        if self.assert_element_exists(by_locator):
            element = self.wait.until(EC.element_to_be_clickable(by_locator))
            element.click()
            return True
        raise Exception(f"Não foi possível clicar no elemento: {by_locator}")

    def click_element_tag_text(self, by_locator: Tuple[str, str], tag: str, text: str) -> bool:
        """
        Clica no elemento que contém a tag e o texto especificados.

        Args:
            by_locator (Tuple[str, str]): O localizador do elemento que se deseja clicar.
            tag (str): A tag HTML do elemento que se deseja clicar.
            text (str): O texto contido no elemento que se deseja clicar.

        Returns:
            bool: Retorna True se o elemento foi clicado com sucesso, caso contrário retorna False.
        
        Raises:
            Exception: Se ocorrer um problema ao clicar no elemento.
        """
        if self.assert_element_exists(by_locator):
            web_element = self.driver.find_element(*by_locator)
            rows = web_element.find_elements(By.TAG_NAME, tag)
            for row in rows:
                if row.text == text:
                    row.click()
                    return True
            return False
        raise Exception(f"Não foi possível clicar no elemento: {by_locator}")

    def click_text(self, by_locator: Tuple[str, str], text: str) -> bool:
        """
        Clica no elemento que contém o localizador e o texto especificados.

        Args:
            by_locator (Tuple[str, str]): O localizador do elemento que se deseja clicar.
            text (str): O texto contido no elemento que se deseja clicar.

        Returns:
            bool: Retorna True se o elemento foi clicado com sucesso, caso contrário retorna False.
        
        Raises:
            Exception: Se ocorrer um problema ao clicar no elemento.
        """
        web_element = self.driver.find_element(*by_locator)
        if text in web_element.text:
            web_element.click()
            return True
        raise Exception(f"Não foi possível clicar no elemento com texto: {text} e localizador: {by_locator}")

    def access_iframe(self, by_locator: Tuple[str, str]) -> None:
        """
        Acessa um iframe utilizando o localizador especificado.
        """
        iframe = EC.visibility_of_element_located(by_locator)
        self.driver.switch_to.frame(self.wait.until(iframe))

    def close_iframe(self) -> None:
        """
        Sai do iframe atual e retorna ao contexto principal.
        """
        self.driver.switch_to.default_content()

    def double_click(self, by_locator: Tuple[str, str]) -> bool:
        """
        Realiza um duplo clique no elemento especificado.

        Args:
            by_locator (Tuple[str, str]): Localizador do elemento no qual o duplo clique será realizado.

        Returns:
            bool: Retorna True se o duplo clique foi realizado com sucesso, caso contrário retorna False.
        """
        element = self.driver.find_element(*by_locator)
        ActionChains(self.driver).double_click(element).perform()
        return True

    def get_attribute(self, by_locator: Tuple[str, str], attribute: str) -> Union[str, None]:
        """
        Obtém o valor de um atributo do elemento especificado.

        Args:
            by_locator (Tuple[str, str]): Uma tupla contendo o tipo de localizador e a string de localização do elemento.
            attribute (str): O nome do atributo que se deseja obter o valor.

        Returns:
            Union[str, None]: Retorna o valor do atributo se o elemento for encontrado, caso contrário retorna None.
        """
        if self.assert_element_exists(by_locator):
            return self.wait.until(EC.visibility_of_element_located(by_locator)).get_attribute(attribute)
        raise Exception(f"Não foi possível obter o atributo {attribute} do elemento: {by_locator}")

    def wait_element(self, by_locator: Tuple[str, str], text: Optional[str] = None, timeout: int = 15):
        """
        Aguarda até que o elemento seja encontrado utilizando o localizador especificado. 
        Se um texto for fornecido, aguarda até que o texto esteja presente no elemento.

        Args:
            by_locator (Tuple[str, str]): O localizador do elemento a ser encontrado ou verificado.
            text (str, opcional): O texto que se espera encontrar no elemento. Se não for fornecido, apenas verifica a presença do elemento.
            timeout (int, opcional): Tempo máximo de espera (em segundos) antes de lançar uma exceção. Padrão é 15.

        Returns:
            bool: Retorna True se o elemento (e possivelmente o texto) for encontrado, False caso contrário.

        Raises:
            Exception: Se ocorrer um problema ao encontrar o elemento ou o texto.
        """
        try:
            if text:
                element = EC.text_to_be_present_in_element(by_locator, text)
            else:
                element = EC.visibility_of_element_located(by_locator)

            WebDriverWait(self.driver, timeout).until(element)
        except (TimeoutError, NoSuchElementException) as e:
            raise Exception(f"Erro ao esperar pelo elemento {by_locator}. Erro: {e}")

    def scroll_to_element(self, by_locator: Tuple[str, str]) -> None:
        """
        Essa função desloca a página até que o elemento especificado seja exibido na tela.

        Args:
            by_locator (Tuple[str, str]): O localizador do elemento que se deseja exibir na tela.
        """
        element = self.driver.find_element(*by_locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def alert_exists(self) -> bool:
        """
        Verifica se um alerta está presente na página.
        """
        try:
            self.wait.until(EC.alert_is_present())
            return True
        except:
            return False

    def alert_accept(self) -> bool:
        """
        Aceita um alerta JavaScript.
        """
        if self.alert_exists():
            self.driver.switch_to.alert.accept()
            return True
        return False

    def alert_dismiss(self) -> bool:
        """
        Descarta o alerta presente na página.
        """
        if self.alert_exists():
            self.driver.switch_to.alert.dismiss()
            return True
        return False

    def alert_text(self) -> Optional[str]:
        """
        Essa função verifica se um alerta está presente na página e retorna o texto contido nele.
        """
        if self.alert_exists():
            return self.driver.switch_to.alert.text
        return None

    def close_windows(self, handle) -> None:
        """
        Fecha todas as janelas abertas no navegador, exceto a janela com o identificador fornecido.

        Args:
            handle (str): O identificador da janela que não deve ser fechada.
        """
        handles = self.driver.window_handles
        for handle_current in handles:
            if handle_current != handle:
                self.driver.switch_to.window(handle_current)
                self.driver.close()
        self.driver.switch_to.window(handle)

    def switch_to_window(self, handle) -> None:
        """
        Troca a janela ativa do navegador para a janela especificada.

        Args:
            handle (str): O identificador da janela que se deseja ativar.

        Raises:
            ValueError: Se o identificador da janela não for encontrado.
        """
        if handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)
        else:
            raise ValueError(f"Window handle {handle} not found.")

    ######## PYAUTOGUI ########

    def click_pyautogui(self, image: str, matching: float = 0.8, timeout: int = 10, max_attempts: int = 2) -> bool:
        """
        Clica em um elemento na tela usando PyAutoGUI com base na imagem fornecida.

        Args:
            image (str): O caminho para a imagem do elemento a ser clicado.
            matching (float, optional): Valor de confiança para correspondência de imagem. Padrão é 0.8.
            timeout (int, optional): Tempo limite em segundos para tentar encontrar o elemento na tela. Padrão é 10.

        Returns:
            bool: Retorna True se o clique for realizado com sucesso, caso contrário retorna False.

        Raises:
            Exception: Se ocorrer um problema ao clicar no elemento.
        """
        for attempt in range(max_attempts):
            try:
                image_location = pyautogui.locateCenterOnScreen(image, confidence=matching)
                if image_location:
                    pyautogui.click(image_location)
                    return True
                else:
                    time.sleep(timeout)
            except Exception as e:
                if attempt == max_attempts:
                    raise Exception(f"Não foi possível clicar no elemento: {image}. Erro: {e}")
                time.sleep(2)
        raise Exception(f"Não foi possível clicar no elemento: {image}")

    def click_pyautogui_list(self, directory: str, matching: float = 0.7) -> bool:
        """
        Clica no primeiro elemento encontrado na lista de imagens do diretório especificado usando o PyAutoGUI.

        Args:
            directory (str): Caminho do diretório que contém as imagens para realizar o clique.
            matching (float, optional): Confiança mínima para o reconhecimento de imagem. Padrão é 0.7.

        Returns:
            bool: Retorna True se o clique foi realizado com sucesso, caso contrário retorna False.
        
        Raises:
            Exception: Se ocorrer um problema ao clicar no elemento.
        """
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):  # Considerando apenas imagens
                    try:
                        if self.click_pyautogui(os.path.join(root, file), matching):
                            return True
                    except Exception as e:
                        print(f"Erro ao clicar na imagem {file}: {e}")
        raise Exception(f"Não foi possível clicar em nenhum elemento das imagens no diretório: {directory}")

    ######## MOUSE E KEYS ########

    def click_mouse(self, x: int, y: int) -> None:
        """
        Clica na posição especificada do mouse.

        Args:
            x (int): A coordenada X do mouse.
            y (int): A coordenada Y do mouse.
        """
        pyautogui.click(x, y)

    def press_key(self, key: str) -> None:
        """
        Pressiona a tecla especificada.

        Args:
            key (str): A tecla a ser pressionada.
        """
        pyautogui.press(key)

    def press_keys(self, keys: str) -> None:
        """
        Pressiona as teclas especificadas.

        Args:
            keys (str): As teclas a serem pressionadas.
        """
        pyautogui.hotkey(keys)

    def press_keys_list(self, keys: list) -> None:
        """
        Pressiona as teclas especificadas.

        Args:
            keys (list): As teclas a serem pressionadas.
        """
        pyautogui.hotkey(*keys)

    def press_key_down(self, key: str) -> None:
        """
        Pressiona a tecla especificada.

        Args:
            key (str): A tecla a ser pressionada.
        """
        pyautogui.keyDown(key)

    def press_key_up(self, key: str) -> None:
        """
        Pressiona a tecla especificada.

        Args:
            key (str): A tecla a ser pressionada.
        """
        pyautogui.keyUp(key)
