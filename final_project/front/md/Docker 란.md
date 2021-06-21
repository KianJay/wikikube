### Docker 란

- **Linux 커널의 기술로 구현되어 있다.**

---

- **도커는 리눅스 컨테이너를 기반으로 하는 오픈소스 가상화 기술이다.**

- **리눅스 커널 기능을 이용해(네임스페이스, 컨트롤 그룹, 유니온파일시스템) 운영체제 위에 컨테이너들을 생성하는 기술이다.**
- **배포 및 관리를 단순하게 해주는 기술이다.**

<br>

#### Docker의 전체 구조

- Docker 시스템은 크게 **내부와 외부**(Docker Hub)의 구조입니다.
- Docker 시스템은 **Client / Server** 되어있다.

<br>

![image](https://user-images.githubusercontent.com/77868828/122772176-10ba0380-d2e2-11eb-8ca3-e8822626008d.png)

<br>

![image](https://user-images.githubusercontent.com/77868828/122772206-1879a800-d2e2-11eb-9b93-c2743602553e.png)

​														docker의 전체구조( 사진 자료=https://docs.docker.com/engine/docker-overview/)

<br>

**1. client(내부)**

- 실 사용자
- 도커 CLI를 통해 클라이언트에게 명령어를 전달하면, 이를 도커 데몬에게 전달한다.

<br>

**2. docker host - Docker Dameon (내부)**

- 도커 데몬은 빌드, 실행, 배포등 클라이언트에게 받은 명령어를 수행합니다.
- 도커 데몬은 호스트 머신에서 돌아가나 유저가 직접 도커 데몬을 컨트롤 하지는 않습니다.
- docker 서비스를 관리 하기 위해서 다른 데몬과 통신을 수행한다.
- docker API Request를 수신 대기 한다.

<br>

**3.registry (외부)**

- docker에서 사용 할 수 있는 공용 및 퍼블릭 image 저장소 이다.
- client 에서 **pull**(다운르드), **push**(업로드) 명령어를 사용한다.

 <br>

#### Docker 의 작동 구조

<br>

![image](https://user-images.githubusercontent.com/77868828/122772242-216a7980-d2e2-11eb-935b-d46e9ae652df.png)

​																	docker 작동 구조(사진 자료=https://www.slideshare.net/rkawkxms/docker-container)

<br>

- **namespace** (컨테이너를 구획화하는 장치)

  - 하나의 이름 공간에서는 하나의 이름이 단 하나의 개체만을 가리키게 된다.

  - 리눅스에서는 접속한 게스트 별로 독립적인 공간을 제공하고 서로가 충돌하지 않도록 리소스를 격리시키는 namespace 기능을 커널에 내장하고 있다. 

  - **Linux 커널에서 지원하는 6가지 namespace 는 다음과 같다.**

    **Mount namespace**

    - namespace 안에 격리된 파일 시스템 트리 생성
    - namespace 안에서 수행한 마운트는 호스트 OS나 다른 namespace에서는 엑세스 불가
    - 호스트 파일시스템에 구애받지 않고 독립적으로 파일시스템을 추가 삭제 기능 제공

    **PID namespace**

    - PID와 프로세스를 격리한다.
    - namespace가 다른 프로세스끼리는 서로 액세스 할 수 없다.
    - 독립적인 프로세스 공간을 할당 한다.

    **Network namespace**

    - 네트워크 디바이스, IP주소, 포트 번호, 라우팅 테이블, 필터링 테이블 등과 같은 네트워크 리소스를 격리된 namespace 마다 독립적으로 가질 수 있다.
    - namespace 간에 network 충돌을 방지

    **IPC namespace**

    - 프로세스 간의 독립적인 통신통로 할당

    **UTS namespace**

    - namespace별로 호스트명이나 도메인명을 독립적으로 가질 수 있다.

    - 독립적인 hostname 할당

    **UID  namespace**

    - UID/GID를 namespace마다 독립적으로 가질 수 있다.
    - namespace 내부와 호스트 OS 상의 UID/GID가 서로 연결되어 namespace 안과 밖에서 서로 다른 UID/GID를 가질 수 있다.


- **cgroups** (릴리스 관리 장치)

  - 실행 프로세스들의 그룹을 만드는 역할을 수행한다
  - 자원에 대한 제어를 가능하게 해주는 리눅스 커널의 기능이며 아래 리소스들을 제어할 수 있다.
    - 메모리 
    - CPU
    - I/O
    - 네트워크

- **union filesystem**

  - 복수의 파일시스템을 하나의 파일시스템으로 마운트하는 기능이다.
  - 하위 파일시스템에 대한 쓰기 작업은 전략에 따라 복사본을 생성 하여 수행 하여, 원본 파일 시스템은 변하지 않는 것이 특징이다.
  - Union File System 종류 는 아래와  같다.
    - UnionFS
      - Linux, FreeBSD, NetBSD를 위해 초기에 구현된 union filesystem 이다.
    - AUFS
      - 소스코드가 읽기 힘들고 주석이 없어 리눅스 커널에 통합되지 않았다.
    - Overlay
      - AUFS와 비슷한 유니온 파일시스템이다.
      - 리눅스 커널 3.18부터 정식으로 지원한다.

  

