import configparser
import pymysql
from peewee import *

CONFIG_PATH = "../resources/"
CONFIG_FILES = [("[SQL]", "mysql_config.ini"), ("[SRV]", "server_config.ini")]

def read_config():
    string = ""
    for pair in CONFIG_FILES:
        with open(CONFIG_PATH + pair[1], 'r') as file:
            string += pair[0] + "\n"
            string += file.read().replace('"', '')

    config = configparser.ConfigParser()
    config.read_string(string)
    return config

class BaseModel(Model):
    class Meta:
        config = read_config()
        database = MySQLDatabase(config["SRV"]["maindb"],
                                 **{"password": config["SQL"]["password"],
                                    "user": config["SQL"]["user"]})

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

