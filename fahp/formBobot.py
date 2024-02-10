from django import forms
from .models import bobot_kriteria_ahp


class dataSiswa(forms.ModelForm):
    class Meta:
        model = bobot_kriteria_ahp
