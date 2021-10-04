from model import Todo, Image
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb+srv://Aryan:R9IKl1EXJXDBRGyb@cluster0.d4pmb.mongodb.net/test?authSource=admin&replicaSet=atlas-2tcy9m-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true')

database = client.TodoList
collection = database.todo

db = client.Image_Collection
coll = db.Images

async def fetch_one_todo(title):    
    document = await collection.find_one({"title":title})
    return document

async def fetch_img(filename):
    document = await coll.find_one({'filename': filename})
    return document
    
async def fetch_all_todos():
    todos = []
    cursor = collection.find({})
    async for document in cursor:
        todos.append(Todo(**document))
    return todos

async def create_todo(todo):
    document = todo
    result = await collection.insert_one(document)
    return document

async def create_img(Images):
    doc = Images
    res = await coll.insert_one({'filename':Images['filename'], 'encoded_img': Images['encoded_img']})
    # res = await coll.insert_one({'filename':Images['filename']}, {'encoded_img': 'Test'})
    #res = await coll.insert_one(Images)
    print(res)
    return doc

async def update_todo(title, desc):
    await collection.update_one({"title":title},{"$set":{
        "description":desc
    }})
    document = await collection.find_one({"title":title})
    return document

async def remove_todo(title):
    await collection.delete_one({"title":title})
    return True
