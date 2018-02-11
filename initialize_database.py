from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, CategoryItem, User

engine = create_engine('sqlite:///item_catalog.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

session = DBSession()


# Create user to own all default Categories
test_User = User(name="Test User", email="user@catalog_app.com")
session.add(test_User)
session.commit()


# Add new categories
session.bulk_insert_mappings(Category,
            [dict(title="Soccer"), dict(title="Basketball"),
             dict(title="Baseball"), dict(title="Frisbee"),
             dict(title="Snowboarding"), dict(title="Rock Climbing"),
             dict(title="Foosball"), dict(title="Skating"),
             dict(title="Hockey")])

session.commit()
