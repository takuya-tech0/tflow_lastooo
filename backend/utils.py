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
GPT_MODEL = "gpt-4o-mini"
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

def get_employee_vectors(db: Session, employee_id: int) -> Dict[str, List[float]]:
    """
    従業員のcareer_info_vectorとpersonality_vectorを取得する
    
    :param db: データベースセッション
    :param employee_id: 従業員ID
    :return: キャリア情報ベクトルと性格ベクトルの辞書
    :raises EmployeeVectorNotFound: 従業員ベクトルが見つからない場合
    """
    employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if employee is None or employee.career_info_vector is None or employee.personality_vector is None:
        raise EmployeeVectorNotFound(f"Employee vectors not found for id: {employee_id}")
    return {
        "career_info_vector": json.loads(employee.career_info_vector),
        "personality_vector": json.loads(employee.personality_vector)
    }

def get_all_job_post_vectors(db: Session) -> Dict[int, List[float]]:
    """
    全ての求人ポストのベクトルを取得する
    
    :param db: データベースセッション
    :return: 求人IDをキー、ベクトルを値とする辞書
    """
    job_post_vectors = db.query(JobPostVector).all()
    return {jpv.job_post_id: json.loads(jpv.vector) for jpv in job_post_vectors}

def get_top_similar_jobs_for_vectors(employee_vectors: Dict[str, List[float]], job_vectors: Dict[int, List[float]], top_n: int = TOP_N_JOBS, return_percentage: bool = False) -> Dict[str, List[Dict[str, Any]]]:
    """
    キャリア情報ベクトルと性格ベクトルそれぞれについて、最も類似度の高い求人IDとオプションでパーセンテージを取得する
    
    :param employee_vectors: 従業員のキャリア情報ベクトルと性格ベクトルの辞書
    :param job_vectors: 求人ベクトルの辞書
    :param top_n: 取得する上位の数
    :param return_percentage: 類似度をパーセンテージで返すかどうかのフラグ
    :return: キャリア情報と性格それぞれの類似度の高い求人IDのリストとオプションで類似度パーセンテージ
    """
    result = {}
    for vector_type, employee_vector in employee_vectors.items():
        job_ids = list(job_vectors.keys())
        job_vector_array = np.array(list(job_vectors.values()))
        similarities = cosine_similarity([employee_vector], job_vector_array)[0]

        if return_percentage:
            similarities = [round(similarity * 100, 2) for similarity in similarities]

        top_indices = np.argsort(similarities)[-top_n:][::-1]
        result[vector_type] = [
            {
                'job_id': job_ids[i],
                'similarity': similarities[i],
                'vector': job_vectors[job_ids[i]]  # Include the vector
            } for i in top_indices
        ]

    return result

def get_job_details(db: Session, job_ids: List[int]) -> List[Dict[str, Any]]:
    """
    求人IDのリストから求人詳細と部署名を取得する
    
    :param db: データベースセッション
    :param job_ids: 求人IDのリスト
    :return: 求人詳細のリスト（部署名含む）
    """
    jobs = db.query(
        JobPost.job_post_id,
        JobPost.job_title,
        JobPost.job_detail,
        Department.department_name
    ).join(
        Department, JobPost.department_id == Department.department_id
    ).filter(
        JobPost.job_post_id.in_(job_ids)
    ).all()

    # デバッグ用にクエリ結果をログに出力
    print("Job details query result:", jobs)

    # 求人詳細に部署名を含めて返す
    return [
        {
            "job_post_id": job.job_post_id,
            "job_title": job.job_title,
            "job_detail": job.job_detail,
            "department_name": job.department_name
        } 
        for job in jobs
    ]

def prepare_recommendation_data(employee_data: Dict[str, Any], top_jobs: List[Dict[str, Any]], employee_vector: List[float]) -> Dict[str, Any]:
    return {
        "employee_info": {
            "name": employee_data['employee_info']['name'],  # ここを変更
            "skills": [skill['skill_name'] for skill in employee_data['skills']],
            "academic_background": employee_data['employee_info']['academic_background'],
            "recruitment_type": employee_data['employee_info']['recruitment_type']
        },
        "employee_vector": employee_vector,
        "top_jobs": [
            {
                "job_id": job['job_id'],
                "job_title": job['job_title'],
                "department_name": job['department_name'],
                "job_detail": job['job_detail'],
                "similarity": job['similarity'],
                "vector": job['vector']
            } for job in top_jobs
        ]
    }

def generate_recommendations(prepared_data: Dict[str, Any], vector_type: str) -> str:

    employee_vector = json.dumps(prepared_data['employee_vector'], separators=(',', ':'))
    job_information = json.dumps(prepared_data['top_jobs'], separators=(',', ':'))

    base_prompt = f"""
    Employee Vector: {employee_vector}
    Job Information: {job_information}

    Provide your answer in Japanese, using natural, professional language appropriate for a business setting. Your response should paint a vivid picture of how the employee would excel in each role. Use the following format EXACTLY, expressing the information in a conversational, engaging manner:

    1. 推奨求人：求人ID: [ID番号]
       マッチング理由：
       ・[具体的な説明1]
       ・[具体的な説明2]

    2. 推奨求人：求人ID: [ID番号]
       マッチング理由：
       ・[具体的な説明1]
       ・[具体的な説明2]

    3. 推奨求人：求人ID: [ID番号]
       マッチング理由：
       ・[具体的な説明1]
       ・[具体的な説明2]

    4. 推奨求人：求人ID: [ID番号]
       マッチング理由：
       ・[具体的な説明1]
       ・[具体的な説明2]

    5. 推奨求人：求人ID: [ID番号]
       マッチング理由：
       ・[具体的な説明1]
       ・[具体的な説明2]

    DO NOT include any additional text, headers, or formatting outside of this exact structure. Each job recommendation should have exactly two bullet points for matching reasons.

    各推奨求人について、この方の活躍が即座にイメージできるような具体的な推論を用いて説明してください。その方の強みやスキルがどのように職務に貢献するか、どのような場面で特に力を発揮するかなど、具体的なシナリオを交えて説明することで、読み手がその人物の適性を明確にイメージできるようにしてください。ただし、求人のタイトルや詳細な情報は含めず、ベクトル情報のみに基づいて推論してください。
    """

    if vector_type == "career_info_vector":
        specific_prompt = """
        Analyze the provided employee vector and job information to suggest the 5 most suitable job matches based on the employee's career information. For each match, provide specific and detailed reasons focusing on the employee's career experiences, skills, and how they align with the job requirements.

        Consider the following aspects in your analysis:
        - The employee's past work experiences and how they relate to the job requirements
        - Specific skills gained throughout their career and how they apply to the new role
        - Career progression and how the recommended job fits into their career path
        - Any notable achievements or projects that demonstrate their capability for the role

        When explaining the matching reasons, focus on:
        - How the employee's career experiences directly relate to the job responsibilities
        - Specific examples of how their skills can be applied in the new role
        - How their career trajectory aligns with the opportunities presented by the job
        """
    elif vector_type == "personality_vector":
        specific_prompt = """
        Analyze the provided employee vector and job information to suggest the 5 most suitable job matches based on the employee's personality traits. For each match, provide specific and detailed reasons focusing on how the employee's personality aligns with the job requirements and company culture.

        Consider the following aspects in your analysis:
        - The employee's key personality traits and how they benefit the role
        - How their personality would fit into the team and company culture
        - Specific scenarios where their personality traits would be particularly valuable
        - Any potential challenges their personality might face in the role and how to overcome them

        When explaining the matching reasons, focus on:
        - How specific personality traits align with job responsibilities and company values
        - Examples of how their personality can contribute to success in the role
        - How their interpersonal skills and work style match the job requirements
        """
    else:
        raise ValueError(f"Invalid vector type: {vector_type}")

    full_prompt = specific_prompt + base_prompt

    try:
        completion = client.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": "あなたは優秀な人材マッチングの専門家です。従業員の特性と求人の要件を詳細に分析し、最適なマッチングを提案します。ビジネスの場で使用される自然な日本語で、具体的かつ臨場感のある推薦を行ってください。指定された形式を厳密に守り、それ以外の追加のテキストや書式は含めないでください。"},
                {"role": "user", "content": full_prompt}
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
                "name": employee.employee_name,  # ここを変更
                "birthdate": str(employee.birthdate),
                "gender": employee.gender,
                "academic_background": employee.academic_background,
                "hire_date": str(employee.hire_date),
                "recruitment_type": employee.recruitment_type,
                "career_info_detail": employee.career_info_detail,
                "personality_detail": employee.personality_detail
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