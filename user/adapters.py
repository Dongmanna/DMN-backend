# user/adapters.py
from allauth.account.adapter import DefaultAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        # 기존의 username, password, email 받아옴
        user = super().save_user(request, user, form, False)
		# 추가한 필드
        user.nickname = data.get('nickname')
        user.address = data.get('address')
        user.profile_image = data.get('profile_image')
        user.save()
        return user