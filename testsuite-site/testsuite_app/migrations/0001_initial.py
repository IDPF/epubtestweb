# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.core.validators
import django.contrib.auth.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', default=False, verbose_name='superuser status')),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=30, error_messages={'unique': 'A user with that username already exists.'}, verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], unique=True)),
                ('first_name', models.CharField(blank=True, verbose_name='first name', max_length=30)),
                ('last_name', models.CharField(blank=True, verbose_name='last name', max_length=30)),
                ('email', models.EmailField(blank=True, verbose_name='email address', max_length=254)),
                ('is_staff', models.BooleanField(help_text='Designates whether the user can log into this admin site.', default=False, verbose_name='staff status')),
                ('is_active', models.BooleanField(help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', default=True, verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_query_name='user', related_name='user_set', verbose_name='groups', to='auth.Group')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_query_name='user', related_name='user_set', verbose_name='user permissions', to='auth.Permission')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ATMetadata',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('assistive_technology', models.CharField(blank=True, null=True, max_length=255)),
                ('input_type', models.CharField(choices=[('1', 'Keyboard'), ('2', 'Mouse'), ('3', 'Touch/Gestures')], default='1', max_length=1)),
                ('supports_screenreader', models.BooleanField(default=False)),
                ('supports_braille', models.BooleanField(default=False)),
                ('notes', models.CharField(blank=True, null=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.TextField()),
                ('category_id', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Epub',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('epubid', models.TextField()),
                ('description', models.TextField()),
                ('title', models.TextField()),
                ('category', models.ForeignKey(to='testsuite_app.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('percent_complete', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('last_updated', models.DateTimeField()),
                ('visibility', models.CharField(choices=[('1', 'Members only'), ('2', 'Public'), ('3', 'Owner only')], default='1', max_length=1)),
                ('status', models.CharField(choices=[('1', 'Current'), ('2', 'Archived')], default='1', max_length=1)),
                ('notes', models.CharField(blank=True, null=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('feature_id', models.TextField()),
                ('name', models.TextField()),
                ('category', models.ForeignKey(to='testsuite_app.Category')),
            ],
        ),
        migrations.CreateModel(
            name='ReadingSystem',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('operating_system', models.CharField(max_length=50)),
                ('version', models.CharField(max_length=50)),
                ('notes', models.CharField(blank=True, null=True, max_length=50)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('result', models.CharField(blank=True, null=True, choices=[('1', 'Supported'), ('2', 'Not Supported'), ('3', 'Not Applicable')], max_length=1)),
                ('notes', models.TextField(blank=True, validators=[django.core.validators.MaxLengthValidator(300)], null=True)),
                ('publish_notes', models.BooleanField(default=False)),
                ('flagged_as_new_or_changed', models.BooleanField(default=False)),
                ('evaluation', models.ForeignKey(to='testsuite_app.Evaluation')),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('percent', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('fraction', models.CharField(max_length=50)),
                ('did_any_pass', models.BooleanField(default=False)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('evaluation', models.ForeignKey(to='testsuite_app.Evaluation')),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('required', models.BooleanField()),
                ('test_id', models.CharField(max_length=50)),
                ('xhtml', models.TextField()),
                ('allow_na', models.BooleanField(default=False)),
                ('order_in_book', models.IntegerField()),
                ('category', models.ForeignKey(to='testsuite_app.Category')),
                ('epub', models.ForeignKey(to='testsuite_app.Epub')),
                ('feature', models.ForeignKey(blank=True, to='testsuite_app.Feature', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestMetadata',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('is_advanced', models.BooleanField(default=False)),
                ('test', models.ForeignKey(to='testsuite_app.Test')),
            ],
        ),
        migrations.CreateModel(
            name='TestSuite',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('version_date', models.DateField(max_length=50)),
                ('version_revision', models.IntegerField()),
                ('testsuite_type', models.CharField(choices=[('1', 'default'), ('2', 'accessibility')], default='1', max_length=1)),
                ('allow_many_evaluations', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=50)),
                ('testsuite_id', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='test',
            name='testsuite',
            field=models.ForeignKey(to='testsuite_app.TestSuite'),
        ),
        migrations.AddField(
            model_name='result',
            name='test',
            field=models.ForeignKey(to='testsuite_app.Test'),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='reading_system',
            field=models.ForeignKey(to='testsuite_app.ReadingSystem'),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='testsuite',
            field=models.ForeignKey(to='testsuite_app.TestSuite'),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='category',
            name='testsuite',
            field=models.ForeignKey(to='testsuite_app.TestSuite'),
        ),
        migrations.AddField(
            model_name='atmetadata',
            name='evaluation',
            field=models.ForeignKey(to='testsuite_app.Evaluation'),
        ),
    ]
