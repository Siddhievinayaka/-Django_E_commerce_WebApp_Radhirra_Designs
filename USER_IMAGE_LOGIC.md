# USER PROFILE IMAGE - UPLOAD & LOAD LOGIC

## MODEL (users/models.py)
```python
from cloudinary.models import CloudinaryField

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profile")
    profile_pic = CloudinaryField("image", default="profile_pics/default.png", blank=True, null=True)
    
    @property
    def imageURL(self):
        try:
            url = self.profile_pic.url  # Cloudinary URL
        except:
            url = ""
        return url
```

## FORM (users/forms.py)
```python
class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'gender', 'profile_pic', 'address', 'city', 'state', 'zipcode']
```

## UPLOAD VIEW (users/views.py)
```python
@login_required
def profile_update_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == "POST":
        form = UserProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()  # Auto uploads to Cloudinary
            return redirect("profile")
    else:
        form = UserProfileUpdateForm(instance=profile)
    
    return render(request, "users/profile_update.html", {"form": form})
```

## DISPLAY IN TEMPLATE
```html
<!-- Load image -->
{% if user.profile.imageURL %}
    <img src="{{ user.profile.imageURL }}" alt="{{ user.username }}">
{% else %}
    <img src="{% static 'images/default-avatar.png' %}" alt="Default">
{% endif %}

<!-- Upload form -->
<form method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.profile_pic }}
    <button type="submit">Update Profile</button>
</form>
```

## FLOW
1. User selects image in form
2. Submit with `enctype="multipart/form-data"`
3. Django receives file in `request.FILES`
4. `form.save()` triggers CloudinaryField
5. Image uploads to Cloudinary automatically
6. Cloudinary returns public_id
7. public_id saved to `profile_pic` field
8. Access via `user.profile.imageURL` or `user.profile.profile_pic.url`

## API UPLOAD (For Admin Dashboard)
```python
import cloudinary.uploader

def upload_profile_pic_api(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        image = request.FILES.get('image')
        
        # Upload to Cloudinary
        result = cloudinary.uploader.upload(image, folder="profile_pics")
        
        # Update profile
        profile = UserProfile.objects.get(user_id=user_id)
        profile.profile_pic = result['public_id']
        profile.save()
        
        return JsonResponse({'url': result['secure_url']})
```

## KEY POINTS
- CloudinaryField handles upload automatically
- No local storage needed
- Image stored as public_id in DB
- Full URL generated via `.url` or `.imageURL`
- Default image: "profile_pics/default.png"
