from allauth.account.forms import SignupForm
from django import forms


class CustomSignupForm(SignupForm):
    date_of_birth = forms.DateField(
        required=True, widget=forms.DateInput(attrs={'type': 'date'}), label='Date of Birth')

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Confirm Password"

    def save(self, request):
        # Validate date_of_birth
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if not date_of_birth:
            raise ValidationError('Date of birth is required.')

        user = super(CustomSignupForm, self).save(request)
        user.date_of_birth = date_of_birth
        user.save()
        return user
