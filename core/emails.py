from djoser import email

class CustomPasswordResetEmail(email.PasswordResetEmail):
    # Use a custom HTML/text template
    template_name = 'email/custom_password_reset.html'

    def get_context_data(self):
        # Get the default context (includes uid, token, user, domain, etc.)
        context = super().get_context_data()
        
        # Add custom fields
        context['uid_value'] = context['uid']
        context['token_value'] = context['token']
        
        # Remove the reset link (we don't want to send a URL)
        context['reset_link'] = None  
        return context
