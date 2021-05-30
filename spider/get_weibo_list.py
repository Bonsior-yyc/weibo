import time

from spider.get_cookie import with_cookie
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


@with_cookie
def get_rumor_weibo_list(driver, start, end):
    with open("rumor_weibo_urls.txt", "w") as f:
        driver.get('https://service.account.weibo.com/?type=5&status=0&page=' + str(start))
        while True:
            weibo_url_list = driver.find_elements_by_class_name('m_table_tit')
            for weibo_url in weibo_url_list[1:]:
                f.write(weibo_url.find_element_by_tag_name('a').get_attribute('href') + "\n")
            if start == end:
                break
            else:
                start += 1
                time.sleep(1)
                driver.get('https://service.account.weibo.com/?type=5&status=0&page=' + str(start))


@with_cookie
def get_real_url(driver):
    with open("rumor_weibo_urls.txt", "r") as f:
        urls = f.readlines()
    with open("rumor_weibo_urls_real.txt", "w") as f:
        for url in urls:
            driver.get(url)
            try:
                weibo_url = driver.find_element_by_css_selector("[class='item top']").find_element_by_class_name(
                    'publisher').find_element_by_tag_name('a').get_attribute('href')
                f.write(weibo_url + "\n")
            except:
                print("bad url:", url)


def get_weibo_rumour_url():
    with open("rumor_weibo_urls_real.txt", "r") as f:
        for line in f.readlines():
            yield line


ym = [
    (2020, 1, 31),
    (2020, 2, 29),
    (2020, 3, 31),
    (2020, 4, 30),
    (2020, 5, 31),
    (2020, 6, 30),
    (2020, 7, 31),
    (2020, 8, 31),
    (2020, 9, 30),
    (2020, 10, 31),
    (2020, 11, 30),
    (2020, 12, 31),
    (2021, 1, 31),
    (2021, 2, 28),
    (2021, 3, 31),
    (2021, 4, 30),
]

words = ["新冠", "疫情", "病毒", "确诊", "疫苗", "复工", "口罩"]


def get_normal_url(driver: webdriver.Chrome, word='|'.join(words), y=2020, m=1, d=31, num=50):
    url = 'https://s.weibo.com/weibo/%25E7%2596%25AB%25E6%2583%2585?q={}&xsort=hot&suball=1&timescope=custom:{}-{}-01:{}-{}-{}&Refer=g&page={}'
    urls = []
    for page in range(1, 10):
        driver.get(url.format(word, y, m, y, m, d, page))
        WebDriverWait(driver, 10, 0.5).until(lambda x: x.find_element_by_class_name('from'))
        card_wraps = driver.find_element_by_class_name('m-con-l').find_elements_by_class_name('card-wrap')
        for i in range(len(card_wraps)):
            urls.append(
                card_wraps[i].find_element_by_class_name("from").find_element_by_tag_name("a").get_attribute("href"))
            if len(urls) > num:
                return urls
    return urls


@with_cookie
def get_normal_url_list(driver):
    urls = []
    with open("normal_weibo_urls_real.txt", "w") as f:
        for i in range(len(ym)):
            for url in get_normal_url(driver, y=ym[i][0], m=ym[i][1], d=ym[i][2], num=60):
                f.write(url + "\n")


def get_weibo_nromal_url():
    with open("normal_weibo_urls_real.txt", "r") as f:
        for line in f.readlines():
            yield line


if __name__ == '__main__':
    web_driver = webdriver.Chrome()
    web_driver.get("https://weibo.com/login.php")
    # get_rumor_weibo_list(web_driver, 1, 84)
    # get_real_url(web_driver)
    get_normal_url_list(driver=web_driver)
    web_driver.close()
