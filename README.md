** Запуск **


 ```docker-compose up --build -d```

БД слушает на 54320

Flower слушает на 5555

Rabbit слушает на 5682, веб морда на 15682

Сам сервис слушает на 1337

**Использование:**

    Получить pdf из ссылки:

    curl --request POST --url http://localhost:1337/api/pdf-actions/pdf_for_url/ --header 'Content-Type: application/json' --data '{"url": "https://google.com"}'

    Получить pdf из html:
    curl --request POST --url http://localhost:1337/api/pdf-actions/pdf_for_file/ --header 'Content-Type: multipart/form-data; boundary=---011000010111000001101001' --form html=@/home/user/Downloads/News.html

    Далее сервис даст ссылку, на результат. По этой ссылке будет возвращаться 425, пока файл не будет готов. Когда файл будет готов вернется ссылка на его скачивание.
