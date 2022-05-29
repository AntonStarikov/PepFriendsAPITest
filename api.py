import requests

class MultipartEncoder:
    pass

class PetFriends:
    def __init__(self):
        self.base_url = "https://petfriends1.herokuapp.com"

    def get_api_key(self, email, password):

        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url+'/api/key', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key, filter):
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url+'/api/pets', headers=headers, params=filter)

        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result
    def add_new_pet(self, auth_key, data):
        headers = {'auth_key': auth_key['key'], 'Content_Type': data.content_type}
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo,''),'image/jpeg')
            }
        )