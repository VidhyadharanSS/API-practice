from fastapi import FastAPI, Depends, HTTPException
from blog import schema, models
from blog.database import engine, SessionLocal
from sqlalchemy.orm import Session  

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

@app.post('/blog')
def create(blog: schema.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title = blog.title, body=blog.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog')
def all(db: Session = Depends(get_db)):
    blog = db.query(models.Blog).all()
    return blog

@app.get('/blog/{id}')
def show(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    return blog