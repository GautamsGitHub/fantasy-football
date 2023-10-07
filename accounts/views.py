from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password
from os import getenv

MEMBER_PASSWORD_CHECK = getenv("MEMBER_PASSWORD_CHECK")

class MemberPassForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput)


def signUp(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    form = UserCreationForm()
    return render(
        request,
        "accounts/signup.html",
        {"form" : form}
    )


def memberPass(request):
    if request.method == 'POST':
        form = MemberPassForm(request.POST)
        if form.is_valid():
            enteredPassword = form.cleaned_data["password"]
            if check_password(enteredPassword, MEMBER_PASSWORD_CHECK):
                request.session["member_authorised"] = True
                return redirect("/")
            else:
                return redirect("Member Authentication")
    form = MemberPassForm()
    return render(
        request,
        "accounts/member_pass.html",
        {"form" : form}
    )