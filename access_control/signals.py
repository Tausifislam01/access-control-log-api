import subprocess
from django.conf import settings
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import AccessLog


def _ps_escape_single_quotes(value: str) -> str:
    return value.replace("'", "''")


def _append_log_line(line: str) -> None:
    log_path = str(settings.BASE_DIR / "system_events.log")
    safe_line = _ps_escape_single_quotes(line)
    safe_path = _ps_escape_single_quotes(log_path)

    cmd = f"Add-Content -Path '{safe_path}' -Value '{safe_line}'"
    subprocess.run(["powershell", "-NoProfile", "-Command", cmd], check=False)


@receiver(post_save, sender=AccessLog)
def log_accesslog_created(sender, instance: AccessLog, created: bool, **kwargs):
    if not created:
        return
    _append_log_line(
        f"Created AccessLog: Card ID {instance.card_id}, Door: {instance.door_name}, Granted: {instance.access_granted}"
    )


@receiver(post_delete, sender=AccessLog)
def log_accesslog_deleted(sender, instance: AccessLog, **kwargs):
    _append_log_line(
        f"Deleted AccessLog: Card ID {instance.card_id}, Door: {instance.door_name}"
    )
