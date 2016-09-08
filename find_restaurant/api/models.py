from find_restaurant import Base
from sqlalchemy import Column, String, Integer

class Restaurant(Base):
    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=True)
    restaurant_id = Column(String(80))
    address = Column(String(250))
    rating = Column(String(10))
    types = Column(String(250))

    def restaurantId(self):
        return self.restaurant_id

    def properties(self):
        return ['id', 'name', 'restaurant_id', 'address', 'rating', 'types']
            
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
