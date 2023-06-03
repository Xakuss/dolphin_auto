from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import json
import csv


def click_button(driver, button) -> None:
    "нажатие на кнопку"
    wait = WebDriverWait(driver, 10)
    next_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, button)))
    ActionChains(driver).move_to_element(next_button).click().perform()


def get_list_id(token: str) -> list:
    "получения листа с айдишниками"
    get_requests = requests.get("https://anty-api.com/browser_profiles", headers={
        'Authorization': token}).text
    return [i["id"] for i in json.loads(get_requests)["data"]]


def get_webdriver(id: int):
    "Получение драйвера"
    # EXTENSION_PATH = 'C:\\Users\\Zver\\pythonProject1\\chromedriver\\10.28.3_0.crx'
    url = f"http://localhost:3001/v1.0/browser_profiles/{id}/start?automation=1"
    response = requests.request("GET", url)
    port = json.loads(response.content).get("automation").get("port")
    options = webdriver.ChromeOptions()
    options.debugger_address = f"127.0.0.1:{port}"
    # options.add_extension(EXTENSION_PATH)
    driver = webdriver.Chrome(executable_path="chromedriver.exe",
                              options=options)
    return driver


def twitter_auth(driver, login: str, password: str, reserve_mail: str) -> None:
    "Заходит в твиттер"
    wait = WebDriverWait(driver, 10)
    driver.get("https://twitter.com/i/flow/login")
    sleep(2)
    driver.find_element(By.NAME,
                        "text").send_keys(login)
    sleep(1)
    click_button(driver,
                 "div[class='css-18t94o4 css-1dbjc4n r-sdzlij r-1phboty r-rs99b7 r-ywje51 r-usiww2 r-2yi16 r-1qi8awa r-1ny4l3l r-ymttw5 r-o7ynqc r-6416eg r-lrvibr r-13qz1uu'")
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "Input[type='password']"))).send_keys(password)
    click_button(driver,
                 "div[class = 'css-18t94o4 css-1dbjc4n r-sdzlij r-1phboty r-rs99b7 r-19yznuf r-64el8z r-1ny4l3l r-1dye5f7 r-o7ynqc r-6416eg r-lrvibr']")
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "Input[type='email']"))).send_keys(reserve_mail)
    click_button(driver,
                 "div[class = 'css-18t94o4 css-1dbjc4n r-sdzlij r-1phboty r-rs99b7 r-19yznuf r-64el8z r-1ny4l3l r-1dye5f7 r-o7ynqc r-6416eg r-lrvibr']")


def work_witch_metamask(driver, seed_phrase: str, password: str) -> None:
    "заходит в метамаск"
    wait = WebDriverWait(driver, 10)
    driver.get("chrome-extension://cfkgdnlcieooajdnoehjhgbmpbiacopjflbjpnkm/home.html#initialize/welcome")
    for i in ["button[class='button btn--rounded btn-primary first-time-flow__button'",
              "button[class='button btn--rounded btn-primary first-time-flow__button'",
              "button[class='button btn--rounded btn-primary page-container__footer-button'"]:
        click_button(driver, i)
    gen = 0
    if len(seed_phrase.split()) == 12:
        for i in seed_phrase.split():
            driver.find_element(By.CSS_SELECTOR, f"Input[id='import-srp__srp-word-{gen}']").send_keys(i)
            gen += 1
    else:
        raise ValueError("12 слов, проверь")
    driver.find_element(By.CSS_SELECTOR, "Input[id='password']").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "Input[id='confirm-password']").send_keys(password)
    for i in ["Input[id='create-new-vault__terms-checkbox']", "button[type='submit']"]:
        next_button_1 = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, i)))
        ActionChains(driver).move_to_element(next_button_1).click().perform()


def add_network(driver, Name: str, RPC_URL, ID: str, symbol: str, block_url: str):
    "для удобства экономии места для каждой сети отдельно"
    sleep(2)
    for i in ["div[role='button']", "button[role='button']"]:
        click_button(driver, i)
        sleep(2)
    for (i, j) in zip(driver.find_elements(By.CSS_SELECTOR, "[class='form-field__input']"), [Name, RPC_URL, ID, symbol,
                                                                                             block_url]):
        i.send_keys(j)
    sleep(2)
    click_button(driver, "button[class='button btn--rounded btn-primary']")


def add_networks_to_metamask(driver, password: str) -> None:
    "добавление сетей в метамск"
    driver.get("chrome-extension://cfkgdnlcieooajdnoehjhgbmpbiacopjflbjpnkm/home.html#unlock")
    sleep(1)
    driver.find_element(By.CSS_SELECTOR, "Input[id='password']").send_keys(password)
    click_button(driver, "button[role='button']")
    click_button(driver, "button[class='button btn--rounded btn-primary']")
    click_button(driver,
                 "button[class='button btn--rounded btn-secondary first-time-flow__button']")
    sleep(10)
    add_network(driver, "Polygon Mainnet", "https://rpc-mainnet.maticvigil.com/", "137", "MATIC",
                "https://polygonscan.com/")
    add_network(driver, "Arbitrum One", "https://arb1.arbitrum.io/rpc", "42161", "AETH", "https://arbiscan.io")
    add_network(driver, "Optimism", "https://mainnet.optimism.io", "10", "ETH", "https://www.mainnet.optimism.io/")


def login_ds(driver, ds_token: str, ) -> None:
    "Логинися в твиттере"
    driver.get('https://discord.com/login')
    sleep(10)
    js = f'''
function login(token) {{
    setInterval(() => {{
        document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${{token}}"`;
    }}, 50);
    setTimeout(() => {{
        location.reload();
    }}, 2500);
}}
login("{ds_token}");
'''
    driver.execute_script(js)


if __name__ == "__main__":
    with open("dolphy.csv", "r") as file:
        reader = csv.DictReader(file)
        for i, row in zip(get_list_id(
                "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6OTI0NjI1LCJ1c2VybmFtZSI6ImtoYWtpbW92LmRhbmlsQG1haWwucnUiLCJyb2xlIjoiYWRtaW4iLCJ0ZWFtSWQiOjg4MTA2NSwidG9rZW5DcmVhdGVkQXQiOjE2ODE1NjQwMDl9.66NxSAdvd7zX6o3UYfdaPMcYy9cPdOhXzL4ibtcZvIA"),
                reader):
            driver_ = get_webdriver(i)
            sleep(7)
            driver_.switch_to.window(driver_.window_handles[0])
            driver_.close()
            try:
                sleep(2)
                twitter_auth(driver_, row["tw_login"], row["tw_password"], row["tw_reserve_mail"])
            except Exception:
                print("Ошибка в корректонсти твиттера (залогигинился или проверь, мб забанили)")
            try:
                sleep(2)
                work_witch_metamask(driver_, row["metamask_seed"], row["metamask_password"])
            except Exception:
                print("ошибка с метамаском, что то не так с сид фразой")
            try:
                sleep(2)
                login_ds(driver_, row["ds_token"])
            except Exception:
                print("что то не так с токеном")
            else:
                print("все ок")
            #             # add_networks_to_metamask(driver_, row["metamask_password"])
            finally:
                sleep(5)
                if len(driver_.window_handles) > 1:
                    for page in range(len(driver_.window_handles)):
                        driver_.switch_to.window(driver_.window_handles[0])
                        driver_.close()
                else:
                    driver_.close()
                driver_.quit()



