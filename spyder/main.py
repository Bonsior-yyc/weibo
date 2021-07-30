from spyder.get_weibo_content import get_weibo
from spyder.get_weibo_comment import get_comment
from spyder.get_cookie import with_cookie
from selenium import webdriver
from spyder.get_weibo_list import get_weibo_rumour_url, get_weibo_nromal_url
import queue
import threading


@with_cookie
def get_weibo_content_and_comments(driver, url, rumor=True):
    weibo_id = get_weibo(driver, url, rumor=rumor)
    get_comment(driver, url, weibo_id)
    print(threading.current_thread().name, "Successfully saved:" + str(weibo_id))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='spyder for weibo ')
    parser.add_argument('-r', '--rumor', default=False, help='是否谣言', action='store_true')
    parser.add_argument('-n', '--normal', default=False, help='是否非谣言', action='store_true')
    parser.add_argument('-w', '--worker', default=1, help='爬虫数量', type=int)
    args = parser.parse_args()

    q_r = queue.Queue()
    q_n = queue.Queue()

    if args.rumor:
        for url in get_weibo_rumour_url():
            q_r.put(url)
    if args.normal:
        for url in get_weibo_nromal_url():
            q_n.put(url)

    print(q_r.unfinished_tasks)
    print(q_n.unfinished_tasks)


    def worker_r():
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(executable_path='./chromedriver', options=options)
        driver.get('https://weibo.com/login.php')
        while True:
            url = q_r.get()
            get_weibo_content_and_comments(driver, url, rumor=True)
            q_r.task_done()


    def worker_n():
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(executable_path='./chromedriver', options=options)
        driver.get('https://weibo.com/login.php')
        while True:
            url = q_n.get()
            get_weibo_content_and_comments(driver, url, rumor=False)
            q_n.task_done()


    for i in range(args.worker):
        threading.Thread(target=worker_r, daemon=True, name="spyder-r-" + str(i)).start()

    for i in range(args.worker):
        threading.Thread(target=worker_n, daemon=True, name="spyder-n-" + str(i)).start()

    q_r.join()
    q_n.join()
    print('All work completed')
