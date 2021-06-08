FROM python:3.8
RUN mkdir /wikikube
WORKDIR ./wikikube
COPY . .
RUN pip install -r ./requirements.txt
WORKDIR ./final_project
EXPOSE 8000