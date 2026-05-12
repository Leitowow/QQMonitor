"""Forms for QQMonitor."""

from django import forms


class QqMonitorEntryForm(forms.Form):
    """Basic input form for QQ monitor entries."""

    qq_number = forms.CharField(
        label="QQ号",
        max_length=32,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "请输入QQ号",
            }
        ),
    )
    main_character_id = forms.IntegerField(
        label="主角色ID",
        required=True,
        min_value=1,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "请输入主角色ID",
            }
        ),
    )
    nickname = forms.CharField(
        label="昵称",
        max_length=64,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "请输入昵称",
            }
        ),
    )
