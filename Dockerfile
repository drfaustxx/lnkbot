FROM python:3.9.5 as base_image
# set work directory
WORKDIR /app
ENV PYTHONPATH=/app
# copy project
COPY . /app
# install dependencies
RUN pip install --user aiogram
RUN pip install --user python-dotenv

FROM base_image as client
CMD [ "python", "app/bot.py"]

