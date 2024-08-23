from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from utils import get_all_job_posts, vectorize_job_post
import json

def update_all_job_vectors():
    db = SessionLocal()
    try:
        job_posts = get_all_job_posts(db)
        for job_post in job_posts:
            job_vector = vectorize_job_post(job_post)
            vector_json = json.dumps(job_vector)
            
            existing_vector = db.query(models.JobPostVector).filter(models.JobPostVector.job_post_id == job_post.job_post_id).first()
            if existing_vector:
                existing_vector.vector = vector_json
            else:
                new_vector = models.JobPostVector(job_post_id=job_post.job_post_id, vector=vector_json)
                db.add(new_vector)
        
        db.commit()
        print("All job post vectors updated successfully.")
    except Exception as e:
        print(f"Error updating job post vectors: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_all_job_vectors()