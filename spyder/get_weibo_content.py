import traceback

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from data.Weibo import Weibo
from spyder.get_weibo_list import get_weibo_rumour_url


def get_weibo(driver: webdriver.Chrome, url: str, rumor=True):
    driver.get(url)
    try:
        WebDriverWait(driver, 30, 0.5).until(lambda x: x.find_element_by_class_name('WB_text'))
        content = driver.find_element_by_class_name('WB_text').get_attribute('innerText')
    except:
        content = None

    try:
        WebDriverWait(driver, 30, 0.5).until(lambda x: x.find_element_by_class_name('WB_from'))
        post_time = driver.find_element_by_class_name('WB_from').find_element_by_tag_name('a').get_attribute(
            'title')
    except:
        post_time = None

    try:
        WebDriverWait(driver, 30, 0.5).until(lambda x: x.find_element_by_class_name('WB_row_line'))
        weibo_rows = driver.find_element_by_class_name('WB_row_line').find_elements_by_tag_name('li')

        try:
            repost_number = int(weibo_rows[1].find_elements_by_tag_name('em')[1].get_attribute('innerText'))
        except:
            repost_number = 0
        try:
            comment_number = int(weibo_rows[2].find_elements_by_tag_name('em')[1].get_attribute('innerText'))
        except:
            comment_number = 0
        try:
            thumb_number = int(weibo_rows[3].find_elements_by_tag_name('em')[1].get_attribute('innerText'))
        except:
            thumb_number = 0
    except:
        repost_number, comment_number, thumb_number = None, None, None

    try:
        WebDriverWait(driver, 30, 0.5).until(lambda x: x.find_element_by_class_name('WB_info'))
        user_url = driver.find_element_by_class_name('WB_info').find_element_by_tag_name('a').get_attribute("href")
        driver.get(user_url)

        try:
            WebDriverWait(driver, 30, 0.5).until(lambda x: x.find_element_by_class_name('tb_counter'))
            s_line = driver.find_element_by_class_name('tb_counter').find_elements_by_class_name('S_line1')
            follow_number = int(s_line[0].find_element_by_tag_name('strong').get_attribute('innerText'))
            fan_number = int(s_line[1].find_element_by_tag_name('strong').get_attribute('innerText'))
            weibo_number = int(s_line[2].find_element_by_tag_name('strong').get_attribute('innerText'))
        except:
            follow_number, fan_number, weibo_number = None, None, None

        try:
            WebDriverWait(driver, 30, 0.5).until(lambda x: x.find_element_by_class_name('PCD_person_info'))
            user_url = driver.find_element_by_class_name('PCD_person_info').find_element_by_class_name(
                'WB_cardmore').get_attribute('href')
            driver.get(user_url)

            try:
                WebDriverWait(driver, 30, 0.5).until(lambda x: x.find_element_by_class_name('username'))
                user_name = driver.find_element_by_class_name('username').get_attribute('innerText')
            except:
                user_name = None

            is_certified = True if len(
                driver.find_element_by_class_name('pf_photo').find_elements_by_class_name('W_icon')) > 0 else False
            if is_certified:
                certification = driver.find_element_by_class_name('pf_photo').find_elements_by_class_name('W_icon')[
                    0].get_attribute('title')
            else:
                certification = None
            # 要改
            try:
                li_1_dict = {"注册时间：": '', "简介：": ''}
                WebDriverWait(driver, 2, 0.5).until(lambda x: x.find_element_by_class_name('li_1'))
                li_1s = driver.find_elements_by_class_name('li_1')
                for li_1 in li_1s:
                    li_1_dict[li_1.find_element_by_class_name('pt_title').text] = li_1.find_element_by_class_name \
                        ('pt_detail') \
                        .get_attribute('innerText') \
                        if len(li_1.find_elements_by_class_name('pt_detail')) != 0 else ''
                register_time = li_1_dict["注册时间："]
                introduction = li_1_dict["简介："]
            except:
                register_time, introduction = None, None
        except:
            user_name, certification, register_time, introduction, is_certified = None, None, None, None, None
    except:
        is_certified, user_url = None, None
        follow_number, fan_number, weibo_number, user_name, certification, register_time, introduction = None, None, None, None, None, None, None

    weibo = Weibo(weibo_url=url, user_url=user_url, content=content, post_time=post_time,
                  repost_number=repost_number, comment_number=comment_number, thumb_number=thumb_number,
                  user_name=user_name, is_certified=is_certified, certification=certification,
                  register_time=register_time, follow_number=follow_number, fan_number=fan_number,
                  weibo_number=weibo_number, introduction=introduction, rumor=rumor)
    weibo.save()
    return weibo.id


if __name__ == '__main__':
    for url in get_weibo_rumour_url():
        get_weibo(url)
