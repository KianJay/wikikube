### Vagrant 란

- **Vagrant는 로컬 환경에서 가상화 관리를 가능하게 해주는 훌륭한 도구이다.**

- **도커와 가상화 환경을 로컬에서 시험하고, 프로덕션(상용) 과 유사한 환경을 만들 수 있다**
- **DevOps 도구로 크게 주목받고 있으며, 가상화를 제어하는 메타프로파일은 Ruby언어로 구성되어 있다.**
- **가상화 도구는 Virtual Box, VMware 솔루션, HyperV 등 대부분의 가상화 도구를 지원한다.**

---

<br>

사진 들어갈예정(https://youngmind.tistory.com/entry/Vagrant-%EC%84%A4%EC%B9%98%EC%99%80-%EA%B5%AC%EC%84%B1) 참고

#### 구성요소

1. 하드웨어
2. 운영체제
3. vagrant
4. Image
5. 가상화 도구



<br>

#### Vagrant 명령어

**Vagrant 명령어는 virtual Box 제어할 수 있다.**

---

<br>

**vagrant 설치 버전 확인**

```
vagrant -v
Vagrant 2.2.16
```

<br>

**vm 생성**

```
vagrant init <BOX_IMAGE>
ex) vagrant init ubuntu/focal64
```

<br>

**vm 실행 (vagrant 실행)**

```
vagrant up
```

<br>

**vm 휴먼, 복원**

```
vagrant suspend	#vm 휴면

vagrant resume  #vm 휴면 -> 복원
```

<br>

**vm 재구동**

```
vagrant reload            #vm 전체 재부팅

vagrant reload <VM_NAME>  #지정한 vm 재부팅
```

<br>

**vm 상태 확인**

```
vagrant status   #vagrantfile 에서 정의한 vm 목록 및 상태 확인
```

<br>

**vm ssh 접속**

```
vagrant ssh 		       #vm 1대일 경우 VM_NAME 필요없이 사용가능

vagrant ssh <VM_NAME>	   #vm ssh 접속
```

<br>

**vm 종료**

```
vagrant halt			   #vm 전체 종료

vagrant halt <VM_NAME>     #지정한 vm 종료
```

<br>

**vm 삭제**

```
vagrant destroy            #vm 삭제

vagrant destroy -f         #vm 강제 삭제
```

<br>

**virtual Box 에 설치된 이미지 목록 확인 , 삭제**

```
vagrant box list				  #box 에 설치된 이미지 목록 확인

vagrant box remove <IMAGE_NAME>   #box 에 설치된 이미지 삭제
```

<br>

**해당 주소에 있는 vagrant box 이미지 생성**

```
vagrant box add <name> <url>

ex) vagrant box add centos66  https://github.com/tommy-muehle/puppet-vagrant-boxes/releases/download/1.0.0/centos-6.6-x86_64.box
```

<br>

**vm 프로비저닝**

- **이미 생성한 vm에 추가 패키지 설치 할떄 주로 사용**
- **여러  vm 에 동일한 패키지 설치시 주로 사용 **
- **provision은 vagrant up 을 실행할떄 만들어 지므로 이미 실행 중일때는 vagrant reload -provision 으로 reload 적용**

```
예제
Vagrantfile
  config.vm.provision "shell", inline: <<-SHELL
    # Enable SSH with Password Auth
    sed -i 's/ChallengeResponseAuthentication no/ChallengeResponseAuthentication yes/g' /etc/ssh/sshd_config
    sudo systemctl restart ssh
    # Change Package Repository
    sed -i 's/archive.ubuntu.com/mirror.kakao.com/g' /etc/apt/sources.list
    sed -i 's/security.ubuntu.com/mirror.kakao.com/g' /etc/apt/sources.list
    # Package Index Update
    sudo apt update
    SHELL
    추가 설명 작성
```

