from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pyautogui
import time
import requests


from utils.util_funcs import start_selenium_drive


# Initialize WebDriver
driver, page = start_selenium_drive("https://uspdigital.usp.br/jupiterweb/obterDisciplina?sgldis=MAT0206&verdis=2")
time.sleep(3)


