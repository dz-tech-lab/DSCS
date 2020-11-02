from main import db

from main import User, Posts

import pandas as pd


db.create_all()

User.query.all()


user1 = User(first_name="Dominique",
             last_name="Paul",
             email="dominique.paul@unisg.ch",
             user_handle="dompi97",
             password="password")

user2 = User(first_name="test",
             last_name="user",
             email="test@unisg.ch",
             user_handle="test00",
             password="test_password")

user3 = User(first_name="Damian",
             last_name="Zaker",
             email="damian.zaker@unisg.ch",
             user_handle="damdam",
             password="damdam00")

user4 = User(first_name="D",
             last_name="Z",
             email="d@z.com",
             user_handle="d@z",
             password="dz")
db.session.add(user1)
db.session.add(user2)
db.session.add(user3)
db.session.commit()
db.session.rollback()

df = pd.read_sql(Posts.query.statement, db.session.bind)
df
df1 = pd.read_sql(User.query.statement, db.session.bind)
df1

my_user = User.query.get(5)
my_user
my_user.posts

user = User.query.filter_by(user_handle="Zak").first()
user.first_name

my_post1 = Posts.query.get(5)
my_post1
my_post1.author

test_df = pd.read_sql(Posts.query.statement, db.session.bind)
test_df
test_df.sort_values(by=['date_created'], ascending=False)
