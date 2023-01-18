import time
from datetime import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

MAX_DELAY = 20

def reserve_gym_spot(username, password, resv_date, resv_time, headless=False, debug=True):
    # options
    print("------------\nStart reserver for "+ username)
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))
    driver.get("http://applications.ucy.ac.cy/pub_sportscenter/main")
    if debug:
        print('Fetched url...')

    # Go to login page
    try:
        tpe_box = WebDriverWait(driver, MAX_DELAY).until(EC.presence_of_element_located((By.ID, 'tpe')))
        tpe_box.click()

        go_to_login_button = WebDriverWait(driver, MAX_DELAY).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[4]/div[3]/div/article/button[1]')))
        go_to_login_button.click()

        if debug:
            print('Reached login page...')

    except TimeoutException:
        print("Loading took too much time!")
        driver.quit()

    # SSO page login
    try:
        username_input = WebDriverWait(driver, MAX_DELAY).until(
            EC.presence_of_element_located((By.ID, 'userNameInput')))
        password_input = WebDriverWait(driver, MAX_DELAY).until(
            EC.presence_of_element_located((By.ID, 'passwordInput')))
        submit_button = WebDriverWait(driver, MAX_DELAY).until(EC.presence_of_element_located((By.ID, 'submitButton')))

        username_input.send_keys(username)
        password_input.send_keys(password)
        submit_button.click()

        if debug:
            print('Logged in...')

    except TimeoutException:
        print("Loading took too much time!")
        driver.quit()

    # go to reservations
    driver.get("https://applications.ucy.ac.cy/sportscenter/online_reservations_pck2.insert_reservation?p_lang=")

    # go sport
    try:
        sport_selection = Select(
            WebDriverWait(driver, MAX_DELAY).until(EC.presence_of_element_located((By.NAME, 'p_sport'))))
        accept_terms = WebDriverWait(driver, MAX_DELAY).until(
            EC.presence_of_element_located((By.NAME, 'terms_accepted')))
        submit_button = WebDriverWait(driver, MAX_DELAY).until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[2]/div/div[4]/form/table/tbody/tr[5]/td[2]/div/button")))

        sport_selection.select_by_value('6')
        accept_terms.click()
        submit_button.click()

        if debug:
            print('Set sport...')

    except TimeoutException:
        print("Loading took too much time!")
        driver.quit()

    # select day given it's not saturday
    try:
        WebDriverWait(driver, MAX_DELAY).until(EC.presence_of_element_located((By.TAG_NAME, 'button')))
        day_button = None
        all_buttons = driver.find_elements(By.TAG_NAME, 'button')
        resv_day = datetime.strptime(resv_date, "%d-%m-%Y").day
        for button in all_buttons:
            if button.text == str(resv_day):
                day_button = button
                break
        if day_button is None:
            for button in all_buttons:
                if button.text == 'Επόμενος Μήνας':
                    button.click()
            WebDriverWait(driver, MAX_DELAY).until(EC.presence_of_element_located((By.TAG_NAME, 'button')))
            all_buttons = driver.find_elements(By.TAG_NAME, 'button')
            for button in all_buttons:
                if button.text == str(resv_day):
                    day_button = button
                    break

        day_button.click()

        if debug:
            print('Got to gym form...')

    except TimeoutException:
        print("Loading took too much time!")
        driver.quit()

    # create gym form
    try:
        sport_selection = Select(
            WebDriverWait(driver, MAX_DELAY).until(EC.presence_of_element_located((By.NAME, 'p_class_code'))))
        set_time = Select(
            WebDriverWait(driver, MAX_DELAY).until(EC.presence_of_element_located(
                (By.XPATH, ' /html/body/div[2]/div/div[4]/form/table/tbody/tr[2]/td/table/tbody/tr/td[3]/select'))))
        purpose = WebDriverWait(driver, MAX_DELAY).until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[2]/div/div[4]/form/table/tbody/tr[3]/td[2]/textarea')))
        submit_button = WebDriverWait(driver, MAX_DELAY).until(EC.presence_of_element_located((By.TAG_NAME, "button")))

        sport_selection.select_by_value('41')
        set_time.select_by_visible_text(resv_time)
        purpose.send_keys("Gym")
        submit_button.click()

        if debug:
            print('Created gym form...')

    except TimeoutException:
        print("Loading took too much time!")
        driver.quit()

    # submit final form
    try:
        submit_button = WebDriverWait(driver, MAX_DELAY).until(EC.presence_of_element_located((By.TAG_NAME, "button")))

        submit_button.click()

        if debug:
            print('Submitted form...')

    except TimeoutException:
        print("Loading took too much time!")
        driver.quit()

    if debug:
        print('Done\n------------\n')
    time.sleep(MAX_DELAY)
    driver.quit()
