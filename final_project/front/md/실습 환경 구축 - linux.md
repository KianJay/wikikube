# 실습 환경 구축



ubuntu-Linux 패키지 관리자 apt 사용하여 설치

설치 및 사용 프로그램 : Virtual Box , vagrant

* Virtual Box : VirtualBox 위에 시스템을 프로비저닝 하여 사용하기 위해 설치
* Vagrant : vagrant 란 vm 관리 서비스 입니다.  code 및 스크립트 작성 된 파일 하나로 vm 생성 할 수 있는 도구 이다.

  


**step1**

**ubuntu-Linux VirtualBox 설치**

***

1. sudo apt update
2. sudo apt install virtualbox



**step2**

**ubuntu-Linux Vagrant설치**

***

1. curl -O https://releases.hashicorp.com/vagrant/2.2.6/vagrant_2.2.6_x86_64.deb
2. sudo apt install ./vagrant_2.2.6_x86_64.deb



**step3**

**Vagrant 설치 여부 확인 및 vm 생성 , 가상 머신 실행 TEST**

***

1. vagrant --version
2. mkdir vagrant-test (테스트 할 폴터 생성)
3. cd vagrant-test   (테스트 할 폴더로 이동)
4. vagrant init <BOX_IMAGE> 
   * (ex) vagrant init ubuntu/focal64)  **Vagrantfile 생성 확인**
5. 설정하고 싶은 설정값 입력
   * (ex) 가상 머신 1대 설치 및 실행 , 도커 설치 , 등등.. 
   * **Vagrantfile 예시**

```
# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|										#Vagrant.configure(“2”)는 Vagrant 2버전을 사용한다.
  config.vm.define "docker-engine" do |ubuntu|							#Vagrant 에서 정의한 가상머신의 이름 
    ubuntu.vm.box = "ubuntu/focal64"									#Vagrant cloud 에서 다운로드 및 실행할 이미지 이름.
    ubuntu.vm.hostname = "docker-engine"								#Ubuntu 에서 사용될 hostname
    ubuntu.vm.network "private_network", ip: "192.168.100.10"			#Vm 네트워크 설정 내부 ip : 192.168.100.10 사용한다.
    ubuntu.vm.provider "virtualbox" do |vb|								#Vagrant의 provider를 정의 vagants는 virtualbox 사용하겠다.
      vb.name   = "docker-engine"										#virtualbox에서 표시할 이름 정의
      vb.cpus   = 2														#virtualbox의 vm에 할당할 cpu 개수
      vb.memory = 2048													#virtualbox의 vm에 할당할 memory 크기
    end																	

    ubuntu.vm.provision "shell", inline: <<-SHELL						#vm이 가동될떄마다 아래의 쉘 명령어 실행
      sudo apt update													#docker 저장소 설정 및 설치(CE)
      sudo apt install -y \												#			.
        apt-transport-https \											#			.
        ca-certificates \												#			.
        curl gnupg lsb-release											#			.
      curl -fsSL https://download.docker.com/linux/ubuntu/gpg \			#Docker의 공식 gpg 키 추가
        | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg			#
      echo \																			#저장소 정보 저장
        "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
        $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
      sudo apt-get update												#
      sudo apt-get install -y docker-ce docker-ce-cli containerd.io		#Docker 설치
      sudo usermod -aG docker vagrant	  #일반 계정이 docker 실행을 하기 위해서는 권한을 가져야 한다. 일반 계정에 docker 실행 권한 부여
    SHELL																				
  end
end

```



