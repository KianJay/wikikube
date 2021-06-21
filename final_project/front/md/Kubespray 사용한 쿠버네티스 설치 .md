

### Kubespray 사용한 쿠버네티스 설치

**kubespray는 대부분의 인프라에서 사용할 수 있기 때문에 인프라에 특별한 종속성을 갖는 편은 아니다.**

---

<br>

#### 테스트 환경

* Master 1
* worker 3

```
OS : ubuntu
Master & etcd : 192.168.201.11
worker : 192.168.201.21 ~ 23
```

<br>

![image](https://user-images.githubusercontent.com/77868828/122776053-b4f17980-d2e5-11eb-92fa-04d7a0a3e9a3.png)

<br>

##### Kubespray 받기

```
1. git clone --branch release-2.14 https://github.com/kubernetes-sigs/kubespray.git
2. cd kubespray
3. sudo apt update
3. sudo apt install python3-pip
4. sudo pip3 install -r requirements.txt
```

<br>

##### SSH 키 인증 구성

```
ssh-keygen
ssh-copy-id vagrant@192.168.201.11
ssh-copy-id vagrant@192.168.201.21
ssh-copy-id vagrant@192.168.201.22
ssh-copy-id vagrant@192.168.201.23
```

<br>

##### 인벤토리 구성

* kubespray는 Ansible을 기반으로 클러스터를 제어하여 쿠버네티스를 설치하기 떄문에 inventory 파일을 수정해야한다.

```
1. cp -r inventory/sample inventory/mycluster
2. vi inventory/mycluster/inventory.ini
3. 해당 아래 내용으로 수정
[all]
k8s-m1 ansible_host=192.168.201.11 ip=192.168.201.11 ansible_connection=local
k8s-w1 ansible_host=192.168.201.21 ip=192.168.201.21
k8s-w2 ansible_host=192.168.201.22 ip=192.168.201.22
k8s-w3 ansible_host=192.168.201.23 ip=192.168.201.23

[kube-master]
k8s-m1

[etcd]
k8s-m1

[kube-node]
k8s-w1
k8s-w2
k8s-w3

[k8s-cluster:children]
kube-master
kube-node
```

<br>

##### /etc/resolv.conf 수정

```
nameserver 169.254.25.10
search default.svc.cluster.local svc.cluster.local cluster.local
options ndots:5
```

<br>

##### 쿠버네티스 배포 및 플레이북 실행

* Ansible을 이용해 playbook 실행 쿠버네티스 설치 작업 완료

```
ansible all -i inventory/mycluster/inventory.ini -m ping     			#inventory 오류 확인 TEST
ansible-playbook -i inventory/mycluster/inventory.ini cluster.yml -b    #playbook 실행
```

자세한 내용은 **[Ansible 명령어](url)** 참조

<br>

##### kubeconfig 파일 복사

* kubeconfig 파일들을 사용하여 클러스터, 사용자, 네임스페이스 및 인증 메커니즘에 대한 정보를 관리. 
* kubectl 커맨드라인 툴은 kubeconfig 파일을 사용하여 클러스터의 선택과 클러스터의 API 서버와의 통신에 필요한 정보를 찾는다.
* 클러스터에 대한 접근을 구성하는 데 사용되는 파일이 kubeconfig 파일 이라고 한다.

```
mkdir $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

<br>

##### kubectl 자동완성 기능

```
kubectl completion bash | sudo tee /etc/bash_completion.d/kubectl
exec bash
```
