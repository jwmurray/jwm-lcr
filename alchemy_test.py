#!/usr/bin/env python3

import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABSE_URI='mysql+mysqlconnector://{user}@{server}/{database}'.format(user='root', server='localhost', database='lcr')

engine = create_engine(DATABSE_URI)
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)

class Eu(Base):
    __tablename__ = 'tabela73'

    id = Column(Integer(), primary_key=True)
    nome = Column(String(200))
    idade = Column(Integer())

    def __init__(self, nome='mel', idade=22):
        self.nome = nome
        self.idade = idade

Base.metadata.create_all() 
# automatically generates a create table: 
#CREATE TABLE tabela73 (
#   id INTEGER NOT NULL, 
#   nome VARCHAR(200), 
#   idade INTEGER, 
#   PRIMARY KEY (id)
#)

eu = Eu()

session = Session()
session.add(eu)
session.commit() # automatically generates the insert:
#INSERT INTO tabela73 (nome, idade) VALUES ('mel', 22)