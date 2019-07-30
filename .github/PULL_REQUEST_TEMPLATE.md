# Выполнено ДЗ №

 - [ ] Основное ДЗ
 - [ ] Задание со *

## В процессе сделано:
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

## Задание со * №1


## Задание со * №2


## PR checklist:
 - [ ] Выставлен label с номером домашнего задания


