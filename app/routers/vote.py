from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, database, models, oath2

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), logged_in: int = Depends(oath2.current_user)): 
    if not db.query(models.Blog.id == vote.post_id).first(): 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {vote.post_id} not found')
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == logged_in.id)
    found_vote = vote_query.first()

    if (vote.dir == 1): 
        if found_vote: 
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'user{logged_in.id} has already voted on the post with id {vote.post_id}')
        new_vote = models.Vote(
            post_id = vote.post_id, 
            user_id = logged_in.id
        )
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return {
            "message": "successfully added vote"
        }
    else: 
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'vote does not exist')
        vote_query.delete()
        db.commit()

        return {
            "message": "deleted vote"
        }

    


        


