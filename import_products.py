#!/usr/bin/env python
import os
import django
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "muravka.settings")
django.setup()

from django.core.management import call_command
from django.db.utils import IntegrityError


def main():
    try:
        print("Starting import of products.json ...")
        call_command("loaddata", "products.json")
        print("Import finished successfully!")
    except IntegrityError as e:
        print("IntegrityError:", e)
    except Exception as e:
        print("Error during import:", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
