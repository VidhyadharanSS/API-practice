from fastapi import FastAPI, Depends, HTTPException, status, Response
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

@app.post('/blog', status_code = 201)
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

@app.get('/blog/{id}', status_code=200)
def show(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status = 'Not found' , detail = 'Blog with {id} id not available')
    return blog

@app.delete('/blog/{id}', status_code = 204)
def destroy(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'Blog with the id {id} not found')
    blog.delete(synchronize_session = False)
    db.commit()
    return {'deletion done'}

@app.put('/blog/{id}', status_code = 202)
def update(id, blog: schema.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'Blog with the id {id} not found')
    blog.update(blog)   
    db.commit()
    return {'Updated'}

