from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class Restaurant(Base):
    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    restaurant_id= Column(String(80))
    address = Column(String(250))
    rating = Column(String(2))
    types = Column(String(100))

    def restaurantId(self):
        return self.restaurant_id

    @property
    def serialize(self):
        return {
            'id': self.id,
            'restaurant_id': self.restaurant_id,
            'restaurant_name': self.name,
            'address': self.address,
            'rating': self.rating,
            'types': self.types
        }

engine = create_engine('sqlite:///restaurants.db')
Base.metadata.create_all(engine)


