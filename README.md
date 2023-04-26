## Запуск

Запуск сервиса осуществляется из директории `/docker_app`

- проект:

    ```docker
    docker-compose -f docker-compose.prod.yml down -v
    docker-compose -f docker-compose.prod.yml up -d --build
    ```
    Настройка кластера для mongodb
   - ```docker exec -it mongocfg1 bash -c 'mongosh < /scripts/init-configserver.js'```
   - ```docker exec -it mongors1n1 bash -c 'mongosh < /scripts/init-shard01.js'```
   - ```docker exec -it mongors2n1 bash -c 'mongosh < /scripts/init-shard02.js'```
   - ```docker exec -it mongos1 bash -c 'mongosh < /scripts/init-router.js'```

  
  Сервис и список доступных урлов:
  1) [Сервис user-preferences](http://127.0.0.1/api/openapi). Для проверки API можно использовать токены ниже. Идентификатор пользователей можно получить из токена на сайте [JWT](https://jwt.io/) 

  <details>
    <summary>
      <h3>Токены разных пользователей для работы с сервисами, требующими аутентификацию:</h3>
    </summary>
    1) <b>АДМИН: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjc5NzM1ODI5LCJqdGkiOiJiODRkZDA2Zi03MDMxLTRmZTQtOTA4OC1lZDIxMzcwYjkyNjgiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjp7InVzZXJfaWQiOiJkZmM3Y2I3YS0yNTlhLTQ2MDktYmU0NS0wODdkMzA5ZDU0NWMiLCJ1c2VyX3JvbGVzIjpbImFkbWluIl0sInVzZXJfYWdlbnQiOiJtb2JpbGUiLCJyZWZyZXNoX2p0aSI6IjljZDdhZWVlLWMzOTMtNGQ3NC1iMGU2LWUyZTZiMDg0ZWE1MCJ9LCJuYmYiOjE2Nzk3MzU4MjksImV4cCI6MTY3OTc0MzAyOX0.EmLwK_Riuhf03iOkeDhpXWk8CFcZtfZ_tCnRRjsd9Nw</b> </br>
    2) eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjc5NzM1ODY4LCJqdGkiOiIwMmJkNDdmMy1iY2NmLTRkY2ItYWY1OS1jODhmYTI3M2JjYTMiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjp7InVzZXJfaWQiOiIwNmY1YmRkZS00ZjUwLTQ5NTYtYTQ5ZC1hZTA3Mzc5ODA5YjYiLCJ1c2VyX3JvbGVzIjpbInVzZXIiXSwidXNlcl9hZ2VudCI6Im1vYmlsZSIsInJlZnJlc2hfanRpIjoiMWNlZWYwZmMtYjBmZi00MGUyLTg1N2QtOTk1OWRlNjA0ZDFlIn0sIm5iZiI6MTY3OTczNTg2OCwiZXhwIjoxNjc5NzQzMDY4fQ.y8u7zzHHNl-jxkFkhObe63Lqe9Hv0Hn2WR15Q-fX6t4 </br>
    3) eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjc5NzM1OTE2LCJqdGkiOiIwZTRjNTdmMC00NmNjLTQxYjktOTBiZS01M2Y5ODk5YjQ1ZjQiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjp7InVzZXJfaWQiOiI5ODY1Nzg1ZS05MDQzLTQwMmEtOGU0YS01ODM3OGY5ZDQ0MjgiLCJ1c2VyX3JvbGVzIjpbInVzZXIiXSwidXNlcl9hZ2VudCI6Im1vYmlsZSIsInJlZnJlc2hfanRpIjoiMzlmZDc3YTAtOTdjMC00OTk1LWIzNDUtZDkzODA2MTA2MzJhIn0sIm5iZiI6MTY3OTczNTkxNiwiZXhwIjoxNjc5NzQzMTE2fQ.SWq1TTRZisARXM3NlCocsUCDh8FAU1_0vsPCHBvm4w0 </br>
    4) eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjc5NzM1OTQ4LCJqdGkiOiJhNWY5MDA3ZS1lOWI5LTRhM2ItODk4OC03ZWQ3ODhjOTg4ZjciLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjp7InVzZXJfaWQiOiIzM2NiZjRhNy02ZGFlLTQ4NmItYjk2My0xNjcyYTU4MTg5NGQiLCJ1c2VyX3JvbGVzIjpbInVzZXIiXSwidXNlcl9hZ2VudCI6Im1vYmlsZSIsInJlZnJlc2hfanRpIjoiMzgxMWU5MGItNGEzZC00ZDFmLWE5ZDktMmY3NzUyMTM1YzI1In0sIm5iZiI6MTY3OTczNTk0OCwiZXhwIjoxNjc5NzQzMTQ4fQ.kPrHu2S1sQbwTeUFnur7mTPG4K7fRgKCDWkHhYbh7E4 </br>
    5) <b>АДМИН-AUTH:</b> eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjgyNTQxMzM2LCJqdGkiOiI3ZDZkNDBlYy01ODk1LTQwMTEtOTJmMS1jM2JiM2QzNGMxN2IiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjp7InVzZXJfaWQiOiIzMTdkOGM1MC1kZWRiLTRlZTktOGMyMC02N2I2YmQwMWUxNDAiLCJ1c2VyX3JvbGVzIjpbImFkbWluIl0sInVzZXJfYWdlbnQiOiJndWVzdF9wYyIsInJlZnJlc2hfanRpIjoiMjk4MDk4MGEtNDhkMy00ZmRhLWIxMzktMjkzZGJiZGNhOTVmIn0sIm5iZiI6MTY4MjU0MTMzNn0.F5vQTFkOkIuSvD11XiwKq-lKi5oJhEMPEKfTUuOLlGU </br>
  </details>