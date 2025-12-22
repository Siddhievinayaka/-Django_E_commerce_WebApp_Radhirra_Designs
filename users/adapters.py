from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_email
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Check if user exists, if not redirect to signup
        """
        if sociallogin.is_existing:
            return
        
        # Check if user with this email already exists
        email = user_email(sociallogin.user)
        if email:
            try:
                existing_user = User.objects.get(email=email)
                # Connect the social account to existing user
                sociallogin.connect(request, existing_user)
            except User.DoesNotExist:
                # User doesn't exist, will proceed to signup
                pass