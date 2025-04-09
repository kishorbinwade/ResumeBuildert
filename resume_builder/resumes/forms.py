# from django import forms

# class ResumeForm(forms.Form):
#     full_name = forms.CharField(max_length=100)
#     email = forms.EmailField()
#     phone = forms.CharField(max_length=20)
#     education = forms.CharField(widget=forms.Textarea)
#     experience = forms.CharField(widget=forms.Textarea)
#     skills = forms.CharField(widget=forms.Textarea)


from django import forms

class ResumeForm(forms.Form):
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    professional_summary = forms.CharField(widget=forms.Textarea)