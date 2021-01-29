from invoke import task
from pathlib import Path
from dotenv import load_dotenv
import os
import json

load_dotenv()


@task
def validate_code(c):
    c.run("pre-commit install")
    c.run("pre-commit run --all-files")


@task
def develop(c):
    c.run("docker-compose up")


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
def force_deployment(c):
    result = c.run(
        "aws ecs list-tasks --cluster $CLUSTER_NAME --region $AWS_REGION  --service-name $SERVICE_NAME | jq '.taskArns'"
    ).stdout.strip()
    if result:
        for servide_id in json.loads(result):
            c.run(f"aws ecs stop-task --region $AWS_REGION --task {servide_id}")
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
