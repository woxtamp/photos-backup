# Дипломный проект «Резервное копирование» первого блока «Основы языка программирования Python».

Неочевидные доделки:
- имя папки на Яндекс диске - с понятным таймстампом текущим

Методы для работы с API Вконтакте реализовал в отдельном классе _VkApiUser_, который 
описан в отдельном файле _vkapi.py_.

В дипломном задании требовалось сохранение фотографий с максимальным размером. Первоначально
было обнаружено, что у изображений, информация о которых доступна в ответе на метод
_photos.get_, существует список _sizes_, со ссылками на изображения в различных разрешениях.
Прямой взаимосвязи между "type" и фактическим размером изображения установлено не было -
у некоторых изображений были определённые _"type"_, у других же этих _"type"_ не было.
Поэтому было принятое решение определять изображение с максимальным размером посредством 
определения максимального _"height"_. Но при тестировании оказалось, что для совсем старых
изображений _"height"_ может не существовать. Поэтому в этих случаях, когда _"height"_
нет, всегда берётся последний размер из существующих.

При создании имени файла, в кейсах когда существует более одной фотографии с одинаковым
количеством лайков, по заданию требовалось добавлять к имени файла дату загрузки.
В итоговой реализации дата загрузки бралась из _"date"_, получаемое в ответе на
_photos.get_, и полученное значение в timestamp преобразовывалось в соответствующие
удобные для восприятия дату и время вида _ГГГГ-ММ-ДД ЧЧ:ММ:СС_. Для этого была
импортирована библиотека _datetime_.


Исходя из того, что API Вконтакте имеет ограничение на количество запросов
с ключом доступа пользователя не чаще 3 раз в секунду, соответствующая задержка
при запросах была добавлена вручную на 0,33 секунды посредством импорта
библиотеки _time_.

При получении каких-либо ошибок со стороны API Вконтакте о невозможности каких-то 
действий (например если профиль пользователя закрыт), реализован вывод таких
ошибок с полученными сообщением и кодом.

Создание json-файла и сохранение в него данных с информацией по файлу реализовано
в методе _get_photos_ класса _VkApiUser_ ещё до загрузки изображений на Яндекс.Диск.
При каждом выполнении программы файл _output.json_либо создаётся заново, либо 
перезаписывается в корневой папке проекта.

В методе _get_photos_ класса _VkApiUser_ формируются два словаря: _sizes_dict_ и 
_urls_dict_. Ключами в обоих словарях являются имена будущих файлов изображений,
которые будут сохранены на Яндекс.Диск. А значениями: для _sizes_dict_ типы
размеров изображений, полученные из API Вконтакте, а для _urls_dict_ - соответствующие
ссылки на изображения в максимально возможном разрешении.

Для реализации требования сохранения из других альбомов Вконтакте был использован
метод API Вконтакте _photos.getAlbums_.

В методе _get_albums_ класса _VkApiUser_ реализован выбор альбома из списка всех
доступных для того или иного пользователя. Этот метод возвращает идентификатор
альбома, которые далее передаётся в метод _get_photos_.

При тестировании было обнаружено, с указанным в задании токеном, фотографии альбома
"Фотографии со страницы" для указанного в задании юзера 
(https://vk.com/begemot_korovin), доступны в методе _get_photos_, но при попытке
получить список альбомов этого пользователя — ошибка с кодом _15_ и сообщением
_"Access denied"_. Не удалось понять причины такого поведения, вероятно, какие-то
действия в предоставленном токене недоступны, поэтому при возникновении
такой ошибки будет автоматически выбран альбом "Фотографии со страницы".


Также при тестировании было обнаружено, что для альбома "Фотографии с пользователем"
отдаётся идентификатор _-9000_, но при попытке получения фотографий альбома по этому
идентификатору получаем ошибку с кодом _100_ и сообщением
_"One of the parameters specified was missing or invalid: album_id is invalid"_.
Эту проблему решить не удалось, она ровно также воспроизводится при
выполнении запроса на сайте Вконтакте.

Для досрочного завершения программы при возникновении ошибок в различных местах
выполнения кода программы была импортировано библиотека _sys_ и использован метод 
_sys.exit()_, с целью того, чтобы при возникновении ошибки дальнейшая программа не 
выполнялась.

Если пользователь ввёл вместо корректного числа фотографий, которые нужно сохранить,
не число, отрицательное число или дробное, то ему будет показано предупреждение,
но будет выполнена попытка сохранения пяти фотографий.

Для отображения прогресса была импортирована библиотека _tqdm_.