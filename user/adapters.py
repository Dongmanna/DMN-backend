# user/adapters.py
from allauth.account.adapter import DefaultAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        user = super().save_user(request, user, form, False)
        user.nickname = data.get('nickname')
        user.address = data.get('address')
        user.profile_image = data.get('profile_image')
        user.save()
        return user