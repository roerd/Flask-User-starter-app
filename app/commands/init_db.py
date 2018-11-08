# This file defines command line commands for the flask command
#
# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>

import datetime

from flask import current_app


def init_db_command(the_app):
    """ Initialize the database."""

    @the_app.cli.command()
    def init_db():
        """ Initialize the database."""

        from app import db

        db.drop_all()
        db.create_all()
        create_users()

        print('Database has been initialized.')


def create_users():
    """ Create users """

    from app import db

    # Create all tables
    db.create_all()

    # Adding roles
    admin_role = find_or_create_role('admin', u'Admin')

    # Add users
    find_or_create_user(u'Admin', u'Example', u'admin@example.com', 'Password1', admin_role)
    find_or_create_user(u'Member', u'Example', u'member@example.com', 'Password1')

    # Save to DB
    db.session.commit()


def find_or_create_role(name, label):
    """ Find existing role or create new role """

    from app import db
    from app.models.user_models import Role

    role = Role.query.filter(Role.name == name).first()
    if not role:
        role = Role(name=name, label=label)
        db.session.add(role)
    return role


def find_or_create_user(first_name, last_name, email, password, role=None):
    """ Find existing user or create new user """

    from app import db
    from app.models.user_models import User

    user = User.query.filter(User.email == email).first()
    if not user:
        user = User(email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=current_app.user_manager.password_manager.hash_password(password),
                    active=True,
                    email_confirmed_at=datetime.datetime.utcnow())
        if role:
            user.roles.append(role)
        db.session.add(user)
    return user
