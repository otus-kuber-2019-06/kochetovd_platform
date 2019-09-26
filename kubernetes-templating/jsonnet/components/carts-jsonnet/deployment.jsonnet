local kube = import "lib/kube.libjsonnet";
local kap = import "lib/kapitan.libjsonnet";
local inv = kap.inventory();

local myContainers = kube.Container("carts") {
    image: inv.parameters.carts.image,
    ports_+: {
        http: {containerPort: inv.parameters.carts.containerPort}
    },
    env_+:{
        ZIPKIN: "zipkin.jaeger.svc.cluster.local",
        JAVA_OPTS: "-Xms64m -Xmx128m -XX:PermSize=32m -XX:MaxPermSize=64m -XX:+UseG1GC -Djava.security.egd=file:/dev/urandom"
    },
    volumeMounts_+: {
        "tmp-volume": { mountPath: "/tmp" }
    },
    securityContext+: {
        runAsNonRoot: true,
        runAsUser: 10001,
        capabilities: { 
            drop: ["all"],
            add:  ["NET_BIND_SERVICE"],
            },
        readOnlyRootFilesystem: true,
    }
};

local deployment = kube.Deployment("carts") {
    spec+: {
        replicas: inv.parameters.carts.replicas,
        template+: {
            spec+: {
                containers_+: {
                    carts: myContainers
                },
                volumes_+: {
                    "tmp-volume": {emptyDir: {medium: "Memory"}}
                },
                nodeSelector+: {
                    "beta.kubernetes.io/os": "linux"
                }, 
            }
        }
    }
};

{
    carts_deployment: deployment
}
