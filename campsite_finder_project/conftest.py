from pytest import fixture 
from config import Config
from selenium import webdriver
import json 

data_path = 'tests/test_data.json'

def pytest_addoption(parser):
    parser.addoption("--env", action="store", help="Envirnment to run test against")
    parser.addoption("--emulation", action="store", help="mobile or desktop?"),
    parser.addoption("--browserlocation", action="store", help="Local, Browserstack or Test Server")
    parser.addoption("--chrome_mode", action="store", help="headless or nonheadless")

@fixture(scope='session')
def env(request):
    return request.config.getoption("--env")

@fixture(scope="session")
def emulation(request):
    return request.config.getoption("--emulation")

@fixture(scope="session")
def browserlocation(request):
    return request.config.getoption("--browserlocation")

@fixture(scope="session")
def chrome_mode(request):
    return request.config.getoption("--chrome_mode")

@fixture(scope='session')
def app_config(env, emulation):
    cfg = Config(env, emulation)
    return cfg

@fixture(scope="function")
def browser(browserlocation, emulation, chrome_mode):
    chrome_options = webdriver.ChromeOptions()

    if browserlocation == 'local':
        mobile_emulation = {"deviceName": "iPhone 6 Plus"}
        if emulation == 'mobile':
            chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    if browserlocation == 'local' and chrome_mode == 'headless':
        chrome_options.add_argument("--headless")

    if browserlocation == 'testserver' and chrome_mode == 'headless':
        chrome_options.add_argument("--headless")
        chrome_options.binary_location = "/usr/bin/google-chrome"

    if browserlocation == 'testserver' and chrome_mode == 'nonheadless':
        chrome_options.binary_location = "/usr/local/bin/chromedriver"
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

    if browserlocation != 'bs':
        chrome_options.add_argument('--no-sandbox')  # Should be the first options passed.
        chrome_options.add_argument("--window-size=1920,1400")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--allow-running-insecure-content')

    # Create the driver
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.set_page_load_timeout(30)

    yield browser

    # Teardown
    browser.quit()
