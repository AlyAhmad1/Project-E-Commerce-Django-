from django import forms

# For Sign Up
class FormA(forms.Form):
    Email = forms.EmailField(max_length=100,
        widget=forms.EmailInput(
            attrs={"type":"email" ,"id":"inputEmail","class":"form-control",
                   "placeholder":"Email address","required":"","autofocus":""})
    )
    Password = forms.CharField(max_length=8,
                               widget=forms.TextInput({
                                   "style": "margin-top:10px;","type": "password","id": "inputPassword","class": "form-control",
                                    "placeholder": "Password", "required": ""}
                               )
                               )

# For Add Items on Index Page
class FormB(forms.Form):
    title = forms.CharField(max_length=50,
                            widget=forms.TextInput(
                                attrs={"type": "text", "placeholder": "Title", "max_length": '50'})
                            )
    Description = forms.CharField(max_length=200,
                                  widget=forms.TextInput(
                                      attrs={"max_length": '200',"type": "text", "placeholder": "Description"})
                                  )
    Price = forms.FloatField(
        widget=forms.TextInput(
            attrs={"placeholder": "Price Per Item"})
    )
    Quantity = forms.FloatField(
        widget=forms.TextInput(
            attrs={"placeholder": "Available Quantity"})
    )
    Image = forms.ImageField()

