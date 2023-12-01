from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Relationship

Base = declarative_base()


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)

    ingredients = Column(Text, nullable=False)

    instructions = Column(Text, nullable=False)

    chef_id = Column(Integer, ForeignKey("chefs.id"))  # many-to-one relationship with chef

    chef = Relationship("Chef", back_populates="recipes")


class Chef(Base):
    __tablename__ = "chefs"

    id = Column(Integer, primary_key=True)

    name = Column(String(50), nullable=False)

    recipes = Relationship("Recipe", back_populates="chef")
