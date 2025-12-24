# CLOUDINARY INTEGRATION LOGIC - RADHIRRA DESIGNS

## 1. SETUP & CONFIGURATION

### Install Packages
```bash
pip install cloudinary django-cloudinary-storage
```

### Environment Variables (.env)
```env
CLOUDINARY_CLOUD_NAME=ddlx2h9hr
CLOUDINARY_API_KEY=999271691163949
CLOUDINARY_API_SECRET=KNWUBus3MXZo5DWaOL5bcjczep0
```

### Django Settings (settings.py)
```python
import cloudinary
import cloudinary_storage

# Load environment variables
CLOUDINARY_CLOUD_NAME = os.environ.get("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.environ.get("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.environ.get("CLOUDINARY_API_SECRET")

# Initialize Cloudinary
cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
    secure=True,  # Use HTTPS
)

# Set Cloudinary as default file storage
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# Cloudinary storage configuration
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": CLOUDINARY_CLOUD_NAME,
    "API_KEY": CLOUDINARY_API_KEY,
    "API_SECRET": CLOUDINARY_API_SECRET,
}

# Add to INSTALLED_APPS
INSTALLED_APPS = [
    # ...
    "cloudinary",
    "cloudinary_storage",
    # ...
]
```

---

## 2. MODEL DEFINITION

### Product Images (Radhirra/models.py)
```python
from cloudinary.models import CloudinaryField

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    image = CloudinaryField("image")  # Cloudinary field
    is_main = models.BooleanField(default=False)
    
    @property
    def thumbnail_url(self):
        # Generate thumbnail on-the-fly
        return self.image.build_url(width=200, height=200, crop="thumb")
```

### User Profile Picture (users/models.py)
```python
from cloudinary.models import CloudinaryField

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profile")
    profile_pic = CloudinaryField(
        "image", 
        default="profile_pics/default.png",  # Default image
        blank=True, 
        null=True
    )
    
    @property
    def imageURL(self):
        try:
            url = self.profile_pic.url
        except:
            url = ""
        return url
```

---

## 3. UPLOAD LOGIC

### A. Django Admin Upload (Current Method)

**Admin Configuration (Radhirra/admin.py)**
```python
from django.contrib import admin
from .models import Product, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Show 1 empty form for new image

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]  # Inline image upload

admin.site.register(Product, ProductAdmin)
```

**How it works:**
1. Admin opens Product in Django Admin
2. Sees inline forms for ProductImage
3. Clicks "Choose File" and selects image
4. On save, Django automatically:
   - Uploads file to Cloudinary
   - Stores Cloudinary URL in database
   - Returns public URL

**Database Storage:**
```
image field stores: "image/upload/v1234567890/product_abc123.jpg"
Full URL: https://res.cloudinary.com/ddlx2h9hr/image/upload/v1234567890/product_abc123.jpg
```

---

### B. Programmatic Upload (For API/Forms)

**Example: Upload via Django Form**
```python
# forms.py
from django import forms
from .models import ProductImage

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['product', 'image', 'is_main']

# views.py
from django.shortcuts import render, redirect
from .forms import ProductImageForm

def upload_product_image(request, product_id):
    if request.method == 'POST':
        form = ProductImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Automatically uploads to Cloudinary
            return redirect('product_detail', product_id)
    else:
        form = ProductImageForm()
    return render(request, 'upload.html', {'form': form})
```

**Example: Direct Cloudinary Upload**
```python
import cloudinary.uploader

def upload_image_direct(image_file, product_id):
    # Upload to Cloudinary
    result = cloudinary.uploader.upload(
        image_file,
        folder=f"products/{product_id}",  # Organize by product
        resource_type="image",
        transformation=[
            {'width': 1000, 'height': 1000, 'crop': 'limit'},  # Max size
            {'quality': 'auto'},  # Auto quality
            {'fetch_format': 'auto'}  # Auto format (WebP if supported)
        ]
    )
    
    # Save to database
    ProductImage.objects.create(
        product_id=product_id,
        image=result['public_id'],  # Store Cloudinary public_id
        is_main=False
    )
    
    return result['secure_url']  # Return HTTPS URL
```

---

## 4. LOAD/DISPLAY LOGIC

### A. In Templates
```html
<!-- Display product image -->
<img src="{{ product.main_image.image.url }}" alt="{{ product.name }}">

<!-- Display with transformation -->
<img src="{{ product.main_image.image.url|cloudinary_url:width=500,height=500,crop='fill' }}" 
     alt="{{ product.name }}">

<!-- Display thumbnail -->
<img src="{{ product.main_image.thumbnail_url }}" alt="{{ product.name }}">

<!-- Display user profile pic -->
{% if user.profile.imageURL %}
    <img src="{{ user.profile.imageURL }}" alt="{{ user.username }}">
{% else %}
    <img src="{% static 'images/default-avatar.png' %}" alt="Default">
{% endif %}
```

### B. In Python/Views
```python
# Get product with images
product = Product.objects.get(id=1)

# Get main image URL
main_image_url = product.main_image.image.url if product.main_image else None

# Get all images
all_images = product.images.all()
for img in all_images:
    print(img.image.url)  # Full URL
    print(img.thumbnail_url)  # Thumbnail URL

# Get user profile pic
user_profile = request.user.profile
profile_pic_url = user_profile.imageURL
```

### C. In API Response (JSON)
```python
from django.http import JsonResponse

def product_api(request, product_id):
    product = Product.objects.get(id=product_id)
    
    data = {
        'id': product.id,
        'name': product.name,
        'main_image': product.main_image.image.url if product.main_image else None,
        'images': [
            {
                'url': img.image.url,
                'thumbnail': img.thumbnail_url,
                'is_main': img.is_main
            }
            for img in product.images.all()
        ]
    }
    
    return JsonResponse(data)
```

---

## 5. IMAGE TRANSFORMATIONS

### On-the-fly Transformations
```python
# In model property
@property
def thumbnail_url(self):
    return self.image.build_url(width=200, height=200, crop="thumb")

@property
def large_url(self):
    return self.image.build_url(width=1200, height=1200, crop="limit")

@property
def square_url(self):
    return self.image.build_url(width=500, height=500, crop="fill", gravity="auto")
```

### Common Transformations
```python
# Resize
image.build_url(width=800, height=600)

# Crop to square
image.build_url(width=500, height=500, crop="fill")

# Thumbnail with face detection
image.build_url(width=200, height=200, crop="thumb", gravity="face")

# Auto quality and format
image.build_url(quality="auto", fetch_format="auto")

# Add watermark
image.build_url(overlay="watermark_logo", gravity="south_east")
```

---

## 6. UPLOAD FLOW DIAGRAM

```
USER ACTION (Admin/Form)
    ↓
Select Image File
    ↓
Submit Form
    ↓
Django receives file (request.FILES)
    ↓
CloudinaryField processes file
    ↓
Upload to Cloudinary API
    ↓
Cloudinary stores image
    ↓
Returns public_id & URL
    ↓
Django saves public_id to database
    ↓
Image accessible via URL
```

---

## 7. API UPLOAD EXAMPLE (For Admin Dashboard)

### Upload Endpoint
```python
# views.py
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import cloudinary.uploader

@csrf_exempt
def upload_product_image_api(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        image_file = request.FILES.get('image')
        is_main = request.POST.get('is_main', False)
        
        # Upload to Cloudinary
        result = cloudinary.uploader.upload(
            image_file,
            folder=f"products/{product_id}",
            resource_type="image"
        )
        
        # Save to database
        product_image = ProductImage.objects.create(
            product_id=product_id,
            image=result['public_id'],
            is_main=is_main
        )
        
        return JsonResponse({
            'success': True,
            'image_id': product_image.id,
            'url': result['secure_url'],
            'thumbnail': product_image.thumbnail_url
        })
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})
```

### Frontend Upload (JavaScript)
```javascript
async function uploadProductImage(productId, imageFile, isMain) {
    const formData = new FormData();
    formData.append('product_id', productId);
    formData.append('image', imageFile);
    formData.append('is_main', isMain);
    
    const response = await fetch('/api/upload-product-image/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    });
    
    const data = await response.json();
    return data;
}

// Usage
const fileInput = document.getElementById('image-upload');
fileInput.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    const result = await uploadProductImage(123, file, false);
    console.log('Uploaded:', result.url);
});
```

---

## 8. DELETE IMAGE

```python
# Delete from Cloudinary and database
def delete_product_image(image_id):
    image = ProductImage.objects.get(id=image_id)
    
    # Delete from Cloudinary
    cloudinary.uploader.destroy(image.image.public_id)
    
    # Delete from database
    image.delete()
```

---

## 9. FOLDER STRUCTURE IN CLOUDINARY

```
cloudinary://
├── products/
│   ├── 1/
│   │   ├── image1.jpg
│   │   └── image2.jpg
│   ├── 2/
│   │   └── image1.jpg
│   └── ...
├── profile_pics/
│   ├── default.png
│   ├── user_123.jpg
│   └── ...
└── ...
```

---

## 10. KEY POINTS

1. **Automatic Upload**: CloudinaryField handles upload automatically on save
2. **URL Storage**: Only public_id stored in DB, full URL generated on-demand
3. **Transformations**: Applied on-the-fly via URL parameters
4. **No Local Storage**: Images never stored on server, directly to Cloudinary
5. **CDN Delivery**: Images served via Cloudinary CDN (fast global delivery)
6. **Secure**: HTTPS by default, API key authentication
7. **Optimized**: Auto format (WebP), auto quality, lazy loading support

---

## 11. ADMIN DASHBOARD IMPLEMENTATION

For your separate admin dashboard, use the API upload approach:

1. Create upload endpoint (see section 7)
2. Use FormData in frontend to send files
3. Display uploaded images using returned URLs
4. Store image URLs/IDs in your admin state
5. On product save, link images to product via API

**Example Flow:**
```
Admin selects images → Upload to Cloudinary → Get URLs → 
Display preview → Admin saves product → Link images to product in DB
```
