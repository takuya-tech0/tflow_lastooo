# utils.py
from openai import OpenAI
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from models import JobPost, JobPostVector, EmployeeVector, Employee, Department, SkillList, RequiredSkill
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from sqlalchemy import func


# 定数
EMBEDDING_MODEL = "text-embedding-ada-002"
GPT_MODEL = "gpt-4o"
TOP_N_JOBS = 5

# 環境変数の読み込み
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class EmployeeVectorNotFound(Exception):
    """従業員ベクトルが見つからない場合の例外"""
    pass

client = OpenAI()
def get_embedding(text, model= EMBEDDING_MODEL):
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding

def get_employee_vector(db: Session, employee_id: int) -> List[float]:
    """
    従業員のベクトルを取得する
    
    :param db: データベースセッション
    :param employee_id: 従業員ID
    :return: 従業員ベクトル
    :raises EmployeeVectorNotFound: 従業員ベクトルが見つからない場合
    """
    employee_vector = db.query(EmployeeVector).filter(EmployeeVector.employee_id == employee_id).first()
    if employee_vector is None:
        raise EmployeeVectorNotFound(f"Employee vector not found for id: {employee_id}")
    return json.loads(employee_vector.vector)

def get_all_job_post_vectors(db: Session) -> Dict[int, List[float]]:
    """
    全ての求人ポストのベクトルを取得する
    
    :param db: データベースセッション
    :return: 求人IDをキー、ベクトルを値とする辞書
    """
    job_post_vectors = db.query(JobPostVector).all()
    return {jpv.job_post_id: json.loads(jpv.vector) for jpv in job_post_vectors}

def get_top_similar_jobs(employee_vector: List[float], job_vectors: Dict[int, List[float]], top_n: int = TOP_N_JOBS, return_percentage: bool = False) -> List[Dict[str, Any]]:
    """
    最も類似度の高い求人IDとオプションでパーセンテージを取得する
    
    :param employee_vector: 従業員ベクトル
    :param job_vectors: 求人ベクトルの辞書
    :param top_n: 取得する上位の数
    :param return_percentage: 類似度をパーセンテージで返すかどうかのフラグ
    :return: 類似度の高い求人IDのリストとオプションで類似度パーセンテージ
    """
    job_ids = list(job_vectors.keys())
    job_vector_array = np.array(list(job_vectors.values()))
    similarities = cosine_similarity([employee_vector], job_vector_array)[0]
    
    # 類似度をパーセンテージに変換
    if return_percentage:
        similarities = [round(similarity * 100, 2) for similarity in similarities]
    
    top_indices = np.argsort(similarities)[-top_n:][::-1]
    
    return [{'job_id': job_ids[i], 'similarity': similarities[i]} for i in top_indices]

def get_job_details(db: Session, job_ids: List[int]) -> List[Dict[str, Any]]:
    """
    求人IDのリストから求人詳細、部署名、複数の必要スキル名を取得する
    
    :param db: データベースセッション
    :param job_ids: 求人IDのリスト
    :return: 求人詳細のリスト（部署名と複数スキル名含む）
    """
    jobs = db.query(
        JobPost.job_post_id,
        JobPost.job_title,
        JobPost.job_detail,
        Department.department_name,
        func.group_concat(SkillList.skill_name).label('skills')  # MySQLのgroup_concatを使用
    ).join(
        Department, JobPost.department_id == Department.department_id
    ).join(
        RequiredSkill, JobPost.job_post_id == RequiredSkill.job_post_id
    ).join(
        SkillList, RequiredSkill.skill_id == SkillList.skill_id
    ).filter(
        JobPost.job_post_id.in_(job_ids)
    ).group_by(
        JobPost.job_post_id, JobPost.job_title, JobPost.job_detail, Department.department_name
    ).all()

    # デバッグ用にクエリ結果をログに出力
    print("Job details query result:", jobs)

    # 求人詳細に部署名とスキル名（カンマ区切りのリスト）を含めて返す
    return [
        {
            "job_post_id": job.job_post_id,
            "job_title": job.job_title,
            "job_detail": job.job_detail,
            "department_name": job.department_name,
            "skills": job.skills.split(",")  # カンマ区切りのスキルをリストに変換
        } 
        for job in jobs
    ]

def prepare_recommendation_data(employee_data: Dict[str, Any], top_jobs: List[Dict[str, Any]], employee_vector: List[float]) -> Dict[str, Any]:
    return {
        "employee_info": {
            "name": employee_data['employee_info']['name'],
            "skills": [skill['skill_name'] for skill in employee_data['skills']],
            "academic_background": employee_data['employee_info']['academic_background'],
            "recruitment_type": employee_data['employee_info']['recruitment_type']
        },
        "employee_vector": employee_vector,  # これは既にOpenAI Embeddingベクトル
        "top_jobs": [
            {
                "job_post_id": job['job_post_id'],
                "job_title": job['job_title'],
                "job_detail": job['job_detail'],
                "department_name": job['department_name'],  # 部署名を追加
                "skills": job['skills']  # スキルリストを追加
            } for job in top_jobs
        ]
    }

def generate_recommendations(prepared_data: Dict[str, Any]) -> str:
    prompt = f"""Analyze the provided employee vector and job information to suggest the 3 most suitable job matches. For each match, provide specific and detailed reasons focusing on the employee's strengths and how they align with the job requirements.

    Employee Vector: {json.dumps(prepared_data['employee_vector'])}
    Job Information: {json.dumps(prepared_data['top_jobs'])}

    Consider both skills and personality traits in your analysis. When discussing personality, focus on strengths and how they contribute to job success. Use concrete examples and scenarios to illustrate how the employee's qualities would be valuable in each role.

    Provide your answer in Japanese, using natural, professional language appropriate for a business setting. Your response should paint a vivid picture of how the employee would excel in each role. Use the following format as a guide, but express the information in a conversational, engaging manner:

    1. 推奨求人：[求人タイトル]（求人ID: [ID番号]）
       マッチング理由：
       ・[具体的なスキルや経験を挙げ、それらがどのように職務で活かされるか、具体的な業務シーンを想像して説明]
       ・[性格や行動特性の強みを挙げ、それらが職場環境や職務遂行にどのように貢献するか、具体的な例を用いて説明]

    2. 推奨求人：[求人タイトル]（求人ID: [ID番号]）
       マッチング理由：
       ・[スキル面での具体的な説明]
       ・[性格面での具体的な説明]

    3. 推奨求人：[求人タイトル]（求人ID: [ID番号]）
       マッチング理由：
       ・[スキル面での具体的な説明]
       ・[性格面での具体的な説明]

    4. 推奨求人：[求人タイトル]（求人ID: [ID番号]）
       マッチング理由：
       ・[スキル面での具体的な説明]
       ・[性格面での具体的な説明]

    5. 推奨求人：[求人タイトル]（求人ID: [ID番号]）
       マッチング理由：
       ・[スキル面での具体的な説明]
       ・[性格面での具体的な説明]

    各推奨求人について、この方の活躍が即座にイメージできるような具体的な推論を用いて説明してください。その方の強みやスキルがどのように職務に貢献するか、どのような場面で特に力を発揮するかなど、具体的なシナリオを交えて説明することで、読み手がその人物の適性を明確にイメージできるようにしてください。"""

    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "あなたは優秀な人材マッチングの専門家です。従業員の特性と求人の要件を詳細に分析し、最適なマッチングを提案します。ビジネスの場で使用される自然な日本語で、具体的かつ臨場感のある推薦を行ってください。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error in API call: {str(e)}"
  
def get_all_employee_data(session: Session, employee: Employee) -> Optional[Dict[str, Any]]:
    try:
        return {
            "employee_info": {
                "id": employee.employee_id,
                "name": employee.name,
                "birthdate": str(employee.birthdate),
                "gender": employee.gender,
                "academic_background": employee.academic_background,
                "hire_date": str(employee.hire_date),
                "recruitment_type": employee.recruitment_type
            },
            "grades": [{"grade_id": g.grade, "grade_name": g.grade_info.grade_name} for g in employee.grades],
            "skills": [{"skill_id": s.skill_id, "skill_name": s.skill.skill_name, "skill_category": s.skill.skill_category} for s in employee.skills],
            "spi": employee.spi.__dict__ if employee.spi else None,
            "evaluations": [{"year": e.evaluation_year, "evaluation": e.evaluation, "comment": e.evaluation_comment} for e in employee.evaluations],
            "departments": [{"department_id": d.department_id, "department_name": d.department.department_name} for d in employee.departments]
        }
    except Exception as e:
        print(f"Error retrieving employee data: {e}")
        return None

def get_all_job_posts(session: Session) -> List[JobPost]:
    """
    全ての求人情報を取得する
    
    :param session: データベースセッション
    :return: JobPostオブジェクトのリスト
    """
    try:
        return session.query(JobPost).all()
    except Exception as e:
        print(f"Error retrieving job posts: {e}")
        return []