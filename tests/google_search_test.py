import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def init_driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    return driver

def test_google_page_load_time():
    start_time = time.time()
    driver = init_driver()
    driver.get("https://www.google.com")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))
    load_time = time.time() - start_time
    assert load_time < 7, f"Trang tải quá lâu: {load_time} giây"
    driver.quit()

def test_google_search_with_valid_keywords():
    driver = init_driver()
    driver.get("https://www.google.com")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("Selenium")
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)
    assert "Selenium" in driver.title
    driver.quit()

def test_invalid_search():
    driver = init_driver()
    driver.get("https://www.google.com")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("filetype:pdf")
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)
    no_results = driver.find_elements(By.ID, "topstuff")
    assert len(no_results) > 0, "Không có thông báo lỗi hiển thị"
    driver.quit()

def test_empty_search():
    driver = init_driver()
    driver.get("https://www.google.com")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(Keys.RETURN)
    assert "Google" in driver.title
    driver.quit()

def test_google_ui_elements():
    driver = init_driver()
    driver.get("https://www.google.com")
    search_box = driver.find_element(By.NAME, "q")
    assert search_box.is_displayed()
    search_button = driver.find_element(By.NAME, "btnK")
    search_button.is_displayed()
    assert search_button.get_attribute("value") == "Tìm trên Google"
    driver.quit()

