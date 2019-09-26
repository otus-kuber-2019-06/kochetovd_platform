local kube = import "lib/kube.libjsonnet";
local kap = import "lib/kapitan.libjsonnet";
local inv = kap.inventory();
local deployment = import "./deployment.jsonnet";

local svc = kube.Service("carts") {
    target_pod:: deployment.carts_deployment.spec.template,
    target_container_name:: "carts",
};


{
    carts_svc: svc
}
