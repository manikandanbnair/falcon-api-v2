import json
from dataclasses import dataclass

from elastic_manager.elastic_manager import ElasticManager
from handler.exception_handler import ValidationException, NotFoundException



@dataclass
class User:
    name: str = None
    age: int = None
    email: str = None


class UserModel:

    _index_name = "users"
    @classmethod
    def create(cls, user:User):
        user_data = user.__dict__
        ElasticManager.insert(user_data,cls._index_name)

    @classmethod
    def find_all(cls):
        users = ElasticManager.find_all(cls._index_name)
        data = list(users)
        if not data:
            raise NotFoundException("No users present")

        for user in data:
            user.pop('_id', None)
        return json.dumps(data)

    @classmethod
    def find_by_email(cls, email):
        user = ElasticManager.find_by_email(email,cls._index_name)
        if not user:
            raise NotFoundException("User not found")
        user.pop('_id',None)
        return json.dumps(user)

    @classmethod
    def exists_by_email(cls, email):
        user = ElasticManager.find_by_email(email,cls._index_name)
        if user:
            return True
        return False

    @classmethod
    def user_validation(cls,age,email):
        if not isinstance(age,int) or age < 0:
            raise ValidationException("Invalid age")
        if cls.exists_by_email(email):
            raise ValidationException("User already exists")


