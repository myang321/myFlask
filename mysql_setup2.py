__author__ = 'Steve'

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()


class Restaurant(Base):
    __tablename__ = 'restaurant'
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)


class MenuItem(Base):
    __tablename__ = 'menu_item'
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    course = Column(String(250))
    description = Column(String(350))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'course': self.course,
        }


def conn():
    username = 'root'
    passwd = '123'
    schema = 'test'
    engine = create_engine(
        "mysql://{0}:{1}@127.0.0.1/{2}?charset=utf8&use_unicode=0".format(username, passwd, schema))
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session


def get_all_restaurants():
    session = conn()
    rows = session.query(Restaurant).all()
    return rows


def get_restaurants_by_id(id1):
    session = conn()
    rest = session.query(Restaurant).filter_by(id=id1).one()
    return rest


def get_all_menu_item():
    session = conn()
    rows = session.query(MenuItem).all()
    return rows


def get_menu_item_by_id(id1):
    session = conn()
    item = session.query(MenuItem).filter_by(id=id1).one()
    return item


def get_all_menu_item_by_restaurant(restaurant_id1):
    session = conn()
    rows = session.query(MenuItem).filter_by(restaurant_id=restaurant_id1)
    return rows


def add_restaurant(name1):
    rest = Restaurant(name=name1)
    session = conn()
    session.add(rest)
    session.commit()


def update_restaurant_name(id1, new_name):
    session = conn()
    rest = session.query(Restaurant).filter_by(id=id1).one()
    rest.name = new_name
    session.commit()


def update_menu_item_name(menu_id, new_name, new_price, new_course, new_description):
    session = conn()
    rest = session.query(MenuItem).filter_by(id=menu_id).one()
    rest.name = new_name
    rest.price = new_price
    rest.course = new_course
    rest.description = new_description
    session.commit()


def delete_menu_item(menu_id):
    session = conn()
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    session.delete(item)
    session.commit()


def delete_restaurant(id1):
    try:
        session = conn()
        rest = session.query(Restaurant).filter_by(id=id1).one()
        session.delete(rest)
        session.commit()
    except Exception as exp:
        print "delete failed"


def find_restaurant_by_id(id1):
    session = conn()
    rest = session.query(Restaurant).filter_by(id=id1).one()
    return rest


def add_item(item_name, rest_id):
    session = conn()
    newItem = MenuItem(name=item_name, restaurant_id=rest_id)
    session.add(newItem)
    session.commit()


if __name__ == "__main__":
    # query()
    print
    # insert()
    # delete()
    # update()
    # query()