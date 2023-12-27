from django.test import TestCase
from users.models import CustomUser
from django.urls import reverse
from django.contrib.auth import get_user


class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse("users:register"),
            data={
                "username": "bekhzod",
                "first_name": "Bekxzod",
                "last_name": "Nabijonov",
                "email": "dycfghjh@example.com",
                "password": "examplepassword",
            }
        )

        user = CustomUser.objects.get(username="bekhzod")

        self.assertEqual(user.first_name, "Bekxzod")
        self.assertEqual(user.last_name, "Nabijonov")
        self.assertEqual(user.email, "dycfghjh@example.com")
        self.assertTrue(user.check_password("examplepassword"))

    def test_required_fields(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "first_name": "Bekhzod",
                "email": "bekhzod@gmail.com",
            }
        )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response.context['form'], "username", "This field is required.")
        self.assertFormError(response.context['form'], "username", "This field is required.")


    def test_invalid_email(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "bekhzod",
                "first_name": "Bekxzod",
                "last_name": "Nabijonov",
                "email": "invalid.imail",
                "password": "examplepassword",
            }
        )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response.context['form'], "email", "Enter a valid email address.")
        
    def test_unique_username(self):
        user = CustomUser.objects.create_user(username="bekhzod", password="Bekhzod")
        user.set_password("examplepassword")
        user.save()

        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "bekhzod",
                "first_name": "Bekhzod",
                "last_name": "Nabijonov",
                "email": "dycfghjh@example.com",
                "password": "examplepassword321",
            }
        )
        
        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 1)
        self.assertFormError(response.context['form'], "username", "A user with that username already exists.")


class LoginTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="Bekhzod")
        self.user.set_password("examplepassword")
        self.user.save()

    def test_successfull_login(self):
        self.client.post(
            reverse("users:login"),
            data={
                "username": "Bekhzod",
                "password": "examplepassword"
            }
        )

        user = get_user(self.client)

        self.assertTrue(user.is_authenticated)

    def test_wrong_credentials(self):
        self.client.post(
            reverse("users:login"),
            data={
                "username": "wrong-username",
                "password": "examplepassword"
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

        self.client.post(
            reverse("users:login"),
            data={
                "username": "Bekhzod",
                "password": "wrong-password"
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)
        
    def test_logout(self):
        self.client.login(username="Bekhzod", password="examplepassword")

        self.client.get(reverse("users:logout"))

        user = get_user(self.client)
        self.assertFalse((user.is_authenticated))


class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("users:profile"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("users:login") + "?next=/users/profile/")

    def test_profile_details(self):
        user = CustomUser.objects.create(
            username="Bekhzod",
            first_name="Bekhzod",
            last_name="Nabijonov",
            email="Bekhzod@gmail.com",
            )
        user.set_password("examplepassword")
        user.save()

        self.client.login(username="Bekhzod", password="examplepassword")

        response = self.client.get(reverse("users:profile"))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)


    def test_update_profile(self):
        user = CustomUser.objects.create(
            username="Bekhzod",
            first_name="Bekhzod",
            last_name="Nabijonov",
            email="Bekhzod@gmail.com",
            )
        user.set_password("examplepassword")
        user.save()

        self.client.login(username="Bekhzod", password="examplepassword")

        response = self.client.post(reverse("users:profile-edit"),
                                    data={
                                        'username': "Bek",
                                        'first_name': "Bekhzod",
                                        'last_name': "Nabijonov",
                                        'email': "Bekhzod2@gmail.com"
                                    })
        
        # user = CustomUser.objects.get(id=user.id)
        user.refresh_from_db()

        self.assertEqual(user.username, "Bek")
        self.assertEqual(user.email, "Bekhzod2@gmail.com")
        self.assertEqual(response.url, reverse('users:profile'))
        