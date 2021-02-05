from invoke import task
from pathlib import Path
from dotenv import load_dotenv
import os
import json

load_dotenv()


@task
def format_code(c):
    c.run("pre-commit install")
    c.run("SKIP=terraform_fmt pre-commit run --all-files")


@task
def develop(c):
    c.run("docker-compose up")


@task
def develop_flush(c):
    c.run("docker-compose build")


@task
def tests(c):
    c.run(
        "docker-compose "
        "-f docker-compose.yml "
        "-f compose-files/docker-compose.test.yml "
        "up --exit-code-from backend"
    )


@task
def get_identity(c):
    c.config["accound_id"] = c.run(
        'aws sts get-caller-identity | jq ".Account"'
    ).stdout.strip()


@task(get_identity)
def apply_repos(c):
    with c.cd("infrastructure/repos"):
        c.run("terraform init && terraform apply --auto-approve")


@task
def destroy_repos(c):
    with c.cd("infrastructure/repos"):
        c.run("terraform init && terraform destroy --auto-approve")


@task(get_identity)
def apply_ecs(c, snapshot_identifier=None):
    snapshot_opt = ""
    if snapshot_identifier:
        snapshot_opt = f"-var 'snapshot_identifier={snapshot_identifier}'"
    with c.cd("infrastructure/ecs"):
        c.run(f"terraform init && terraform apply --auto-approve {snapshot_opt}")


@task
def destroy_ecs(c):
    with c.cd("infrastructure/ecs"):
        c.run("terraform init && terraform destroy --auto-approve")


@task
def login(c):
    c.run(
        f"aws ecr get-login-password --region $AWS_REGION | "
        f"docker login --username AWS --password-stdin {c.accound_id}.dkr.ecr.eu-central-1.amazonaws.com"
    )


@task(login)
def build(c):
    with c.cd("infrastructure/repos"):
        repo_url = c.run("terraform output backend_repo_url").stdout.split()[0]
    if not repo_url:
        return
    c.run(f"docker build -t {repo_url} ./backend")
    c.run(f"docker push {repo_url}")


@task
def ecs_stop(c):
    result = c.run(
        "aws ecs list-tasks --cluster $CLUSTER_NAME --region $AWS_REGION  --service-name $SERVICE_NAME | jq '.taskArns'"
    ).stdout.strip()

    if result:
        for servide_id in json.loads(result):
            c.run(f"aws ecs stop-task --region $AWS_REGION --task {servide_id}")


@task
def force_deployment(c):
    ecs_stop(c)
    c.run(
        "aws ecs update-service --region=$AWS_REGION --cluster $CLUSTER_NAME  --service $SERVICE_NAME --force-new-deployment"
    )


@task
def backup(c):
    c.run(
        "aws rds create-db-snapshot --region $AWS_REGION "
        "--db-snapshot-identifier max-db-snapshot "
        "--db-instance-identifier max-dev-max-dev-test-db"
    )


@task
def restore(c):
    # c.run(
    # 'aws rds modify-db-instance --region $AWS_REGION '
    # '--db-instance-identifier max-dev-max-dev-test-db '
    # '--new-db-instance-identifier old-max-dev-max-dev-test-db '
    # '--apply-immediately'
    # )
    with c.cd("infrastructure/ecs"):
        c.run(
            "terraform init && terraform destroy --auto-approve --target=module.rds_instance"
        )
    apply_ecs(c, snapshot_identifier="max-db-snapshot")


@task
def list(c):
    c.run(
        "aws rds describe-db-snapshots --region $AWS_REGION "
        "--db-instance-identifier max-dev-max-dev-test-db"
    )


@task(get_identity)
def together(c):
    apply_repos(c)
    login(c)
    build(c)
    apply_ecs(c)
    force_deployment(c)
    with c.cd("infrastructure/ecs"):
        c.run("terraform output dns")


@task(get_identity)
def refresh(c):
    with c.cd("infrastructure/ecs"):
        c.run("terraform refresh")


@task(get_identity)
def destroy_all(c):
    destroy_ecs(c)
    destroy_repos(c)


@task
def ci_server(c):
    c.run("docker-compose up -d")


CI_NAME = "dle"
PIPELINE_NAME = "on-pr"


@task
def concourse_login(c):
    c.run(f"fly login -t {CI_NAME} -u test -p test -c http://localhost:8080")


@task(concourse_login)
def set_pipelines(c):
    GAT = os.getenv("GAT")
    for pipeline_name in ["on-pr", "on-merge"]:
        c.run(
            f"fly -t {CI_NAME} set-pipeline -c ./CI/{pipeline_name}.yml -p {pipeline_name} "
            f'-v github-access-token="{GAT}"'
        )


@task
def unpause(c):
    c.run(f"fly -t {CI_NAME} unpause-job --job {PIPELINE_NAME}/set-self")


@task
def trigger(c, name=PIPELINE_NAME):
    assert name
    pipeline_name = name
    c.run(f"fly -t {CI_NAME} trigger-job --job {pipeline_name}/print-creds")
