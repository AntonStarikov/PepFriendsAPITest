from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверка запроса api ключа и возврата статуса 200"""

    status, result = pf.get_api_key(email,password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    """ Проверка запроса списка питомцев и возврата не пустого скписка"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Ронни', animal_type='Русская борзая',
                                     age='3', pet_photo='images/Dog1.jpg'):
    """ Проверка добавления питомца с верными данными"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_successful_delete_self_pet():
    """ Проверка возможности удаления питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Боб", "Голубой кот", "4", "images/Dog1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Рон', animal_type='Барбос', age=5):
    """ Проверка возможности обновления информации о питомце"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

def test_getapi_key_for_no_valid_email(email = 'New@rambler.ru', password = valid_password):
    """ Проверка ввода неверного e-mail для получения ключа, статус кода 401"""

    status, result = pf.get_api_key(email, password)
    assert status == 401

def test_add_new_pet_with_no_valid_age(name = 'Кэмел', animal_type = 'верблюд', age = 'вот это чушь', pet_photo = 'images/Dog1.jpg'):
    """ Проверка добавления питомца с вводом нечислового возраста"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400