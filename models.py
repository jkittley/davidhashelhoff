from sqlalchemy import Column, Integer, String
from sqlalchemy.types import Date, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Question(Base):
	__tablename__ = 'question'
	id = Column(Integer, primary_key=True)
	datestamp = Column(Date())
	headline = Column(String(160))
	question = Column(String(160))
	answer = Column(String(20))
	solver = Column(String(20))
	solvetime = Column(DateTime())
	status = Column(Integer)

class QuestionOption(Base):
	__tablename__ = 'questionoption'
	id = Column(Integer, primary_key=True)
	number = Column(Integer)
	headline = Column(String(160))
	question = Column(String(160))
	answer = Column(String(20))