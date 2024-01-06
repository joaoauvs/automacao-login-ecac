from selenium.webdriver.common.by import By


class Locators():
    
    URL_ECAC = "https://cav.receita.fazenda.gov.br/autenticacao/login"
    URL_FRAME_DCTF = "https://cav.receita.fazenda.gov.br/Servicos/ATSPO/DCTF/Consulta/Abrir.asp"
    URL_WINDOW_COPIA_ARQUIVO = "https://cav.receita.fazenda.gov.br/Servicos/ATSDR/DECWEB/dadosdec.asp?Declaracao=DCTF"
    URL_LOGOUT = "https://cav.receita.fazenda.gov.br/autenticacao/Login/LogoutGovBR"
    
    # --- LOGIN GOV BR ---

    IMAGE_GOV = (By.XPATH, "//*[@id='login-dados-certificado']/p[2]/input")
    BUTTON_CERTIFICADO_DIGITAL = (By.XPATH, "//*[@id='login-certificate']")
    MSG_ERROR_LOGIN = (By.CLASS_NAME, "login-caixa-erros-validacao")
    FORM_LOGIN = (By.ID, "loginData")
    
    # -- LOGOUT --

    BTN_LOGOUT = ("#sairSeguranca")