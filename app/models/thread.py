from db import db

class Thread(db.Model):
    __tablename__ = 'threads'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Unicode())
    
async def create_thread(name):
    thread = await Thread.create(name=name)
    return thread

async def get_all_threads():
    threads = await Thread.query.gino.all()
    return threads