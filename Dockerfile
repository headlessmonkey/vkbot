# Установка базового образа
FROM ubuntu



# Установка зависимостей бота
RUN apt-get update
RUN apt-get install -y python3-pip
RUN pip install  vk_api
RUN pip install --upgrade vk_api[keyboard]

COPY . /bot

# Команда, которая будет выполняться при запуске контейнера
ENTRYPOINT ["python3", "probnik.py"]
