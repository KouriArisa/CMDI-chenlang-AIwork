from django import forms

from apps.todos.models import TodoPriority, TodoStatus


class TodoForm(forms.Form):
    title = forms.CharField(
        label="任务标题",
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "输入待办标题"}),
    )
    description = forms.CharField(
        label="任务描述",
        required=False,
        widget=forms.Textarea(attrs={"rows": 4, "placeholder": "输入详细描述"}),
    )
    status = forms.ChoiceField(
        label="当前状态",
        choices=TodoStatus.choices,
        initial=TodoStatus.PENDING,
    )
    priority = forms.ChoiceField(
        label="优先级",
        choices=TodoPriority.choices,
        initial=TodoPriority.MEDIUM,
    )
    due_date = forms.DateField(
        label="截止日期",
        required=False,
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(attrs={"type": "date"}),
    )
