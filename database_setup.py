from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, column_property
from sqlalchemy import create_engine, select


Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    items = relationship("CategoryItem", back_populates="category")

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'title': self.title,
            'id': self.id,
        }


class CategoryItem(Base):
    __tablename__ = 'category_item'

    id = Column(Integer, primary_key=True)
    creation_date = Column(DateTime, default=func.now())
    last_updated = Column (DateTime, default=func.now())
    title = Column(String(80), nullable=False)
    description = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship (Category, back_populates="items")
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    category_name= column_property (
        select([Category.title]).\
        where(Category.id==category_id))


    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'title': self.title,
            'description': self.description,
            'id': self.id,
        }


engine = create_engine('sqlite:///item_catalog.db')


Base.metadata.create_all(engine)
