from django.db import models
from django.db.models import Q


class TodoStatus(models.TextChoices):
    PENDING = "pending", "未完成"
    COMPLETED = "completed", "已完成"


class TodoPriority(models.TextChoices):
    LOW = "low", "低"
    MEDIUM = "medium", "中"
    HIGH = "high", "高"


class TodoItem(models.Model):
    title = models.CharField("标题", max_length=100)
    description = models.TextField("描述", blank=True)
    status = models.CharField(
        "状态",
        max_length=20,
        choices=TodoStatus.choices,
        default=TodoStatus.PENDING,
    )
    priority = models.CharField(
        "优先级",
        max_length=20,
        choices=TodoPriority.choices,
        default=TodoPriority.MEDIUM,
    )
    due_date = models.DateField("截止日期", null=True, blank=True)
    completed_at = models.DateTimeField("完成时间", null=True, blank=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        db_table = "todo_item"
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                check=Q(status__in=TodoStatus.values),
                name="todo_item_status_valid",
            ),
            models.CheckConstraint(
                check=Q(priority__in=TodoPriority.values),
                name="todo_item_priority_valid",
            ),
        ]
        indexes = [
            models.Index(fields=["status"], name="todo_item_status_idx"),
            models.Index(fields=["due_date"], name="todo_item_due_date_idx"),
        ]

    def __str__(self):
        return self.title
