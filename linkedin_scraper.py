from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time
from config import email, senha # Para usar o scraper necessário contemplar essas variáveis com o login e senha do LinkedIn

def get_vagas(busca, local, paginas):
 
    data = []

    cService = Service(r'.\chromedriver.exe')
    browser = webdriver.Chrome(service = cService)
    browser.implicitly_wait(10)

    browser.get("https://www.linkedin.com/login")
    input_email = browser.find_element(By.ID, "username")
    input_email.send_keys(email)

    input_senha = browser.find_element(By.ID, "password")
    input_senha.send_keys(senha)

    btn_login = browser.find_element(By.XPATH, "//button[@type='submit']")
    btn_login.click()

    teste = True

    while teste:
        teste = int(input("Digite [0] caso tenha completado os testes de interação humana ou não tenha nenhum!"))

    for pag_num in range(1, paginas):
        url = f'https://www.linkedin.com/jobs/search/?keywords={busca}&location={local}&start={25 * (pag_num - 1)}'
        browser.get(url)
        
        time.sleep(5)

        vagas = browser.find_elements(By.CLASS_NAME, "jobs-search-results__list-item")

        for vaga in vagas:
            vaga.location_once_scrolled_into_view
            vaga.click()
            time.sleep(1)
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            try:
                vaga_titulo = soup.find("span", {"class": "job-details-jobs-unified-top-card__job-title-link"}).get_text().strip()
            except AttributeError:
                vaga_titulo = None

            try:
                vaga_detalhes = soup.find("div", {"class": "job-details-jobs-unified-top-card__primary-description-without-tagline"}).get_text().strip("\n").split('·')
                vg_detalhes_strip = []
                for vgds in vaga_detalhes:
                    vgds = vgds.strip()
                    vg_detalhes_strip.append(vgds)
                vaga_detalhes = vg_detalhes_strip
            except AttributeError:
                vaga_detalhes = None
            
            try:
                vaga_tipo = soup.find("li", {"class": "job-details-jobs-unified-top-card__job-insight"}, "span").get_text().strip().split('.')
                vg_tipo_strip = []
                for vgt in vaga_tipo:
                    vgt = vgt.strip("\n")
                    vg_tipo_strip.append(vgt)
                vaga_tipo = vg_tipo_strip
            except AttributeError:
                vaga_tipo = None

            try:
                vaga_descricao = soup.find("div", {"class": "jobs-description-content__text"}).find("span").get_text().strip()
            except AttributeError:
                vaga_descricao = None

            data.append({
                'Titulo da vaga': vaga_titulo,
                'Detalhe da vaga': vaga_detalhes,
                'Tipo da vaga': vaga_tipo,
                "Descrição da vaga": vaga_descricao
            })
    browser.quit()        
    return pd.DataFrame(data)

