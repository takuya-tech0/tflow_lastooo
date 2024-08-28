# main.py
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.params import Body
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from auth import SECRET_KEY, ALGORITHM, authenticate_user, create_access_token
from utils import (
    get_employee_vectors,
    get_all_job_post_vectors,
    get_top_similar_jobs_for_vectors,
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

# main. py
@app.post("/recommendations")
async def recommend_jobs(
    current_user: models.Employee = Depends(get_current_user),
    db: Session = Depends(get_db),
    vector_type: str = Body(..., embed=True)
):
    try:
        employee_vectors = get_employee_vectors(db, current_user.employee_id)
        job_post_vectors = get_all_job_post_vectors(db)

        if vector_type not in ["personality", "career"]:
            raise HTTPException(status_code=400, detail="Invalid vector_type")

        if vector_type == "personality":
            vector_to_use = {"personality_vector": employee_vectors["personality_vector"]}
        else:  # career
            vector_to_use = {"career_info_vector": employee_vectors["career_info_vector"]}

        top_job_ids = get_top_similar_jobs_for_vectors(vector_to_use, job_post_vectors, return_percentage=True)

        if not top_job_ids:
            raise HTTPException(status_code=404, detail="No top job recommendations found")

        recommendations = {}
        top_jobs = {}
        for vec_type, jobs in top_job_ids.items():
            job_ids = [job['job_id'] for job in jobs]
            job_details = get_job_details(db, job_ids)
            
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

            prepared_data = prepare_recommendation_data(employee_data, combined_jobs, vector_to_use[vec_type])

            recommendations[vec_type] = generate_recommendations(prepared_data, vec_type)
            top_jobs[vec_type] = combined_jobs

        return {"recommendations": recommendations, "top_jobs": top_jobs}

    except Exception as e:
        print(f"Error in job recommendation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in job recommendation: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)