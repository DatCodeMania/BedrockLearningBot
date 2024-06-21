from selenium import webdriver


class Setup:
    def get_chromedriver(self):
        #UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
              #"(KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36")

        chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_argument("--headless=new")
        chrome_options.add_extension('./uBlock0.chromium.crx')

        # Disabling images from loading
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)

        #chrome_options.add_argument(f'--user-agent={UA}')

        driver = webdriver.Chrome(options=chrome_options)
        return driver
