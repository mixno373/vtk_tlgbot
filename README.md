# Telegram CRM для лазертаг клуба

## О чем проект?
Проект студента АСУбз-23-1 Минеева Михаила Владимировича.

Суть проекта заключается в доработке существующего рабочего Telegram бота с целью интеграции
в него CRM-системы для работы с клиентами и автоматизации рабочих процессов менеджера.

Стек технологий:
> - Python v3.9.7
> - PostgreSQL v13.7
> - SQLite
> - Telegram API
> - Unix-server Ubuntu v21.10

## Как использовать?
Администратор бота (инструктор, менеджер) отправляет команды и добавляет, удаляет, редактирует заявки в календаре.


## Техническое задание
### Frontend 
***Bot (telegram)***
> - +++++++++

***Команды бота***
> - /client - Информация о клиенте (поиск, добавить, изменить, удалить <- "reaction button" кнопки)
> - /order - Создание новой заявки
> - /calendar - Просмотр заявок в виде календаря


### Backend  
***Database (Postgres)***  
Используется для хранения постоянной информации о клиентах, заявках и т.д.
  
• crm_clients - Таблица клиентов
| Name | Type | Default value | Description |
| --- | --- | --- | --- |
| uid | int | Autoinc primary key | Идентификатор |
| surname | varchar(20) | ' ' | Фамилия |
| name | varchar(20) | Not null | Имя |
| midname | varchar(20) | ' ' | Отчество |
| phone | varchar(12) | Not null | Номер телефона |
| secondphone | varchar(12) | ' ' | Дополнительный номер телефона |
| description | varchar(100) | ' ' | Примечание |
| from | varchar(25) | ' ' | Откуда узнал |
	


• crm_orders - Таблица заявок
| Name | Type | Default value | Description |
| --- | --- | --- | --- |
| uid | int | Autoinc primary key | Идентификатор |
| client_uid | int | 0 | UID клиента -> crm_clients |
| date | timestamp | timezone('utc', now()) | Дата игры с элементом времени начала |
| gametime | int | 3600 | Время игры, сек. |
| resttime | int | 3600 | Время зоны отдыха после игры, сек. |
| restroom | int | 0 | Номер зоны отдыха (1 либо 2. 0 при отсутствии) |
| players | int | 1 | Количество игроков |
| polygon | varchar(10) | 'arena' | Площадка игры. [arena, park, forest] |
| gametype | varchar(10) | 'birthday' | Тип игры. [game, birthday, quest] |
| gifts | varchar(10) | 'bandana' | Тип подарков. [bandana, bullets, dogtag, snood, without] |
| ..... | ..... | ..... | ..... |
	


***Database (SQLite)***  
Используется для хранения временной информации о диалоге с пользователем:  
текущий статус заполнения данных о клиенте/заявке, временно сохраненные данные ввода пользователя до их переноса в постоянное хранилищие.  
  
• DialogStatuses - Таблица предварительно сохраненной информации о диалоге с пользователем
| Name | Type | Default value | Description |
| --- | --- | --- | --- |
| uid | int | Autoinc primary key | Идентификатор |
| chat_id | text | Unique | Идентификатор чата в Telegram (л/с юзера) |
| status | text | '-' | Статус диалога [-, invite, crm, crm_client, crm_order...] |
| data | text | '-' | Дополнительные данные. Например, идентификатор клиента для обновления данных... |

```python
# Добавить данные диалога (создать/обновить)
def add_dialog_data(chat_id, status: str='-'): pass

# Получить статус диалога и дополнительные данные (при наличии)
def get_dialog_status(chat_id): pass

# Установить статус диалога и дополнительные данные (при наличии)
def set_dialog_status**(chat_id, status, data=''): pass
```
	


***Bot (python telebot)***
> - +++++++++
> - +++++++++
> - +++++++++

 
 ## Предварительные итоги

Реализовано:
> - /client -> возвращает две кнопки (Найти, Добавить)
> - В кнопке "Найти" работает поиск по номеру телефона (основной либо дополнительный) и по имени/фамилии/отчеству/общей слейке
  
 Пример работы функции /client -> "Найти":
![График](https://github.com/mixno373/vtk_tlgbot/blob/main/reports/client_find_1.png?raw=true)  
