# kochetovd_platform
kochetovd Platform repository

<br><br>
## Домашнее задание 1
### Выполнено
- Установил утилиту kubectl - https://kubernetes.io/docs/tasks/tools/install-kubectl/#install-kubectl-on-linux;
- Установил minikube - https://kubernetes.io/docs/tasks/tools/install-minikube/;
- Запустил ВМ с кластером minikube start;
- Проверил, что контейнеры восстанавливаются после удаления;
- Создан Dockerfile, который запускает веб-сервер nginx, запускающий виртуальный хост на 8000 порту, имеющем root директорию /app и выполняющейся под UID 1001; 
- Подготовлен манифест web-pod.yml, описывающий pod, состоящий из двух контейнеров;
- Выполнен деплой pod web , состоящий из двух контейнеров. Первый init контейнер скачивает index.html файл и сохраняет его в volume app, второй контейнер это веб-сервер, который при запросе отдает скаченный файл. Volume app монтируется к обоим контенйерам в каталог /app;
- Использован kubectl port-forward для доступа к поду.


### Ответы на вопросы
> Разберитесь почему все pod в namespace kube-system восстановились после удаления.
kube-apiserver это статический pod, который при удалении создается немедленно.
Для pod-а core-dns имеет установленный priorityClassName в system-cluster-critical, что показывает, что данный pod является критическим для кластера и этот pod всегда перепланируется.


<br><br>
## Домашнее задание 2
### Выполнено
TASK01:
  - Создал SA bob, Сделал clusterrolebinding для sa bob и clusterrole admin
  - Создал SA dave без связки с ролью
TASK02:
  - Создал ns prometheus
  - Создал SA carol в ns prometheus
  - Сделал cluster роль, позволяющую делать get, list, watch в отношении Pods всего кластера
  - Сделал clusterrolebindind даной роль и ns prometheus
TASK03:
  - Создал ns dev
  - Создал sa jane в ns dev
  - Создал role admin, Сделал rolebinding sa jane и role admin
  - Создал sa ken в ns dev
  - Создал role view, Сделал rolebinding sa jane и role admin



<br><br>
## Домашнее задание 3
### Выполнено
- Добавил к ранее созданному манифесту kubernetes-intro/web-pod.yml readinessProbe и livenessProbe;
- Создал манифест deployment web-deploy.yaml для пода из web-pod.yml;
- Добавил в Deployment стратегию обновления;
- Создал манифест Service с ClusterIP web-svc-cip.yaml, проверил работу;
- Включил для kube-proxy режим `ipvs`, посмотрел конфигурацию IPVS; 
- Установил MetalLB, выполнил настройку с помощью ConfigMap metallb-config.yaml;
- Создал манифест Service c LoadBalancer web-svc-lb.yaml, проверил работу  пода-контроллера MetalLB;
- Настроил маршрут в кластер kubernetes, проверил доступность веб-сервера в браузере;
- Установил и настроил ingress-nginx; 
- Создал манифест для Headless-сервиса  web-svc-headless.yaml;
- Создал манифест Ingress  web-ingress.yaml для доступа к подам через Headless-сервис.


### Ответы на вопросы
> Попробуйте разные варианты деплоя с крайними значениями maxSurge и maxUnavailable (оба 0, оба 100%, 0 и 100%)
если maxSurge и maxUnavailable выставить в 0 - то получаем ошибку невозможности выполнения деплоя, вида 
```
The Deployment "web" is invalid: spec.strategy.rollingUpdate.maxUnavailable: Invalid value: intstr.IntOrString{Type:0, IntVal:0, StrVal:""}: may not be 0 when `maxSurge` is 0
```
При других вариантах все работает корректно, т.к. maxUnavailable указывает максимальное количество подов, которое может быть недоступно в процессе обновления, а maxSurge - максимальное количество подов, которое может быть создано от желаемое количество подов, указанного в `replicas`;




<br><br>
## Домашнее задание 4
### Выполнено
- Развернут StatefulSet с Minio;
- Развернут Headless Service для доступа к Minio;
- Проверил работу Minio.

### Задание со * 
- Учетные данные из StatefulSet вынесены в secret (манифест minio-secrets.yaml);
- Для кодирования учетных данных в base64 необходимо выполнить команды:
  - `echo -n 'minio' | base64`;
  - `echo -n 'minio123' | base64`
- Полученные значения записать в secret манифест, а в манифесте StatefulSet изменить задание переменных окружения на:
```
       env:
        - name: MINIO_ACCESS_KEY
          valueFrom:
            secretKeyRef:
              name: minio-secrets
              key: minio_access_key
        - name: MINIO_SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: minio-secrets
              key: minio_secret_key 
```



<br><br>
## Домашнее задание 5

### Задание про kubectl debug
- Установил kubectl-debug по инструкции
- Попробовал выполнить трассировку
```
	bash-5.0# strace -c -p1
	strace: test_ptrace_get_syscall_info: PTRACE_TRACEME: Operation not permitted
	strace: attach: ptrace(PTRACE_ATTACH, 1): Operation not permitted
```
- Попробовал выполнить strace
- Проверил capbilities у debug контенейра:
```
            "CapAdd": null,
            "CapDrop": null,
```
- Установка ptrace и admin capbilities была реализована в агенте версии 0.1.1
- Образ для контененра в файле https://raw.githubusercontent.com/aylei/kubectl-debug/master/scripts/agent_daemonset.yml используется версии 0.0.1
- Изменил версию образа докер на latest - strace/agent_daemonset.yml
- Применить изменения `kubectl apply -f strace/agent_daemonset.yml
- Проверил трассировку
```
	bash-5.0# strace -c -p1
	strace: Process 1 attached
	Handling connection for 10027
```



Status:
  Client Pod:          netperf-client-42010a800074
  Server Pod:          netperf-server-42010a800074
  Speed Bits Per Sec:  15039.62
  Status:              Done
Events:                <none>


Events:
  Type     Reason      Age    From                                                    Message
  ----     ------      ----   ----                                                    -------
  Normal   Scheduled   2m59s  default-scheduler                                       Successfully assigned default/netperf-server-42010a800074 to gke-your-first-cluster-1-pool-1-ca8e398d-fdhv
  Normal   Pulling     2m58s  kubelet, gke-your-first-cluster-1-pool-1-ca8e398d-fdhv  pulling image "tailoredcloud/netperf:v2.7"
  Normal   Pulled      2m57s  kubelet, gke-your-first-cluster-1-pool-1-ca8e398d-fdhv  Successfully pulled image "tailoredcloud/netperf:v2.7"
  Normal   Created     2m57s  kubelet, gke-your-first-cluster-1-pool-1-ca8e398d-fdhv  Created container
  Normal   Started     2m57s  kubelet, gke-your-first-cluster-1-pool-1-ca8e398d-fdhv  Started container
  Warning  PacketDrop  2m55s  kube-iptables-tailer                                    Packet dropped when receiving traffic from 10.4.1.22
  Warning  PacketDrop  46s    kube-iptables-tailer                                    Packet dropped when receiving traffic from client (10.4.1.22)

