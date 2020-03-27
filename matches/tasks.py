import tarfile
from io import BytesIO

import docker as dockerlib
import docker.errors as docker_errors
from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.utils import timezone

from .models import Match

logger = get_task_logger(__name__)


def tar(files):
    stream = BytesIO()
    archive = tarfile.TarFile(fileobj=stream, mode="w")
    for name, file in files.items():
        info = tarfile.TarInfo(name)
        info.size = file.size
        archive.addfile(info, file)
    archive.close()
    stream.seek(0)
    return stream


@shared_task(name="matches.tasks.run_match")
def run_match(match_id):
    logger.info(f'running match "{match_id}"...')
    match = Match.objects.get(pk=match_id)
    if match.finished_at is not None:
        logger.error(
            f"{match_id} is finished at {match.finished_at}. Re-running matches isn't possible"
        )
        return

    docker = dockerlib.DockerClient(base_url=settings.DOCKER_BASE_URL)
    try:
        match_container = docker.containers.create(
            image=settings.DOCKER_MATCH_RUNNER, name=f"match-{match.pk}",
        )
        archive = tar(
            {
                "game.py": match.game.code,
                "robot1.py": match.robot1.code,
                "robot2.py": match.robot2.code,
            }
        )
        if not match_container.put_archive("/game", archive):
            logger.error(
                f'failed to put codes archive into the "{match_container.name}" container'
            )
            return
        if match_container.wait() != 0:
            logger.error(f"{match_container.name} failed to run successfully")
    except (docker_errors.APIError, docker_errors.ImageNotFound) as e:
        # TODO: Define a "successful" attribute for matches
        logger.error(e)
        return

    match.runner_log = match_container.logs()
    match.finished_at = timezone.now()
    match.save()
