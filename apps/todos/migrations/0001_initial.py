from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="TodoItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100, verbose_name="标题")),
                ("description", models.TextField(blank=True, verbose_name="描述")),
                (
                    "status",
                    models.CharField(
                        choices=[("pending", "未完成"), ("completed", "已完成")],
                        default="pending",
                        max_length=20,
                        verbose_name="状态",
                    ),
                ),
                (
                    "priority",
                    models.CharField(
                        choices=[("low", "低"), ("medium", "中"), ("high", "高")],
                        default="medium",
                        max_length=20,
                        verbose_name="优先级",
                    ),
                ),
                (
                    "due_date",
                    models.DateField(
                        blank=True,
                        null=True,
                        verbose_name="截止日期",
                    ),
                ),
                (
                    "completed_at",
                    models.DateTimeField(
                        blank=True,
                        null=True,
                        verbose_name="完成时间",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="更新时间"),
                ),
            ],
            options={
                "db_table": "todo_item",
                "ordering": ["-created_at"],
            },
        ),
        migrations.AddConstraint(
            model_name="todoitem",
            constraint=models.CheckConstraint(
                condition=models.Q(status__in=["pending", "completed"]),
                name="todo_item_status_valid",
            ),
        ),
        migrations.AddConstraint(
            model_name="todoitem",
            constraint=models.CheckConstraint(
                condition=models.Q(priority__in=["low", "medium", "high"]),
                name="todo_item_priority_valid",
            ),
        ),
        migrations.AddIndex(
            model_name="todoitem",
            index=models.Index(fields=["status"], name="todo_item_status_idx"),
        ),
        migrations.AddIndex(
            model_name="todoitem",
            index=models.Index(fields=["due_date"], name="todo_item_due_date_idx"),
        ),
    ]
