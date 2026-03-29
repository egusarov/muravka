from django.db import migrations


def create_site(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')

    Site.objects.all().delete()

    Site.objects.create(
        id=1,
        domain="muravka.onrender.com",
        name="muravka.onrender.com"
    )


class Migration(migrations.Migration):
    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('store', '0005_alter_product_image'),
    ]

    operations = [
        migrations.RunPython(create_site),
    ]
