import os
from django.core.management.base import BaseCommand
from seo.utils.sitemap_builder import build_sitemap


class Command(BaseCommand):
    help = "Generate static sitemap.xml file"

    def handle(self, *args, **kwargs):

        xml_content = build_sitemap()

        output_path = "/home/muravka/apps/muravka/public/sitemap.xml"

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(xml_content)

        self.stdout.write(
            self.style.SUCCESS("Sitemap generated successfully")
        )