from sqlalchemy import Column, Integer, String, DateTime, Text, create_engine
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base
import toml

Base = declarative_base()

DATABASE_URI = toml.load("./config.toml")["dbConnectionString"]


class ChatGPT_Threads(Base):
    __tablename__ = "ChatGPT_Threads"

    thread_id = Column(Integer, primary_key=True, autoincrement=True)
    gpt_thread_id = Column(String(255))
    gpt_object = Column(String(10), default="thread")
    createdAt = Column(DateTime, default=func.now())
    gpt_metadata = Column(Text)


class ChatGPT_Assistants(Base):
    __tablename__ = "ChatGPT_Assistants"

    asst_id = Column(Integer, primary_key=True, autoincrement=True)
    gpt_asst_id = Column(Text, nullable=False)
    gpt_name = Column(String(255), nullable=False)
    gpt_model = Column(String(50), nullable=False)
    createdAt = Column(DateTime, default=func.now())
    lastUpdatedAt = Column(DateTime, default=func.now(), onupdate=func.now())
    gpt_description = Column(String(255))
    gpt_object = Column(Text)
    gpt_instructions = Column(Text)


# Replace 'DATABASE_URI' with your actual database URI
engine = create_engine(DATABASE_URI)
Base.metadata.create_all(engine)
