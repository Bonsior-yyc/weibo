import traceback

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import time
from data.Weibo_comment import Comments


def get_comment(driver: webdriver.Chrome, url: str, weibo_id: int):
    driver.get(url)
    try:
        WebDriverWait(driver, 30, 0.5).until(lambda x: x.find_element_by_class_name('list_li'))
    except:
        pass
    temp_height = 0
    while True:
        # 循环将滚动条下拉
        driver.execute_script("window.scrollBy(0,1000)")
        # sleep一下让滚动条反应一下
        time.sleep(0.1)
        # 获取当前滚动条距离顶部的距离
        check_height = driver.execute_script(
            "return document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;")
        # 如果两者相等说明到底了
        if len(driver.find_elements_by_class_name('more_txt')) != 0:
            time.sleep(0.1)
            try:
                driver.find_element_by_class_name('more_txt').click()
            except:
                break
        if check_height == temp_height:
            time.sleep(1)
            if len(driver.find_elements_by_css_selector("[node-type='root_comment']")) > 500:
                break
            if len(driver.find_elements_by_class_name('more_txt')) != 0:
                driver.find_element_by_class_name('more_txt').click()
            else:
                break
        temp_height = check_height

    comment_list = driver.find_elements_by_class_name('list_li')
    for comment in comment_list:
        try:
            content = comment.find_element_by_class_name('list_con').find_element_by_class_name('WB_text').get_attribute(
                'innerText')
            thumb_number = \
                comment.find_element_by_css_selector("[node-type='like_status']").find_elements_by_tag_name('em')[
                    -1].get_attribute('innerText')
            if thumb_number == '赞':
                thumb_number = 0
            else:
                thumb_number = int(thumb_number)
            is_certified = False if len(comment.find_elements_by_css_selector("[title='微博个人认证 ']")) == 0 else True
            reply_number = comment.find_element_by_css_selector(
                "[action-type='click_more_child_comment_big']").get_attribute("innerText") if (len(
                comment.find_elements_by_css_selector("[action-type='click_more_child_comment_big']"))) > 0 else 0
            if reply_number != 0:
                reply_number = int(reply_number.split('条')[0][1:])

            Comments(weibo_id=weibo_id, content=content, thumb_number=thumb_number,
                     is_certified=is_certified,reply_number=reply_number).save()
        except Exception as e:
            traceback.print_exc()
            print("error comment:", url)
