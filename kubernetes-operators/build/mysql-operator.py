import kopf
import yaml
import kubernetes
import time
from jinja2 import Environment, FileSystemLoader


def render_template(filename, vars_dict):
    env = Environment(loader=FileSystemLoader('./templates'))
    template = env.get_template(filename)
    yaml_manifest = template.render(vars_dict)
    json_manifest = yaml.load(yaml_manifest)
    return json_manifest

def delete_success_jobs(mysql_instance_name):
    api = kubernetes.client.BatchV1Api()
    jobs = api.list_namespaced_job('default')
    for job in jobs.items:
        jobname = job.metadata.name
        print (job.metadata.name)
        print (job.status.succeeded)
        if (jobname == f"backup-{mysql_instance_name}-job"):
            if job.status.succeeded == 1:
                api.delete_namespaced_job(jobname,'default',propagation_policy='Background')

def wait_until_job_end(jobname):
    api = kubernetes.client.BatchV1Api()
    job_finished = False
    jobs = api.list_namespaced_job('default')
    while (not job_finished) and any(job.metadata.name == jobname for job in jobs.items):
        time.sleep(1)
        jobs = api.list_namespaced_job('default')
        for job in jobs.items:
            print (job.metadata.name)
            print (job.status.succeeded)
            if job.metadata.name == jobname:
                if job.status.succeeded == 1:
                    job_finished = True


@kopf.on.create('otus.homework', 'v1', 'mysqls')
# Функция, которая будет запускаться при создании объектов тип MySQL:
def mysql_on_create(body, spec, **kwargs):
    name = body['metadata']['name']
    image = body['spec']['image'] # cохраняем в переменные содержимое описания MySQL из CR
    password = body['spec']['password']
    database = body['spec']['database']
    storage_size = body['spec']['storage_size']
    # Генерируем JSON манифесты для деплоя
    persistent_volume = render_template('mysql-pv.yml.j2',{'name': name,'storage_size': storage_size})
    persistent_volume_claim = render_template('mysql-pvc.yml.j2',{'name': name,'storage_size': storage_size})
    service = render_template('mysql-service.yml.j2', {'name': name})
    deployment = render_template('mysql-deployment.yml.j2', {'name': name,'image': image,'password': password,'database': database})
    restore_job = render_template('restore-job.yml.j2', {'name': name,'image': image,'password': password,'database': database})
    # Определяем, что созданные ресурсы являются дочерними к управляемому CustomResource:
    kopf.append_owner_reference(persistent_volume, owner=body)
    kopf.append_owner_reference(persistent_volume_claim, owner=body) # addopt
    kopf.append_owner_reference(service, owner=body)
    kopf.append_owner_reference(deployment, owner=body)
    kopf.append_owner_reference(restore_job, owner=body)
    # ^ Таким образом при удалении CR удалятся все, связанные с ним pv,pvc,svc,deployments
    api = kubernetes.client.CoreV1Api()
    # Создаем mysql PV:
    api.create_persistent_volume(persistent_volume)
    # Создаем mysql PVC:
    api.create_namespaced_persistent_volume_claim('default', persistent_volume_claim)
    # Создаем mysql SVC:
    api.create_namespaced_service('default', service)
    # Создаем mysql Deployment:
    api = kubernetes.client.AppsV1Api()
    api.create_namespaced_deployment('default', deployment)

    restore_status = True
    # Пытаемся восстановиться из backup
    try:
        api = kubernetes.client.BatchV1Api()
        api.create_namespaced_job('default', restore_job)
    except kubernetes.client.rest.ApiException:
        restore_status = False

    # Cоздаем PVC и PV для бэкапов:
    try:
        backup_pv = render_template('backup-pv.yml.j2', {'name': name})
        api = kubernetes.client.CoreV1Api()
        api.create_persistent_volume(backup_pv)
    except kubernetes.client.rest.ApiException:
        pass

    try:
        backup_pvc = render_template('backup-pvc.yml.j2', {'name': name})
        api = kubernetes.client.CoreV1Api()
        api.create_namespaced_persistent_volume_claim('default', backup_pvc)
    except kubernetes.client.rest.ApiException:
        pass

    if restore_status:
        kopf.event(body, type='Normal', reason='Logging', message="mysql created with restore-job")
        return {'Message': "mysql created with restore-job"}
    else:
        kopf.event(body, type='Normal', reason='Logging', message=logger.info)
        return {'Message': "mysql created without restore-job"}


@kopf.on.delete('otus.homework', 'v1', 'mysqls')
def delete_object_make_backup(body, **kwargs):
    name = body['metadata']['name']
    image = body['spec']['image']
    password = body['spec']['password']
    database = body['spec']['database']
    delete_success_jobs(name)
    # Cоздаем backup job:
    api = kubernetes.client.BatchV1Api()
    backup_job = render_template('backup-job.yml.j2', {
        'name': name,
        'image': image,
        'password': password,
        'database': database})
    api.create_namespaced_job('default', backup_job)
    wait_until_job_end(f"backup-{name}-job")
    return {'message': "mysql and its children resources deleted"}


@kopf.on.field('otus.homework', 'v1', 'mysqls', field='spec.database')
def mysql_change_db_name(body, old, new, **kwargs):
    name = body['metadata']['name']
    image = body['spec']['image']
    password = body['spec']['password']

    renamedb_job = render_template('change-name-db-job.yml.j2', {'name': name,'image': image,'password': password,'database_old': old, 'database_new': new})
    api = kubernetes.client.BatchV1Api()
    api.create_namespaced_job('default', renamedb_job)
    wait_until_job_end(f"renamedb-{name}-job")
    return {'message': f"Change name db from {old} to {new}"}
