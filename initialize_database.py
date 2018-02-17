from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, CategoryItem, User

engine = create_engine('sqlite:///item_catalog.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

session = DBSession()


# Create user to own all default Categories
test_user = User(name="Test User", email="user@catalog_app.com")
session.add(test_user)
session.commit()


# Add new categories
categories = [Category(title="Soccer"),
              Category(title="Basketball"),
              Category(title="Baseball"),
              Category(title="Frisbee"),
              Category(title="Snowboarding"),
              Category(title="Rock Climbing"),
              Category(title="Foosball"),
              Category(title="Skating"),
              Category(title="Hockey")]


session.bulk_save_objects(categories)
session.commit()


# Add some items - Soccer
session.bulk_insert_mappings(CategoryItem,
            [dict(title = "Nike Soccer Ball",
                  description = "A professional soccer ball with FIFA standard size (No. 5).",
                  category = categories[0],
                  user = test_user),
             dict(title = "Goalie Gloves",
                   description = "Medium size soccer goalie gloves.",
                   category = categories[0],
                   user = test_user),
             dict(title = "Sheen Guards",
                  description = "Adult size sheen guards.",
                  category = categories[0],
                  user = test_user),
             dict(title = "Official TFC Fan Scarf",
                  description = "TFC Season ticket holder scarf for 2017-2018 Season.",
                  category = categories[0],
                  user = test_user)])


# Add some items - Basketball
session.bulk_insert_mappings(CategoryItem,
            [dict(title = "Jordans",
                  description = "Limited Edition Jordan Basketball Shoes.",
                  category = categories[1],
                  user = test_user),
             dict(title = "Toronto Raptors Jersey",
                   description = "2017 Jersey for the Toronto Raptors.",
                   category = categories[1],
                   user = test_user),
             dict(title = "Basketball",
                  description = "A professional basketball",
                  category = categories[1],
                  user = test_user)])


# Add some items - Baseball
session.bulk_insert_mappings(CategoryItem,
            [dict(title = "Standard Bat",
                  description = "MLB Authorized Bat.",
                  category = categories[2],
                  user = test_user),
             dict(title = "Toronto Blue Jays Hat",
                   description = "206 Post-Season Hat for the Toronto Blue Jays.",
                   category = categories[2],
                   user = test_user),
             dict(title = "Helmet",
                  description = "An adult sized helmet with NY Yankees theme",
                  category = categories[2],
                  user = test_user)])


# Add some items - Frisbee
session.bulk_insert_mappings(CategoryItem,
            [dict(title = "Ultimate Frisbee - Blue",
                  description = "An ultimate certified frisbee in color blue.",
                  category = categories[3],
                  user = test_user)])


# Add some items - Snowboarding
session.bulk_insert_mappings(CategoryItem,
            [dict(title = "Snowboard",
                  description = "Regular snowboard.",
                  category = categories[4],
                  user = test_user),
             dict(title = "Snowboarding boots",
                   description = "Black boots with Canada's olympic theme",
                   category = categories[4],
                   user = test_user)])


# Add some items - Rock Climbing
session.bulk_insert_mappings(CategoryItem,
            [dict(title = "Caribiner",
                  description = "1 Caribiner with a breaking strength of 10,000 lbf",
                  category = categories[5],
                  user = test_user),
             dict(title = "Magnesium",
                   description = "Ideal for bouldering.",
                   category = categories[5],
                   user = test_user)])


# Add some items - Foosball
session.bulk_insert_mappings(CategoryItem,
            [dict(title = "Replacement balls",
                  description = "Regular sized balls for foosball table",
                  category = categories[6],
                  user = test_user)])


# Add some items - Skating
session.bulk_insert_mappings(CategoryItem,
            [dict(title = "Women's Ice Skates",
                  description = "Women's skates for figure skating",
                  category = categories[7],
                  user = test_user),
             dict(title = "Rollerblades",
                   description = "Hockey style rollerblades with replacement wheels included.",
                   category = categories[7],
                   user = test_user)])


# Add some items - Hockey
session.bulk_insert_mappings(CategoryItem,
            [dict(title = "Goalie Outfit",
                  description = "Regular goalie equiment with Toronto Maple Leaf's theme",
                  category = categories[8],
                  user = test_user),
             dict(title = "Hockey Stick",
                   description = "Children size hockey stick - pretaped.",
                   category = categories[8],
                   user = test_user)])

session.commit()
