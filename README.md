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
Frontend 
> Bot (telegram)
> - ***
>
> Команды бота
> - /client - Информация о клиенте (поиск, добавить, изменить, удалить <- "reaction button" кнопки)
> - /order - Создание новой заявки
> - /calendar - Просмотр заявок в виде календаря


Backend  
**Database (Postgres)**  
*crm_clients*  
| Name | Type | Description |
| --- | --- || --- |
| uid | int | Идентификатор |
| name | varchar(50) | Название |

> Database (SQLite)
> - +++++++++
> - +++++++++
> - +++++++++
> 
> Bot (python telebot)
> - +++++++++
> - +++++++++
> - +++++++++

 
