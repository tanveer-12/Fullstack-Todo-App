from fastapi import FastAPI

# creating an instance of fastapi class named 'app'
app = FastAPI()

# root path
# decorator 
@app.get('/')
async def root ():
    return {"message": "Welcome to dailyDo todo app"}