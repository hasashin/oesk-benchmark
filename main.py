#!python3
from datetime import datetime
import email
from statistics import median
from tkinter import StringVar
from peewee import *
from playhouse.db_url import connect
from gui import DbGui
from faker import Faker
from argon2 import PasswordHasher

db = DatabaseProxy()

class DBConnector:
    def __init__(self):
        self.type = DbGui.db_type["MySQL"]

    def connect_to_database(self, url:StringVar):
        global db
        db
        if self.type == DbGui.db_type["MySQL"]:
            if url.get().startswith('mysql://'):
                db.initialize(connect(url.get()))
            else:
                url.set('mysql://')
        elif self.type == DbGui.db_type['PostgreSQL']:
            if url.get().startswith('postgresql://'):
                db.initialize(connect(url.get()))
            else:
                url.set('postgresql://')
        elif self.type == DbGui.db_type['SQLite']:
            if url.get().startswith('sqlite:///'):
                db.initialize(connect(url.get()))
            else:
                url.set('sqlite:///')
        else:
            raise ValueError('Invalid database type')

    def start(self, num:int):
        db.connect()

        Comment.bind(db)
        Content.bind(db)
        Media.bind(db)
        Account.bind(db)

        db.drop_tables([Comment,Content,Media,Account])
        db.create_tables([Comment,Content,Media,Account])
        # prepare data
        fake_data={'Account':[], 'Content':[], 'Comment':[], 'Media': []}
        fake = Faker()
        ph = PasswordHasher()
        for _ in range(num):
            account = {}
            account['email'] = fake.company_email()
            account['password'] = ph.hash(fake.password(length=16))
            account['name'] = fake.name()
            account['token'] = fake.uuid4()
            account['isAdmin'] = fake.pybool()
            created_date = datetime.strptime(fake.date(), '%Y-%m-%d')
            account['dateCreated'] = created_date
            account['lastLogin'] = fake.date_between(start_date=created_date)
            fake_data['Account'].append(account)

            content = {}
            content['isPage'] = fake.pybool()
            content['isHidden'] = fake.pybool()
            content['slug'] = fake.name()
            content['title'] = fake.word()
            content['body'] = fake.paragraph(nb_sentences=10)
            created_date = datetime.strptime(fake.date(), '%Y-%m-%d')
            content['dateCreated'] = created_date
            content['dateModified'] = fake.date_between(start_date=created_date)
            content['authorId'] = fake.pyint(min_value=1, max_value=num)
            content['modifiedById'] = fake.pyint(min_value=1, max_value=num)
            fake_data['Content'].append(content)

            comment = {}
            comment['body'] = fake.paragraph(nb_sentences=3)
            comment['dateCreated'] = datetime.strptime(fake.date(), '%Y-%m-%d')
            comment['authorId'] = fake.pyint(min_value=1, max_value=num)
            comment['contentId'] = fake.pyint(min_value=1, max_value=num)
            fake_data['Comment'].append(comment)

            media = {}
            media['name'] = fake.file_name(category='image')
            media['path'] = fake.file_path()
            media['dateCreated'] = datetime.strptime(fake.date(), '%Y-%m-%d')
            media['authorId'] = fake.pyint(min_value=1, max_value=num)
            fake_data['Media'].append(media)
        
        starttime = datetime.now()
        for row in db.batch_commit(fake_data['Account'], num):
            Account.create(**row)
    
        for row in db.batch_commit(fake_data['Content'], num):
            Content.create(**row)
    
        for row in db.batch_commit(fake_data['Comment'], num):
            Comment.create(**row)
    
        for row in db.batch_commit(fake_data['Media'], num):
            Media.create(**row)
                
        stoptime = datetime.now()
        db.close()
        return stoptime-starttime


class Account(Model):
    email = CharField()
    password = CharField()
    name = CharField()
    token = CharField()
    isAdmin = BooleanField(default=False)
    dateCreated = DateField()
    lastLogin = DateField()

class Content(Model):
    isPage = BooleanField(default=False)
    isHidden = BooleanField(default=False)
    slug = CharField()
    title = CharField()
    body = TextField()
    dateCreated = DateField()
    dateModified = DateField()
    authorId = ForeignKeyField(Account)
    modifiedById = ForeignKeyField(Account)

class Comment(Model):
    body = CharField()
    dateCreated = DateField()
    authorId: ForeignKeyField(Account)
    contentId: ForeignKeyField(Content)

class Media(Model):
    name = CharField()
    path = CharField(default='')
    dateCreated = DateField()
    authorId = ForeignKeyField(Account)

if __name__ == '__main__':
    gui = DbGui(DBConnector())
    gui.prepare()
    gui.start()