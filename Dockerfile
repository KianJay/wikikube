FROM python:3.8
RUN mkdir /wikikube
WORKDIR ./wikikube
COPY . .
RUN pip install -r ./requirements.txt
WORKDIR ./final_project
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
EXPOSE 8000