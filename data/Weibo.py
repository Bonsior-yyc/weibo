from peewee import *

db = MySQLDatabase(
    'rumor', user='root', password='password',
    host='127.0.0.1', port=3306)


class Weibo(Model):
    id = AutoField()
    content = TextField(null=True)
    post_time = CharField(null=True)
    comment_number = IntegerField(null=True)
    thumb_number = IntegerField(null=True)
    repost_number = IntegerField(null=True)
    user_name = CharField(null=True)
    is_certified = BooleanField(null=True)
    certification = CharField(null=True)
    introduction = CharField(null=True)
    follow_number = IntegerField(null=True)
    fan_number = IntegerField(null=True)
    weibo_number = IntegerField(null=True)
    weibo_url = CharField(null=True)
    user_url = CharField(null=True)
    register_time = CharField(null=True)
    rumor = BooleanField(null=False)

    class Meta:
        database = db

    def __str__(self):
        return {
            "id": self.id,
            "content": self.content,
            "post_time": self.post_time,
            "comment_number": self.comment_number,
            "thumb_number": self.thumb_number,
            "repost_number": self.repost_number,
            "user_name": self.user_name,
            "is_certified": self.is_certified,
            "certification": self.certification,
            "introduction": self.introduction,
            "follow_number": self.follow_number,
            "fan_number": self.fan_number,
            "weibo_number": self.weibo_number,
            "weibo_url": self.weibo_url,
            "user_url": self.user_url,
            "register_time": self.register_time,
            "rumor": self.rumor
        }.__str__()


if __name__ == '__main__':
    Weibo.drop_table()
    Weibo.create_table()
