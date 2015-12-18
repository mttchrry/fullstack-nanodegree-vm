## SQL Alchemy database setup.
import os
import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()


class Catagory(Base):
	__tablename__ = 'catagory'
	id = Column(Integer, primary_key = True)
	name = Column(String(250), nullable = False)


class CatalogItem(Base):
	__tablename__ = 'catalog_item'
	id = Column(Integer, primary_key = True)
	name = Column(String(250), nullable = False)
	description = Column(String(250))
	price = Column(String(8))
	catagory_id = Column(Integer, ForeignKey('catagory.id'))
	catagory = relationship(Catagory)

# ORM finishing stuff for SqlAlchemy
engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind = engine)
session = DBSession()
firstCatagory = Catagory(name = "Football")
session.add(firstCatagory)
football = CatalogItem(name = "Football", description = "oblong spheroid generealy made of leather used to play American style Gridiron Football",
					   price = "$50.00", catagory_id = firstCatagory.id, catagory = firstCatagory)
session.add(football)
volleyball = Catagory(name = "Volleyball")
session.add(volleyball)
vb_net = CatalogItem(name = "Volleyball Net", description = "Net used to seperate sides of the court for Volleyball or badmitton",
					   price = "$100.00", catagory_id = volleyball.id, catagory = volleyball)
session.add(vb_net)
volley_ball = CatalogItem(name = "Volleyball", description = "Ball for batting around above a net",
					   price = "$30.00", catagory_id = volleyball.id, catagory = volleyball)
session.add(volley_ball)
session.commit()