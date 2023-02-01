# from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

print('\n############## Initialising tests: ##################\n')
# Create your tests here.


class T01UserRegistration(APITestCase):
    url = reverse('register-user')

    def test_01_register_user_without_email(self):
        """
        Ensure we can create a new account object.
        """
        print("## User registration with missing email field")
        data = {'username': 'Foo', 'password': 'q1w2e3!/'}
        # print(f"input user: {data}")
        response = self.client.post(self.url, data, format='json')

        self.assertEqual("email" in response.data.keys(), True)
        # print(f"Response: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_02_register_user_success(self):
        """
        Ensure a new user is created and the response returns the user data and its token
        """
        print("## User registration success")
        data = {'username': 'Foo', 'password': 'q1w2e3!/',
                'email': 'foo@test.com'}
        # print(f"input user: {data}")
        userOutput = {
            'id': 1,
            'username': 'Foo',
            'email': 'foo@test.com'
        }
        response = self.client.post(self.url, data, format='json')
        # print(f"Response: {response.data}")
        self.assertEqual(response.data["user"], userOutput)
        self.assertEqual(type(response.data["token"]), str)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'Foo')


class T02LoginLogoutTests(APITestCase):
    # API end points for register, login and logout
    registerUrl = reverse('register-user')
    userUrl = reverse('get-current-user')
    loginUrl = reverse('login')
    logoutUrl = reverse('logout')

    # create an user Foo
    userData = {'username': 'Foo', 'password': 'q1w2e3!/',
                'email': 'foo@test.com'}

    def setUp(self):
        # print("# Creating an user for the test")
        response = self.client.post(
            self.registerUrl, self.userData, format='json')
        self.user = response.data['user']
        self.token = response.data['token']
        # print(response.status_code)

        self.headers = {
            "HTTP_AUTHORIZATION": "Token " + self.token
        }

    def test_01_get_user_after_registration(self):

        print("## Get user after registration")

        response = self.client.get(
            self.userUrl, **self.headers, format='json')
        # print(f"Response: {response.data}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
                         k: self.user[k] for k in ['id', 'username', 'email']})

    def test_02_logout(self):
        """
        """
        print("## Logout test")

        response = self.client.post(
            self.logoutUrl, **self.headers, format='json')
        # print(f"Response: {response.data}")

        self.assertEqual(response.status_code,
                         status.HTTP_204_NO_CONTENT)

    def test_03_login(self):
        """
        """
        # print("logging out...")
        self.client.post(
            self.logoutUrl, **self.headers, format='json')

        print("## Login test")
        response = self.client.post(
            self.loginUrl, self.userData, format='json')
        # print(f"Response: {response.data}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(type(response.data['token']), str)
        self.assertEqual(response.data['user'], self.user)

    def test_04_register_another_user_with_same_credentials(self):
        """
        """
        print("# Trying to create an user with existing credentials")
        self.userData["username"] = "bar"
        response = self.client.post(
            self.registerUrl, self.userData, format='json')

        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class T03TokenTests(APITestCase):
    # API end points for register, login and logout
    registerUrl = reverse('register-user')
    userUrl = reverse('get-current-user')
    loginUrl = reverse('login')
    logoutUrl = reverse('logout')
    updateUrl = reverse('update-user')
    changePassUrl = reverse('change-password')

    # create an user Foo
    userData = {'username': 'Foo', 'password': 'q1w2e3!/',
                'email': 'foo@test.com'}

    def setUp(self):
        # print("\n\n# Creating an user for the test\n")
        # register a test user
        response = self.client.post(
            self.registerUrl, self.userData, format='json')
        self.user = response.data['user']
        self.token = response.data['token']
        # print(response.status_code)
        headers = {
            "HTTP_AUTHORIZATION": "Token " + self.token
        }
        # logout
        self.client.post(
            self.logoutUrl, **headers, format='json')

    def test_01_login(self):
        print("## Login and token comparison")
        response = self.client.post(
            self.loginUrl, self.userData, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data['token'], self.token)
        self.assertEqual(response.data['user'], self.user)

    def test_02_get_user_with_new_token(self):
        print("## Get user with new token")
        loginResponse = self.client.post(
            self.loginUrl, self.userData, format='json')
        newToken = loginResponse.data['token']
        headers = {
            "HTTP_AUTHORIZATION": "Token " + newToken
        }
        response = self.client.get(
            self.userUrl, self.userData, **headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
                         k: self.user[k] for k in ['id', 'username', 'email']})

    def test_03_get_user_with_prev_token(self):
        print("## Trying to get user with prev token")
        self.client.post(
            self.loginUrl, self.userData, format='json')
        headers = {
            "HTTP_AUTHORIZATION": "Token " + self.token
        }
        response = self.client.get(
            self.userUrl, self.userData, **headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotEqual(response.data, {
            k: self.user[k] for k in ['id', 'username', 'email']})

    def test_04_get_user_after_logout(self):
        print("## Trying to get user with prev token after logout")
        headers = {
            "HTTP_AUTHORIZATION": "Token " + self.token
        }
        response = self.client.get(
            self.userUrl, self.userData, **headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotEqual(response.data, {
            k: self.user[k] for k in ['id', 'username', 'email']})

    def test_05_update_user_profile_after_logout(self):
        print("## Profile update after logout")
        headers = {
            "HTTP_AUTHORIZATION": "Token " + self.token
        }
        currentUsername = self.user['username']
        self.user['username'] = 'Bar'
        response = self.client.put(
            self.updateUrl, self.user, **headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.patch(
            self.updateUrl, {'username': 'Bar'}, **headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # login and compare username field
        response = self.client.post(
            self.loginUrl, self.userData, format='json')
        self.assertEqual(response.data['user']['username'], currentUsername)

    def test_05_update_user_profile_logged_in(self):
        print("## Profile update logged in")
        # login
        response = self.client.post(
            self.loginUrl, self.userData, format='json')
        self.token = response.data['token']
        headers = {
            "HTTP_AUTHORIZATION": "Token " + self.token
        }

        newName = 'Bar'
        self.userData['username'] = newName
        response = self.client.put(
            self.updateUrl, self.userData, **headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], newName)

        newEmail = 'bar@test.com'
        self.userData['email'] = newEmail
        response = self.client.patch(
            self.updateUrl, {'username': newName, 'email': newEmail}, **headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], newEmail)
        self.assertEqual(response.data['username'], newName)

        # currentPass = self.userData['password']
        newPass = '%ygYgY987896&^^'
        self.userData['password'] = newPass
        response = self.client.put(
            self.updateUrl, self.userData, **headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # try to login with new pass
        response = self.client.post(
            self.loginUrl, self.userData, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class Test04CrossUserAccess(APITestCase):
    # API end points for register, login and logout
    registerUrl = reverse('register-user')
    userUrl = reverse('get-current-user')
    loginUrl = reverse('login')
    logoutUrl = reverse('logout')
    updateUrl = reverse('update-user')
    changePassUrl = reverse('change-password')

    # create an user Foo
    user1Data = {'username': 'Foo', 'password': 'q1w2e3!/',
                 'email': 'foo@test.com'}
    user2Data = {'username': 'Bar', 'password': 'q1w2e3!/',
                 'email': 'bar@test.com'}

    def setUp(self):
        # register test users
        # 1
        response = self.client.post(
            self.registerUrl, self.user1Data, format='json')
        self.user1 = response.data['user']
        # self.token1 = response.data['token']
        # 2
        response = self.client.post(
            self.registerUrl, self.user2Data, format='json')
        self.user2 = response.data['user']
        self.token2 = response.data['token']

        headers = {
            "HTTP_AUTHORIZATION": "Token " + self.token2
        }
        # logout
        self.client.post(
            self.logoutUrl, **headers, format='json')

    def test_01_update_user_with_existing_credentials(self):
        """
        """
        print('## Trying to update the username and email with existing credentials')
        # login
        response = self.client.post(
            self.loginUrl, self.user1Data, format='json')
        self.token = response.data['token']
        headers = {
            "HTTP_AUTHORIZATION": "Token " + self.token
        }

        response = self.client.patch(
            self.updateUrl, {'username': self.user2Data['username']}, **headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.patch(
            self.updateUrl, {'email': self.user2Data['email']}, **headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_02_update_another_user_profile(self):
        """
        """
        print('## Trying to update the profile of another')
        # login
        response = self.client.post(
            self.loginUrl, self.user1Data, format='json')
        self.token = response.data['token']
        headers = {
            "HTTP_AUTHORIZATION": "Token " + self.token
        }

        response = self.client.patch(
            self.userUrl + f"/{self.user2['id']}", {'username': 'fgjhkfjhf'}, **headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.patch(
            f"admin/auth/user/{self.user2['id']}", {'username': 'fgjhkfjhf'}, **headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
