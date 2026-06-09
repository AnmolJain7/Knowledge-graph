from app.repositories.user_repositiories import (UserRepository)

repo = UserRepository()


class UserService:

    def create_user(self, db, user_data):

        existing = repo.get_user_by_phone(db, user_data.phone_number)

        if existing:
            raise Exception(
                "Phone number already exists"
            )

        return repo.create_user(db,user_data)

    def get_user(self, db, user_id):
        return repo.get_user_by_id(db, user_id)

    def get_all_users(self,db):
        return repo.get_all_users(db)

    def get_user_by_phone(self, db, phone_number):
        return repo.get_user_by_phone(db, phone_number)

    def update_user(self, db, user_id, user_data):
        existing_user = repo.get_user_by_id(db, user_id)

        if not existing_user:
            return None

        updates = user_data.model_dump(exclude_none=True)

        if "phone_number" in updates:
            duplicate = repo.get_user_by_phone(db, updates["phone_number"])
            if duplicate and duplicate.id != user_id:
                raise Exception("Phone number already exists")

        if not updates:
            return existing_user

        return repo.update_user(db, existing_user, updates)

    def delete_user(self,db,user_id):
        return repo.delete_user(db,user_id)

service = UserService()
