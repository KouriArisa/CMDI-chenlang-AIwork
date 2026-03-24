from django import forms

from apps.todos.models import TodoPriority, TodoStatus


class TodoForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "输入待办标题"}),
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 4, "placeholder": "输入详细描述"}),
    )
    status = forms.ChoiceField(
        choices=TodoStatus.choices,
        initial=TodoStatus.PENDING,
    )
    priority = forms.ChoiceField(
        choices=TodoPriority.choices,
        initial=TodoPriority.MEDIUM,
    )
    due_date = forms.DateField(
        required=False,
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(attrs={"type": "date"}),
    )
