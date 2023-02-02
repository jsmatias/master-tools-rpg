# from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse

# Create your tests here.
SHOW_DETAILS = "summary"  # "complete", "partial", "summary"

# API end points for register, login and logout
registerUrl = reverse('register-user')
userUrl = reverse('get-current-user')
loginUrl = reverse('login')
updateUrl = reverse('update-user')
changePassUrl = reverse('change-password')
logoutUrl = reverse('logout')

npcUrl = reverse('npc-list')
characterUrl = reverse('character-list')
campaignUrl = reverse('campaign-list')
npcCampaignFilterUrl = reverse('campaign-npc')

# Test Users
user1 = {
    "username": "Fion",
    "email": "fion@test.com",
    "password": "q1w2e3!/"
}
user2 = {
    "username": "Marie",
    "email": "Marie@test.com",
    "password": "q1w2e3!/"
}

# Test NPCs
npc1 = {
    "name": "Killy",
    "race": "dwarf",
    "title": "Captain",
    "city": "Mountain",
    "history": "Travelled across the valley to conquer the west",
}

# Test Characters
character1 = {
    "ownerName": "Fion",
    "characterName": "Gerard",
    "race": "human",
    "className": "witcher",
    "armorClass": 20,
    "charisma": 5,
    "constitution": 5,
    "dexterity": 5,
    "intelligence": 5,
    "level": 6,
    "strength": 5,
    "totalhp": 5,
    "wisdom": 5
}

# HTTP config
headers = {
    "content-type": "application/json",
    "HTTP_AUTHORIZATION": "Token " + ""
}


class TestA(APITestCase):
    """Test A - Create NPC and Character
    """

    def __init__(self, *args, **kwargs):
        super(TestA, self).__init__(*args, **kwargs)
        self.headers = headers.copy()

    @staticmethod
    def getinfo(structure, response=None):
        if (response is None) and (SHOW_DETAILS.lower() in ["partial", "complete"]):
            showDetails = "summary"
        else:
            showDetails = SHOW_DETAILS

        match showDetails:
            case "summary":
                msg = structure.__doc__.strip()
            case "partial":
                msg = "\n".join(
                    [structure.__doc__.strip(), f"Status: {response.status_code}"])
            case "complete":
                msg = "\n".join(
                    [structure.__doc__.strip(), f"Status: {response.status_code}", f"RES: {response.data}"])
            case _:
                msg = ""
        print(msg)

    def setUp(self):
        self.user1LoggedRes = self.client.post(
            registerUrl, user1, format='json')
        self.headers.update({"HTTP_AUTHORIZATION": " ".join(
            ["Token", self.user1LoggedRes.data["token"]])})

    def test_01_npc_creation(self):
        """NPC creation
        """
        response = self.client.post(npcUrl, npc1, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.getinfo(self.test_01_npc_creation, response)

    def test_02_character_creation(self):
        """Character creation
        """
        response = self.client.post(characterUrl, character1, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.getinfo(self.test_02_character_creation, response)


class TestB(APITestCase):
    """Test B - Read, Update, and Delete NPCs and Characters
    """

    def __init__(self, *args, **kwargs):
        super(TestB, self).__init__(*args, **kwargs)
        self.user1headers = headers.copy()
        self.user2headers = headers.copy()

    @staticmethod
    def getinfo(structure, response=None):
        if (response is None) and (SHOW_DETAILS.lower() in ["partial", "complete"]):
            showDetails = "summary"
        else:
            showDetails = SHOW_DETAILS
        msg = "\n"
        match showDetails:
            case "summary":
                msg += structure.__doc__.strip()
            case "partial":
                msg += "\n".join(
                    [structure.__doc__.strip(), f"Status: {response.status_code}"])
            case "complete":
                msg += "\n".join(
                    [structure.__doc__.strip(), f"Status: {response.status_code}", f"RES: {response.data}"])
            case _:
                msg = ""
        print(msg)

    def setUp(self):
        # set user1 and create a Npc
        self.user1LoggedRes = self.client.post(
            registerUrl, user1, format='json')
        self.user1headers.update({"HTTP_AUTHORIZATION": " ".join(
            ["Token", self.user1LoggedRes.data["token"]])})
        self.client.post(npcUrl, npc1, **self.user1headers)

        # set user2 and create a character
        self.user2LoggedRes = self.client.post(
            registerUrl, user2, format='json')
        self.user2headers.update({"HTTP_AUTHORIZATION": " ".join(
            ["Token", self.user2LoggedRes.data["token"]])})
        self.client.post(characterUrl, character1, **self.user2headers)

    def test_01_read_npc(self):
        """Read NPC by creator
        """
        response = self.client.get(npcUrl, **self.user1headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        self.getinfo(self.test_01_read_npc, response)

    def test_02_read_npc(self):
        """Read NPC by another user
        """
        response = self.client.get(npcUrl, **self.user2headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        self.getinfo(self.test_02_read_npc, response)

    def test_03_read_character(self):
        """Read character by creator
        """
        response = self.client.get(
            characterUrl, **self.user1headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        self.getinfo(self.test_03_read_character, response)

    def test_04_read_character(self):
        """Read character by another user
        """
        response = self.client.get(
            characterUrl, **self.user2headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        self.getinfo(self.test_04_read_character, response)

    def test_05_update_character(self):
        """Update character by creator
        """
        res = self.client.get(characterUrl, **self.user2headers, format='json')
        url = characterUrl + dict(res.data[0])['id'] + "/"

        character = character1.copy()
        character.update({'characterName': 'Updated ----'})
        response = self.client.put(
            url, data=character, **self.user2headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['characterName'], character['characterName'])

        self.getinfo(self.test_05_update_character, response)

    def test_06_update_npc(self):
        """Update npc by creator
        """
        res = self.client.get(npcUrl, **self.user1headers, format='json')
        url = npcUrl + dict(res.data[0])['id'] + "/"

        npc = npc1.copy()
        npc.update({'name': 'Updated ----'})
        response = self.client.put(
            url, data=npc, **self.user1headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], npc["name"])
        self.getinfo(self.test_06_update_npc, response)
