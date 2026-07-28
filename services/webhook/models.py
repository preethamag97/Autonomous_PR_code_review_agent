import uuid
from sqlalchemy import BigInteger, Column, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import TIMESTAMP
from pydantic_settings import BaseSettings

Base = declarative_base()

#below code defines a SQLAlchemy model for a pull request. It represents the structure of the "pull_requests" table in the database, with columns for id, repo_full_name, pr_number, head_sha, installation_id, status, and created_at. The model is used to interact with the database and perform CRUD operations related to pull requests.   
class PullRequest(Base):
    __tablename__ = "pull_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    repo_full_name = Column(Text, nullable=False)
    pr_number = Column(Integer, nullable=False)
    head_sha = Column(Text, nullable=False)
    installation_id = Column(BigInteger, nullable=False)
    status = Column(Text, nullable=False, default="pending")
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://user:password@postgres:5432/codereviewer"
    redis_url: str = "redis://redis:6379/0"

    class Config:
        env_file = ".env"
