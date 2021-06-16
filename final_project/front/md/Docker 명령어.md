### Docker 명령어

---

<br>

#### 현재 사용자를 docker 그룹 추가

- root 계정이 아닌 유저 계정에서 docker 명령어 사용하기 위해 아래 내용 실행

```
$ sudo usermod -aG docker vagrant
```

<br>

#### docker 이미지 관련 명령

```
$ docker images                           # 이미지 조회
$ docker image ls -a                      # 모든 이미지를 표시
$ docker image ls -q                      # 이미지 id만 표시

$ docker search [이미지 이름]               # 도커 허브에 공개되어 있는 이미지 검색

$ docker pull [이미지 이름]:[태그]           # 이미지 가져오기

$ docker build <옵션> <Dockerfile 경로>     # 이미지 생성하기

$ docker image tag [기존 이미지명]:[태그] [새이미지명]:[태그] #이미지 태그 붙이기

$ docker rmi [이미지 id]                    # 이미지 삭제하기
  --f 		                               # 이미지 강제 삭제
  --no-prune                               # 태그가 없는 부모 이미지를 삭제하지 않음
$ docker [] prune [id]                     # 이미지/컨테이너 일괄삭제
  [] : container                           # 중지된 모든 컨테이너 삭제
  [] : image                               # 이름 없는 모든 이미지 삭제
  [] : network                             # 사용되지 않는 도커 네트워크 모두 삭제
  [] : volume                              # 사용하지 않는 모든 도커 볼륨 삭제
```

<br>

#### docker 컨테이너 관련 명령

```
$ docker ps                                # 현재 실행되고 있는 docker의 목록을 조회

docker create [옵션] [이미지 이름]:[태그]   # 컨테이너 생성하기
[옵션]
-i : 입출력
-t : 터미널 활성화하여 bash 쉘을 사용

docker start [이미지 이름]:[태그]           # 컨테이너 실행하기
```

<br>

#### docker system 관련 명령어

```
$ docker system info                     # docker 실행 환경 확인

$ docker system df                       # docker 가 사용하고 있는 disk 이용 상황
```

<br>

#### docker 세부 정보 확인 명령어

```
ex)
$ docker inspect <option> <image or container>  					# 세부정보 출력 사용법
$ docker inspect ubuntu |grep IPAddress   							# 이미지 세부 정보 확인
$ docker inspect -f "{{ .Architecture }} {{ .Os }}" ubuntu:14.04    # 아키텍처와 OS 출력
amd64 linux
$ docker inspect -f "{{ .NetworkSettings.IPAddress }}" hello  		# 컨테이너 IP 주소 출력
172.17.0.85
```

<br>

#### docker 로그인 및 이미지 업로드

```
$ docker login 					# hub.docker 로그인 
$ docker push [이미지]:[태그]	 # hub.docker 이미지 업로드
```

<br>

#### docker 이미지 생성시 수정해야할 파일 : Dockerfile

```
문법 		
FROM  : 어떤 base 이미지를 사용하는 지 기술 
COPY  : 호스트에서 이미지에 파일 추가 
ADD   : 호스트에서 이미지에 파일 추가(tar등 아카이브파일이나 압축파일은 압축을 풀어준다) 
ENTRYPOINT  :  빌드한 이미지를 컨테이너로 생성할때 단 한번 실행(run) 
CMD   : 빌드한 이미지를 생성 및 시작할때 실행(Docker run, start) 단 하나의 CMD만 유효하다 
WORKDIR  : RUN 명령어가 실행되는 위치를 지정하며, 컨테이너의 위치를 지정한다(bash의 cd와 유사합니다)
```

<br>

#### docker 이미지 실행 명령어

```
$ docker run -i t ubuntu
```

<br>

#### 실행중인 컨테이너에 접속 명령어

````
$ docker attach <container name>
````

<br>

#### 외부에서 컨테이너 안의 명령 실행하기

```
$ docker exec <container name> <command>
ex) docker exec test ls -l
```

<br>

#### docker 컨테이너 내부의 로그 확인

```
$ docker logs -t <container ID>          # docker attach 로 접속하여 로그확인할 필요가 없다.
```

