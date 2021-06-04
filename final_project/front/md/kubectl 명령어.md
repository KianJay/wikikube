### kubectl 명령어

- **쿠버네티스에서는 기본적으로 kubectl 명령어를 사용한다.**

---

<br>

사진

<br>

**kubectl 명령어 형식**

- kubectl 명령어는 쿠버네티스 및 클러스터 관리, 디버그 및 트러블 슈팅을 할 수있다

```
kubectl [command] [type] [name] [flags]
```

- command : 자원에 실행하려는 동작
  - create : 생성
  - get : 정보 출력
  - describe: 자세한 정보 출력
  - delete : 삭제
- type : 자원 타입
  - pod
  - service
- name : 자원이름(파드의 이름)
- flags : 옵션

<br>

**kubectl 권한 설정**

- 일반 사용자 kubectl 명령 사용 권한 추가

```
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

export KUBECONFIG=/etc/kubernetes/admin.conf

systemctl restart kubelet
```

<br>

**kubernetes 설치 버전 확인**

- Client Version = kubectl 명령의 버전을 의미합니다.
- Server Version = 쿠버네티스 컨트롤플레인의 버전을 의미합니다.

```
$ kubectl version --short
Client Version: v1.18.10
Server Version: v1.18.10
```

<br>

**kubectl 예제**

- **kubectl create**

```
// apache-pod.yaml 파일에 정의된 서비스를 생성
$ kubectl create -f apache-pod.yaml 
```

<br>

- **kubectl get**

```
// pod list 출력
$ kubectl get pods

// -o wide 옵션을 사용하면 상세한 정보 조회가 가능
$ kubectl get pods -o wide

// 클러스터 내부의 노드 확인
$ kubectl get nodes

// -o wide 옵션을 사용하면 상세한 정보 조회가 가능
$ kubectl get nodes -o wide

// 특정 <rc-name> 의 정보를 출력
$ kubectl get replicationcontroller <rc-name>

// 모든 rc, service들 정보를 출력
$ kubectl get rc,services

// 모든 ds(daemon sets)에 대한 정보를 출력(uninitialized ds도 포함)
$ kubectl get ds --include-uninitialized
```

<br>

- **kubectl describe**

```
// 특정 <node-name>의 node 정보 출력
$ kubectl describe nodes <node-name>

// 특정 <pod-name>의 pod 정보 출력
$ kubectl describe pods <pod-name>

// 특정 <rc-name>의 rc가 제어하는 pod들 정보 출력
$ kubectl describe pods <rc-name>

// 모든 pod 정보 출력(uninitialized pod은 제외)
$ kubectl describe pods --include-uninitialized=false
```

<br>

- **kubectl delete**

```
// pod.yaml 파일에 선언된 pod들을 제거
$ kubectl delete -f pod.yaml

// 특정 <label-name>이 정의된 pod, service들 제거
$ kubectl delete pods,services -l name=<label-name>

// 특정 <label-name>이 정의된 pod, service들 제거(uninitialized pod, service 포함)
$ kubectl delete pods,services -l name=<label-name> --include-uninitialized

// 모든 pod 제거
$ kubectl delete pods --all
```

<br>

- **kubectl exec**

```
// 특정 <pod-name> pod의 첫번째 container에 'ls' 명령어 실행 후 출력
$ kubectl exec <pod-name> ls

// 특정 <pod-name> pod의 특정 <container-name> container에 'ls' 명령어 실행 후 출력
$ kubectl exec <pod-name> -c <container-name> ls

// 특정 <pod-name> pod의 첫번째 container에 bash shell실행 
$ kubectl exec -ti <pod-name> /bin/bash
```

<br>

- **kubectl logs**

```
// 특정 <pod-name> pod의 로그 조회
$ kubectl logs <pod-name>

// 특정 <pod-name> pod의 로그 tail -f 조회(실시간 조회)
$ kubectl logs -f <pod-name>
```

<br>

**kubectl run**

```
kubectl run [-i] [--tty] --attach <name> --image=<image>
kubectl run {pod_name} --image {image} --port={port} ...{options}...
```

```
//nginx 이미지로
$ kubectl run nginx --image nginx --port=80

//저장소에 미리 생성해둔 이미지를 test 라는 이름으로 배쉬 터미널 생성 프로세스 종료시 컨테이너 자동 제거
$ kubectl run test -it --image <image url, name> --rm
```

