from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from datetime import timedelta

# Blog model
from django.db import models
from django.utils.text import slugify
import os
from django.contrib.auth.models import User

class Blog(models.Model):
    CATEGORY_CHOICES = [
        ('tech', 'Technology'),
        ('sports', 'Sports'),
        ('general', 'General'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='blogs/', blank=True)
    content = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='general')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        original_slug = self.slug
        counter = 1
        while Blog.objects.filter(slug=self.slug).exists():
            self.slug = f"{original_slug}-{counter}"
            counter += 1
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    
# !Notice System Model
class Notice(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='notices/', blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        original_slug = self.slug
        counter = 1
        while Notice.objects.filter(slug=self.slug).exists():
            self.slug = f"{original_slug}-{counter}"
            counter += 1

        super().save(*args, **kwargs)

    @staticmethod
    def delete_old_notice():
        expiration_date = timezone.now() - timedelta(days=60)
        old_notices = Notice.objects.filter(created_at__lt=expiration_date)
        old_notices.delete()

    def __str__(self):
        return self.title
        
        
        
class Ourteam(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    image = models.ImageField(upload_to='team/', blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    facebook = models.URLField(max_length=250, blank=True)
    instagram = models.URLField(max_length=250, blank=True)
    linkedin = models.URLField(max_length=250, blank=True)

    def get_salutation(self):
        return "Mr." if self.gender == 'M' else "Ms."

    def __str__(self):
        return f"{self.get_salutation()} {self.name}"

# Course model
class Course(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='courses/')
    short_description = models.TextField()
    overview = models.TextField()
    credit_hours = models.IntegerField()

    def __str__(self):
        return self.title

class Semester(models.Model):
    course = models.ForeignKey(Course, related_name='semesters', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Subject(models.Model):
    semester = models.ForeignKey(Semester, related_name='subjects', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    teacher_name = models.CharField(max_length=100)
    contact_info = models.TextField(blank=True, null=True)
    syllabus_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.semester.title} - {self.name}"

# Contact form model
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"Message from {self.name}"

# Online-Admission form model
class ApplyOnline(models.Model):
    fullname = models.CharField(max_length=100)
    program = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField()
    previous_College = models.CharField(max_length=350)
    message = models.TextField()

    def __str__(self):
        return f"Applied Online by {self.fullname}"

# Appointment form model
class Appointment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f"Appointment by {self.name}"

# # Gallery model
class Gallery(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='gallery/')
    # description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title if self.title else f"Image {self.id}"


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    
    
    def __str__(self):
        return self.question[:30]
    
##! Timer Coundown model to store timer and offer
class CountdownTimer(models.Model):
    event_name=models.CharField(max_length=255)
    end_time=models.DateTimeField()
    def __str__(self):
        return self.event_name    
    
    
##! file management model

# Mapping extensions to Font Awesome icons
ICON_MAP = {
    "pdf": "fas fa-file-pdf",
    "doc": "fas fa-file-word",
    "docx": "fas fa-file-word",
    "xls": "fas fa-file-excel",
    "xlsx": "fas fa-file-excel",
    "ppt": "fas fa-file-powerpoint",
    "pptx": "fas fa-file-powerpoint",
    "txt": "fas fa-file-alt",
    "jpg": "fas fa-file-image",
    "jpeg": "fas fa-file-image",
    "png": "fas fa-file-image",
    "gif": "fas fa-file-image",
    "zip": "fas fa-file-archive",
    "rar": "fas fa-file-archive",
    "mp3": "fas fa-file-audio",
    "mp4": "fas fa-file-video",
    "avi": "fas fa-file-video",
    "csv": "fas fa-file-csv",
}

class UploadedFile(models.Model):
    title = models.CharField(max_length=255, help_text="Enter a title for the file")
    file = models.FileField(upload_to="files/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)  # Make it nullable temporarily for migration

    def __str__(self):
        return self.title

    def get_extension(self):
        """Extract file extension (lowercase, without the dot)"""
        return os.path.splitext(self.file.name)[1][1:].lower()

    def get_size(self):
        """Return file size in bytes"""
        return self.file.size

    def get_icon_class(self):
        """Return Font Awesome icon class based on file extension"""
        return ICON_MAP.get(self.get_extension(), "fas fa-file")  # Default icon if not found

    def delete(self, *args, **kwargs):
        """Delete the file from storage when the object is deleted"""
        if self.file and os.path.isfile(self.file.path):
            os.remove(self.file.path)
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        """Delete the old file when replacing it with a new one"""
        if self.pk:
            try:
                old_file = UploadedFile.objects.get(pk=self.pk).file
                if old_file != self.file and os.path.isfile(old_file.path):
                    os.remove(old_file.path)
            except UploadedFile.DoesNotExist:
                pass  # No previous file
        super().save(*args, **kwargs)