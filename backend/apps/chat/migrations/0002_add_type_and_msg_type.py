from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="chatroom",
            name="type",
            field=models.CharField(
                choices=[("private", "私聊"), ("group", "群聊")],
                default="private",
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name="message",
            name="msg_type",
            field=models.CharField(
                choices=[("text", "文本"), ("image", "图片"), ("file", "文件"), ("system", "系统")],
                default="text",
                max_length=10,
            ),
        ),
    ]
