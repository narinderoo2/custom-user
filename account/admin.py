from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from account.models import User,Post

class UserAdmin(UserAdmin):
    list_display=('username','email','is_staff','is_superuser')
    list_filter=('email',)
    fieldsets = (
        (None, {
            "fields": (
                'username','email','password','phone','first_name','last_name',
            )}),
        ('Permissions',{
            "fields":(
                'is_staff','is_active','is_superuser',
            )}),
        
    )
    add_fieldsets=(
        (None,{
            'classes':('wide',),
            'fields':('email','password1','password2')
        }),
    )

class PostAdmin(admin.ModelAdmin):
    list_display = ['title','owner']
    
admin.site.register(User,UserAdmin)
admin.site.register(Post,PostAdmin)