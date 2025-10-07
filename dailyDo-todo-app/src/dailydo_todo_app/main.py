from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Field, create_engine, Session
from dailydo_todo_app import settings
from typing import Annotated


# create model
class Todo (SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    content: str = Field(index=True, min_length=3, max_length=54)
    is_completed : bool = Field(default=False)

# fetching the connec string from the .env file through settings.py
connection_string: str = str(settings.DATABASE_URL).replace("postgresql","postgresql+psycopg")
# creating the engine(one single engine for the entire application), it takes in our db url (db connec string)
engine = create_engine(connection_string, connect_args={"sslmode":"require"}, pool_recycle=300, echo=True)   # sslmode for the encryption over the internet

# creation of table using the engine
SQLModel.metadata.create_all(engine)


# todo1: Todo = Todo(content="first task")
# todo2: Todo = Todo(content="second task")

# # session (sessions can be multiple, unlike engine which can be a single obj only for the entire application)
# # separate session for each functionality / transaction
# session = Session(engine)

# # create todos in database
# session.add(todo1)
# session.add(todo2)
# print(f'before commit {todo1}')
# session.commit()
# print(f'after commit {todo1}')
# session.close()

def get_session():
    with Session(engine) as session:
        yield session





# creating an instance of fastapi class named 'app'
app:   FastAPI = FastAPI()

# root path
# decorator 
@app.get('/')
async def root ():
    return {"message": "Welcome to dailyDo todo app"}


@app.post('/todos/', response_model=Todo)
async def create_todo(todo: Todo, session:Annotated[Session, Depends(get_session)]):
    session.add(todo)
    session.commit() 
    session.refresh(todo)
    return todo


@app.get('/todos/')
async def get_all():
    ...


@app.get('/todos/{id}')
async def get_single_tod():
    ...


@app.put('/todos/{id}')
async def edit_todo():
    ...


@app.delete('/todos/{id}')
async def delete_todo():
    ...