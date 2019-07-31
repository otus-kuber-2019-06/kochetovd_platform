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
  - Создал SA bob, Сделал clusterrolebinding для sa bob и clusterrole admin;
  - Создал SA dave без связки с ролью.

TASK02:
  - Создал ns prometheus;
  - Создал SA carol в ns prometheus;
  - Сделал cluster роль, позволяющую делать get, list, watch в отношении Pods всего кластера;
  - Сделал clusterrolebindind даной роль и ns prometheus.

TASK03:
  - Создал ns dev;
  - Создал sa jane в ns dev;
  - Создал role admin, Сделал rolebinding sa jane и role admin;
  - Создал sa ken в ns dev;
  - Создал role view, Сделал rolebinding sa jane и role admin.



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

### Задание со *
> Сделайте сервис LoadBalancer, который откроет доступ к CoreDNS снаружи кластера (позволит получать записи из CoreDNS через внешний IP. Например nslookup web.default.cluster.local 172.17.255.10).

- Созданы манифесты Service типа LoadBalancer для CoreDNS, позволяющие получить доступ к 53 TCP, UDP портам снаружи кластера.
Для проверки нужно выполнить команды
```
kubectl apply -f core-dns-svc-lb-udp.yaml
kubectl apply -f core-dns-svc-lb-tcp.yaml 
```
Затем проверить работу dns
```
$ nslookup web-svc.default.svc.cluster.local 172.17.255.3
Server:		172.17.255.3
Address:	172.17.255.3#53

Name:	web-svc.default.svc.cluster.local
Address: 172.17.0.6
Name:	web-svc.default.svc.cluster.local
Address: 172.17.0.3
Name:	web-svc.default.svc.cluster.local
Address: 172.17.0.4
```

> добавьте доступ к kubernetesdashboard через наш Ingress-прокси (сервис должен быть доступен через префикс /dashboard)

- Создал манифест с ресурсом Ingress для предоставления доступа к kubernetes-dashboard извне кластера;
- Для применения манифеста выполнить команду `kubectl apply -f kubernetes-dashboard-ingress.yaml`;
- С помощью команды `kubectl  get ing -A` определить ip адрес назначений Ingress-у;
- Перейти по ссылке https://<ip>/dashboard/.

> Реализуйте канареечное развертывание (перенаправление части трафика на выделенную группу подов по HTTPзаголовку). Документация . Естественно, что вам понадобятся 1-2 "канареечных" пода.

- Создал манифесты canary-ns.yaml, canary-prod-ing.yaml, canary-canary-ing.yaml для реализации канареечного развертывания подов;
- Применить манифест для создания namespace `kubectl apply -f canary-ns.yaml`;

- Применить манифесты `kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/docs/examples/http-svc.yaml -n echo-production` для развертывания приложения(Создается Deployment, Service) в ns echo-production
- Применить манифест для деплоя Ingress для доступа к приложению в ns echo-production `kubectl apply -f canary-prod-ing.yaml -n echo-production`

- Применить манифесты `kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/docs/examples/http-svc.yaml -n echo-canary` для развертывания приложения(Создается Deployment, Service) в ns echo-canary
- Применить манифест для деплоя Ingress, реализующего канареечное развертывание, для доступа к приложению в ns echo-canary `kubectl apply -f canary-canary-ing.yaml -n echo-canary`

- Узнать ip адрес Ingress, выполнив команду `kubectl  get ing -A`. Добавить в hosts строку `<ip>	echo.com`
- Для проверки выполнить в консоли запросы с помощью curl
```
curl echo.com
curl --header "Canary-By-Header:always" echo.com
```
В первом случае, в выводе команды будет `pod namespace:	echo-production`, а во втором случае, `pod namespace:	echo-canary`


### Ответы на вопросы
> Попробуйте разные варианты деплоя с крайними значениями maxSurge и maxUnavailable (оба 0, оба 100%, 0 и 100%)

если maxSurge и maxUnavailable выставить в 0 - то получаем ошибку невозможности выполнения деплоя, вида 
```
The Deployment "web" is invalid: spec.strategy.rollingUpdate.maxUnavailable: Invalid value: intstr.IntOrString{Type:0, IntVal:0, StrVal:""}: may not be 0 when `maxSurge` is 0
```
При других вариантах все работает корректно, т.к. maxUnavailable указывает максимальное количество подов, которое может быть недоступно в процессе обновления, а maxSurge - максимальное количество подов, которое может быть создано от желаемое количество подов, указанного в `replicas`.




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


