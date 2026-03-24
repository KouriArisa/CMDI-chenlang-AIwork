from django import forms

from apps.todos.models import TodoPriority, TodoStatus

ALL_PRIORITY_CHOICES = [("", "全部"), *TodoPriority.choices]
ALL_STATUS_CHOICES = [("", "全部"), *TodoStatus.choices]


class TodoListQueryForm(forms.Form):
    status = forms.ChoiceField(required=False, choices=ALL_STATUS_CHOICES)
    priority = forms.ChoiceField(required=False, choices=ALL_PRIORITY_CHOICES)


class TodoCreateForm(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField(required=False)
    status = forms.ChoiceField(required=False, choices=TodoStatus.choices)
    priority = forms.ChoiceField(required=False, choices=TodoPriority.choices)
    due_date = forms.DateField(required=False, input_formats=["%Y-%m-%d"])

    def clean_description(self) -> str:
        return _validate_nullable_text(
            data=self.data,
            name="description",
            value=self.cleaned_data["description"],
        )

    def clean_status(self) -> str:
        return _validate_optional_choice(
            data=self.data,
            name="status",
            value=self.cleaned_data["status"],
        )

    def clean_priority(self) -> str:
        return _validate_optional_choice(
            data=self.data,
            name="priority",
            value=self.cleaned_data["priority"],
        )


class TodoUpdateForm(forms.Form):
    title = forms.CharField(max_length=100, required=False)
    description = forms.CharField(required=False)
    status = forms.ChoiceField(required=False, choices=TodoStatus.choices)
    priority = forms.ChoiceField(required=False, choices=TodoPriority.choices)
    due_date = forms.DateField(required=False, input_formats=["%Y-%m-%d"])

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
            data=self.data,
            name="description",
            value=self.cleaned_data["description"],
        )

    def clean_status(self) -> str:
        return _validate_optional_choice(
            data=self.data,
            name="status",
            value=self.cleaned_data["status"],
        )

    def clean_priority(self) -> str:
        return _validate_optional_choice(
            data=self.data,
            name="priority",
            value=self.cleaned_data["priority"],
        )


def _validate_nullable_text(
    *,
    data: dict[str, object],
    name: str,
    value: str,
) -> str:
    if name in data and data[name] is None:
        raise forms.ValidationError(f"{name} 不能为 null。")
    return value


def _validate_optional_choice(
    *,
    data: dict[str, object],
    name: str,
    value: str,
) -> str:
    if name in data and not value:
        raise forms.ValidationError(f"{name} 不能为空。")
    return value
