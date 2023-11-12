from models import ChatGPT_Threads, engine
from sqlalchemy.orm import sessionmaker


def create_thread(gpt_thread_id, gpt_object, gpt_metadata):
    try:
        thread = ChatGPT_Threads(
            gpt_thread_id=gpt_thread_id,
            gpt_object=gpt_object,
            gpt_metadata=gpt_metadata,
        )
        Session = sessionmaker(bind=engine)
        session = Session()

        session.add(thread)
        session.commit()
        session.close()
        return True
    except Exception as e:
        print(e)
        return False


def get_thread(thread_id):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()

        thread = session.query(ChatGPT_Threads).filter_by(thread_id=thread_id).first()

        session.close()

        return thread
    except Exception as e:
        print(e)
        return None


# if __name__ == "__main__":
#     new_thread = create_thread("test", "test", "test")
