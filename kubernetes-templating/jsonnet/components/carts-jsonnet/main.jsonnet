local svc = import "./service.jsonnet";
local deployment = import "./deployment.jsonnet";


{
    "app-service": svc.carts_svc,
    "app-deployment": deployment.carts_deployment,
}
