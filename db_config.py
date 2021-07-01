from peewee import (CharField, DateField, DateTimeField, FloatField,
                    IntegerField, Model, SqliteDatabase)

from config import DATABASE_NAME

db = SqliteDatabase(DATABASE_NAME)

class UserData(Model):
    uid = IntegerField(primary_key=True, unique=True)
    uslug = CharField(unique=True, null=True)
    name = CharField(unique=True, null=True)
    url = CharField(unique=True, null=True)
    ranking = IntegerField(unique=True, null=True)
    avatar_url = CharField(null=True)
    FP_count = FloatField(null=True)
    FTN_count = FloatField(null=True)
    assets_count = IntegerField(null=True)
    gender = IntegerField(null=True)
    followers_count = IntegerField(null=True)
    fans_count = IntegerField(null=True)
    articles_count = IntegerField(null=True)
    wordage = IntegerField(null=True)
    likes_count = IntegerField(null=True)
    badges = CharField(null=True)
    last_update_time = DateTimeField(null=True)
    vip_type = CharField(null=True)
    vip_expire_date = DateTimeField(null=True)
    introduction_text = CharField(null=True)
    
    class Meta:
        database = db
