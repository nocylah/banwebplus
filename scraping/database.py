import configparser
import pymysql
from peewee import *

config_path = "../resources/mysql_config.ini"
db_name = "beanwebplus"
config = configparser.ConfigParser()
config.read_string("[DB]\n" + open(config_path).read().replace('"',""))
config = config["DB"]

class BaseModel(Model):
    class Meta:
        database = MySQLDatabase(db_name,
                                 **{"password": config["password"],
                                    "user": config["user"]})

class Classes(BaseModel):
    campus = CharField(null=False)
    course = CharField(null=False)
    crn = IntegerField(index=True,null=False)
    days = CharField(null=False)
    days_times_locations = CharField(null=False)
    end_date = DateTimeField(null=False)
    enroll = IntegerField(null=False)
    hours = IntegerField(null=False)
    instructor = CharField(null=False)
    last_mod_time = DateTimeField(null=False)
    limit = IntegerField(null=False)
    location = CharField(null=False)
    parent_class = IntegerField(null=False)
    seats = IntegerField(null=False)
    semester = CharField(index=True,null=False)
    start_date = DateTimeField(null=False)
    subclass_identifier = IntegerField(null=False)
    subject = CharField(null=False)
    time = CharField(null=False)
    title = CharField(null=False)
    user_ids_with_access = CharField(null=False)
    year = IntegerField(index=True,null=False)

    class Meta:
        db_table = 'classes'
        primary_key = False

class Subjects(BaseModel):
    abbr = CharField(null=False)
    semester = CharField(index=True,null=False)
    title = CharField(null=False)
    year = IntegerField(index=True,null=False)

    class Meta:
        db_table = 'subjects'
        primary_key = False

