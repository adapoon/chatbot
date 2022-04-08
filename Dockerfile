FROM python
COPY chatbot.py /chatbot.py
COPY requirements.txt /requirements.txt
RUN pip install pip update
RUN pip install -r requirements.txt
ENV ACCESS_TOKEN=
EXPOSE 80
ENTRYPOINT ["python", "/chatbot.py"]
