from django.contrib import admin
from .models import Comment, Mention

class MentionInline(admin.TabularInline):
    model = Mention
    extra = 1

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'text_short', 'created_at')
    inlines = [MentionInline]

    def text_short(self, obj):
        return obj.text[:50] # Matnni qisqartirib ko'rsatish
    text_short.short_description = 'Komment matni'
