from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

def criar_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    options.binary_location = "/usr/bin/chromium"  # caminho do Chrome no container
    service = Service("/usr/bin/chromedriver")     # caminho do chromedriver no container

    driver = webdriver.Chrome(service=service, options=options)
    return driver

def buscar_posicao_furia():
    driver = criar_driver()
    try:
        driver.get('https://www.hltv.org/ranking/teams')
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ranked-team"))
        )
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        ranked_teams = soup.find_all("div", class_="ranked-team")

        for team in ranked_teams:
            team_name = team.find("span", class_="name").text.strip()
            if "FURIA" in team_name.upper():
                position = team.find("span", class_="position").text.strip().replace("#", "")
                points = team.find("span", class_="points").text.strip().replace("(", "").replace(")", "").replace("HLTV points", "").strip()
                return f"🏆 A FURIA está na posição {position}ª com {points} pontos na HLTV."

        return "😔 Não encontrei a FURIA no ranking."

    except Exception as e:
        return f"Erro ao buscar ranking: {e}"

    finally:
        driver.quit()

def buscar_top_30():
    driver = criar_driver()
    try:
        driver.get('https://www.hltv.org/ranking/teams')
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ranked-team"))
        )

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        ranked_teams = soup.find_all("div", class_="ranked-team")[:30]

        lista = []
        for team in ranked_teams:
            team_name = team.find("span", class_="name").text.strip()
            position = int(team.find("span", class_="position").text.strip().replace("#", ""))
            points = team.find("span", class_="points").text.strip().replace("(", "").replace(")", "").replace("HLTV points", "").strip()
            lista.append({
                "Posição": position,
                "Time": team_name,
                "Pontos": points
            })

        df = pd.DataFrame(lista).sort_values("Posição").reset_index(drop=True)
        return df.to_dict(orient="records")  # retorna em formato amigável à API

    except Exception as e:
        return f"Erro ao buscar Top 30: {e}"

    finally:
        driver.quit()

def buscar_lineup_furia():
    driver = criar_driver()
    try:
        driver.get('https://www.hltv.org/team/8297/furia#tab-rosterBox')
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "playerNickname"))
        )

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        players = [div.text.strip() for div in soup.select("div.playerNickname")]
        coach_tag = soup.find("div", class_="coach-name")

        coach = coach_tag.text.strip() if coach_tag else "Desconhecido"

        return players, coach

    except Exception as e:
        return [], f"Erro ao buscar lineup: {e}"

    finally:
        driver.quit()
