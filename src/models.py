from sqlalchemy import BigInteger, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base


class User(Base):
    __tablename__ = "users"

    github_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    login: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    followers: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    following: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    public_repos: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    html_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    repos: Mapped[list["Repo"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )


class Repo(Base):
    __tablename__ = "repos"

    github_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    user_github_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.github_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    stargazers_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    forks_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    language: Mapped[str | None] = mapped_column(String(120), nullable=True)
    html_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    updated_at: Mapped[str | None] = mapped_column(String(50), nullable=True)

    user: Mapped[User] = relationship(back_populates="repos")
