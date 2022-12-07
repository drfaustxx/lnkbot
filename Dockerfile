FROM python:3.8
# set work directory
WORKDIR /app/
# copy project
COPY . /app/
# install dependencies
RUN pip install --user aiogram
RUN pip install --user dotenv
# run app
CMD ["python3", "/app/bot.py"]
