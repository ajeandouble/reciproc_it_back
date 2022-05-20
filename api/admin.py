from django.contrib import admin
from .models import ( Note, MyUser, MyUserManager )

# Register the Note model to the admin/ interface. (TODO: display the fields as mentioned in the pdf)
admin.site.register(Note)

admin.site.register(MyUser) # DEBUG

