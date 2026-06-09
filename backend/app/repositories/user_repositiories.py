from sqlalchemy.orm import Session
from app.models.user import User


class UserRepository:

    def create_user(self, db: Session, user_data):

        user = User(**user_data.model_dump())
        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    def get_user_by_id(self, db: Session, user_id: int):

        return (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    def get_user_by_phone(self, db: Session, phone_number: str):

        return (
            db.query(User)
            .filter(
                User.phone_number == phone_number
            )
            .first()
        )

    def get_all_users(self, db: Session):
        return db.query(User).all()

    def update_user(self, db: Session, user: User, updates: dict):
        for field, value in updates.items():
            setattr(user, field, value)

        db.commit()
        db.refresh(user)
        return user

    def delete_user(self, db: Session, user_id: int):
        user = self.get_user_by_id(db, user_id)

        if not user:
            return None

        db.delete(user)
        db.commit()
        return True
