from django.db import migrations
from api.user.models import CustomUser


class Migration(migrations.Migration):
    def seed_data(apps, schema_editor):
        user = CustomUser(name="ananthan",
                          email="ananthankrishnan77@gmail.com",
                          is_staff=True,
                          is_superuser=True,
                          phone="9048448514",
                          gender="Male"
                          )
        user.set_password("12345")
        user.save()

    dependencies = [

    ]

    operations = [
        migrations.RunPython(seed_data),
    ]
