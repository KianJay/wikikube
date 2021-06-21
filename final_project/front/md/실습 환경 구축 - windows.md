# 실습 환경 구축

<br>

windows 패키지 관리자 chocolatey 설치

설치 및 사용 프로그램 : Virtual Box , vagrant, vscode, windows PowerShell

* Virtual Box : Linuix os 설치 및 docker 설치를 위한 가상환경 구성을 위한 프로그램
* Vagrant : vagrant 란 vm 관리 서비스 입니다. 직접 virtual box 클릭 하여 vm을 생성 할 수 있지만 손 쉽게 code 및 스크립트 작성 된 파일 하나로 vm 생성 할 수 있는 도구 이다. 
  * 사용 목적 : virtual box 의 vm 생성 간편화 및 자동화

* Vscode : 소스 코드 에디터 및 통합 개발 환경(IDE) vm 접속 및 vm(k8s)에서 사용하는 code 수정 에디터 입니다. 
* Windows PowerShell : 시스템 관리 및 자동화 등을 목적으로 설계된 명령줄 쉘 스크립트팅 언어이며 linux 등에서 접해본 shell 과 상당히 유사하다.

<br>

**step1**

**윈도우에 가상환경 설치**

***

1. 관리자로 실행 Powershell 열어 windows 패키지 관리자 chocolatey 설치 실행 

2. Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
3. https://chocolatey.org/install ( 설치가 되지 않는다면 해당 url 에서 확인 )

<br>

**step2**

**윈도우 패키지 관리자 chocolatey 이용하여 vagrant, virtualbox, vscode 설치 후 재부팅**

***

1. choco install vagrant virtualbox vscode

<br>

**step3**

**vm 생성 및 가상 머신 실행 TEST**

***

1. mkdir vagrant-test (테스트 할 폴터 생성)
2. cd vagrant-test   (테스트 할 폴더로 이동)
3. vagrant init <BOX_IMAGE> 
   * (ex) vagrant init ubuntu/focal64)  **Vagrantfile 생성 확인**

4. 설정하고 싶은 설정값 입력
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



