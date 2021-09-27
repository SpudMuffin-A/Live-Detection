import io
import numpy as np
import cv2 as cv
import base64
from starlette import responses
from starlette.responses import StreamingResponse
from model import Image, Todo
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from db import (
    fetch_one_todo,
    fetch_all_todos,
    create_todo,
    update_todo,
    remove_todo,

)

app = FastAPI()

# vector = cv.imread('/Users/Manjiri1/OpenCV/photos/ im1.jpeg')

origins = ['https://localhost:3000']

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/")
def read_root():
    return {"ping":"pong"}

@app.get("/api/todo")
async def get_todo():
    response = await fetch_all_todos()
    return response

@app.get("/api/todo{title}", response_model=Todo)
async def get_todo_by_id(title):
    response = await fetch_one_todo(title)
    if response:
        return response
    raise HTTPException(404, 'no TODO item')

@app.post("/api/todo", response_model=Todo)
async def post_todo(todo:Todo):
    response = await create_todo(todo.dict())
    if response:
        return response
    raise HTTPException(400, "bad request")

# @app.post('/api/image/')
# async def image(*, vector, todo:Todo):
#     res, im_jpg = cv.imencode('.jpeg', vector)
#     StreamingResponse = await create_todo(todo.dict())
#     return StreamingResponse(io.BytesIO(im_jpg.tobytes()), media_type='image/jpeg')

# @app.post('/api/todo/', response_model=Image)
# async def image(file: UploadFile = File('/Users/Manjiri1/OpenCV/photos/ im1.jpeg')):
#     response = await create_todo(todo.dict())
#     contents = await file.read()
#     nparr = np.fromstring(contents, np.uint8)
#     img = cv.imdecode(nparr, cv.IMREAD_COLOR)

#     img_dimensions = str(img.shape)
#     encoded_img = base64.b64encode(img)

@app.post('/api/image', response_model=Image)
async def image(Images: UploadFile = File('/Users/Manjiri1/OpenCV/photos/ im1.jpeg')):
    response = await create_img(Images.dict())
    if response:
        return response
    raise HTTPException(400, "bad request")

@app.put("/api/todo{title}", response_model=Todo)
async def put_todo(title:str, desc:str):
    response = await update_todo(title, desc)
    if response:
        return response
    raise HTTPException(404, 'no TODO item')

@app.delete("/api/todo{title}")
async def delete_todo(title):
    response = await remove_todo(title)
    if response:
        return "Deleted item"
    raise HTTPException(404, 'no TODO item')
