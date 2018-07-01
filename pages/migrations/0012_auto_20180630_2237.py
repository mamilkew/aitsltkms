# Generated by Django 2.0.5 on 2018-06-30 15:37

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0011_auto_20180630_1926'),
    ]

    operations = [
        migrations.AddField(
            model_name='forcegraph',
            name='faceted_search',
            field=smart_selects.db_fields.ChainedManyToManyField(chained_field='repository_query', chained_model_field='domain_subject', horizontal=True, to='pages.Property', verbose_name='writer'),
        ),
        migrations.AlterField(
            model_name='forcegraph',
            name='domain_subject',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='repository_query', chained_model_field='repository_query', on_delete=django.db.models.deletion.CASCADE, to='pages.Domain'),
        ),
    ]