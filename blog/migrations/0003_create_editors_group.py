from django.db import migrations


def create_editors_group(apps, schema_editor):
    # create an Editors group for role-based permissions
    from django.contrib.auth.models import Group
    Group.objects.get_or_create(name='Editors')


def remove_editors_group(apps, schema_editor):
    from django.contrib.auth.models import Group
    Group.objects.filter(name='Editors').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_category_options_post_author'),
    ]

    operations = [
        migrations.RunPython(create_editors_group, remove_editors_group),
    ]
