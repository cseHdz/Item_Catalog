from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, CategoryItem, User

<<<<<<< HEAD
engine = create_engine('postgresql:///catalog')
=======
engine = create_engine('sqlite:///item_catalog.db')
>>>>>>> parent of c553022... Updates to PSQL Connection

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

session = DBSession()


# Create user to own all default Categories
test_user = User(name="Test User", email="user@catalog_app.com")
session.add(test_user)
session.commit()

# Add some items - Soccer
category1 = Category(title="Soccer")

session.add(category1)
session.commit()

citem1 = CategoryItem(title="Nike Soccer Ball",
                      description="""A professional soccer ball with FIFA
                                  standard size (No. 5).""",
                      category=category1,
                      user=test_user)

session.add(citem1)
session.commit()

citem2 = CategoryItem(title="Goalie Gloves",
                      description="Medium size soccer goalie gloves.",
                      category=category1,
                      user=test_user)

session.add(citem2)
session.commit()

citem3 = CategoryItem(title="Sheen Guards",
                      description="Adult size sheen guards.",
                      category=category1,
                      user=test_user)

session.add(citem3)
session.commit()

citem4 = CategoryItem(title="Official TFC Fan Scarf",
                      description="""TFC Season ticket holder scarf for
                                  2017-2018 Season.""",
                      category=category1,
                      user=test_user)

session.add(citem4)
session.commit()


# Add some items - Basketball
category2 = Category(title="Basketball")

session.add(category2)
session.commit()

citem5 = CategoryItem(title="Jordans",
                      description="Limited Edition Jordan Basketball Shoes.",
                      category=category2,
                      user=test_user)

session.add(citem5)
session.commit()

citem6 = CategoryItem(title="Toronto Raptors Jersey",
                      description="2017 Jersey for the Toronto Raptors.",
                      category=category2,
                      user=test_user)

session.add(citem6)
session.commit()

citem7 = CategoryItem(title="Basketball",
                      description="A professional basketball",
                      category=category2,
                      user=test_user)

session.add(citem7)
session.commit()


# Add some items - Baseball
category3 = Category(title="Baseball")

session.add(category3)
session.commit()

citem8 = CategoryItem(title="Standard Bat",
                      description="MLB Authorized Bat.",
                      category=category3,
                      user=test_user)

session.add(citem8)
session.commit()

citem9 = CategoryItem(title="Toronto Blue Jays Hat",
                      description="""206 Post-Season Hat for the
                                    Toronto Blue Jays.""",
                      category=category3,
                      user=test_user)

session.add(citem9)
session.commit()

citem10 = CategoryItem(title="Helmet",
                       description="""An adult sized helmet with
                                   NY Yankees theme""",
                       category=category3,
                       user=test_user)

session.add(citem10)
session.commit()


# Add some items - Frisbee
category4 = Category(title="Frisbee")

session.add(category4)
session.commit()

citem11 = CategoryItem(title="Ultimate Frisbee - Blue",
                       description="""An ultimate certified
                                   frisbee in color blue.""",
                       category=category4,
                       user=test_user)

session.add(citem11)
session.commit()


# Add some items - Snowboarding
category5 = Category(title="Snowboarding")

session.add(category5)
session.commit()

citem12 = CategoryItem(title="Snowboard",
                       description="Regular snowboard.",
                       category=category5,
                       user=test_user)

session.add(citem12)
session.commit()

citem13 = CategoryItem(title="Snowboarding boots",
                       description="Black boots with Canada's olympic theme",
                       category=category5,
                       user=test_user)

session.add(citem13)
session.commit()


# Add some items - Rock Climbing
category6 = Category(title="Rock Climbing")

session.add(category6)
session.commit()

citem14 = CategoryItem(title="Caribiner",
                       description="""1 Caribiner with a breaking
                                   strength of 10,000 lbf""",
                       category=category6,
                       user=test_user)

session.add(citem14)
session.commit()

citem15 = CategoryItem(title="Magnesium",
                       description="Ideal for bouldering.",
                       category=category6,
                       user=test_user)

session.add(citem15)
session.commit()


# Add some items - Foosball
category7 = Category(title="Foosball")

session.add(category7)
session.commit()

citem16 = CategoryItem(title="Replacement balls",
                       description="Regular sized balls for foosball table",
                       category=category7,
                       user=test_user)

session.add(citem16)
session.commit()


# Add some items - Skating
category8 = Category(title="Skating")

session.add(category8)
session.commit()

citem17 = CategoryItem(title="Women's Ice Skates",
                       description="Women's skates for figure skating",
                       category=category8,
                       user=test_user)

session.add(citem17)
session.commit()

citem18 = CategoryItem(title="Rollerblades",
                       description="""Hockey style rollerblades with
                                   replacement wheels included.""",
                       category=category8,
                       user=test_user)

session.add(citem18)
session.commit()


# Add some items - Hockey
category9 = Category(title="Hockey")
session.add(category9)
session.commit()

citem19 = CategoryItem(title="Goalie Outfit",
                       description="""Regular goalie equiment with
                                   Toronto Maple Leaf's theme""",
                       category=category9,
                       user=test_user)

session.add(citem19)
session.commit()

citem20 = CategoryItem(title="Hockey Stick",
                       description="Children size hockey stick - pretaped.",
                       category=category9,
                       user=test_user)

session.add(citem20)
session.commit()
