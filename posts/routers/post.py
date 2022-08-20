from posts import schemas, models
from fastapi import status, Depends, HTTPException, APIRouter, Response
from sqlalchemy.orm import Session
from posts.database import get_db
from typing import List, Optional
from posts import oauth2
from sqlalchemy import func


router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)


# @router.get("/", response_model=List[schemas.Post])
# def get_posts(db: Session = Depends(get_db),
#               get_current_user: int = Depends(oauth2.get_current_user)):
#
#     # all existing post in the system
#     posts = db.query(models.Post).all()
#
#     # only post of logged in user
#     # posts = db.query(models.Post).filter(models.Post.owner_id == get_current_user.id).all()
#
#     return posts

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),
              get_current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ''):

    # all existing post in the system without voting
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # join - inner join by default
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).\
        join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).\
        group_by(models.Post.id).\
        filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()



    # only post of logged in user
    # posts = db.query(models.Post).filter(models.Post.owner_id == get_current_user.id).all()

    return results

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
                 get_current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(f'''INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * ''',
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(owner_id=get_current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post_by_id(id: int, db: Session = Depends(get_db),
                   get_current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(f'''SELECT * FROM posts WHERE id = (%s)''', (str(id),))
    # post = cursor.fetchone()
    # post without voting
    #post = db.query(models.Post).filter(models.Post.id == id).first()

    # query with the voting count
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).\
        join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).\
        group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")

    # if post.owner_id != get_current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail='Not authorized to perform this action')

    return post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db),
                 get_current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute('''DELETE FROM posts WHERE id = (%s) RETURNING * ''', (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")

    if post.owner_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Not authorized to perform this action')

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_posts(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),
                 get_current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute('''UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *''',
    #                (post.title, post.content, post.published, str(id),))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_update = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_update.first()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")

    if updated_post.owner_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Not authorized to perform this action')

    post_update.update(post.dict(), synchronize_session=False)

    db.commit()

    return post_update.first()
