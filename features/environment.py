import os
from behave import before_all
from selenium import webdriver
from service import app
from service.models import db, Product

BASE_URL = os.getenv("BASE_URL", "http://localhost:8080")
DRIVER = os.getenv("DRIVER", "chrome")

def before_all(context):
    context.app = app
    context.client = app.test_client()
    context.base_url = BASE_URL
    context.wait_seconds = 2

    if DRIVER == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
        context.driver = webdriver.Chrome(options=options)
    elif DRIVER == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        context.driver = webdriver.Firefox(options=options)
    
    context.driver.implicitly_wait(context.wait_seconds)
    context.driver.set_window_size(1200, 600)

    with app.app_context():
        Product.init_db(app)

def after_all(context):
    context.driver.quit()
