from spider.get_weibo_content import get_weibo
from spider.get_weibo_comment import get_comment
from spider.get_cookie import with_cookie
from selenium import webdriver
from spider.get_weibo_list import get_weibo_rumour_url, get_weibo_nromal_url
import queue
import threading


@with_cookie
def get_weibo_content_and_comments(driver, url):
    weibo_id = get_weibo(driver, url)
    if weibo_id > 0:
        get_comment(driver, url, weibo_id)
    print("Successfully saved:" + str(weibo_id))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument('-r', '--rumor', default=False, help='是否谣言', action='store_true')
    parser.add_argument('-n', '--normal', default=False, help='是否谣言', action='store_true')
    parser.add_argument('-w', '--worker', default=1, help='爬虫数量', type=int)
    args = parser.parse_args()

    q = queue.Queue()

    if args.rumor:
        for url in get_weibo_rumour_url():
            q.put(url)
    if args.normal:
        for url in get_weibo_nromal_url():
            q.put(url)

    print(q.unfinished_tasks)


    def worker():
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(options=options)
        driver.get('https://weibo.com/login.php')
        while True:
            url = q.get()
            get_weibo_content_and_comments(driver, url)
            q.task_done()


    for i in range(args.worker):
        threading.Thread(target=worker, daemon=True, name="spider-" + str(i)).start()

    q.join()
    print('All work completed')
