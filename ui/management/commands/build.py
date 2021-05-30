from .utils import render_html_static, move_react_media
import json
import subprocess
import sys  # noqa
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    STATIC_ROOT = settings.STATIC_ROOT

    def _run_npm(self, cmd, args=None, npm_bin="npm"):
        """Run NPM."""
        if npm_bin == "npm":
            command = [npm_bin, "run", cmd] + list(args)
        else:
            command = [npm_bin, cmd] + list(args)
        pkgdir = settings.BASE_DIR / "frontend"
        with open(pkgdir / "package.json", "r") as f:
            if cmd not in json.load(f)["scripts"]:
                raise CommandError("command not found")

        return subprocess.call(
            command,
            cwd=pkgdir,
        )

    def handle(self, *args, **kwargs):
        self._run_npm("build", args="")
        call_command("collectstatic", "--noinput")
        render_html_static(self.STATIC_ROOT)
        move_react_media(
            self.STATIC_ROOT / "static" / "media", self.STATIC_ROOT / "media"
        )
        self.stdout.write(
            self.style.SUCCESS(
                "build complete. Run python manage.py run to start both dev servers"
            )
        )
        self.stdout.write(
            self.style.NOTICE(
                "Run python manage.py run to start both dev servers separately "
            )
        )
        self.stdout.write(
            self.style.NOTICE("Run python manage.py runserver to start django server")
        )
