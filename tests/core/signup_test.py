import pytest
from django.contrib.auth.hashers import make_password
from rest_framework import status


@pytest.mark.django_db
def test_signup(client, user):
    """Тест на регистрацию нового пользователя и хеширование пароля"""
    data = {"username": "test_user",
            "password": "1q2w3eR$",
            "password_repeat": "1q2w3eR$"}

    expected_response = {
        "username": "test_user",
        "first_name": "",
        "last_name": "",
        "email": ""
    }

    response = client.post('/core/signup', data, content_type="application/json")
    expected_response['id'] = response.data['id']

    assert response.status_code == status.HTTP_201_CREATED
    assert user.password != "1q2w3eR$"
    print(user.password)
    assert response.data == expected_response


@pytest.mark.django_db
def test_signup_not_repeated_password(client):
    """Тест на невозможность регистрации при несовпадении указанных паролей"""
    data = {"username": "test_user",
            "password": "2nghdk5od",
            "password_repeat": "1232nghdk5od"}

    response = client.post('/core/signup', data, content_type="application/json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
