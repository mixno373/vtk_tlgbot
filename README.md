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
> - ***

***Команды бота***
> - /client - Информация о клиенте (поиск, добавить, изменить, удалить <- "reaction button" кнопки)
> - /order - Создание новой заявки
> - /calendar - Просмотр заявок в виде календаря


### Backend  
***Database (Postgres)***  
• crm_clients - Таблица клиентов
| Name | Type | Default value | Description |
| --- | --- | --- | --- |
| uid | int | Autoinc primary key | Идентификатор |
| surname | varchar(20) | '' | Фамилия |
| name | varchar(20) | Not null | Имя |
| midname | varchar(20) | '' | Отчество |
| phone | varchar(12) | Not null | Номер телефона |
| secondphone | varchar(12) | '' | Дополнительный номер телефона |
| description | varchar(100) | '' | Примечание |
| from | varchar(25) | '' | Откуда узнал |
  
• crm_orders - Таблица заявок
| Name | Type | Description |
| --- | --- | --- |
| uid | int | Идентификатор |
| client_uid | int | Autoinc primary key | UID клиента -> crm_clients |
| date | timestamp | timezone('utc'::text, now()) | Дата игры |
| ..... | ..... | ..... | ..... |

***Database (SQLite)***
> - +++++++++
> - +++++++++
> - +++++++++

***Bot (python telebot)***
> - +++++++++
> - +++++++++
> - +++++++++

 
