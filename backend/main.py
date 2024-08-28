# main.py
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from auth import SECRET_KEY, ALGORITHM, authenticate_user, create_access_token
from utils import (
    get_employee_vectors,  # get_employee_vector から変更
    get_all_job_post_vectors,
    get_top_similar_jobs_for_vectors,  # この関数名も更新されている可能性があります
    get_job_details,
    prepare_recommendation_data,
    generate_recommendations,
    get_all_employee_data
)
from database import get_db, engine
import models

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=400, detail="Invalid authentication credentials")
        user = db.query(models.Employee).filter(models.Employee.employee_name == username).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ユーザー名またはパスワードが正しくありません",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.employee_name})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user: models.Employee = Depends(get_current_user), db: Session = Depends(get_db)):
    employee_data = get_all_employee_data(db, current_user)
    if employee_data is None:
        raise HTTPException(status_code=500, detail="Error retrieving employee data")
    return employee_data

# main.py
@app.post("/recommendations")
async def recommend_jobs(current_user: models.Employee = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        employee_vectors = get_employee_vectors(db, current_user.employee_id)
        job_post_vectors = get_all_job_post_vectors(db)

        if not job_post_vectors:
            raise HTTPException(status_code=404, detail="No job vectors found")

        top_job_ids = get_top_similar_jobs_for_vectors(employee_vectors, job_post_vectors, return_percentage=True)

        if not top_job_ids:
            raise HTTPException(status_code=404, detail="No top job recommendations found")

        recommendations = {}
        top_jobs = {}
        for vector_type, jobs in top_job_ids.items():
            job_ids = [job['job_id'] for job in jobs]
            job_details = get_job_details(db, job_ids)
            
            # Combine job details with similarity scores
            combined_jobs = []
            for job in jobs:
                job_detail = next((detail for detail in job_details if detail['job_post_id'] == job['job_id']), None)
                if job_detail:
                    combined_job = {
                        **job,
                        'job_title': job_detail['job_title'],
                        'department_name': job_detail['department_name'],
                        'job_detail': job_detail['job_detail']
                    }
                    combined_jobs.append(combined_job)

            employee_data = get_all_employee_data(db, current_user)

            if employee_data is None:
                raise HTTPException(status_code=404, detail="Error retrieving employee data")

            prepared_data = prepare_recommendation_data(employee_data, combined_jobs, employee_vectors[vector_type])

            recommendations[vector_type] = generate_recommendations(prepared_data, vector_type)

            top_jobs[vector_type] = combined_jobs

        return {"recommendations": recommendations, "top_jobs": top_jobs}

    except Exception as e:
        print(f"Error in job recommendation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in job recommendation: {str(e)}")   


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)