import shutil
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.test import Client, override_settings
from django.urls import reverse, get_script_prefix, set_script_prefix

from core.models import Regions


class Command(BaseCommand):
    help = "Render the site to plain HTML files (for GitHub Pages)."

    def add_arguments(self, parser):
        parser.add_argument('--out', default='dist')
        parser.add_argument('--base', default='', help="URL prefix, e.g. /repo-name")

    def handle(self, *args, out, base, **opts):
        base = base.rstrip('/')
        out = Path(out)
        if out.exists():
            shutil.rmtree(out)
        out.mkdir(parents=True)

        with override_settings(
            FORCE_SCRIPT_NAME=base or None,
            STATIC_URL=f'{base}/static/',
            MEDIA_URL=f'{base}/media/',
            STATIC_ROOT=out / 'static',
            ALLOWED_HOSTS=['*'],
            DEBUG=False,
            STORAGES={
                'default': settings.STORAGES['default'],
                'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'},
            },
        ):
            call_command('collectstatic', interactive=False, verbosity=0)
            shutil.copytree(settings.MEDIA_ROOT, out / 'media')

            old_prefix = get_script_prefix()
            set_script_prefix(f'{base}/')
            client = Client()
            pages = {'index.html': reverse('main')}
            for pk in Regions.objects.values_list('pk', flat=True):
                pages[f'region/{pk}/index.html'] = reverse('local_records:region', args=[pk])
            for rel, url in pages.items():
                # reverse() already includes `base`; the test client wants the path without it
                path = url[len(base):] if base and url.startswith(base) else url
                resp = client.get(path)
                if resp.status_code != 200:
                    raise SystemExit(f'{url} -> {resp.status_code}')
                target = out / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(resp.content)
            set_script_prefix(old_prefix)
        (out / '.nojekyll').touch()
        (out / '404.html').write_text(
            f'<meta http-equiv="refresh" content="0; url={base or ""}/">')
        self.stdout.write(self.style.SUCCESS(f'Exported {len(pages)} pages to {out}'))
