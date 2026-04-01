from django import forms
from .models import Student, Parent


class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = '__all__'
        widgets = {
            'father_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'mother_email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        # On exclut le champ 'parent' car il sera géré manuellement dans la vue
        exclude = ('parent',)