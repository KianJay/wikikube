### wikikube docker image 생성

---

**docker version : 상관없음**

**docker os: 상관없음**



#### **Step1**

- **Vagrantfile**

```
Vagrant.configure("2") do |config|
config.vm.define "docker-engine" do |ubuntu|
ubuntu.vm.box = "ubuntu/focal64"
ubuntu.vm.hostname = "docker-engine"
ubuntu.vm.network "private_network", ip: "192.168.100.10"
ubuntu.vm.provider "virtualbox" do |vb|
vb.name   = "docker-engine"
vb.cpus   = 2
vb.memory = 2048
end
ubuntu.vm.provision "shell", inline: <<-SHELL
sudo apt update
sudo apt install -y \
apt-transport-https \
ca-certificates \
curl gnupg lsb-release
curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
| sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo \
"deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
$(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io
sudo usermod -aG docker vagrant
SHELL
 end
end
```

<br>

#### Step2

- **소스코드 내려받기**

```
git clone https://github.com/KianJay/wikikube.git 
```

<br>

#### Step3

- **Dockerfile **

```
code Dockerfile

FROM python:3.8
COPY ./wikikube /wikikube
COPY ./requirements.txt .
RUN pip install -r ./requirements.txt
WORKDIR ./wikikube/final_project
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
EXPOSE 8000
```

<br>

#### Step4

- **이미지 생성시 반영하지 않는 (디렉토리 , 파일) 지정하기**

```
cd wikikube     

code .dockerignore
Dockerfile 
venv
```

<br>

#### Step5

- **github action 사용하여 이미지 생성하기**

```
cd .github/workflows

code main.yml

name: wikikube Docker Image Build & Push
on:
  push:
    branches:
      - 'master'
jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - 
        name: Check out repository
        uses: actions/checkout@v2
      -
        name: Set up QEMU
        uses: docker/setup-qemu-action@v1
      -
        name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v1
      -
        name: Login to DockerHub
        uses: docker/login-action@v1 
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
      -
        name: Build & push
        id: docker_build
        uses: docker/build-push-action@v2
        with:
          push: true
          tags: kianjay/wikikube:latest
      -
        name: Image digest
        run: echo ${{ steps.docker_build.outputs.digest }}
```

<br>

#### Step6

- **도커 이미지 생성 확인**

```
git add .
git commit -m "test"
git push
소스 수정 후 push 할때마다 새로운 이미지 생성됨

접속
https://hub.docker.com/
검색
tags: kianjay/wikikube:latest 
```







