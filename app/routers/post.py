from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import session
from .. import database, schemas, oath2, models

router = APIRouter(
    tags= ['Blog Posts'], 
    prefix= '/posts'

)


@router.get('/')
def get_post(db: session = Depends(database.get_db)): 
    all_posts = db.query(models.Blog).all()

    return {
        "post": all_posts
    }

# creating a blog posts 
@router.post('/')
def create_posts(blog: schemas.Blog, db: session = Depends(database.get_db), logged_user: int = Depends(oath2.current_user)): 

    new_post = models.Blog(
        owner_id = logged_user.id, **blog.dict()
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

# retrieve a particular blog posts by id 

@router.get('/{id}', status_code=status.HTTP_200_OK)
def single_post(id: int, db: session = Depends(database.get_db), loggedin_user: int = Depends(oath2.current_user)): 
    # getting a particular posts from the database based on the ID
    retrieved_posts = db.query(models.Blog).filter(models.Blog.id == id)
    posts = retrieved_posts.first()
    # checking if the posts with the provided ID is found 
    if not posts: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'no post with id: {id} found')
    
    # checking if the logged in user is the owner of the posts 
    if posts.owner_id != loggedin_user.id: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='you are not allowed')
   
    return retrieved_posts

# deleting single post based on ID

@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete_post(id: int, db: session = Depends(database.get_db), logged_in: int = Depends(oath2.current_user)): 

    post = db.query(models.Blog).filter(models.Blog.id == id).first()

    if post == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f' no post found with id: {id}')
    
    # checking posts ownership
    if logged_in.id != post.owner_id: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='you are not allowed to delete this posts')
    
    db.delete(post)
    db.commit()

    return post

# updating a posts based on Id and Ownership
@router.put('/{id}', status_code=status.HTTP_200_OK)
def update_posts(id: int, db: session = Depends(database.get_db), logged_in: int = Depends(oath2.current_user)): 
    posts = db.query(models.Blog).filter(models.Blog.id == id).first()

    if posts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'posts with id {id} not found') 
    
    # check ownership 
    if logged_in.id != posts.owner_id: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='you are not allowed to modify this posts')
    
    for key, value in posts.items.dict(): 
        if value is not None: 
            setattr(posts, key, value)
    db.update(posts)
    db.commit()
    db.refresh(posts)


    return posts






