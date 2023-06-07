<a name="readme-top"></a>

Авторы:
 - [Антон](https://github.com/mistandok)
 - [Михаил](https://github.com/Mikhail-Kushnerev)
 - [Илья](https://github.com/Bexram)
 - [Евгений](https://github.com/ME-progr)

<details>
  <summary>
    <h1>Оглавление</h1>
  </summary>
  <ol>
    <li><a href="#репозитории">Репозитории</a></li>
    <li><a href="#описание">Описание</a></li>
    <li><a href="#запуск">Запуск</a></li>
    <li><a href="#список-доступных-урлов">Список доступных урлов</a></li>
    <li><a href="#использование">Использование</a></li>
    <li><a href="#tokens">Токены разных пользователей для работы с сервисами, требующими аутентификацию</a></li>
  </ol>
</details>

## Репозитории
- [Сервис аутентификации](https://github.com/mistandok/auth_service)
- [Сервисы уведомлений и пользовательских предпочтений](https://github.com/mistandok/notifications)


## Описание

Общую архитектуру взаимодействия сервисов можно посмотреть на схеме `notification_architecture_celery.drawio.png`, ее можно найти в папке `./architecture`

В данном спринте реализованы:
- сервис [user_preference](https://github.com/mistandok/notifications_sprint_1/tree/main/user-preferences) для хранения настроек подписок пользователя
- сервис [notify_service](https://github.com/mistandok/notifications_sprint_1/tree/main/notify_service) для управления уведомлениями и их отправкой
- интеграция [notify_service](https://github.com/mistandok/notifications_sprint_1/tree/main/notify_service) с [auth](https://github.com/mistandok/Auth_sprint_1) сервисом (запрос пользовательской информации)
- интеграция [notify_service](https://github.com/mistandok/notifications_sprint_1/tree/main/notify_service) с [user_preference](https://github.com/mistandok/notifications_sprint_1/tree/main/user-preferences) сервисом (запрос пользовательских настроек по подпискам)

## Запуск

Запуск текущих сервисов осуществляется из директории `/docker_app`

1) Старт проекта:

    ```docker
    docker-compose -f docker-compose.prod.yml down -v
    docker-compose -f docker-compose.prod.yml up -d --build
    ```
    Настройка кластера для mongodb
   - ```docker exec -it mongocfg1 bash -c 'mongosh < /scripts/init-configserver.js'```
   - ```docker exec -it mongors1n1 bash -c 'mongosh < /scripts/init-shard01.js'```
   - ```docker exec -it mongors2n1 bash -c 'mongosh < /scripts/init-shard02.js'```
   - ```docker exec -it mongos1 bash -c 'mongosh < /scripts/init-router.js'```

<p align="right"><a href="#readme-top">вверх</a></p>

## Список доступных урлов

  1) [Swagger](http://127.0.0.1/api/openapi) сервиса [user_preference](https://github.com/mistandok/notifications_sprint_1/tree/main/user-preferences). Для проверки API можно использовать токены ниже. Идентификатор пользователей можно получить из токена на сайте [JWT](https://jwt.io/) 
  2) [Django админ панель](http://127.0.0.1:80/admin/) сервиса [notify_service](https://github.com/mistandok/notifications_sprint_1/tree/main/notify_service).

<p align="right"><a href="#readme-top">вверх</a></p>

## Использование

После старта проекта в сервисе авторизации автоматически добавляется пользователь администратора, которому доступны все действия на сервисе. Авторизироваться под ним можно со следующими параметрами входа: `login/password: admin/admin`


### Пайплайн проверки работоспособности сервисов

1) ### Необходимо произвести начальные настройки в админке Django сервиса notify_service (создать типы уведомлений и прикрепить к ним шаблоны.)

   #### Администрирование Django в [админ панели](http://127.0.0.1:80/admin/):
   - для начала работы необходимо завести типы уведомлений. (пример значения поля "слаг": `auth`, `top_film`) и задать им шаблон <br>
     **[В сервисе нотификации](https://github.com/mistandok/notifications_sprint_1/tree/main/notify_service) мы можем работать и создавать любые типы уведомлений, с любым слагом, но у нас есть сервис [user_preference](https://github.com/mistandok/notifications_sprint_1/tree/main/user-preferences), которы  позволяет пользователям подписываться и отписываться от определенных типов событий. Поэтому для проверки работоспособности сервиса лучше завести два типа уведомлений: auth (одиночное уведомление) и top_film (групповое уведомление)**
     - подразумевается, что слаги типов уведомлений синхронизированы с другими сервисами
     - для просмотра типов уведомлений необходимо перейти во вкладку `Типы уведомлений`
     - для добавления нового типа уведомления необходимо нажать на `+ Добавить` слева, напротив вкладки `Типы уведомлений`
       или нажать на `Добавить шаблон +` спрова вверху, если вы уже находитесь во вкладке `Типы уведомлений`
     - для просмотра шаблонов сообщений необходимо перейти во вкладку `Шаблоны`
     - для добавления нового шаблона необходимо нажать на `+ Добавить` слева, напротив вкладки `Шаблоны`
       или нажать на `Добавить шаблон +` спрова вверху, если вы уже находитесь во вкладке `Шаблоны`
       Пример шаблона: <br>
       ```<html><span>Привет, surname! Ваш код для авторизации code.</span></html>```
     - переменные в шаблоне будут автоматически изменены на данные, приходящие от API или сервисов
   
   В таблице уведомлений хранится их история и ошибки отправки
   - для просмотра уведомлений необходимо перейти во вкладку `Уведомления`
     - для добавления нового уведомления необходимо нажать на `+ Добавить` слева, напротив вкладки `Уведомления`
       или нажать на `Добавить шаблон +` спрова вверху, если вы уже находитесь во вкладке `Уведомления`
   
   Раздел рассылок отвечает за периодические рассылки (например, `top_film`)
   - для просмотра рассылок необходимо перейти во вкладку `Рассылки`
     - для добавления новой рассылки необходимо нажать на `+ Добавить` слева, напротив вкладки `Рассылки`
       или нажать на `Добавить шаблон +` спрова вверху, если вы уже находитесь во вкладке `Рассылки`
   
   Вся работа с уведомлениями основана на `Celery` и на `celery-beat`
   - во вкладке `Периодические задачи` необходимо активировать (создать) две периодические задачи: `collect_periodic_mail` и `retry_error_mailing`
     - для просмотра периодических задач необходимо перейти во вкладку `Периодические задачи`
     - для добавления новой периодической задачи необходимо нажать на `+ Добавить` слева, напротив вкладки `Периодические задачи`
       или нажать на `Добавить шаблон +` спрова вверху, если вы уже находитесь во вкладке `Периодические задачи`
   
   ### ВАЖНО!!!

    Для тестирования отправки уведомления можно скопировать html-код из файла `notify_service\auth_template_example.html`, создать тип уведомления авторизация и присвоить ему сохраненный шаблон. В таблице уведомлений создать пустое уведомление с этим типом и выполнить код.
   ```
   from notify.tasks import send_message 
   data = [{'email':'<<почта получателя>>', 'surname': '<<имя получателя>>', 'code': '4343'}] 
   send_message(data, 'mail', <<id созданного уведомления>>)
   ```
   также можно несколько получателей в массив добавить.

   В данный момент при отправке уведомлений вы можете увидеть вот такую ошибку:
   ```Error
   Ошибка на стороне сервиса отправки сообщений:
   (530, b'5.7.0 Authentication Required. Learn more at\n5.7.0  https://support.google.com/mail/?p=WantAuthError u12-20020a2e9b0c000000b002a8b205bb50sm2986820lji.61 - gsmtp', 'None')
   ```
   Сообщение ушло на сервис отправки писем, но мы на нем не регистрировались, поэтому здесь ошибка аутентификации. Можно считать, что сообщение отправлено

2) ###  Необходимо зарегистрировать пользователя, залогиниться под ним, получить его токен, задать ему пользовательские настройки подписки на события и вызвать api, которое запустит процесс формирования уведомления.

   Для того, чтобы это осуществить, достаточно воспользоваться подготовленным файлом postman, который располагается по пути:
   ```Postman
   ./postman_api_examples/notification_pipeline.postman_collection.json
   ```
   Импортируйте его в постман и последовательно выполните вызов предоставленных ручек:
   - произведите вызов **signup** (данные уже внесены)
   - произведите вызов  **login** (данные уже внесены), запомните полученный access_token
   - произведите вызов  **create user preferences** (данные уже внесены, но необходимо вбить актуальный токен, полученный на предыдущем шаге, в авторизацию)
   - извлеките из токена идентификатор пользователя на сайте [JWT](https://jwt.io/). Он будет лежать в поле user_id
   - произведите вызов **create PERSONAL event in notify service** в поле user_id внесите актуальный идентификатор пользователя. Запустится процесс отправки персонального уведомление для пользователя, можно посмотреть в админке.
   - произведите вызов **create GROUP event in notify service** (данные уже внесены). Запустится процесс отправки группового уведомление для пользователя
   



<p align="right"><a href="#readme-top">вверх</a></p>

  <details>
    <summary>
      <h3>
        Токены разных пользователей для работы с сервисами, требующими аутентификацию:
      </h3>
      <a name="tokens"></a>
    </summary>
    1) <b>АДМИН: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjc5NzM1ODI5LCJqdGkiOiJiODRkZDA2Zi03MDMxLTRmZTQtOTA4OC1lZDIxMzcwYjkyNjgiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjp7InVzZXJfaWQiOiJkZmM3Y2I3YS0yNTlhLTQ2MDktYmU0NS0wODdkMzA5ZDU0NWMiLCJ1c2VyX3JvbGVzIjpbImFkbWluIl0sInVzZXJfYWdlbnQiOiJtb2JpbGUiLCJyZWZyZXNoX2p0aSI6IjljZDdhZWVlLWMzOTMtNGQ3NC1iMGU2LWUyZTZiMDg0ZWE1MCJ9LCJuYmYiOjE2Nzk3MzU4MjksImV4cCI6MTY3OTc0MzAyOX0.EmLwK_Riuhf03iOkeDhpXWk8CFcZtfZ_tCnRRjsd9Nw</b> </br>
    2) eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjc5NzM1ODY4LCJqdGkiOiIwMmJkNDdmMy1iY2NmLTRkY2ItYWY1OS1jODhmYTI3M2JjYTMiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjp7InVzZXJfaWQiOiIwNmY1YmRkZS00ZjUwLTQ5NTYtYTQ5ZC1hZTA3Mzc5ODA5YjYiLCJ1c2VyX3JvbGVzIjpbInVzZXIiXSwidXNlcl9hZ2VudCI6Im1vYmlsZSIsInJlZnJlc2hfanRpIjoiMWNlZWYwZmMtYjBmZi00MGUyLTg1N2QtOTk1OWRlNjA0ZDFlIn0sIm5iZiI6MTY3OTczNTg2OCwiZXhwIjoxNjc5NzQzMDY4fQ.y8u7zzHHNl-jxkFkhObe63Lqe9Hv0Hn2WR15Q-fX6t4 </br>
    3) eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjc5NzM1OTE2LCJqdGkiOiIwZTRjNTdmMC00NmNjLTQxYjktOTBiZS01M2Y5ODk5YjQ1ZjQiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjp7InVzZXJfaWQiOiI5ODY1Nzg1ZS05MDQzLTQwMmEtOGU0YS01ODM3OGY5ZDQ0MjgiLCJ1c2VyX3JvbGVzIjpbInVzZXIiXSwidXNlcl9hZ2VudCI6Im1vYmlsZSIsInJlZnJlc2hfanRpIjoiMzlmZDc3YTAtOTdjMC00OTk1LWIzNDUtZDkzODA2MTA2MzJhIn0sIm5iZiI6MTY3OTczNTkxNiwiZXhwIjoxNjc5NzQzMTE2fQ.SWq1TTRZisARXM3NlCocsUCDh8FAU1_0vsPCHBvm4w0 </br>
    4) eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjc5NzM1OTQ4LCJqdGkiOiJhNWY5MDA3ZS1lOWI5LTRhM2ItODk4OC03ZWQ3ODhjOTg4ZjciLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjp7InVzZXJfaWQiOiIzM2NiZjRhNy02ZGFlLTQ4NmItYjk2My0xNjcyYTU4MTg5NGQiLCJ1c2VyX3JvbGVzIjpbInVzZXIiXSwidXNlcl9hZ2VudCI6Im1vYmlsZSIsInJlZnJlc2hfanRpIjoiMzgxMWU5MGItNGEzZC00ZDFmLWE5ZDktMmY3NzUyMTM1YzI1In0sIm5iZiI6MTY3OTczNTk0OCwiZXhwIjoxNjc5NzQzMTQ4fQ.kPrHu2S1sQbwTeUFnur7mTPG4K7fRgKCDWkHhYbh7E4 </br>
    5) <b>АДМИН-AUTH:</b> eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjgyNTQxMzM2LCJqdGkiOiI3ZDZkNDBlYy01ODk1LTQwMTEtOTJmMS1jM2JiM2QzNGMxN2IiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjp7InVzZXJfaWQiOiIzMTdkOGM1MC1kZWRiLTRlZTktOGMyMC02N2I2YmQwMWUxNDAiLCJ1c2VyX3JvbGVzIjpbImFkbWluIl0sInVzZXJfYWdlbnQiOiJndWVzdF9wYyIsInJlZnJlc2hfanRpIjoiMjk4MDk4MGEtNDhkMy00ZmRhLWIxMzktMjkzZGJiZGNhOTVmIn0sIm5iZiI6MTY4MjU0MTMzNn0.F5vQTFkOkIuSvD11XiwKq-lKi5oJhEMPEKfTUuOLlGU </br>
  </details>

<p align="right"><a href="#readme-top">вверх</a></p>
