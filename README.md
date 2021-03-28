# Дипломный проект «Резервное копирование» первого блока «Основы языка программирования Python».

Основная логика программы описана в файле _main.py_. Классы для работы с API Вконтакте
и API Яндекс.Диск вынесены в отдельные файлы.

### API Вконтакте

Методы для работы с API Вконтакте реализованы в отдельном классе _VkApiUser_, который 
описан в отдельном файле _vkapi.py_.

В дипломном задании требовалось сохранение фотографий с максимальным размером. Первоначально
было обнаружено, что у изображений, информация о которых доступна в ответе на метод
_photos.get_, существует список _sizes_, со ссылками на изображения в различных разрешениях.
Прямой взаимосвязи между "type" и фактическим размером изображения установлено не было -
у каких-то изображений были какие-то определённые _"type"_, у других же этих _"type"_ не было.
Поэтому было принятое решение определять изображения с максимальным размером посредством 
определения максимального _"height"_. Но при тестировании оказалось, что для совсем старых
изображений _"height"_ может не существовать. Поэтому в этих случаях, когда _"height"_
нет, всегда берётся последний размер из существующих.

При создании имени файла, в кейсах когда существует более одной фотографии с одинаковым
количеством лайков, по заданию требовалось добавлять к имени файла дату загрузки.
В итоговой реализации дата загрузки берётся из поля _"date"_, получаемого в ответе на
_photos.get_, а затем полученное значение в виде timestamp преобразовывается в соответствующее
удобное для восприятия дату и время вида _ГГГГ-ММ-ДД ЧЧ-ММ-СС_. Для этого была
импортирована библиотека _datetime_. Двоеточия для времени были специально заменены
на пробелы, поскольку для файлов с двоеточиями в имени наблюдались проблемы
при их загрузке на Яндекс.Диск.

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
которые будут сохранены на Яндекс.Диск. А значениями: для _sizes_dict_ - типы
размеров изображений, полученные из API Вконтакте, а для _urls_dict_ - соответствующие
ссылки на изображения в максимально возможном разрешении.

Для реализации дополнительного требования задания о сохранении изображений из 
других альбомов Вконтакте был использован метод API Вконтакте _photos.getAlbums_. В методе 
_get_albums_ класса _VkApiUser_ реализован выбор альбома из списка всех
доступных для того или иного пользователя. Этот метод возвращает идентификатор
альбома, которые далее передаётся в метод _get_photos_.

При тестировании было обнаружено, что с указанным в задании токеном фотографии альбома
"Фотографии со страницы" для указанного в задании юзера 
(https://vk.com/begemot_korovin), доступны в методе _get_photos_, но при попытке
получить список альбомов этого пользователя — ошибка с кодом _15_ и сообщением
_"Access denied"_. Не удалось понять причины такого поведения, вероятно, какие-то
действия в предоставленном токене недоступны, поэтому при возникновении
такой ошибки будет автоматически выбран альбом "Фотографии со страницы" и 
будет выполнена попытка получения фотографий именно из этого альбома.

Также при тестировании было обнаружено, что для альбома "Фотографии с пользователем"
может отдаваться идентификатор _-9000_, но при попытке получения фотографий альбома по этому
идентификатору получаем ошибку с кодом _100_ и сообщением
_"One of the parameters specified was missing or invalid: album_id is invalid"_.
Эту проблему решить не удалось, она ровно также воспроизводится при
выполнении запроса через внутренний сваггер VK Developers.

Если пользователь введёт вместо корректного числа фотографий, которые нужно сохранить,
не число, отрицательное число или дробное, то ему будет показано предупреждение,
но будет выполнена попытка сохранения пяти фотографий, как и требовалось в задании.

### API Яндекс.Диск

Методы для работы с API Яндекс.Диск реализованы в отдельном классе _YaDiskUser_, который 
описан в отдельном файле _yadiskapi.py_.

Метод _upload_ класса _YaDiskUser_ оперирует со словарём. Этот словарь формируется на
основании полученных данных из Вконтакте, ключами в нём являются имена будущих файлов, 
а значениями ссылки на эти файлы в максимально возможном разрешении.

После получения файлов по ссылкам, полученным из API Вконтакте происходит
создание папки _photos_temp_ в корневой директории. Если эта папка уже существует до
начала выполнения программы, то происходит её удаление. При сохранении файлов
на Яндекс.Диск они берутся из этой папки, но после завершения этого действия
папка удаляется со всем содержимым. Для создания папки была импортирована библиотека 
_os_, для удаления папки со всем содержимым — библиотека shutil.

Перед непосредственной загрузкой изображений на Яндекс.Диск в нём предварительно
создаётся папка с уникальным именем. Имя создаваемой папки на Яндекс.Диск представляет 
собой строку содержащую идентификатор пользователя и дату загрузки вида:
_<"идентификатор пользователя Вконтакте> ГГГГ-ММ-ДД ЧЧ-ММ-СС"_. Для этого были
импортированы две библиотеки _time_(для получения текущих даты и времени в
формате timestamp) и _datetime_ (для преобразования timestamp в читаемый
формат). Двоеточия во времени при формировании имени папки для фото на Яндекс.Диск,
как и в случае формирования имени изображений с датой, как уже было сказано ранее,
были заменены на тире из-за того, что Яндекс.Диск почему-то не мог корректно создать папку
с двоеточиями в имени.

### Общие нюансы

Для досрочного завершения программы при возникновении ошибок в различных местах
выполнения кода программы была импортировано библиотека _sys_ и использован метод 
_sys.exit()_, с целью того, чтобы при возникновении ошибки дальнейшая программа не 
выполнялась.

Для отображения прогресса при получении фотографи из Вконтакте, записи информации
об изображениях в json-файл, а также для отображения прогресса загрузки фотографий
на Яндекс.Диск была импортирована библиотека _tqdm_.
