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

### Обычное домашнее задание
- Подготовил кофиг для кластера с установкой опции VolumeSnapshatDataSource=true  `cluster/cluster.yaml`
- Выполнил создание кластера с указанием конфига
`kind create cluster --config cluster/cluster.yaml`
- установил CSI Hostpath Driver https://github.com/kubernetes-csi/csi-driver-host-path выполнив скрипт 
`deploy/kubernetes-1.15/deploy-hostpath.sh`
- Создал StorageClass csi-hostpath-sc hw/storage_class.yml
`kubectl apply -f hw/01-storage_class.yml`
- Создал объект PVC c именем storage-pvc и StorageClass csi-hostpath-sc
`kubectl apply -f hw/02-pvc_storageclass.yml`
- Создал объект Pod c именем storage-pod и монтирующем pvc storage-pvc в каталог /data
`kubectl apply -f hw/03-pod_storaclass.yml`



### Задание со *
- Развернул кластер в GCP, состоящий из 3 ВМ. Развернул кластер kubernetes с помощью kubespray
- Создал доп ВМ для хранилища с дополнительным диском
- Добавил ко всем ВМ дополнительный сетевой интерфейс
- На машине для iscsi установил targetcli-fb
- Создал LVM
```
root@instance-4:~# pvcreate /dev/sdb1 
  Physical volume "/dev/sdb1" successfully created.
root@instance-4:~# vgcreate VolGroup00 /dev/sdb1 
  Volume group "VolGroup00" successfully created
root@instance-4:~# lvcreate -L 3G -n kvmVM VolGroup00
  Logical volume "kvmVM" created.
```
- Создание iscsi хранилище
```
root@instance-4:~# targetcli
targetcli shell version 2.1.fb43
Copyright 2011-2013 by Datera, Inc and others.
For help on commands, type 'help'.
```
Создал блочное устройство в бэксторе
```
/> /backstores/block create storage1 /dev/mapper/VolGroup00-kvmVM 
Created block storage object storage1 using /dev/mapper/VolGroup00-kvmVM.
```
Создал iscsi таргет
```
/> /iscsi create 
Created target iqn.2003-01.org.linux-iscsi.instance-4.x8664:sn.37b09c000f75.
Created TPG 1.
Global pref auto_add_default_portal=true
Created default portal listening on all IPs (0.0.0.0), port 3260.
```
Перейдем в иерархии targetcli на уровень tpg1 и установим параметры авторизации
```
iscsi/iqn.20...9c000f75/tpg1> set parameter AuthMethod=None
Parameter AuthMethod is now 'None'.
/iscsi/iqn.20...9c000f75/tpg1> set attribute authentication=0
Parameter authentication is now '0'.
```
Укажем iqn имя инициатора, который будет иметь право подключаться к таргету.
```
/iscsi/iqn.20...9c000f75/tpg1> acls/ create iqn.2005-03.org.open-iscsi:f72465cabb26
Created Node ACL for iqn.2005-03.org.open-iscsi:f72465cabb26
/iscsi/iqn.20...9c000f75/tpg1> acls/ create iqn.2005-03.org.open-iscsi:b5ecfb87ba70
Created Node ACL for iqn.2005-03.org.open-iscsi:b5ecfb87ba70
```
Создадим LUN на основе объекта хранилища в бэксторе
```
/iscsi/iqn.20...9c000f75/tpg1> luns/ create /backstores/block/storage1 
Created LUN 0.
Created LUN 0->0 mapping in node ACL iqn.2005-03.org.open-iscsi:b5ecfb87ba70
Created LUN 0->0 mapping in node ACL iqn.2005-03.org.open-iscsi:f72465cabb26
```
Укажем IP-адрес, который будет слушать таргет. 
```
/iscsi/iqn.20...9c000f75/tpg1> portals/ create 10.127.0.13 3261
Created network portal 10.127.0.13:3261.
```
Посмотрим иерархию, в виде которой представлен таргет
```
/> ls
o- / ......................................................................................................................... [...]
  o- backstores .............................................................................................................. [...]
  | o- block .................................................................................................. [Storage Objects: 1]
  | | o- storage1 ..................................................... [/dev/mapper/VolGroup00-kvmVM (3.0GiB) write-thru activated]
  | o- fileio ................................................................................................. [Storage Objects: 0]
  | o- pscsi .................................................................................................. [Storage Objects: 0]
  | o- ramdisk ................................................................................................ [Storage Objects: 0]
  o- iscsi ............................................................................................................ [Targets: 1]
  | o- iqn.2003-01.org.linux-iscsi.instance-4.x8664:sn.7fe91425ce4b ...................................................... [TPGs: 1]
  |   o- tpg1 ............................................................................................... [no-gen-acls, no-auth]
  |     o- acls .......................................................................................................... [ACLs: 2]
  |     | o- iqn.2005-03.org.open-iscsi:b5ecfb87ba70 .............................................................. [Mapped LUNs: 1]
  |     | | o- mapped_lun0 .............................................................................. [lun0 block/storage1 (rw)]
  |     | o- iqn.2005-03.org.open-iscsi:f72465cabb26 .............................................................. [Mapped LUNs: 1]
  |     |   o- mapped_lun0 .............................................................................. [lun0 block/storage1 (rw)]
  |     o- luns .......................................................................................................... [LUNs: 1]
  |     | o- lun0 .................................................................. [block/storage1 (/dev/mapper/VolGroup00-kvmVM)]
  |     o- portals .................................................................................................... [Portals: 3]
  |       o- 0.0.0.0:3260 ..................................................................................................... [OK]
  |       o- 10.127.0.13:3261 ................................................................................................. [OK]
  |       o- 10.127.0.6:3261 .................................................................................................. [OK]
  o- loopback ......................................................................................................... [Targets: 0]
  o- vhost ............................................................................................................ [Targets: 0]
```
- Создаим PersistentVolume `kubectl apply -f kubernetes-storage/iscsi/pv.yaml`
- Создаим PersistentVolumeClaim `kubectl apply -f kubernetes-storage/iscsi/pvc.yaml`
- Создаим Pod `kubectl apply -f kubernetes-storage/iscsi/pod.yaml`
- Подключимся к pod и запишем данные в /data/file
```
root@instance-1:~# kubectl exec -ti  pod-iscsi bash
root@pod-iscsi:/# cd /data/
root@pod-iscsi:/data# echo "Hello World!" > file
root@pod-iscsi:/data# cat file 
Hello World!
```
- Сделаем снапшот LVM раздела 
```
root@instance-4:~# lvcreate --size 3G --snapshot --name kvmVM_snap /dev/VolGroup00/kvmVM
  Using default stripesize 64.00 KiB.
  Logical volume "kvmVM_snap" created.
root@instance-4:~# lvs
  LV         VG         Attr       LSize Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert
  kvmVM      VolGroup00 owi-aos--- 3.00g
  kvmVM_snap VolGroup00 swi-a-s--- 3.00g      kvmVM  0.00
```
- Удалим данные, pod, pvc, pv, lvm из iscsi
```
root@instance-1:~# kubectl exec -ti  pod-iscsi bash
root@pod-iscsi:/# rm /data/*

root@instance-1:~# kubectl delete pods --all
pod "pod-iscsi" deleted
root@instance-1:~# kubectl delete pvc --all
persistentvolumeclaim "pvc-iscsi" deleted
root@instance-1:~# kubectl delete pv --all
persistentvolume "pv-iscsi" deleted

root@instance-4:~# targetcli 
targetcli shell version 2.1.fb43
Copyright 2011-2013 by Datera, Inc and others.
For help on commands, type 'help'.
/> backstores/block/ delete storage1 
```
- Восстаналиваем lvm из снапшота
```
root@instance-4:~# lvconvert --merge /dev/VolGroup00/kvmVM_snap 
  Merging of volume VolGroup00/kvmVM_snap started.
  VolGroup00/kvmVM: Merged: 100.00%
Deleted storage object storage1.
```
Снова добавляем раздел в хранилище iscsi
```
root@instance-4:~# targetcli 
targetcli shell version 2.1.fb43
Copyright 2011-2013 by Datera, Inc and others.
For help on commands, type 'help'.
/> /backstores/block create storage1 /dev/mapper/VolGroup00-kvmVM 
Created block storage object storage1 using /dev/mapper/VolGroup00-kvmVM.
/> cd iscsi/iqn.2003-01.org.linux-iscsi.instance-4.x8664:sn.7fe91425ce4b/tpg1/
/iscsi/iqn.20...1425ce4b/tpg1> luns/ create /backstores/block/storage1 
Created LUN 0.
Created LUN 0->0 mapping in node ACL iqn.2005-03.org.open-iscsi:b5ecfb87ba70
Created LUN 0->0 mapping in node ACL iqn.2005-03.org.open-iscsi:f72465cabb26
/iscsi/iqn.20...1425ce4b/tpg1> exit
Global pref auto_save_on_exit=true
Last 10 configs saved in /etc/rtslib-fb-target/backup.
Configuration saved to /etc/rtslib-fb-target/saveconfig.json
```
- Создадим pv, pvc, pod. Зайдем в pod и проверим данные
```
root@instance-1:~# kubectl get pods
NAME        READY   STATUS    RESTARTS   AGE
pod-iscsi   1/1     Running   0          23s
root@instance-1:~# kubectl exec -ti pod-iscsi bash
root@pod-iscsi:/# cd /data/
root@pod-iscsi:/data# ls -al
total 28
drwxr-xr-x 3 root root  4096 Oct 23 12:05 .
drwxr-xr-x 1 root root  4096 Oct 23 12:11 ..
-rw-r--r-- 1 root root    13 Oct 23 12:05 file
drwx------ 2 root root 16384 Oct 23 12:00 lost+found
root@pod-iscsi:/data# cat file 
Hello World!
```
- Данные на месте





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
