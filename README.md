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
## Домашнее задание 6

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

### Задание про iptables-tailer
- Выполнил деплой приложения netperf-operator в кластер, применив манифесты
```
	kubectl apply -f ./deploy/crd.yaml
	kubectl apply -f ./deploy/rbac.yaml
	kubectl apply -f ./deploy/operator.yaml
```
- Запустил тесты `kubectl apply -f ./deploy/crd.yaml`
```
Status:
  Client Pod:          netperf-client-42010a800074
  Server Pod:          netperf-server-42010a800074
  Speed Bits Per Sec:  15039.62
  Status:              Done
Events:                <none>
```
- Применил манифест с сетевой политикой `kubectl apply -f kubernetes-debug/kit/netperf-calico-policy.yaml`
- Повторно запустил тесты. Проверил логи на нодах кластера:
```
gke-your-first-cluster-1-pool-1-ca8e398d-gxhh ~ # journalctl -k | grep calico
Sep 10 12:23:31 gke-your-first-cluster-1-pool-1-ca8e398d-gxhh kernel: calico-packet: IN=calia8df726959a OUT=cali4b8ed8b7d66 MAC=ee:ee:ee:ee:ee:ee:c6:22:0b:f9:63:81:08:00 SRC=10.4.1.13 DST=10.4.1.12 LEN=60 TOS=0x00 PREC=0x00 TTL=63 ID=31337 DF PROTO=TCP SPT=60743 DPT=12865 WINDOW=28400 RES=0x00 SYN URGP=0 
Sep 10 12:23:32 gke-your-first-cluster-1-pool-1-ca8e398d-gxhh kernel: calico-packet: IN=calia8df726959a OUT=cali4b8ed8b7d66 MAC=ee:ee:ee:ee:ee:ee:c6:22:0b:f9:63:81:08:00 SRC=10.4.1.13 DST=10.4.1.12 LEN=60 TOS=0x00 PREC=0x00 TTL=63 ID=31338 DF PROTO=TCP SPT=60743 DPT=12865 WINDOW=28400 RES=0x00 SYN URGP=0 
Sep 10 12:23:34 gke-your-first-cluster-1-pool-1-ca8e398d-gxhh kernel: calico-packet: IN=calia8df726959a OUT=cali4b8ed8b7d66 MAC=ee:ee:ee:ee:ee:ee:c6:22:0b:f9:63:81:08:00 SRC=10.4.1.13 DST=10.4.1.12 LEN=60 TOS=0x00 PREC=0x00 TTL=63 ID=31339 DF PROTO=TCP SPT=60743 DPT=12865 WINDOW=28400 RES=0x00 SYN URGP=0 
Sep 10 12:23:38 gke-your-first-cluster-1-pool-1-ca8e398d-gxhh kernel: calico-packet: IN=calia8df726959a OUT=cali4b8ed8b7d66 MAC=ee:ee:ee:ee:ee:ee:c6:22:0b:f9:63:81:08:00 SRC=10.4.1.13 DST=10.4.1.12 LEN=60 TOS=0x00 PREC=0x00 TTL=63 ID=31340 DF PROTO=TCP SPT=60743 DPT=12865 WINDOW=28400 RES=0x00 SYN URGP=0 
Sep 10 12:23:47 gke-your-first-cluster-1-pool-1-ca8e398d-gxhh kernel: calico-packet: IN=calia8df726959a OUT=cali4b8ed8b7d66 MAC=ee:ee:ee:ee:ee:ee:c6:22:0b:f9:63:81:08:00 SRC=10.4.1.13 DST=10.4.1.12 LEN=60 TOS=0x00 PREC=0x00 TTL=63 ID=31341 DF PROTO=TCP SPT=60743 DPT=12865 WINDOW=28400 RES=0x00 SYN URGP=0 
Sep 10 12:24:03 gke-your-first-cluster-1-pool-1-ca8e398d-gxhh kernel: calico-packet: IN=calia8df726959a OUT=cali4b8ed8b7d66 MAC=ee:ee:ee:ee:ee:ee:c6:22:0b:f9:63:81:08:00 SRC=10.4.1.13 DST=10.4.1.12 LEN=60 TOS=0x00 PREC=0x00 TTL=63 ID=31342 DF PROTO=TCP SPT=60743 DPT=12865 WINDOW=28400 RES=0x00 SYN URGP=0 
Sep 10 12:24:36 gke-your-first-cluster-1-pool-1-ca8e398d-gxhh kernel: calico-packet: IN=calia8df726959a OUT=cali4b8ed8b7d66 MAC=ee:ee:ee:ee:ee:ee:c6:22:0b:f9:63:81:08:00 SRC=10.4.1.13 DST=10.4.1.12 LEN=60 TOS=0x00 PREC=0x00 TTL=63 ID=31343 DF PROTO=TCP SPT=60743 DPT=12865 WINDOW=28400 RES=0x00 SYN URGP=0 
Sep 10 12:25:44 gke-your-first-cluster-1-pool-1-ca8e398d-gxhh kernel: calico-packet: IN=calia8df726959a OUT=cali4b8ed8b7d66 MAC=ee:ee:ee:ee:ee:ee:c6:22:0b:f9:63:81:08:00 SRC=10.4.1.13 DST=10.4.1.12 LEN=60 TOS=0x00 PREC=0x00 TTL=63 ID=48346 DF PROTO=TCP SPT=35161 DPT=12865 WINDOW=28400 RES=0x00 SYN URGP=0 
Sep 10 12:25:45 gke-your-first-cluster-1-pool-1-ca8e398d-gxhh kernel: calico-packet: IN=calia8df726959a OUT=cali4b8ed8b7d66 MAC=ee:ee:ee:ee:ee:ee:c6:22:0b:f9:63:81:08:00 SRC=10.4.1.13 DST=10.4.1.12 LEN=60 TOS=0x00 PREC=0x00 TTL=63 ID=48347 DF PROTO=TCP SPT=35161 DPT=12865 WINDOW=28400 RES=0x00 SYN URGP=0 
```
- Создал DaemonSet применив манифест `kubernetes-debug/kit/iptables-tailer.yaml`. Для исправления ошибок с правами применить манифест `kubernetes-debug/kit/iptables-tailer-sa.yaml`.
- Перезапустил тесты. Проверил события:
```
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
```



### Задание со *

1. Исправьте ошибку в нашей сетевой политике, чтобы Netperf снова начал работать
- Для исправления сетевой политики нужно изменить selector 
- Для исправления применить манифест kubernetes-debug/kit/netperf-calico-policy_check.yaml


2. Поправьте манифест DaemonSet из репозитория, чтобы в логах отображались имена Podов, а не их IP-адреса
- Для отображения имен Подов нужно изменить переменную окружения POD_IDENTIFIER на name
- Пересоздать DaemonSet iptables-tailer
- Перезапустить тесты, получим:
```
Events:
  Type     Reason      Age                    From                                                    Message
  ----     ------      ----                   ----                                                    -------
  Normal   Scheduled   4m29s                  default-scheduler                                       Successfully assigned default/netperf-client-42010a800074 to gke-your-first-cluster-1-pool-1-ca8e398d-gxhh
  Normal   Pulled      2m18s (x2 over 4m28s)  kubelet, gke-your-first-cluster-1-pool-1-ca8e398d-gxhh  Container image "tailoredcloud/netperf:v2.7" already present on machine
  Normal   Created     2m18s (x2 over 4m28s)  kubelet, gke-your-first-cluster-1-pool-1-ca8e398d-gxhh  Created container
  Normal   Started     2m17s (x2 over 4m28s)  kubelet, gke-your-first-cluster-1-pool-1-ca8e398d-gxhh  Started container
  Warning  PacketDrop  2m17s                  kube-iptables-tailer                                    Packet dropped when sending traffic to netperf-server-42010a800074 (10.4.1.33)
```

```
Events:
  Type     Reason      Age    From                                                    Message
  ----     ------      ----   ----                                                    -------
  Normal   Scheduled   4m31s  default-scheduler                                       Successfully assigned default/netperf-server-42010a800074 to gke-your-first-cluster-1-pool-1-ca8e398d-gxhh
  Normal   Pulled      4m30s  kubelet, gke-your-first-cluster-1-pool-1-ca8e398d-gxhh  Container image "tailoredcloud/netperf:v2.7" already present on machine
  Normal   Created     4m30s  kubelet, gke-your-first-cluster-1-pool-1-ca8e398d-gxhh  Created container
  Normal   Started     4m30s  kubelet, gke-your-first-cluster-1-pool-1-ca8e398d-gxhh  Started container
  Warning  PacketDrop  4m28s  kube-iptables-tailer                                    Packet dropped when receiving traffic from 10.4.1.34
  Warning  PacketDrop  2m17s  kube-iptables-tailer                                    Packet dropped when receiving traffic from netperf-client-42010a800074 (10.4.1.34)
```


<br><br>
## Домашнее задание 7
- Создал манифест для CustomResource Mysql `deploy/cr.yml`
- Создал манифест для CRD для ресурса Mysql `deploy/crd.yml`
- В описание CRD добавил поля requires для указания обязательных полей
- Подготовил MySQL контроллер `kubernetes-operators/build/mysql-operator.py`
- Проверил работу контроллера - Запустил контроллер `kopf run mysql-operator.py`, Создал CR, Заполнил БД, Удалил CR, Снова создал CR, Проверил что БД восстановилась
```
$ kubectl get pods
NAME                               READY   STATUS      RESTARTS   AGE
backup-mysql-instance-job-nj7xn    0/1     Completed   0          2m9s
mysql-instance-58ccc56f84-99gj5    1/1     Running     0          76s
restore-mysql-instance-job-x9fwz   0/1     Completed   3          76s

$ kubectl get job
NAME                         COMPLETIONS   DURATION   AGE
backup-mysql-instance-job    1/1           2s         2m21s
restore-mysql-instance-job   1/1           43s        88s

$ export MYSQLPOD=$(kubectl get pods -l app=mysql-instance -o jsonpath="{.items[*].metadata.name}")

$ kubectl exec -it $MYSQLPOD -- mysql -potuspassword -e "select * from test;" otus-database
mysql: [Warning] Using a password on the command line interface can be insecure.
+----+-------------+
| id | name        |
+----+-------------+
|  1 | some data   |
|  2 | some data-2 |
+----+-------------+
```

### Задание со *
1) Исправить контроллер, чтобы он писал в status subresource
В функцию `mysql_on_create` добавил код в конце
```
    if created_backup_pv:
        kopf.event(body, type='Normal', reason='Logging', message="mysql created with created backup-pv ")
        return {'Message': "mysql created with created backup-pv"}
    else:
        kopf.event(body, type='Normal', reason='Logging', message="mysql created without created backup-pv,  backup-pv exist ")
        return {'Message': "mysql created without created backup-pv,  backup-pv exist"}
```
Также изменил создание PV для backup для установки флага успешности создания PV
```
    created_backup_pv = True
    # Cоздаем PVC и PV для бэкапов:
    try:
        backup_pv = render_template('backup-pv.yml.j2', {'name': name})
        api = kubernetes.client.CoreV1Api()
        api.create_persistent_volume(backup_pv)
    except kubernetes.client.rest.ApiException:
        created_backup_pv = False
```
Функция kopf.event создает сообщения для события kubernetes для объекта.
Из документации kopf: "Все, что возвращается из любого обработчика, сохраняется в статусе объекта под идентификатором этого обработчика (который по умолчанию является именем функции)." Поэтому добавил в функцию mysql_on_create возврат сообщения. Получили следующие результаты:
При первом создании CR:
```
Status:
  Kopf:
  mysql_on_create:
    Message:  mysql created with created backup-pv
Events:
  Type    Reason   Age   From  Message
  ----    ------   ----  ----  -------
  Normal  Logging  2s    kopf  Handler 'mysql_on_create' succeeded.
  Normal  Logging  2s    kopf  All handlers succeeded for creation.
  Normal  Logging  2s    kopf  mysql created with created backup-pv
```

При повторном создании
```
Status:
  Kopf:
  mysql_on_create:
    Message:  mysql created without created backup-pv,  backup-pv exist
Events:
  Type    Reason   Age   From  Message
  ----    ------   ----  ----  -------
  Normal  Logging  3s    kopf  Handler 'mysql_on_create' succeeded.
  Normal  Logging  3s    kopf  mysql created without created backup-pv,  backup-pv exist
  Normal  Logging  3s    kopf  All handlers succeeded for creation.
```

2) Добавить в контроллер логику обработки изменений CR
Реализовал изменение имени БД в mysql. Добавил декоратор:
```
@kopf.on.field('otus.homework', 'v1', 'mysqls', field='spec.database')
def mysql_change_db_name(body, old, new, **kwargs):
    name = body['metadata']['name']
    image = body['spec']['image']
    password = body['spec']['password']

    renamedb_job = render_template('rename-db-job.yml.j2', {'name': name,'image': image,'password': password,'database_old': old, 'database_new': new})
    api = kubernetes.client.BatchV1Api()
    api.create_namespaced_job('default', renamedb_job)
    wait_until_job_end(f"renamedb-{name}-job")
    return {'message': f"Change name db from {old} to {new}"}
```
Функция mysql_change_db_name вызывает при изменении поля spec.database объекта Mysql. В данной функции получаются текущие поля объета, затем из шаблона генерируется манифест для Job по изменения имени БД, этот манифест применяется, ожидается его завершения выполнения и в status объекта CR возвращается сообщение.
Сначала у нас есть заполненная БД otus-database
```
$ kubectl exec -it $MYSQLPOD -- mysql -potuspassword -e "show databases;"
mysql: [Warning] Using a password on the command line interface can be insecure.
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| otus-database      |
| performance_schema |
| sys                |
+--------------------+

$ kubectl exec -it $MYSQLPOD -- mysql -potuspassword -e "select * from test;" otus-database
mysql: [Warning] Using a password on the command line interface can be insecure.
+----+-------------+
| id | name        |
+----+-------------+
|  1 | some data   |
|  2 | some data-2 |
+----+-------------+
```
Изменили в манифесте deploy/cr.yaml имя БД на  otus-database-test, применили манифест. Получили сообщение в status CR:
```
Status:
  Kopf:
  mysql_change_db_name/spec.database:
    Message:  Change name db from otus-database to otus-database-test
  mysql_on_create:
    Message:  mysql created with created backup-pv
```
И следущие состояние в mysql
```
$ kubectl exec -it $MYSQLPOD -- mysql -potuspassword -e "show databases;"
mysql: [Warning] Using a password on the command line interface can be insecure.
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| otus-database-test |
| performance_schema |
| sys                |
+--------------------+

$ kubectl exec -it $MYSQLPOD -- mysql -potuspassword -e "select * from test;" otus-database
mysql: [Warning] Using a password on the command line interface can be insecure.
ERROR 1049 (42000): Unknown database 'otus-database'
command terminated with exit code 1

$ kubectl exec -it $MYSQLPOD -- mysql -potuspassword -e "select * from test;" otus-database-test
mysql: [Warning] Using a password on the command line interface can be insecure.
+----+-------------+
| id | name        |
+----+-------------+
|  1 | some data   |
|  2 | some data-2 |
+----+-------------+
```



<br><br>
## Домашнее задание 10

### Подготовка
- Установил клиента helm2 на локальную машину
```
$ helm version --client
Client: &version.Version{SemVer:"v2.14.3", GitCommit:"0e7f3b6637f7af8fcfddb3d2941fcc7cbebb0085", GitTreeState:"clean"}
```
- Подготовил манифесты для создания сервисного аккаунта для работы helm - kubernetes-templating/helm_rbac.yaml
- Инициализировал helm `helm init --service-account=tiller`
- Проверил корректность установки
```
$ helm version
Client: &version.Version{SemVer:"v2.14.3", GitCommit:"0e7f3b6637f7af8fcfddb3d2941fcc7cbebb0085", GitTreeState:"clean"}
Server: &version.Version{SemVer:"v2.14.3", GitCommit:"0e7f3b6637f7af8fcfddb3d2941fcc7cbebb0085", GitTreeState:"clean"}
```


### nginx-ingress
- Выполнил деплой nginx-ingress использую  Helm 2 и tiller с правами cluster-admin
```
$ helm list
NAME         	REVISION	UPDATED                 	STATUS  	CHART               	APP VERSION	NAMESPACE    
nginx-ingress	1       	Thu Sep 26 11:35:22 2019	DEPLOYED	nginx-ingress-1.11.1	0.25.0     	nginx-ingress
```


### cert-manager
- Для создания сервисного аккаунта tiller-cert-manager в namespace cert-manager подготовил манифест kubernetes-templating/cert-manager/cert_manager_tiller_rbac.yaml
- Применил манифесты ` kubectl apply -f kubernetes-templating/cert-manager/cert_manager_tiller_rbac.yaml `
- Инициализировал helm в namespace cert-manager - `helm init --tiller-namespace cert-manager --service-account tiller-cert-manager`
- Выполнил подготовительные действия для деплоя cert-manager
```
helm repo add jetstack https://charts.jetstack.io
kubectl apply -f https://raw.githubusercontent.com/jetstack/cert-manager/release-0.9/deploy/manifests/00-crds.yaml
kubectl label namespace cert-manager certmanager.k8s.io/disable-validation="true"
```
- Проверил, что у helm нет прав для установки в namespace nginx-ingress
- При установки в namespace cert-manager также возникает ошибка. Для установки cert-manager для helm нужны права cluster-admin.
```
UPGRADE FAILED
Error: "cert-manager" has no deployed releases
ROLLING BACKError: Could not get information about the resource: clusterroles.rbac.authorization.k8s.io "cert-manager-cainjector" is forbidden: User "system:serviceaccount:cert-manager:tiller-cert-manager" cannot get resource "clusterroles" in API group "rbac.authorization.k8s.io" at the cluster scope
```
- Инициализируем helm с сервисным аккаунтом tiller - `helm init --service-account=tiller`
- Деплоем cert-manager - `helm upgrade --install cert-manager jetstack/cert-manager --wait --namespace=cert-manager --version=0.9.0 --atomic`
- Для корректной работы cert-manager нужно создать ресурс ClusterIssuer. Ресурс Issuer не подходит так, как позволяет создавать сертификат только в определенном namespace.
`kubectl apply -f kubernetes-templating/cert-manager/clusterissue.yaml`


### chartmuseum
- Установил плагин helm-tiller `helm plugin install https://github.com/rimusz/helm-tiller`
- Кастомизировал установку chartmuseum kubernetes-templating/chartmuseum/values.yaml
- Выполнил деплой с помощью helm-tiller
```
helm tiller run \
helm upgrade --install chartmuseum stable/chartmuseum --wait \
--namespace=chartmuseum \
--version=2.3.2 \
-f kubernetes-templating/chartmuseum/values.yaml
```
- Проверил, что tiller в кластере не знает про релиз chartmuseum, а локальный знает
```
$ helm list
NAME         	REVISION	UPDATED                 	STATUS  	CHART               	APP VERSION	NAMESPACE    
cert-manager 	1       	Thu Sep 26 11:50:39 2019	DEPLOYED	cert-manager-v0.9.0 	v0.9.0     	cert-manager 
nginx-ingress	1       	Thu Sep 26 11:35:22 2019	DEPLOYED	nginx-ingress-1.11.1	0.25.0     	nginx-ingress
```
```
$ helm tiller run helm list
NAME       	REVISION	UPDATED                 	STATUS  	CHART            	APP VERSION	NAMESPACE  
chartmuseum	1       	Thu Sep 26 11:59:14 2019	DEPLOYED	chartmuseum-2.3.2	0.8.2      	chartmuseum
```
- Переустановил chartmuseum c установленной переменной окружения HELM_TILLER_STORAGE=configmap,  tiller внутри кластера увидел release
```
$ helm status chartmuseum
LAST DEPLOYED: Thu Sep 26 12:14:58 2019
NAMESPACE: chartmuseum
STATUS: DEPLOYED

RESOURCES:
==> v1/Pod(related)
NAME                                      READY  STATUS   RESTARTS  AGE
chartmuseum-chartmuseum-646949dc6b-mtx5b  1/1    Running  0         27s
```
- chartmuseum доступен по адресу https://chartmuseum.34.69.15.120.nip.io/ с валиндным ssl сертификатом.


### chartmuseum | Задание со ⭐
- По умолчанию в chartmuseum отключено API, включается установкой переменной окружения  `DISABLE_API: false`. Актуальный список API - https://github.com/helm/chartmuseum
- Загрузим в chartmuseum chart для frontend
```
curl --data-binary "@frontend-0.1.0.tgm.34.69.15.120.nip.io/api/charts
{"saved":true}
```
- Также можно загрузить chart с помощью плагина helm push `helm push rabbitmq/ chartmuseum`
- Список chart
```
curl https://chartmuseum.34.69.15.120.nip.io/api/charts
{
"frontend":[
{"name":"frontend","version":"0.1.0","description":"A Helm chart for Kubernetes","apiVersion":"v1","appVersion":"1.0","urls":["charts/frontend-0.1.0.tgz"],"created":"2019-09-26T11:57:08.300421572Z","digest":"3be560ba4e38bbc11b9833c5400a41584745af825c3d4374b5c380e717586402"}
],
"rabbitmq":[
{"name":"rabbitmq","version":"0.1.0","description":"A Helm chart for Kubernetes","apiVersion":"v1","appVersion":"1.0","urls":["charts/rabbitmq-0.1.0.tgz"],"created":"2019-09-26T12:00:37.10017848Z","digest":"72ad02f46c5736e57a88cc9e27122e316d040518d021c3a4d70d76bd0b89f039"}
]
}
```
- Добавим репозиторий
```
$ helm repo add chartmuseum https://chartmuseum.34.69.15.120.nip.io
"chartmuseum" has been added to your repositories
```
- Проверим наличие chart-ов
```
$ helm search chartmuseum
NAME                	CHART VERSION	APP VERSION	DESCRIPTION                        
chartmuseum/frontend	0.1.0        	1.0        	A Helm chart for Kubernetes        
chartmuseum/rabbitmq	0.1.0        	1.0        	A Helm chart for Kubernetes 
```


### harbor
- Установил helm3
```
$ helm3 version
version.BuildInfo{Version:"v3.0.0-beta.3", GitCommit:"5cb923eecbe80d1ad76399aee234717c11931d9a", GitTreeState:"clean", GoVersion:"go1.12.9"}
```
- Параметризовал установку harbor - kubernetes-templating/harbor/values.yaml
- Выполнил деплой 
```
helm3 upgrade --install harbor harbor/harbor --wait \
--namespace=harbor \
--version=1.1.2 \
-f kubernetes-templating/harbor/values.yaml
```
```
$ helm3 list --namespace=harbor
NAME  	NAMESPACE	REVISION	UPDATED                                	STATUS  	CHART       
harbor	harbor   	1       	2019-09-26 12:40:31.415542396 +0300 MSK	deployed	harbor-1.1.2
```
- harbor доступен по адресу https://harbor.34.69.15.120.nip.io/ с валиндным ssl сертификатом.


### Используем helmfile | Задание со ⭐
Подготовил helmfile - kubernetes-templating/helmfile/helmfile.yaml для установки nginx-ingress, cert-manager, harbor
Для harbor создал файл kubernetes-templating/helmfile/values/harbor.yaml.gotmpl c параметрищацией переменных helm чарта
Применим helmfile - `$ helmfile --environment production apply`
```
$ helm list
NAME         	REVISION	UPDATED                 	STATUS  	CHART               	APP VERSION	NAMESPACE    
cert-manager 	1       	Thu Sep 26 12:58:00 2019	DEPLOYED	cert-manager-v0.9.0 	v0.9.0     	cert-manager 
chartmuseum  	1       	Thu Sep 26 12:14:58 2019	DEPLOYED	chartmuseum-2.3.2   	0.8.2      	chartmuseum  
harbor       	2       	Thu Sep 26 12:58:01 2019	DEPLOYED	harbor-1.1.2        	1.8.2      	harbor       
nginx-ingress	1       	Thu Sep 26 11:35:22 2019	DEPLOYED	nginx-ingress-1.11.1	0.25.0     	nginx-ingress
```


### Создаем свой helm chart
- Средствами helm инициализируем структуру директории  `helm create kubernetes-templating/socks-shop`. Перенес файл all.yaml в директорию templates
- Установил helm chart `helm upgrade --install socks-shop kubernetes-templating/socks-shop --namespace=socks-shop`
- Проверил работу сайта по адресу - http://35.222.253.191:30001/
- Создадим helm chart для микросервиса frontend - helm create kubernetes-templating/frontend
- В директории kubernetes-templating/frontend/template создадим файлы deployment.yaml, service.yaml, ingress.yaml с манифестами для frontend извлеченными из файла all.yaml
- Переустановил chart socks-shop, доступ к UI пропал.
- Установил chart frontend - `helm upgrade --install frontend kubernetes-templating/frontend --namespace socks-shop`, доступ к UI вновь появился
- Шаблонизируем chart frontend - kubernetes-templating/frontend/values.yaml
- Для chart socks-shop создали зависимость от frontend - kubernetestemplating/socks-shop/requirements.yaml
- Обновил зависимости - `helm dep update kubernetes-templating/socks-shop`
- Обновил release socks-shop, сервис работает корректно https://shop.34.69.15.120.nip.io/index.html


### Создаем свой helm chart | Задание со ⭐
- Реализовал установку сервиса RabbitMQ через зависимости:
- Создадим helm chart для микросервиса rabbitmq - helm create kubernetes-templating/rabbitmq
- В директории kubernetes-templating/rabbitmq/template создадим файлы deployment.yaml, service.yaml с манифестами для rabbitmq извлеченными из файла all.yaml
- Для chart socks-shop создали зависимость от rabbitmq - kubernetestemplating/socks-shop/requirements.yaml
- Обновил зависимости - `helm dep update kubernetes-templating/socks-shop`
- Обновил release socks-shop, сервис работает корректно https://shop.34.69.15.120.nip.io/index.html


### Работа с helm-secrets
- Установил зависимость sops
- Установил plugin - `helm plugin install https://github.com/futuresimple/helm-secrets --version 2.0.2`
- Сгенерировла ключ `gpg --full-generate-key`, проверил наличие ключа
```
$ gpg -k
/home/initlab/.gnupg/pubring.kbx
--------------------------------
pub   rsa3072 2019-09-25 [SC]
      6C54E9A34703577D642088BF04293AC9F69304F1
uid         [  абсолютно ] initlab <d.kochetov@initlab.ru>
sub   rsa3072 2019-09-25 [E]
```
- Создал файл kubernetes-templating/frontend/secrets.yaml
```
visibleKey: hiddenValue
```
- Зашифровали файл ` sops -e -i --pgp 6C54E9A34703577D642088BF04293AC9F69304F1 secrets.yaml `
```
$ cat secrets.yaml 
visibleKey: ENC[AES256_GCM,data:AiIcnYJpkC5pbis=,iv:P5iYttXenkFOsK6xqyWXOv28HbHnDafVwMyFwcpKc2k=,tag:FYgRkwyAfWly1SDqWYrIRg==,type:str]
sops:
    kms: []
    gcp_kms: []
    azure_kv: []
    lastmodified: '2019-09-26T10:36:16Z'
```
- Создали файл kubernetes-templating/frontend/templates/secret.yaml с манифестом для ресурса Secret
- Выполним установку
```
helm secrets upgrade --install frontend kubernetes-templating/frontend --namespace=socks-shop \
-f kubernetes-templating/frontend/values.yaml \
-f kubernetes-templating/frontend/secrets.yaml
```
- Проверим что Secret создался
```
$ kubectl get secrets secret -nsocks-shop -o yaml
apiVersion: v1
data:
  visibleKey: aGlkZGVuVmFsdWU=
kind: Secret
metadata:
  creationTimestamp: "2019-09-26T10:40:36Z"
  name: secret
  namespace: socks-shop
  resourceVersion: "36104"
  selfLink: /api/v1/namespaces/socks-shop/secrets/secret
  uid: 1308e843-e04a-11e9-a442-42010a80026f
type: Opaque

$ echo "aGlkZGVuVmFsdWU=" | base64 --decode
hiddenValue
```


### Проверка
- Создал архивы для chart `helm package . `
- Загрузил архивы в репозиторий harbor
- Создадим файл kubernetes-templating/repo.sh
```
#!/bin/bash
helm repo add templating https://harbor.34.69.15.120.nip.io/chartrepo/helm
```
- Выполним данный файл и проверим наличие chart в репозитории
```
$ bash repo.sh 
"templating" has been added to your repositories

$ helm search templating
NAME                 	CHART VERSION	APP VERSION	DESCRIPTION                
templating/frontend  	0.1.0        	1.0        	A Helm chart for Kubernetes
templating/rabbitmq  	0.1.0        	1.0        	A Helm chart for Kubernetes
templating/socks-shop	0.1.0        	1.0        	A Helm chart for Kubernetes
```


### Kubecfg
- В директорию  kubernetes-templating/kubecfg вынес манифесты,описывающие service и deployment, для сервисов catalogue и payment
- Установил kubecfg - https://github.com/bitnami/kubecfg
`brew install kubecfg`
```
$ kubecfg version
kubecfg version: v0.13.0
jsonnet version: v0.12.0
client-go version: v0.0.0-master+38d6080
```
- Подготовил файл kubernetes-templating/kubecfg/services.jsonnet, в котором сначала идет шаблон, включающий описание
service и deployment, затем для конкретных сервисов используется данный шаблон и указываются требуемые параметры
- Проверил, что манифесты генерируются корректно `kubecfg show services.jsonnet`
- Установил их - `kubecfg update services.jsonnet --namespace socks-shop`
- Магазин снова работает корректно


### Использовать решение на основе jsonnet | Задание со ⭐
- Использлвал Kapitan - инструмент для управления сложными развертываниями с использованием jsonnet
- Изучил документацию и пример использования Kapitan для kubernetes
- Из all.yaml убрал Deployment и  Service для carts, Обновил socks-shop, корзина перестала работать
- На основе примера для kubernetes в Kapital создал конфиги для генерации манифестов для микросервиса carts в каталоге kubernetes-templating/jsonnet
- Для компиляции нужно в данном каталоге выполнить команду `docker run -t --rm -v $(pwd):/src:delegated deepmind/kapitan compile`
- В каталоге compiled/socks-shop-kapitan/manifests/ появятся манифесты. Для их деплоя нужно выполнить команду 
`bash kubernetes-templating/jsonnet/compiled/socks-shop-kapitan/carts-deploy.sh`
- После деплоя восстановилась работа корзины


### Kustomize
- Для кастомизации используем сервис `user`
- В каталог kubernetes-templating/kustomize/base разместим манифесты для deployment и service. Также положим файл kustomization.yaml, в котором указывается за какие ресурсы отвечает Kustomize
- В каталоге kubernetes-templating/kustomize/overlays создадим директории с параметрами для двух окружений - socks-shop и socks-shop-prod. В данных параметрах указывается в каком namespace создавать ресурсы, какой добавлять префикс к ресурсам, Какие нужно сгенерировать label и с каким тагом использовать image.
- Выполним установку для окружения socks-shop
```
$ kubectl apply -k kubernetes-templating/kustomize/overlays/socks-shop/
service/dev-user created
deployment.extensions/dev-user created

$ kubectl get pods -nsocks-shop
NAME                            READY   STATUS    RESTARTS   AGE
carts-66bc68f95f-md5vf          1/1     Running   0          78m
carts-db-7d79c89fdb-zbd5w       1/1     Running   0          78m
catalogue-64d9568bcb-2lr6t      1/1     Running   0          70m
catalogue-db-55965799b9-n9wv7   1/1     Running   0          78m
### dev-user-66c4764c5d-vxfsh       1/1     Running   0          15s
front-end-6694dcd58f-zlsn9      1/1     Running   0          49m
orders-65bb8fcf9b-2zlgk         1/1     Running   0          78m
orders-db-6cdb57dc6d-drkqf      1/1     Running   0          78m
payment-9749b4948-cz7d8         1/1     Running   0          70m
queue-master-6b5b5c7658-pwkbp   1/1     Running   0          78m
rabbitmq-7764597b7b-7jf97       1/1     Running   0          78m
shipping-7f86cf76f8-gq58h       1/1     Running   0          78m
user-db-86dcc8cdb5-mmfjq        1/1     Running   0          78m
```



<br><br>
## Домашнее задание 11

### Выполнено:
- Установлен кластер vault в kubernetes
- Создали секреты и политики
- Настроили авторизацию в vault через kubernetes sa
- Сделали под с контейнером nginx, в который прокинем секреты из vault через consul-template

### Ход выполнения ДЗ:
- Склонировал репозиторий и установил consul с помощью helm
```
git clone https://github.com/hashicorp/consul-helm.git
helm install --name=consul consul-helm
```
- Склонировал репозиторий git clone https://github.com/hashicorp/vault-helm.git, Изменил переменные в файле values.yaml, Установил vault с помощью helm `helm install --name=vault .`
Поды не находятся в состоянии READY так, как не был инициализирован vault, из-за чего не выполнялись проверки "Readiness probe".
```
$helm status vault

LAST DEPLOYED: Mon Oct 28 16:59:32 2019
NAMESPACE: default
STATUS: DEPLOYED

RESOURCES:
==> v1/ConfigMap
NAME          DATA  AGE
vault-config  1     2m21s

==> v1/Pod(related)
NAME     READY  STATUS   RESTARTS  AGE
vault-0  0/1    Running  0         2m21s
vault-1  0/1    Running  0         2m21s
vault-2  0/1    Running  0         2m21s

==> v1/Service
NAME      TYPE       CLUSTER-IP   EXTERNAL-IP  PORT(S)            AGE
vault     ClusterIP  10.12.3.22   <none>       8200/TCP,8201/TCP  2m21s
vault-ui  ClusterIP  10.12.2.202  <none>       8200/TCP           2m21s

==> v1/ServiceAccount
NAME   SECRETS  AGE
vault  1        2m21s

==> v1/StatefulSet
NAME   READY  AGE
vault  0/3    2m21s

==> v1beta1/PodDisruptionBudget
NAME   MIN AVAILABLE  MAX UNAVAILABLE  ALLOWED DISRUPTIONS  AGE
vault  N/A            1                0                    2m21s


NOTES:

Thank you for installing HashiCorp Vault!

Now that you have deployed Vault, you should look over the docs on using
Vault with Kubernetes available here:

https://www.vaultproject.io/docs/


Your release is named vault. To learn more about the release, try:

  $ helm status vault
  $ helm get vault
```

```
$kubectl logs vault-0

2019-10-28T13:59:55.893Z [INFO]  core: seal configuration missing, not initialized
```
- Выполнили инициализацию vault
```
$ kubectl exec -it vault-0 -- vault operator init --key-shares=1 --key-threshold=1
Unseal Key 1: B06D+rBuZ/lN5k36fZ1ti5AWuRXLLdO8knXU+5BNK/k=

Initial Root Token: s.9J7G09Y1pGgku12CLeVusb2A

Vault initialized with 1 key shares and a key threshold of 1. Please securely
distribute the key shares printed above. When the Vault is re-sealed,
restarted, or stopped, you must supply at least 1 of these keys to unseal it
before it can start servicing requests.

Vault does not store the generated master key. Without at least 1 key to
reconstruct the master key, Vault will remain permanently sealed!

It is possible to generate new unseal keys, provided you have a quorum of
existing unseal keys shares. See "vault operator rekey" for more information.
```
- После этого поды перешли в состояние READY
```
$kubectl logs vault-0
2019-10-28T14:02:46.829Z [INFO]  core: seal configuration missing, not initialized
2019-10-28T14:02:47.000Z [INFO]  core: security barrier not initialized
2019-10-28T14:02:47.023Z [INFO]  core: security barrier initialized: shares=1 threshold=1
2019-10-28T14:02:47.100Z [INFO]  core: post-unseal setup starting
2019-10-28T14:02:47.140Z [INFO]  core: loaded wrapping token key
2019-10-28T14:02:47.140Z [INFO]  core: successfully setup plugin catalog: plugin-directory=
2019-10-28T14:02:47.142Z [INFO]  core: no mounts; adding default mount table
2019-10-28T14:02:47.165Z [INFO]  core: successfully mounted backend: type=cubbyhole path=cubbyhole/
2019-10-28T14:02:47.166Z [INFO]  core: successfully mounted backend: type=system path=sys/
2019-10-28T14:02:47.166Z [INFO]  core: successfully mounted backend: type=identity path=identity/
2019-10-28T14:02:47.220Z [INFO]  core: successfully enabled credential backend: type=token path=token/
2019-10-28T14:02:47.220Z [INFO]  core: restoring leases
2019-10-28T14:02:47.221Z [INFO]  rollback: starting rollback manager
2019-10-28T14:02:47.223Z [INFO]  expiration: lease restore complete
2019-10-28T14:02:47.239Z [INFO]  identity: entities restored
2019-10-28T14:02:47.240Z [INFO]  identity: groups restored
2019-10-28T14:02:47.241Z [INFO]  core: post-unseal setup complete
2019-10-28T14:02:47.260Z [INFO]  core: root token generated
2019-10-28T14:02:47.260Z [INFO]  core: pre-seal teardown starting
2019-10-28T14:02:47.260Z [INFO]  rollback: stopping rollback manager
2019-10-28T14:02:47.260Z [INFO]  core: pre-seal teardown complete
```
```
$ kubectl exec -it vault-0 -- vault status
Key                Value
---                -----
Seal Type          shamir
Initialized        true
Sealed             true
Total Shares       1
Threshold          1
Unseal Progress    0/1
Unseal Nonce       n/a
Version            1.2.2
HA Enabled         true
command terminated with exit code 2
```
- Распечатали каждый под с vault, проверили статус
```
$ kubectl exec -it vault-0 -- vault status
Key             Value
---             -----
Seal Type       shamir
Initialized     true
Sealed          false
Total Shares    1
Threshold       1
Version         1.2.2
Cluster Name    vault-cluster-cddd13ab
Cluster ID      69454c29-7063-0f06-1154-01fa9a334fa9
HA Enabled      true
HA Cluster      https://10.8.2.7:8201
HA Mode         active
```
```
$ kubectl exec -it vault-1 -- vault status
Key                    Value
---                    -----
Seal Type              shamir
Initialized            true
Sealed                 false
Total Shares           1
Threshold              1
Version                1.2.2
Cluster Name           vault-cluster-cddd13ab
Cluster ID             69454c29-7063-0f06-1154-01fa9a334fa9
HA Enabled             true
HA Cluster             https://10.8.2.7:8201
HA Mode                standby
Active Node Address    http://10.8.2.7:8200
```
```
$ kubectl exec -it vault-2 -- vault status
Key                    Value
---                    -----
Seal Type              shamir
Initialized            true
Sealed                 false
Total Shares           1
Threshold              1
Version                1.2.2
Cluster Name           vault-cluster-cddd13ab
Cluster ID             69454c29-7063-0f06-1154-01fa9a334fa9
HA Enabled             true
HA Cluster             https://10.8.2.7:8201
HA Mode                standby
Active Node Address    http://10.8.2.7:8200
```
- Проверим список доступных авторизаций
```
$ kubectl exec -it vault-0 -- vault auth list
Error listing enabled authentications: Error making API request.

URL: GET http://127.0.0.1:8200/v1/sys/auth
Code: 400. Errors:

* missing client token
command terminated with exit code 2
```
- Залогинимся в vault
```
$ kubectl exec -it vault-0 -- vault login
Token (will be hidden): 
Success! You are now authenticated. The token information displayed below
is already stored in the token helper. You do NOT need to run "vault login"
again. Future Vault requests will automatically use this token.

Key                  Value
---                  -----
token                s.9J7G09Y1pGgku12CLeVusb2A
token_accessor       E332LCKf2xRlcOYW5Gd8c224
token_duration       ∞
token_renewable      false
token_policies       ["root"]
identity_policies    []
policies             ["root"]
```
- Повторно запросим список авторизаций
```
$ kubectl exec -it vault-0 -- vault auth list
Path      Type     Accessor               Description
----      ----     --------               -----------
token/    token    auth_token_d5ef3858    token based credentials
```
- Создадим секреты в vault
```
$ kubectl exec -it vault-0 -- vault secrets list --detailed
Path          Plugin       Accessor              Default TTL    Max TTL    Force No Cache    Replication    Seal Wrap    Options    Description                                                UUID
----          ------       --------              -----------    -------    --------------    -----------    ---------    -------    -----------                                                ----
cubbyhole/    cubbyhole    cubbyhole_de30e36b    n/a            n/a        false             local          false        map[]      per-token private secret storage                           98cbfb7f-c273-944a-9342-7757bffd6ac0
identity/     identity     identity_a57b8f2e     system         system     false             replicated     false        map[]      identity store                                             ba0d257b-9a4b-a76b-4103-cb9dff107ba2
otus/         kv           kv_b1c88032           system         system     false             replicated     false        map[]      n/a                                                        d9ed38da-84ff-5d99-df69-218525850889
sys/          system       system_993f8629       n/a            n/a        false             replicated     false        map[]      system endpoints used for control, policy and debugging    ca64fa1b-f715-52de-0e24-86ec16ef9a87
```
```
$ kubectl exec -it vault-0 -- vault read otus/otus-ro/config
Key                 Value
---                 -----
refresh_interval    768h
password            asajkjkahs
username            otus
```
```
$ kubectl exec -it vault-0 -- vault kv get otus/otus-rw/config
====== Data ======
Key         Value
---         -----
password    asajkjkahs
username    otus
```
- Включим авторизацию черерз k8s
```
$ kubectl exec -it vault-0 -- vault auth list
Path           Type          Accessor                    Description
----           ----          --------                    -----------
kubernetes/    kubernetes    auth_kubernetes_09b60bc1    n/a
token/         token         auth_token_d5ef3858         token based credentials
```
- Создадим Service Account vault-auth и применим ClusterRoleBinding
```
$ kubectl create serviceaccount vault-auth
serviceaccount/vault-auth created

$ kubectl apply --filename vault-auth-service-account.yml
clusterrolebinding.rbac.authorization.k8s.io/role-tokenreview-binding created
```
- Подготовим переменные для записи в конфиг кубер авторизации
```
$ export VAULT_SA_NAME=$(kubectl get sa vault-auth -o jsonpath="{.secrets[*]['name']}")
$ export SA_JWT_TOKEN=$(kubectl get secret $VAULT_SA_NAME -o jsonpath="{.data.token}" | base64 --decode; echo)
$ export SA_CA_CRT=$(kubectl get secret $VAULT_SA_NAME -o jsonpath="{.data['ca\.crt']}" | base64 --decode; echo)
$ export K8S_HOST=$(more ~/.kube/config | grep server |awk '/http/ {print $NF}')

### alternative way
$ export K8S_HOST=$(kubectl cluster-info | grep ‘Kubernetes master’ | awk ‘/https/ {print $NF}’ | sed ’s/\x1b\[[0-9;]*m//g’ )
```
- Запишем конфиг в vault `kubectl exec -it vault-0 -- vault write auth/kubernetes/config token_reviewer_jwt="$SA_JWT_TOKEN" kubernetes_host="$K8S_HOST" kubernetes_ca_cert="$SA_CA_CRT"	`
- Создадим файл политики otus-policy.hcl
```
path "otus/otus-ro/*" {
	capabilities = ["read", "list"]
}
path "otus/otus-rw/*" {
	capabilities = ["read", "create", "list"]
}
```
- Создадим политку и роль в vault
```
$ kubectl cp otus-policy.hcl vault-0:/home/vault/

$ kubectl exec -it vault-0 -- vault policy write otus-policy /home/vault/otus-policy.hcl

$ kubectl exec -it vault-0 -- vault write auth/kubernetes/role/otus bound_service_account_names=vault-auth bound_service_account_namespaces=default policies=otus-policy ttl=24h
```
- Проверим как работает авторизация 
Создал под nginx, установил в него curl, jq. 
Залогинимся и получим клиентский токен
```
$ VAULT_ADDR=http://vault:8200

$ KUBE_TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)

$ curl --request POST --data '{"jwt": "'$KUBE_TOKEN'", "role": "otus"}' $VAULT_ADDR/v1/auth/kubernetes/login | jq

$ TOKEN=`curl -s --request POST --data '{"jwt": "'$KUBE_TOKEN'", "role": "otus"}' $VAULT_ADDR/v1/auth/kubernetes/login | jq '.auth.client_token'`
$ echo $TOKEN
s.sj8Sao9BJlJEmPrEAWLRcbNu
```
- Прочитаем записанные ранее секреты и попробуем их обновить
проверим чтение
```
$ curl --header "X-Vault-Token:s.sj8Sao9BJlJEmPrEAWLRcbNu" $VAULT_ADDR/v1/otus/otus-ro/config
{"request_id":"98999cc0-8b5f-beb0-ef48-26d30330a818","lease_id":"","renewable":false,"lease_duration":2764800,"data":{"password":"asajkjkahs","username":"otus"},"wrap_info":null,"warnings":null,"auth":null}

$ curl --header "X-Vault-Token:s.sj8Sao9BJlJEmPrEAWLRcbNu" $VAULT_ADDR/v1/otus/otus-rw/config1
{"request_id":"375b5e2a-876a-6a25-97a7-641977208cd4","lease_id":"","renewable":false,"lease_duration":2764800,"data":{"password":"asajkjkahs","username":"otus"},"wrap_info":null,"warnings":null,"auth":null}
```
проверим запись
```
$ curl --request POST --data '{"bar": "baz"}' --header "X-Vault-Token:s.TbzaluoJf6okw6UtKeqtF7e3" $VAULT_ADDR/v1/otus/otus-ro/config
{"errors":["1 error occurred:\n\t* permission denied\n\n"]}

$ curl --request POST --data '{"bar": "baz"}' --header "X-Vault-Token:s.TbzaluoJf6okw6UtKeqtF7e3" $VAULT_ADDR/v1/otus/otus-rw/config
{"errors":["1 error occurred:\n\t* permission denied\n\n"]}

$ curl --request POST --data '{"bar": "baz"}' --header "X-Vault-Token:s.TbzaluoJf6okw6UtKeqtF7e3" $VAULT_ADDR/v1/otus/otus-rw/config1
```

# > Почему мы смогли записать otus-rw/config1, но не смогли otus-rw/config
Потому что секрета otus-rw/config1 не существовало и мы его создали, а секрет otus-rw/config существовал, но политика прав не дает возможности изменять секреты

# > Измените политику так, чтобы можно было менять otus-rw/config
Изменил политику на следующую 
```
path "otus/otus-ro/*" {
   capabilities = ["read", "list"]
}
path "otus/otus-rw/*" {
   capabilities = ["read", "create", "list", "update"]
}
```

## Use case использования авторизации через кубер
- Заберем репозиторий с примерами
` git clone https://github.com/hashicorp/vault-guides.git `
- В каталоге vault-guides/identity/vault-agent-k8s-demo/configs-k8s скорректируем конфиги с учетом ранее созданых ролей и секретов
Изменил путь секрета в файле consul-template-config.hcl
Изменил имя роли  в файле vault-agent-config.hcl
Изменил значение для переменной окружения VAULT_ADDR в манифесте подов example-k8s-spec.yml
- Запускаем пример
```
$ kubectl create configmap example-vault-agent-config --from-file=./configs-k8s/

$ kubectl get configmap example-vault-agent-config -o yaml

$ kubectl apply -f example-k8s-spec.yml --record
```
- Проверка
Проверим, что consul получил пользовательский токен
```
$ kubectl exec -it vault-agent-example --container consul-template sh
/ # echo $(cat /home/vault/.vault-token)
s.lplKsU5wLz12fbBLPvXY1Eex
```
Из контейнера nginx скопировал файл index.html
```
$ cat kubernetes-vault/index.html 
  <html>
  <body>
  <p>Some secrets:</p>
  <ul>
  <li><pre>username: otus</pre></li>
  <li><pre>password: asajkjkahs</pre></li>
  </ul>
  
  </body>
  </html>
```

## создадим CA на базе vault
- Включим pki секретс
```
$ kubectl exec -it vault-0 -- vault secrets enable pki
Success! Enabled the pki secrets engine at: pki/

$ kubectl exec -it vault-0 -- vault secrets tune -max-lease-ttl=87600h pki
Success! Tuned the secrets engine at: pki/

$ kubectl exec -it vault-0 -- vault write -field=certificate pki/root/generate/internal common_name="exmaple.ru" ttl=87600h > CA_cert.crt
```
- пропишем URL для ca и отозванных сертификатов
```
$ kubectl exec -it vault-0 -- vault write pki/config/urls \
> issuing_certificates="http://vault:8200/v1/pki/ca" \
> crl_distribution_points="http://vault:8200/v1/pki/crl"
Success! Data written to: pki/config/urls
```
- создадим промежуточный сертификат
```
$ kubectl exec -it vault-0 -- vault secrets enable --path=pki_int pki
Success! Enabled the pki secrets engine at: pki_int/

$ kubectl exec -it vault-0 -- vault secrets tune -max-lease-ttl=87600h pki_int
Success! Tuned the secrets engine at: pki_int/

$ kubectl exec -it vault-0 -- vault write -format=json pki_int/intermediate/generate/internal common_name="example.ru Intermediate Authority" | jq -r '.data.csr' > pki_intermediate.csr
```
- пропишем промежуточный сертификат в vault
```
$ kubectl cp pki_intermediate.csr vault-0:/home/vault/

$ kubectl exec -it vault-0 -- vault write -format=json pki/root/sign-intermediate csr=@/home/vault/pki_intermediate.csr format=pem_bundle ttl="43800h" | jq -r '.data.certificate' > intermediate.cert.pem

$ kubectl cp intermediate.cert.pem vault-0:/home/vault/

$ kubectl exec -it vault-0 -- vault write pki_int/intermediate/set-signed certificate=@/home/vault/intermediate.cert.pem
Success! Data written to: pki_int/intermediate/set-signed
```
- Создадим и отзовем новые сертификаты
Создадим роль для выдачи с ертификатов
` kubectl exec -it vault-0 -- vault write pki_int/roles/example-dot-ru allowed_domains="example.ru" allow_subdomains=true max_ttl="720h"`

Создадим  сертификат
```
$ kubectl exec -it vault-0 -- vault write pki_int/issue/example-dot-ru common_name="gitlab.example.ru" ttl="24h"
Key                 Value
---                 -----
ca_chain            [-----BEGIN CERTIFICATE-----
MIIDnDCCAoSgAwIBAgIUJyT2R3MOoMle0Jmt295MYMHMljIwDQYJKoZIhvcNAQEL
BQAwFTETMBEGA1UEAxMKZXhtYXBsZS5ydTAeFw0xOTEwMjkwNzI5NTdaFw0yNDEw
MjcwNzMwMjdaMCwxKjAoBgNVBAMTIWV4YW1wbGUucnUgSW50ZXJtZWRpYXRlIEF1
dGhvcml0eTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAMYDpIDoEIUy
mBoT/wXGE0/L+QKxZyfsOnRpJUceKwbs59Di07avJe31rxP+v9mwSoG2uiiGe5hm
z6CsM05qACBEyOta+enyrSB7rcHYBishAOQDd8M1hjuwgi+27n9pg2I41Vjc0+NV
rvzK8rarOz2WQcrk4/g4VfQb19Ra+uE9Exldjxb4B8OGJWBY2+hlN5lfdftHH8l7
0O1rHCgE+W1thMv1zEqsz5Ri3CplarZWvek9Lmw9S3tOlz+hBWAzMwhIctaBUQ5f
DSSMiRGKARHaW2eKymaRRwLrd0s8Vjtk2vCKFlPPTSCuTJvsjqf0sW9LJ2n50+uB
0IhIPMmf9HECAwEAAaOBzDCByTAOBgNVHQ8BAf8EBAMCAQYwDwYDVR0TAQH/BAUw
AwEB/zAdBgNVHQ4EFgQUioAkspGY2Py77mhOxIZOlYWw6pIwHwYDVR0jBBgwFoAU
E/oQwdj6/QvOM8xO+osnx22+0mYwNwYIKwYBBQUHAQEEKzApMCcGCCsGAQUFBzAC
hhtodHRwOi8vdmF1bHQ6ODIwMC92MS9wa2kvY2EwLQYDVR0fBCYwJDAioCCgHoYc
aHR0cDovL3ZhdWx0OjgyMDAvdjEvcGtpL2NybDANBgkqhkiG9w0BAQsFAAOCAQEA
ubW6P6QBoMAjtAM2ltrOAz4v5OIrtJPheNTirNTgG2oDWn7q5g4OWlp1FxiuC8KW
GnYh7zg9ne0ALzh2/q87e2I2Mi7+wHzfvnhyjVl3SaO2c5lGJmDkG48eq+EG/OaS
yYdFPdehgUKjWmDuAKeuwhlKTsesCYl3GfzEvmW7ZEgcjsJbLnHx9Q/LsmQvVqPT
f8CPdwDVV2/7+pQpuTuzyEpZIlCpwgFQkevbSyQW4pYXYxGDiwE/F9rjiQivCf1n
HP14ISqKkcZIdQvflN1h1z6dmTgn+U5SsMmO5+BjBf/X6bYplWGCUwDF3465PT6k
EjsoL1ptSLIe8YCdlS5IxQ==
-----END CERTIFICATE-----]
certificate         -----BEGIN CERTIFICATE-----
MIIDZzCCAk+gAwIBAgIUGEfHsypupEyLIueLxSTmk4QyqvswDQYJKoZIhvcNAQEL
BQAwLDEqMCgGA1UEAxMhZXhhbXBsZS5ydSBJbnRlcm1lZGlhdGUgQXV0aG9yaXR5
MB4XDTE5MTAyOTA3MzMxM1oXDTE5MTAzMDA3MzM0M1owHDEaMBgGA1UEAxMRZ2l0
bGFiLmV4YW1wbGUucnUwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCz
i8x4+GSG1QUFvLT6Q0HMkPFqKNPQHQQsYjU6saGKODcydU2zCcBtlVH7iRVB5oY/
+j0OzzkPRZZm0cPlbT5ek5UgE8R3a3TEDPgBTHWNEtdw2NX8qkcSdbsRFWznVxQg
sC4zIsYSB35SHyF75aY2WE4AZY1JklG4tmWgdPiHPOsPactZug6WAlfOxtXis1Ak
ZVvf4yU5mtHm/6m78xhNwl90llRkurj2pkE+sULEZ8xFIyZ9swFCwzga67Beqz8s
wGFmHrz6yYaM8SSl7VgaiF8HqqTL7tPsqrhaTbv/cjjzj4o7H/iULfIBNoIIZGMX
nt+q+jOgisxQzNrU6devAgMBAAGjgZAwgY0wDgYDVR0PAQH/BAQDAgOoMB0GA1Ud
JQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjAdBgNVHQ4EFgQUwPWB/tnGEeu9swGP
r4Qpq8mG2Q0wHwYDVR0jBBgwFoAUioAkspGY2Py77mhOxIZOlYWw6pIwHAYDVR0R
BBUwE4IRZ2l0bGFiLmV4YW1wbGUucnUwDQYJKoZIhvcNAQELBQADggEBAF0i1huZ
J1wEVJbVvghRskDnXAdGNvrJfKd90pbX5mHZJGNK5N6FmXgl5IOkc59WMtlkngm/
84x+vkUtPitt0vGuaYqmef0PMZOl48RtcIg9RCITiL5WURn4VKOege7veMOsx6MF
miUoZTilR6w6j63rUvoEM2+qm5KQkCVV2qMi/X0JvKHTMFy6X7AOHjpTcbb6tOrm
nfr6+QQBtg6L9z8LVkRMpPLBxeP1TTCXGyiHBu6+cT3QNZSPI4G5QCXrBqU9HpP3
7MF7j+F3+OdnN9yIuVQXBSlCO9BxzSZoe2i6u0GOh6RSayk82gCfn1JUnixpSn2G
4iQqghT3JxVQYAU=
-----END CERTIFICATE-----
expiration          1572420823
issuing_ca          -----BEGIN CERTIFICATE-----
MIIDnDCCAoSgAwIBAgIUJyT2R3MOoMle0Jmt295MYMHMljIwDQYJKoZIhvcNAQEL
BQAwFTETMBEGA1UEAxMKZXhtYXBsZS5ydTAeFw0xOTEwMjkwNzI5NTdaFw0yNDEw
MjcwNzMwMjdaMCwxKjAoBgNVBAMTIWV4YW1wbGUucnUgSW50ZXJtZWRpYXRlIEF1
dGhvcml0eTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAMYDpIDoEIUy
mBoT/wXGE0/L+QKxZyfsOnRpJUceKwbs59Di07avJe31rxP+v9mwSoG2uiiGe5hm
z6CsM05qACBEyOta+enyrSB7rcHYBishAOQDd8M1hjuwgi+27n9pg2I41Vjc0+NV
rvzK8rarOz2WQcrk4/g4VfQb19Ra+uE9Exldjxb4B8OGJWBY2+hlN5lfdftHH8l7
0O1rHCgE+W1thMv1zEqsz5Ri3CplarZWvek9Lmw9S3tOlz+hBWAzMwhIctaBUQ5f
DSSMiRGKARHaW2eKymaRRwLrd0s8Vjtk2vCKFlPPTSCuTJvsjqf0sW9LJ2n50+uB
0IhIPMmf9HECAwEAAaOBzDCByTAOBgNVHQ8BAf8EBAMCAQYwDwYDVR0TAQH/BAUw
AwEB/zAdBgNVHQ4EFgQUioAkspGY2Py77mhOxIZOlYWw6pIwHwYDVR0jBBgwFoAU
E/oQwdj6/QvOM8xO+osnx22+0mYwNwYIKwYBBQUHAQEEKzApMCcGCCsGAQUFBzAC
hhtodHRwOi8vdmF1bHQ6ODIwMC92MS9wa2kvY2EwLQYDVR0fBCYwJDAioCCgHoYc
aHR0cDovL3ZhdWx0OjgyMDAvdjEvcGtpL2NybDANBgkqhkiG9w0BAQsFAAOCAQEA
ubW6P6QBoMAjtAM2ltrOAz4v5OIrtJPheNTirNTgG2oDWn7q5g4OWlp1FxiuC8KW
GnYh7zg9ne0ALzh2/q87e2I2Mi7+wHzfvnhyjVl3SaO2c5lGJmDkG48eq+EG/OaS
yYdFPdehgUKjWmDuAKeuwhlKTsesCYl3GfzEvmW7ZEgcjsJbLnHx9Q/LsmQvVqPT
f8CPdwDVV2/7+pQpuTuzyEpZIlCpwgFQkevbSyQW4pYXYxGDiwE/F9rjiQivCf1n
HP14ISqKkcZIdQvflN1h1z6dmTgn+U5SsMmO5+BjBf/X6bYplWGCUwDF3465PT6k
EjsoL1ptSLIe8YCdlS5IxQ==
-----END CERTIFICATE-----
private_key         -----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAs4vMePhkhtUFBby0+kNBzJDxaijT0B0ELGI1OrGhijg3MnVN
swnAbZVR+4kVQeaGP/o9Ds85D0WWZtHD5W0+XpOVIBPEd2t0xAz4AUx1jRLXcNjV
/KpHEnW7ERVs51cUILAuMyLGEgd+Uh8he+WmNlhOAGWNSZJRuLZloHT4hzzrD2nL
WboOlgJXzsbV4rNQJGVb3+MlOZrR5v+pu/MYTcJfdJZUZLq49qZBPrFCxGfMRSMm
fbMBQsM4GuuwXqs/LMBhZh68+smGjPEkpe1YGohfB6qky+7T7Kq4Wk27/3I484+K
Ox/4lC3yATaCCGRjF57fqvozoIrMUMza1OnXrwIDAQABAoIBAQCW77FHCNnJl46P
UiJ6OMw54qdwbT4TODFn9m91FhsNDVEps/9Lwajo9pxi7szWB6tYYU+vAXmgYwmb
CkC6wGmsLDkzLCr/kXAp2BUtUk+H9wzyKvdJXwQ8eoh2RiK1IDklebZ8+oC0a2RA
OTd25ooiKX35S2XJMZ5Nv9gTWgIL/TulKlNEQ20/eaUj+h/9iQVHaYAwFpu5sT4Q
RM55hNuSm4XGlrQH7afCEU6BDXlENKG6cJLoLXlCy45Iz/T6UA4MJt1QnsUVONqs
M8MJef2nTxkc/DWx1+096S/tEhWOvhE0m00Mr0qTFvft/9Bn5Rmmy1/XdLGFkhKS
RbJ4SsrxAoGBANz6gicPEY9R0IbI7zQFcYkaNBjtIbDTKJhiAdnBcDl1fyW3Yfzk
0sOUwmPMOeGOqzBe/ckL6LvCINXGhqCpBMH3nyXfCWUU4O53/Si9Jzs1rRufN7lY
NOysh+rz4RLh/vq9KiLwxWant31pDFNrekjRKxMTvT2CK4qndamdTPsVAoGBANAA
TUxUJLGfQSzg7t/vaUKz2Hnffxe+2RVCedYLpqdPoPbfufwK0Cj6xIjznTheJONs
gXkY+4Jv0bDYpTHcYTAekiqDopxcdlpoPv43r+DV0QxRRliqY/3q3Aap5KIMYVqU
3lZsX+hiy5X2OPc3rTJyhBZUGfyMXk7UD2rYLyizAoGAQbTfRHvvjb0XEyzmK4K+
2rSG7y57iReQh5cE09n3463zS6S2pzrnDK7MCl6si0wfzPdB4SkAX+v+VXJ9j4IS
XxahJOKn6X2G0IGvLhDofGueeIskR6FZw1Id7BfuQe4fIjFjORZ8q+SM4+Z7esaH
iuVfOIHzEDoHdmgKzY9vV20CgYEAkoWD7h7f8ley+8A/xXPK/HfgKInt53ZDSZyY
YtW2QenwA7g6NXgQhq2PwMGLoOeAqMwIsJuOoKXQWvlh9Su/Mrx2ToiIBgmEPc9t
gHsN5B36suiV22O8KGRHNlJ7gkOiWMLBlLOnI/ZkX3EhU9TepsjQj0ITRDpFPNZZ
PfSn080CgYAcmpV7BIHUZ3tThMFOxrhp1aSopRuCFgXlVvWfjy1L2hwTv7CHRlbK
vDi6LyzWpP7fGSrUQyvHSYm5Qtkl568VDZZCgdBCMdfUR3Swt8J1qRzAxo74oshP
e1AZFSfPKOE3D98AIwrLysAt1Eps+hLLY4063RIX6hOM9o6ox86bDg==
-----END RSA PRIVATE KEY-----
private_key_type    rsa
serial_number       18:47:c7:b3:2a:6e:a4:4c:8b:22:e7:8b:c5:24:e6:93:84:32:aa:fb
```

Отзовем сертификат
```
$ kubectl exec -it vault-0 -- vault write pki_int/revoke serial_number="18:47:c7:b3:2a:6e:a4:4c:8b:22:e7:8b:c5:24:e6:93:84:32:aa:fb"
Key                        Value
---                        -----
revocation_time            1572334476
revocation_time_rfc3339    2019-10-29T07:34:36.102254302Z





## Домашние задание 11


$  kubectl get pods -n istio-reddit
NAME                                    READY   STATUS    RESTARTS   AGE
comment-75998f4f65-zqvsk                2/2     Running   0          13m
istio-reddit-mongodb-6b89798d84-fjsj7   2/2     Running   0          13m
post-647b568657-fs2mh                   2/2     Running   0          163m
ui-69bc95c8b7-5492t                     2/2     Running   0          163m
ui-69bc95c8b7-wdpqr                     2/2     Running   0          13m
ui-69bc95c8b7-xsvqq                     2/2     Running   0          163m

$ kubectl get gateway -n istio-reddit
NAME             AGE
reddit-gateway   7s



$ kubectl get vs -A
NAMESPACE      NAME     GATEWAYS           HOSTS   AGE
istio-reddit   reddit   [reddit-gateway]   [*]     36s




$ kubectl get svc istio-ingressgateway -n istio-system
NAME                   TYPE           CLUSTER-IP    EXTERNAL-IP    PORT(S)                                                                                                                                      AGE
istio-ingressgateway   LoadBalancer   10.12.0.155   34.66.50.173   15020:30462/TCP,80:31380/TCP,443:31390/TCP,31400:31400/TCP,15029:31516/TCP,15030:30133/TCP,15031:31588/TCP,15032:31988/TCP,15443:32745/TCP   3h2m




$ kubectl get canary -n istio-reddit
NAME   STATUS         WEIGHT   LASTTRANSITIONTIME
ui     Initializing   0        2019-11-25T17:30:16Z


$ kubectl describe canary ui -n istio-reddit
...
Events:
  Type     Reason  Age   From     Message
  ----     ------  ----  ----     -------
  Warning  Synced  77s   flagger  Halt advancement ui-primary.istio-reddit waiting for rollout to finish: 0 out of 3 new replicas have been updated
  Warning  Synced  47s   flagger  Halt advancement ui-primary.istio-reddit waiting for rollout to finish: 1 of 3 updated replicas are available
  Normal   Synced  17s   flagger  Initialization done! ui.istio-reddit



$ kubectl get pods -n istio-reddit
NAME                                    READY   STATUS    RESTARTS   AGE
comment-75998f4f65-zqvsk                2/2     Running   0          23m
istio-reddit-mongodb-6b89798d84-fjsj7   2/2     Running   0          23m
post-647b568657-fs2mh                   2/2     Running   0          173m
ui-primary-d897cf7f9-c7fvr              2/2     Running   0          71s
ui-primary-d897cf7f9-g4cxq              2/2     Running   0          71s
ui-primary-d897cf7f9-hdpcf              2/2     Running   0          71s


$ kubectl describe canary ui -n istio-reddit
...
Events:
  Type     Reason  Age                    From     Message
  ----     ------  ----                   ----     -------
  Warning  Synced  29m                    flagger  Halt advancement ui-primary.istio-reddit waiting for rollout to finish: 0 out of 3 new replicas have been updated
  Warning  Synced  28m                    flagger  Halt advancement ui-primary.istio-reddit waiting for rollout to finish: 1 of 3 updated replicas are available
  Normal   Synced  28m                    flagger  Initialization done! ui.istio-reddit
  Normal   Synced  6m53s                  flagger  New revision detected! Scaling up ui.istio-reddit
  Normal   Synced  6m23s                  flagger  Starting canary analysis for ui.istio-reddit
  Normal   Synced  6m23s                  flagger  Advance ui.istio-reddit canary weight 5
  Warning  Synced  3m23s (x6 over 5m53s)  flagger  Halt advancement no values found for metric request-success-rate probably ui.istio-reddit is not receiving traffic
  Warning  Synced  83s (x4 over 2m53s)    flagger  Halt ui.istio-reddit advancement external check load-test failed Post http://flagger-loadtester.test/: dial tcp: lookup flagger-loadtester.test on 10.12.0.10:53: no such host
  Warning  Synced  53s                    flagger  Rolling back ui.istio-reddit failed checks threshold reached 10
  Warning  Synced  53s                    flagger  Canary failed! Scaling down ui.istio-reddit



$ kubectl get pods -n istio-reddit
NAME                                    READY   STATUS    RESTARTS   AGE
comment-75998f4f65-zqvsk                2/2     Running   0          53m
flagger-loadtester-655d8987d-g6x5n      2/2     Running   0          5m
istio-reddit-mongodb-6b89798d84-fjsj7   2/2     Running   0          53m
post-647b568657-fs2mh                   2/2     Running   0          3h22m
ui-88b57b7d9-zr5z8                      2/2     Running   0          19s
ui-primary-d897cf7f9-c7fvr              2/2     Running   0          30m
ui-primary-d897cf7f9-g4cxq              2/2     Running   0          30m
ui-primary-d897cf7f9-hdpcf              2/2     Running   0          30m



$ kubectl describe canary ui -n istio-reddit
...
Events:
  Type     Reason  Age                From     Message
  ----     ------  ----               ----     -------
  Warning  Synced  9m36s              flagger  Halt advancement ui-primary.istio-reddit waiting for rollout to finish: 0 out of 1 new replicas have been updated
  Normal   Synced  9m6s               flagger  Initialization done! ui.istio-reddit
  Normal   Synced  6m36s              flagger  New revision detected! Scaling up ui.istio-reddit
  Normal   Synced  6m6s               flagger  Starting canary analysis for ui.istio-reddit
  Normal   Synced  6m6s               flagger  Advance ui.istio-reddit canary weight 5
  Normal   Synced  5m36s              flagger  Advance ui.istio-reddit canary weight 10
  Normal   Synced  5m6s               flagger  Advance ui.istio-reddit canary weight 15
  Normal   Synced  4m36s              flagger  Advance ui.istio-reddit canary weight 20
  Normal   Synced  4m6s               flagger  Advance ui.istio-reddit canary weight 25
  Normal   Synced  3m36s              flagger  Advance ui.istio-reddit canary weight 30
  Normal   Synced  6s (x7 over 3m6s)  flagger  (combined from similar events): Promotion completed! Scaling down ui.istio-reddit


$ kubectl get pods -n istio-reddit
NAME                                    READY   STATUS    RESTARTS   AGE
comment-75998f4f65-zqvsk                2/2     Running   0          81m
flagger-loadtester-655d8987d-g6x5n      2/2     Running   0          32m
istio-reddit-mongodb-6b89798d84-fjsj7   2/2     Running   0          81m
post-647b568657-fs2mh                   2/2     Running   0          3h50m
ui-primary-7595576687-7r46d             2/2     Running   0          2m7s

$  kubectl get canaries -n istio-reddit
NAME   STATUS      WEIGHT   LASTTRANSITIONTIME
ui     Succeeded   0        2019-11-25T18:27:28Z





```
