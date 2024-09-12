from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oath2

router = APIRouter(
    tags=['authentication']
)


# creating a new user , more like signup 
@router.post('/user', status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.User, db: Session = Depends(database.get_db)): 
    # we cannot be passing an unhashed password into the database so we hash the password before sending it to the database
    hashed_pasword = utils.hash_pasword(user.password)
    user.password = hashed_pasword

    # creating a new user 
    new_user = models.User(
        **user.dict()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "new_user": new_user
    }

# login user 

@router.post('/login', status_code=status.HTTP_200_OK)
def login_user(user: schemas.Login, db: Session = Depends(database.get_db)): 
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    # checking if the user with the provided email exist
   
    if not db_user: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'no user exist with provided credentials try creating an account')
    # checking if the provided password is same as the hashed version from the database
    if not utils.verify_password(user.password, db_user.password):
          
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'no user exist with provided credentials try creating an account')
    
    # creating an access token 
    access_token = oath2.create_access_token({"user_id": db_user.id })

    return {
        "access token": access_token
    }


