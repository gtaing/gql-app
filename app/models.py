from typing import List
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Employer(Base):
    __tablename__ = "employers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    contact_email: Mapped[str] = mapped_column(String)
    industry: Mapped[str] = mapped_column(String)
    jobs: Mapped[List["Job"]] = relationship(back_populates="employer")

    def __repr__(self) -> str:
        return f"Employer(id={self.id}, name={self.name}, contact_email={self.contact_email}, industry={self.industry})"


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    employer_id: Mapped[int] = mapped_column(Integer, ForeignKey("employers.id"))
    employer: Mapped["Employer"] = relationship(back_populates="jobs")

    def __repr__(self) -> str:
        return f"Job(id={self.id}, title={self.title}, description={self.description}, employer_id={self.employer_id})"
