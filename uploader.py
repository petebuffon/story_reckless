import os
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located, element_to_be_clickable

def anchor_upload(episode, input_path):
    print("starting upload...")
    env_var = os.environ
    email = env_var["EMAIL"]
    password = env_var["PASSWORD"]
    options = Options()
    options.add_argument("--headless")
    with webdriver.Firefox(options=options) as driver:
        # driver = webdriver.Firefox(options=options)
        wait = WebDriverWait(driver, 14400)
        driver.get("https://anchor.fm/dashboard/episode/new")
        print(f"logging in as {email}")
        driver.find_element(By.NAME, "email").send_keys(email)
        driver.find_element(By.NAME, "password").send_keys(password + Keys.RETURN)
        print("choosing file")
        file_input = wait.until(presence_of_element_located((By.XPATH, "//input[@type='file']")))
        file_input.send_keys(input_path)
        print("uploading " + episode.video_id + "...")
        time.sleep(5)
        save_changes = wait.until(element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Save episode')]")))
        save_changes.click()
        form = wait.until(presence_of_element_located((By.TAG_NAME, "form")))
        print("adding metadata")
        form.find_element(By.XPATH, "//button[contains(text(), 'Switch to HTML')]").click()
        text_area = form.find_element(By.NAME, "description")
        text_area.clear()
        text_area.send_keys(episode.description)
        form.find_element(By.NAME, "title").send_keys(episode.title)
        form.find_element(By.NAME, "podcastSeasonNumber").send_keys(episode.season)
        form.find_element(By.NAME, "podcastEpisodeNumber").send_keys(episode.episode)
        radio = driver.find_element(By.ID, "podcastEpisodeIsExplicit_1")
        driver.execute_script("arguments[0].click();", radio)
        publish_now = wait.until(element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Publish now')]")))
        publish_now.click()
        print("episode published")
