from vkapi import VkApiUser


VK_TOKEN = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
VK_API_VERSION = '5.130'


vk_user_id = input('Введите идентификатор пользователя Вконтакте: ')
if not vk_user_id.isdecimal():
    print("Ошибка! Введено не число, отрицательное число или число не целое!")
else:
    vkuser = VkApiUser(VK_TOKEN, VK_API_VERSION)
    album_id = vkuser.get_albums(vk_user_id)
    photos_count = input('Введите число фотографий, которые вы хотите сохранить на Яндекс.Диск: ')
    if photos_count == 0:
        print('Ошибка! Вы не можете сохранить 0 фотографий!')
    if not photos_count.isdecimal():
        print("Введено не число, отрицательное число или число не целое! Будет сохранено 5 фотографий.")
        vkuser = VkApiUser(VK_TOKEN, VK_API_VERSION)
        vkuser.get_photos(vk_user_id)
    else:
        photos_count = int(photos_count)
        vkuser = VkApiUser(VK_TOKEN, VK_API_VERSION)
        vkuser.get_photos(vk_user_id, album_id, photos_count)

