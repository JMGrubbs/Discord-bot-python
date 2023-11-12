from models import ChatGPT_Assistants, engine
from sqlalchemy.orm import sessionmaker


def create_assistants(
    gpt_asst_id, gpt_name, gpt_model, gpt_description, gpt_object, gpt_instructions
):
    try:
        assistant = ChatGPT_Assistants(
            gpt_asst_id=gpt_asst_id,
            gpt_name=gpt_name,
            gpt_model=gpt_model,
            gpt_description=gpt_description,
            gpt_object=gpt_object,
            gpt_instructions=gpt_instructions,
        )
        Session = sessionmaker(bind=engine)
        session = Session()

        session.add(assistant)
        session.commit()
        session.close()
        return True
    except Exception as e:
        print(e)
        return False


def get_assistant(gpt_asst_id):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()

        assistant = session.query(ChatGPT_Assistants).filter_by(gpt_asst_id=gpt_asst_id).first()

        session.close()

        return assistant
    except Exception as e:
        print(e)
        return None
