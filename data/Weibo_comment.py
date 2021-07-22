from peewee import *

db = MySQLDatabase(
    'rumor', user='root', password='password',
    host='127.0.0.1', port=3306)


class Comments(Model):
    id = AutoField()
    weibo_id = IntegerField()
    content = TextField(null=True)
    thumb_number = IntegerField(null=True)
    reply_number = IntegerField(null=True)
    is_certified = BooleanField(null=True)

    class Meta:
        database = db

    def __str__(self):
        return {
            "id": self.id,
            "weibo_id": self.weibo_id,
            "content": self.content,
            "thumb_number": self.thumb_number,
            "reply_number": self.reply_number,
            "is_certified": self.is_certified
        }.__str__()


if __name__ == '__main__':
    Comments.drop_table()
    Comments.create_table()
