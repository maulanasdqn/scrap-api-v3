from selenium import webdriver
from selenium_stealth import stealth
from bs4 import BeautifulSoup
from flask import Flask, request
import time

app = Flask(__name__)

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
# options.binary_location = "/nix/store/2a0fz2n5ri0gd6sdqwfvs4pyz3n66m31-google-chrome-102.0.5005.61/bin/google-chrome-stable"
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
prefs = {'profile.default_content_setting_values': {'cookies': 2, 'images': 2, 'javascript': 2, 
                            'plugins': 2, 'popups': 2, 'geolocation': 2, 
                            'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2, 
                            'mouselock': 2, 'mixed_script': 2, 'media_stream': 2, 
                            'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2, 
                            'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2, 
                            'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2, 
                            'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2, 
                            'durable_storage': 2}}
options.add_experimental_option('prefs', prefs)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options)

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

def BliBli(url):
    driver.get(url)
    time.sleep(1)
    page = driver.page_source
    soup = BeautifulSoup(page, 'html5lib')
    name = soup.select(".product-name")
    price = soup.select(".product-price__after")
    rname = name[0].next.strip()
    rprice = price[0].next
    obj = {
        "product_name": rname,
        "product_price": rprice,
    }
    return obj

@app.route("/", methods=["POST"])
def root():
    url = request.get_json()["url"]
    try:
        return BliBli(url)
    except:
        return {"Message": "Error"}

if __name__ == "__main__":
    app.run(debug=False)