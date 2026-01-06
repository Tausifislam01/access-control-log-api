import sys
import subprocess
from django.conf import settings
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import AccessLog


def _append_log_line(line: str) -> None:
    log_path = str(settings.BASE_DIR / "system_events.log")
    subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys; p=sys.argv[1]; s=sys.argv[2]; "
            "open(p, 'a', encoding='utf-8').write(s + '\\n')",
            log_path,
            line,
        ],
        check=False,
    )


@receiver(post_save, sender=AccessLog)
def log_accesslog_created(sender, instance: AccessLog, created: bool, **kwargs):
    if not created:
        return

    timestamp = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")
    status = "GRANTED" if instance.access_granted else "DENIED"
    _append_log_line(
        f"[{timestamp}] - CREATE: Access log created for card {instance.card_id}. Status: {status}."
    )


@receiver(post_delete, sender=AccessLog)
def log_accesslog_deleted(sender, instance: AccessLog, **kwargs):
    timestamp = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")
    _append_log_line(
        f"[{timestamp}] - DELETE: Access log (ID: {instance.pk}) for card {instance.card_id} was deleted."
    )
