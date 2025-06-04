from django.db import models


# Create your models here.
class news(models.Model):
   # img = models.ImageField(_(""), upload_to=None, height_field=None, width_field=None, max_length=None)
   title = models.CharField(
    max_length=200,
    default="News title"
   )
   news_script = models.CharField(max_length=2000, default="News...")

class services(models.Model):

   name=models.CharField(max_length=300,default='')
   category = models.CharField(max_length=200, default="")
   


# firebase_utils.py
import uuid
from .firebase import bucket

import uuid

def upload_image_to_firebase(image_file, folder="outreach_images"):
    """
    Uploads an image file to Firebase Storage and returns its public URL.
    `image_file` can be InMemoryUploadedFile or ImageFieldFile.
    """
    ext = image_file.name.split('.')[-1]
    filename = f"{folder}/{uuid.uuid4()}.{ext}"

    blob = bucket.blob(filename)

    # Try to get content_type if present, else guess it
    content_type = getattr(image_file, 'content_type', None)
    if content_type is None:
        import mimetypes
        content_type, _ = mimetypes.guess_type(image_file.name)

    blob.upload_from_file(image_file, content_type=content_type or 'application/octet-stream')

    blob.make_public()

    return blob.public_url




class MedicalOutreach(models.Model):
    title = models.CharField(max_length=255)
    team_lead = models.CharField(max_length=255)
    description = models.TextField()
    status = models.BooleanField(default=False)  # True if completed, False if ongoing
    image = models.ImageField(upload_to='temp/')  # temporary local path
    image_url = models.URLField(blank=True)
    location = models.CharField(max_length=255,default="Katooke, Sanyu hospital grounds")
    event_date = models.DateField(default=None, blank=True, null=True)  # Date of the outreach
    # Donations Summary
    amount_raised = models.DecimalField(max_digits=12, decimal_places=2)
    goal_amount = models.DecimalField(max_digits=12, decimal_places=2)
    donor_count = models.PositiveIntegerField()
    
    # Patients Treated
    patients_treated = models.PositiveIntegerField()
    total_cost = models.DecimalField(max_digits=12, decimal_places=2)
    testimonial = models.TextField(blank=True, null=True)

    # Media & Links
    video_link = models.URLField(blank=True, null=True)
    detail_page_slug = models.SlugField(unique=True)
    ad_source = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Upload image to Firebase if URL isn't already set
        if self.image and not self.image_url:
            self.image_url = upload_image_to_firebase(self.image)
        super().save(*args, **kwargs)

    @property
    def top_donor(self):
        return self.donors.order_by('-amount').first()


class Donor(models.Model): 
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    anonimity = models.BooleanField(default=False, help_text="Check if you want to remain anonymous")
    
    outreach = models.ForeignKey(
        MedicalOutreach,
        related_name='donors',
        on_delete=models.CASCADE
    )

    image = models.ImageField(upload_to='temp/', blank=True, null=True)
    image_url = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.name} - {self.amount}"

    def save(self, *args, **kwargs):
        if self.image and not self.image_url:
            self.image_url = upload_image_to_firebase(self.image)
        super().save(*args, **kwargs)



from django.db import models

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    image = models.ImageField(upload_to='doctors/', blank=True, null=True)
    image_url = models.URLField(blank=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.position}"

    def save(self, *args, **kwargs):
        if self.image and not self.image_url:
            self.image_url = upload_image_to_firebase(self.image)
        super().save(*args, **kwargs)


class Facility(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='facilities/')

    image_url = models.URLField(blank=True)
    def save(self, *args, **kwargs):
        if self.image and not self.image_url:
            self.image_url = upload_image_to_firebase(self.image)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    

class NewsItem(models.Model):
    title = models.CharField(max_length=255)
    summary = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    image = models.ImageField(upload_to='news/')

    def save(self, *args, **kwargs):
        if self.image and not self.image_url:
            self.image_url = upload_image_to_firebase(self.image)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    

class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=100, default="fas fa-heartbeat", help_text="Font Awesome class, e.g. 'fas fa-heartbeat'")
    image = models.ImageField(upload_to='services/', null=True, blank=True)
    image_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.image and not self.image_url:
            self.image_url = upload_image_to_firebase(self.image)
        super().save(*args, **kwargs)


class Slide(models.Model):
    stat = models.CharField(max_length=255)
    headline = models.CharField(max_length=255)
    sub = models.TextField()
    image = models.ImageField(upload_to='slides/', null=True, blank=True)
    image_url = models.URLField(blank=True, null=True)  

    def __str__(self):
        return self.headline
    def save(self, *args, **kwargs):
        if self.image and not self.image_url:
            self.image_url = upload_image_to_firebase(self.image)
        super().save(*args, **kwargs)

class Speciality(models.Model):
    title = models.CharField(max_length=255)
    label = models.CharField(max_length=255)
    image = models.ImageField(upload_to='specialities/', null=True, blank=True)
    image_url = models.URLField(blank=True, null=True)  

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.image and not self.image_url:
            self.image_url = upload_image_to_firebase(self.image)
        super().save(*args, **kwargs)


class BankDs(models.Model):
    name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=50)
    swift_code = models.CharField(max_length=20, blank=True, null=True)
    iban = models.CharField(max_length=34, blank=True, null=True)
    image = models.ImageField(upload_to='banks/', null=True, blank=True)
    wise_email = models.EmailField(blank=True, null=True, help_text="Wise email for donations",default="donate@sanyuhospital.org")
    mtn = models.CharField(max_length=20, blank=True, null=True, help_text="MTN number for donations", default="0771234567")
    airtel = models.CharField(max_length=20, blank=True, null=True, help_text="Airtel number for donations", default="0771234567")
    image_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True, help_text="Is this bank active for donations?")
    formspree = models.CharField(max_length=255, blank=True, null=True, help_text="Formspree endpoint for donation form")
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.image and not self.image_url:
            self.image_url = upload_image_to_firebase(self.image)
        super().save(*args, **kwargs)



from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date = models.DateField()
    location = models.CharField(max_length=255)
    video_url = models.URLField(blank=True, null=True)  # For past events video link (YouTube etc.)
    status = models.BooleanField(default=False, help_text="True if event has occurred, False if upcoming")
    image = models.ImageField(upload_to='events/', null=True, blank=True)
    google_link = models.URLField(blank=True, null=True, help_text="Google Maps link for event location")
    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title

    @property
    def is_upcoming(self):
        from django.utils.timezone import now
        return self.date >= now().date()

    @property
    def is_past(self):
        from django.utils.timezone import now
        return self.date < now().date()
    


class Payments(models.Model):
    user = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[('CREDIT CARDS', 'CREDIT CARDS'), ('bank_transfer', 'Bank Transfer'), ('MTN MOBILE MONEY', 'MTN MOBILE MONEY'), ('AIRTEL MOBILE MONEY', 'AIRTEL MOBILE MONEY')], default='ALL')
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending')
    transaction_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    firstname = models.CharField(max_length=100, blank=True, null=True)
    lastname = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    status = models.BooleanField(default=False, help_text="True if payment is successful, False if pending or failed")
    phone = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    callback_url = models.URLField(blank=True, null=True, help_text="URL to redirect after payment")
    notification_id = models.CharField(max_length=100, blank=True, null=True, help_text="Notification ID for IPN setup")
    merchant_reference = models.CharField(max_length=100, unique=True, blank=True, null=True, help_text="Unique reference for the merchant")
    reason = models.TextField(blank=True, null=True, help_text="Reason for the payment, e.g. 'Donation', 'Service Payment'")
    currency = models.CharField(max_length=10, default='USD', help_text="Currency for the payment, e.g. 'USD', 'EUR'")
    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = f"PAY-{uuid.uuid4()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.amount} - {self.status}"


class Departments(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='departments/', null=True, blank=True)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.image and not self.image_url:
            self.image_url = upload_image_to_firebase(self.image)
        super().save(*args, **kwargs)


from django.db import models

class Partner(models.Model):
    PARTNER_TYPES = [
        ('NGO', 'Non-Governmental Organization'),
        ('CORP', 'Corporate'),
        ('BUS', 'Business'),
        ('GOV', 'Government'),
        ('ACA', 'Academic Institution'),
        ('INT', 'International Organization'),
        ('FND', 'Foundation'),
        ('IND', 'Individual'),
    ]
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='partners/logos/')
    website = models.URLField(max_length=200)
    partner_type = models.CharField(max_length=4, choices=PARTNER_TYPES)

    def __str__(self):
        return self.name
