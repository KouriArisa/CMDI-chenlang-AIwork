from django import forms

from apps.todos.models import TodoItem


class TodoItemForm(forms.ModelForm):
    class Meta:
        model = TodoItem
        fields = ["title", "description", "status", "priority", "due_date"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "输入待办标题"}),
            "description": forms.Textarea(
                attrs={"rows": 4, "placeholder": "输入详细描述"}
            ),
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }
