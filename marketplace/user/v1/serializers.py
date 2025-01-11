from marketplace import ma
from marketplace.persistence.model import User

class UserSchema(ma.Schema):
    class Meta:
        model = User
        fields = ('id', 'username', 'fullname', 'phone', 'created_at', 'updated_at')

user_schema = UserSchema()
users_schema = UserSchema(many=True)
