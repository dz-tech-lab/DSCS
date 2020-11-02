def register_user(form_data):

    def email_already_taken(email):
        if User.query.filter_by(email=email).count() > 0:
            return True
        else:
            return False

    if email_already_taken(form_data.email.data):
        return False

    user = User(name=form_data.name.data,
                email=form_data.email.data,
                password=form_data.password.data)

    db.session.add(user)

    db.session.commit()

    return True


def is_login_successful(form_data):

    user_handle = form_data.user_handle.data
    password = form_data.password.data

    are_credentials_correct = User.query.filter_by(user_handle=user_handle,
                                                   password=password)\
        .count()

    return are_credentials_correct


def add_tweet(form_data):

    tweet = Posts(content=form_data.content.data,
                  description=form_data.description.data,
                  price=form_data.price.data,
                  user_id=current_user.id)

    db.session.add(tweet)

    db.session.commit()


def get_tweets():
    df = pd.read_sql(Posts.query.statement, db.session.bind)

    return df
