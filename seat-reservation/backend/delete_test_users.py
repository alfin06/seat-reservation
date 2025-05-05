from django.contrib.auth import get_user_model
User = get_user_model()

# Delete test users
test_emails = ['test1@example.com', 'test2@example.com', 'test3@example.com']
for email in test_emails:
    try:
        user = User.objects.get(email=email)
        user.delete()
        print(f"Deleted user: {email}")
    except User.DoesNotExist:
        print(f"User not found: {email}")

print("Cleanup complete!") 