import random

import click
from flask.cli import with_appcontext
from faker import Faker
from faker.providers import profile
from faker.providers import lorem
from app.db import db
from app.models.user import User
from app.models.product import Product
from werkzeug.security import generate_password_hash

fake = Faker(locale='la')
fake.add_provider(profile)
fake.add_provider(lorem)


@click.command()
@with_appcontext
def seed_db():
    db.drop_all()
    db.create_all()

    for i in range(20):
        user = User(username=fake.profile()['username'], password=generate_password_hash('123'))
        product = Product(name=" ".join(fake.words(2)).title(), description=fake.paragraph(),
                          price=float(random.randint(10, 100)),
                          image="404.png")
        db.session.add_all([user, product])
        db.session.commit()
