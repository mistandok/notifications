"""
Модуль объектов документации swagger.
Создано автоматически модулем `creating_api_documentations.py`
"""

GET_USER_PREFERENCES_LIST_DESCRIPTION = """&emsp;Ручка позволяет получить информацию по предпочтениям для заданных пользовательских идентификаторов.<br>&emsp;Доступна только под правами администратора!<br><br>&emsp;`Args`:<br>&emsp;&emsp;user_ids: список пользователей, по которым необходимо получить информацию. Не более 1000 пользователей за раз.<br>&emsp;&emsp;only_with_events: показывать только тех пользователей, которые подписаны хотябы на одно уведомление.<br><br>&emsp;`Returns`:<br>&emsp;&emsp;list[UserPreferences]<br>  """
DROP_CUSTOM_USER_PREFERENCE_DESCRIPTION = """&emsp;Ручка позволяет отписать пользователя от различных типов уведомлений.<br><br>   `Args`:<br>&emsp;&emsp;body: тело запроса.<br><br>&emsp;`Returns`:<br>&emsp;&emsp;Response<br>  """
UPSERT_USER_PREFERENCES_DESCRIPTION = """&emsp;Ручка позволяет пользователю создавать, добавлять или изменять пользовательские предпочтения.<br><br>&emsp;`Args`:<br>&emsp;&emsp;body: тело запроса.<br><br>&emsp;`Returns`:<br>&emsp;&emsp;IsResponse<br>  """
