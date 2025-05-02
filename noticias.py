from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options


def criar_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--remote-debugging-port=9222')
    options.binary_location = "/usr/bin/chromium-browser"  # Render usa chromium-browser

    service = Service("/usr/bin/chromedriver")  # funciona se chromedriver estiver neste caminho
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def buscar_noticias():
    driver = criar_driver()
    try:
        driver.get('https://www.hltv.org/')

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "newsline"))
        )

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        noticias = soup.select('.newsline.article')[:10]

        lista_noticias = []
        for noticia in noticias:
            titulo_tag = noticia.select_one('.newstext')
            if titulo_tag:
                titulo = titulo_tag.get_text(strip=True)
                link = "https://www.hltv.org" + noticia.get("href", "")
                lista_noticias.append({"titulo": titulo, "link": link})

        return lista_noticias

    except Exception as e:
        return f"Erro ao buscar notícias: {e}"

    finally:
        driver.quit()
