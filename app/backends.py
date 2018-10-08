from django.contrib.auth.hashers import check_password
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from .models import Student, Faculty

User = get_user_model()

class StudentBackend:

    def authenticate(self, request, username=None, password=None):
        if "-" not in username:
            return

        registration_number = username.split("-")

        # get user based on registration_number
        try:
            student = Student.objects.get(batch__name=registration_number[0],
                                          program__name=registration_number[1],
                                          number=registration_number[2])
            user = student.user
            if user:
                # check password of user
                if check_password(password, user.password):
                    return user
            return None

        except Student.DoesNotExist:
            user = User.objects.create_user(username, username, password)
            user.is_superuser = False
            user.is_staff = True
            user.save()
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class FacultyBackend:

    def authenticate(self, request, username=None, password=None):
        # get user based on email
        try:
            user = User.objects.get(email=username)
            if user is not None:
                if user.check_password(password):
                    return user
            return None

        except User.DoesNotExist:
            user = User.objects.create_user(username,username,password)
            user.is_superuser = False
            user.is_staff = True
            user.save()
            return user

    def get_user(self, user_id):
        try:
             return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None