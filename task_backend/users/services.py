from django.db import transaction
from .models import BaseUser, Profile

def create_profile(*, user: BaseUser) -> Profile:
    return Profile.objects.create(user=user)

def create_user(*, phone: str, password: str) -> BaseUser:
    return BaseUser.objects.create_user(phone=phone, password=password)

@transaction.atomic
def register(*, phone: str, password: str) -> BaseUser:
    user = create_user(phone=phone, password=password)
    create_profile(user=user)
    return user

def update_profile(user, first_name, last_name, gender, avatar):
    profile, created = Profile.objects.update_or_create(
        user_id=user,
        defaults={
            'first_name': first_name,
            'last_name': last_name,
            'gender': gender,
            'avatar': avatar,
        }
    )
    return profile
