from pydantic import BaseModel

class Image(BaseModel):
    filename: str
    img_dimensions: str
    encoded_img: str

class Todo(BaseModel):
    title: str
    description: str

