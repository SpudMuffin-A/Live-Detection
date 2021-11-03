import numpy as np
import cv2 as cv
import base64
# import face_recog 
# from pydantic.networks import int_domain_regex
# from pydantic.typing import display_as_type
# from starlette import responses
# from starlette.responses import StreamingResponse
from model import Image, Todo, ImageResponse
from fastapi import FastAPI, HTTPException, UploadFile, File, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from db import (
    create_img,
    fetch_img,
    fetch_one_todo,
    fetch_all_todos,
    create_todo,
    update_todo,
    remove_todo,
)

app = FastAPI()
templates = Jinja2Templates(directory="templates/")

origins = ['https://localhost:3000/ ']

app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/")
def read_root():
    return {"ping":"pong"}

# @app.get('/form')
# def form_post(request: Request):
#     result = "Enter name"
#     return templates.TemplateResponse('form.html', context={'request': request, 'result': result})

@app.post('/image')
def show_image(request: Request):
    return templates.TemplateResponse('form.html')

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
#     if response:
#         return response
#     raise HTTPException(400, "bad request")

@app.post('/api/Images')
async def image(Images: UploadFile = File(...)):
    filename = Images.filename
    content = await Images.read() 
    encoded_img = base64.b64encode(content)
    img = {}
    img['filename'] = filename
    img['encoded_img'] = encoded_img
    response = await create_img(img)
    print(len(content))
    print(len(encoded_img))
    if response:
        return response
    raise HTTPException(400, "bad request")

@app.get('/api/Images/{filename}', response_model=ImageResponse)
async def get_image(filename):
    response = await fetch_img(filename)
    i = base64.b64decode(response['encoded_img'])
    # print(i)
    # new_img = cv.imread(i, cv.cvtColor)
    # i = open('img', "rb")
    img = response['encoded_img'].decode('utf-8')
    # return templates.TemplateResponse('image.html')
    # print(img)
    # img_tag = "<img src = data:image/jpg;base64,{0}>".format(sent_img)
    # f = open('image.html', 'w')
    # message = """<html>
    # <head></head>
    # <body>""" + img_tag + """</body>
    # </html>"""
    # print(message)
    # f_name = 'file:///Users/Manjiri1/fastapi/' + 'image.html'
    # webbrowser.open_new_tab(f_name)
    # img = img
    # cv.imshow('Image', img)
    # face_recog.recognize(sent_img)
    # print(img_tag)
    #response['encoded_img'] = img
    return response

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
