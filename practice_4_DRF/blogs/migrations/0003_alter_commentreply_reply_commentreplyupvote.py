# Generated by Django 4.2.6 on 2023-12-16 12:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blogs', '0002_comment_remove_blog_authors_blog_author_commentreply_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentreply',
            name='reply',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.CreateModel(
            name='CommentReplyUpvote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='upvotes', to='blogs.commentreply')),
                ('upvoted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('upvoted_by', 'reply')},
            },
        ),
    ]
