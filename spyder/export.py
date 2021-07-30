from data.Weibo import Weibo
from data.Weibo_comment import Comments
import pandas as pd


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='export data ')
    parser.add_argument('-e', '--excel', default=False, help='导出excel', action='store_true')
    parser.add_argument('-c', '--csv', default=False, help='导出csv', action='store_true')

    args = parser.parse_args()
    comments = Comments.select().dicts()
    weibos = Weibo.select().dicts()

    if args.excel:
        pd.DataFrame(weibos).to_excel("weibo.xlsx", encoding='utf-8', index=False)
        pd.DataFrame(comments).to_excel("comments.xlsx", encoding='utf-8', index=False)

    if args.csv:
        pd.DataFrame(weibos).to_csv("weibo.csv", encoding='utf-8', index=False)
        pd.DataFrame(comments).to_csv("comments.csv", encoding='utf-8', index=False)
