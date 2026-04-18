from django.contrib import admin
from .models import Category, Post, Reaction, Poll, PollOption

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    # Nomini yozganda slugni o'zi yozadi (faqat inglizcha harflar uchun yaxshi ishlaydi)
    prepopulated_fields = {"slug": ("name",)}

class PollOptionInline(admin.TabularInline):
    model = PollOption
    extra = 3

class PollInline(admin.StackedInline):
    model = Poll
    extra = 1

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'views', 'created_at')
    list_filter = ('category', 'created_at', 'author')
    search_fields = ('title', 'content')
    # Post yaratish sahifasining o'zida So'rovnomani ham chiqaradi
    inlines = [PollInline]

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    inlines = [PollOptionInline]

admin.site.register(Reaction)