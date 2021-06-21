### Kubernetes에 Apache 설치

**실습 환경은 [kubespray 사용한 쿠버네티스 설치](url) 과 동일**

---

<br>

### httpd

**setp1**

```
mkdir httpd
code httpd-pod.yaml

apiVersion: v1
kind: Pod
metadata:
  name: my-httpd-pod
spec:
  containers:
  - name: my-httpd-container
    image: httpd
    ports:
    - containerPort: 80
      protocol: TCP
```

```
vagrant@k8s-m1:~/apache$ kubectl get pods
NAME            READY   STATUS    RESTARTS   AGE
my-apache-pod   1/1     Running   0          86s
```

```
vagrant@k8s-m1:~/apache$ kubectl describe pods my-apache-pod 
Name:         my-apache-pod
Namespace:    default
Priority:     0
Node:         k8s-w1/192.168.201.21
Start Time:   Tue, 01 Jun 2021 12:43:40 +0000
Labels:       <none>
Annotations:  Status:  Running
IP:           10.233.94.60
IPs:
  IP:  10.233.94.60
Containers:
  my-apache-container:
    Container ID:   docker://43b66b8403083b4c68ba72e81399551e007bdc0321670a1d3c84b78909df610e
    Image:          httpd:latest
    Image ID:       docker-pullable://httpd@sha256:48bae0ac5d0d75168f1c1282c0eb21b43302cb1b5c5dc9fa3b4a758ccfb36fe9
    Port:           8080/TCP
    Host Port:      0/TCP
    State:          Running
      Started:      Tue, 01 Jun 2021 12:45:40 +0000
    Last State:     Terminated
      Reason:       Completed
      Exit Code:    0
      Started:      Tue, 01 Jun 2021 12:43:45 +0000
      Finished:     Tue, 01 Jun 2021 12:45:36 +0000
    Ready:          True
    Restart Count:  1
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from default-token-l8xvs (ro)
Conditions:
  Type              Status
  Initialized       True 
  Ready             True 
  ContainersReady   True 
  PodScheduled      True 
Volumes:
  default-token-l8xvs:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  default-token-l8xvs
    Optional:    false
QoS Class:       BestEffort
Node-Selectors:  <none>
Tolerations:     node.kubernetes.io/not-ready:NoExecute for 300s
                 node.kubernetes.io/unreachable:NoExecute for 300s
Events:
  Type    Reason     Age                    From               Message
  ----    ------     ----                   ----               -------
  Normal  Scheduled  5m56s                  default-scheduler  Successfully assigned default/my-apache-pod to k8s-w1
  Normal  Pulling    5m55s                  kubelet            Pulling image "httpd"
  Normal  Pulled     5m51s                  kubelet            Successfully pulled image "httpd"
  Normal  Killing    4m1s                   kubelet            Container my-apache-container definition changed, will be restarted
  Normal  Pulling    4m                     kubelet            Pulling image "httpd:latest"
  Normal  Pulled     3m57s                  kubelet            Successfully pulled image "httpd:latest"
  Normal  Created    3m56s (x2 over 5m51s)  kubelet            Created container my-apache-container
  Normal  Started    3m56s (x2 over 5m51s)  kubelet            Started container my-apache-container
```

```
vagrant@k8s-m1:~/apache$ curl 10.233.94.60
<html><body><h1>It works!</h1></body></html>
```

<br>

### nginx

##### step1

```
mkdir nginx            #테스트 할 폴터 생성
code nginx-pod.yaml    #nginx 컨테이너 생성 파일 작성

apiVersion: v1
kind: Pod
metadata:
  name: my-nginx-pod
spec:
  containers:
  - name: my-nginx-container
    image: nginx:latest
    ports:
    - containerPort: 80
     protocol: TCP
```

```
vagrant@k8s-m1:~/nginx$ kubectl get pods
NAME           READY   STATUS    RESTARTS   AGE
my-nginx-pod   1/1     Running   0          36s
```

```
vagrant@k8s-m1:~/nginx$ curl 10.233.94.44
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```

```
kubectl run -i --tty --rm debug --image=alicek106/ubuntu:curl --restart=Never bash
```

```
vagrant@k8s-m1:~/nginx$ kubectl logs my-nginx-pod 

10.233.106.0 - - [01/Jun/2021:03:22:02 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.68.0" "-"
10.233.94.45 - - [01/Jun/2021:03:23:58 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.35.0" "-"
10.233.94.45 - - [01/Jun/2021:03:24:07 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.35.0" "-"
```

