import datetime
import pytz
import os,sys
from kubernetes import client, config

#DEPLOYMENT_NAME = "nginx-deployment"
#os.system("python3 deployment_create_crud.py arg1 arg2")

def create_deployment_object():
    # Configureate Pod template container
    container = client.V1Container(
        name=sys.argv[1],
        image=sys.argv[2],
        ports=[client.V1ContainerPort(container_port=8888)],
        resources=client.V1ResourceRequirements(
            requests={"cpu": "100m", "memory": "200Mi"},
            limits={"cpu": "500m", "memory": "500Mi"},
        ),
    )

    # Create and configurate a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "nginx"}),
        spec=client.V1PodSpec(containers=[container]),
    )

    # Create the specification of deployment
    spec = client.V1DeploymentSpec(
        replicas=1, template=template, selector={
            "matchLabels":
            {"app": "nginx"}})

    # Instantiate the deployment object
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=sys.argv[1]),
        spec=spec,
    )

    return deployment


def create_deployment(api, deployment):
    # Create deployement
    resp = api.create_namespaced_deployment(
        body=deployment, namespace="default"
    )

    print("\n[INFO] deployment `nginx-deployment` created.\n")
    print("%s\t%s\t\t%s\t%s" % ("NAMESPACE", "NAME", "REVISION", "IMAGE"))
    print(
        "%s\t\t%s\t\t%s\t\t%s\n"
        % (
            resp.metadata.namespace,
            resp.metadata.name,
            resp.metadata.generation,
            sys.argv[2]
            #resp.spec.template.spec.containers[0].image,
        )
    )

def main():
    # Configs can be set in Configuration class directly or using helper
    # utility. If no argument provided, the config will be loaded from
    # default location.
    config.load_kube_config()
    apps_v1 = client.AppsV1Api()

    # Uncomment the following lines to enable debug logging
    # c = client.Configuration()
    # c.debug = True
    # apps_v1 = client.AppsV1Api(api_client=client.ApiClient(configuration=c))

    # Create a deployment object with client-python API. The deployment we
    # created is same as the `nginx-deployment.yaml` in the /examples folder.
    deployment = create_deployment_object()

    create_deployment(apps_v1, deployment)

if __name__ == "__main__":
    main()
