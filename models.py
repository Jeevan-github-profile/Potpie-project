from pydantic import BaseModel
from typing import List


class TopicRequest(BaseModel):
    topic: str


class ResumeRequest(BaseModel):
    resume_text: str


class StudyRequest(BaseModel):
    goal: str


class InterviewQuestions(BaseModel):
    technical: List[str]
    behavioral: List[str]
    system_design: List[str]
