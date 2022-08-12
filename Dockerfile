FROM python:3.8

RUN mkdir /bot

WORKDIR /bot

COPY ./ /bot
RUN pip install aiogram
RUN pip install asyncio
RUN pip install requests

CMD python main.py