FROM python:3.11

RUN useradd -m user

USER root

ENV url=${url}

WORKDIR /home/user

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .
COPY modules/ /home/user/modules/
COPY data/stop_words_french.json /home/user/data/stop_words_french.json
COPY ML/ /home/user/ML/

EXPOSE 5000

CMD ["python", "app.py"]