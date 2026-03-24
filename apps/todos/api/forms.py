from django import forms

from apps.todos.models import TodoPriority, TodoStatus

EMPTY_CHOICE = ("", "全部")
DATE_INPUT_FORMAT = "%Y-%m-%d"
ALL_PRIORITY_CHOICES = [EMPTY_CHOICE, *TodoPriority.choices]
ALL_STATUS_CHOICES = [EMPTY_CHOICE, *TodoStatus.choices]


class TodoListQueryForm(forms.Form):
    status = forms.ChoiceField(required=False, choices=ALL_STATUS_CHOICES)
    priority = forms.ChoiceField(required=False, choices=ALL_PRIORITY_CHOICES)


class BaseTodoPayloadForm(forms.Form):
    description = forms.CharField(required=False)
    status = forms.ChoiceField(required=False, choices=TodoStatus.choices)
    priority = forms.ChoiceField(required=False, choices=TodoPriority.choices)
    due_date = forms.DateField(required=False, input_formats=[DATE_INPUT_FORMAT])

    def clean_description(self) -> str:
        return _validate_nullable_text(
            submitted_data=self.data,
            field_name="description",
            value=self.cleaned_data["description"],
        )

    def clean_status(self) -> str:
        return _validate_optional_choice(
            submitted_data=self.data,
            field_name="status",
            value=self.cleaned_data["status"],
        )

    def clean_priority(self) -> str:
        return _validate_optional_choice(
            submitted_data=self.data,
            field_name="priority",
            value=self.cleaned_data["priority"],
        )


class TodoCreateForm(BaseTodoPayloadForm):
    title = forms.CharField(max_length=100)


class TodoUpdateForm(BaseTodoPayloadForm):
    title = forms.CharField(max_length=100, required=False)

    def clean(self) -> dict[str, object]:
        cleaned_data = super().clean()
        if not self.data:
            raise forms.ValidationError("请求体不能为空。")
        return cleaned_data

    def clean_title(self) -> str:
        value = self.cleaned_data["title"]
        if "title" in self.data and not value:
            raise forms.ValidationError("标题不能为空。")
        return value

    def clean_description(self) -> str:
        return _validate_nullable_text(
            submitted_data=self.data,
            field_name="description",
            value=self.cleaned_data["description"],
        )


def _validate_nullable_text(
    *,
    submitted_data: dict[str, object],
    field_name: str,
    value: str,
) -> str:
    if field_name in submitted_data and submitted_data[field_name] is None:
        raise forms.ValidationError(f"{field_name} 不能为 null。")
    return value


def _validate_optional_choice(
    *,
    submitted_data: dict[str, object],
    field_name: str,
    value: str,
) -> str:
    if field_name in submitted_data and not value:
        raise forms.ValidationError(f"{field_name} 不能为空。")
    return value
