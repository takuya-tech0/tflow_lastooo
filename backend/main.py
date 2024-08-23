# main.py
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from auth import SECRET_KEY, ALGORITHM, authenticate_user, create_access_token
from utils import (
    get_all_employee_data, get_all_job_posts, prepare_recommendation_data, generate_recommendations,
    get_employee_vector, get_all_job_post_vectors, get_top_similar_jobs,
    get_job_details, EmployeeVectorNotFound
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
        user = db.query(models.Employee).filter(models.Employee.name == username).first()
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
    access_token = create_access_token(data={"sub": user.name})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user: models.Employee = Depends(get_current_user), db: Session = Depends(get_db)):
    employee_data = get_all_employee_data(db, current_user)
    if employee_data is None:
        raise HTTPException(status_code=500, detail="Error retrieving employee data")
    return employee_data

# main.py の recommend_jobs エンドポイントを更新
@app.post("/recommendations")
async def recommend_jobs(current_user: models.Employee = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        # データ取得部分
        employee_vector = get_employee_vector(db, current_user.employee_id)
        job_post_vectors = get_all_job_post_vectors(db)
        
        if not job_post_vectors:
            raise HTTPException(status_code=500, detail="No job vectors found")
            
        # パーセンテージで類似度を取得
        top_job_ids = get_top_similar_jobs(employee_vector, job_post_vectors, return_percentage=True)
        
        if not top_job_ids:
            raise HTTPException(status_code=500, detail="No top job recommendations found")
        
        # デバッグ用: top_job_idsの内容を確認
        print("Top Job IDs:", top_job_ids)
        
        top_jobs = get_job_details(db, [job['job_id'] for job in top_job_ids])
        
        # デバッグ用: top_jobsの内容を確認
        print("Top Jobs:", top_jobs)

        if not top_jobs:
            raise HTTPException(status_code=500, detail="No job details found for the recommended jobs")
        
        employee_data = get_all_employee_data(db, current_user)
        
        if employee_data is None:
            raise HTTPException(status_code=500, detail="Error retrieving employee data")
        
        # データ準備
        prepared_data = prepare_recommendation_data(employee_data, top_jobs, employee_vector)
        
        # デバッグ用: prepared_dataの内容を確認
        print("Prepared Data:", prepared_data)
        
        # 推薦生成
        recommendations = generate_recommendations(prepared_data)
        
        # デバッグ用: recommendationsの内容を確認
        print("Recommendations:", recommendations)
        
        # 類似度パーセンテージと部門名、スキル名も含めて返す
        for i, job in enumerate(top_jobs):
            job['similarity'] = top_job_ids[i]['similarity']
        
        # デバッグ用: 類似度が追加された top_jobs の確認
        print("Top Jobs with Similarity:", top_jobs)
        
        return {"recommendations": recommendations, "top_jobs": top_jobs}
    
    except EmployeeVectorNotFound:
        print(f"Employee vector not found for employee ID: {current_user.employee_id}")
        raise HTTPException(status_code=404, detail="Employee vector not found")
    
    except Exception as e:
        print(f"Error in job recommendation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in job recommendation: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)