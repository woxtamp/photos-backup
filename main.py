from vkapi import VkApiUser

VK_TOKEN = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
VK_USER_ID = '552934290'
VK_API_VERSION = '5.130'
PHOTOS_COUNT = 5

vkuser = VkApiUser(VK_TOKEN, VK_API_VERSION)
vkuser.get_photos(VK_USER_ID, 'profile', PHOTOS_COUNT)
