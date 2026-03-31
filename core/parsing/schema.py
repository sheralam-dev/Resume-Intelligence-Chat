from pydantic import BaseModel, Field
from typing import List, Optional


# Nested models for detailed resume sections
class ContactInformation(BaseModel):
    email: str = Field(None, description="Email address.")
    phone: Optional[str] = Field(None, description='mobile number eg. +92 03011234567')
    linkedin: Optional[str] = None
    github: Optional[str] = None
    hugging_face: Optional[str] = None
    kaggle: Optional[str] = None


class Education(BaseModel):
    institution: str
    degree: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class Experience(BaseModel):
    title: str = Field(description="Job role/title.")
    company: str = Field(description="Name of the company or organization.")
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class Project(BaseModel):
    name: str = Field(description="Name of a project.")
    description: str = Field(description="Project Description")
    technologies: List[str] = None
    url: Optional[str] = None
    difficulty_score: int = Field(
      ...,
      ge=1,
      le=10,
      description=(
        "Strictly evaluate AI engineering complexity. "
        "1-3: Simple 'wrapper' apps, basic prompting, or out-of-the-box RAG with a single data source. "
        "4-6: Production-grade apps with persistent memory, multi-step tool use (agents), "
        "complex data parsing (PDFs/Tables), or basic fine-tuning for style. "
        "7-8: Advanced architectures featuring multi-agent orchestration, self-healing loops, "
        "complex hybrid search (vector + keyword), or custom evaluation frameworks (LLM-as-a-judge). "
        "9-10: Highly complex, mission-critical systems with real-time streaming, "
        "multi-modal integration, or heavy optimization for cost and latency at scale. "
        "If the project only uses a single API call without complex logic, it must not exceed 3."
        )
    )

# Main AI Developer Resume Schema
class Resume(BaseModel):
    full_name: str = Field(..., description="Full name of the applicant.")
    contact: ContactInformation
    summary: str = Field(..., description="Professional summary focusing on AI/ML.")
    education: Optional[List[Education]] = Field(
            ..., description="List of educational degrees. Return null if not explicitly present."
        )
    experience: Optional[List[Experience]] = Field(
            ..., description="List of experiences. Return null if not explicitly present."
        )
    ai_ml_skills: List[str] = Field(..., description="Specific AI/ML skills (e.g., LLMs, Computer Vision).")
    technical_skills: List[str] = Field(..., description="Programming languages and tools.")
    projects: Optional[List[Project]] = None
    certifications: Optional[List[str]] = None
