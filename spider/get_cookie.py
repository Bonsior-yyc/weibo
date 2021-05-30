import json
from selenium import webdriver


def get_login_cookies(path):
    driver = webdriver.Chrome()
    driver.get('https://weibo.com/login.php')
    login_url = driver.current_url
    while driver.current_url == login_url:
        pass
    with open(path, "w") as f:
        json.dump(driver.get_cookies(), f)
    driver.close()


def with_cookie(func):
    def wrap_func(driver: webdriver.Chrome, *args, **kwargs):
        with open("cookie.txt", "r") as f:
            cookies = json.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)
        return func(driver, *args, **kwargs)
    return wrap_func


if __name__ == '__main__':
    get_login_cookies("cookie.txt")
