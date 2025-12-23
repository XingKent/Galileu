from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "nome", "is_active", "is_staff", "created_at")
    search_fields = ("email", "nome", "cpf")
