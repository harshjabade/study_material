from django.contrib import admin
from .models import User, Subject, Material, Rating, Comment, Like


# ─────────────────────────────────────────────
# Register all models so they appear in Django Admin
# ─────────────────────────────────────────────

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display  = ('user_id', 'name', 'email', 'course', 'year', 'created_at')
    search_fields = ('name', 'email', 'course')
    list_filter   = ('course', 'year')
    ordering      = ('-created_at',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display  = ('subject_id', 'subject_name', 'course', 'semester')
    search_fields = ('subject_name', 'course')
    list_filter   = ('course', 'semester')


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display  = ('material_id', 'title', 'subject', 'uploaded_by', 'upload_date', 'downloads')
    search_fields = ('title', 'description')
    list_filter   = ('subject', 'upload_date')
    ordering      = ('-upload_date',)
    readonly_fields = ('upload_date', 'downloads')


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display  = ('rating_id', 'material', 'user', 'rating')
    list_filter   = ('rating',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display  = ('comment_id', 'material', 'user', 'comment_date')
    search_fields = ('comment_text',)
    ordering      = ('-comment_date',)
    readonly_fields = ('comment_date',)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('like_id', 'material', 'user')
