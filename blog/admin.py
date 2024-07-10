from django.contrib import admin
from .models import *

# Register Post Model
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'slug', 'status', 'category_to_str', 'tag_to_str', 'visit_count', 'comment_status',)
	list_filter = ('publish', 'status',)
	search_fields = ('title', 'description', 'content',)
	prepopulated_fields = {'slug': ('title',)}
	ordering = ('-status', '-publish',)
	# exclude = ('author', )
	readonly_fields = ('visit_count',)

	def category_to_str(self, obj):
		return [category for category in obj.categories.all()]
	category_to_str.short_description = 'Categories'

	def tag_to_str(self, obj):
		return [tag for tag in obj.tags.all()]
	tag_to_str.short_description = 'Tags'

# Register Category Model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug', 'status',)
	list_filter = ('status',)
	search_fields = ('name', )
	prepopulated_fields = {'slug':('name',)}

# Register Tag Model
admin.site.register(Tag)

# Register Comment Model
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ('email', 'post', 'parent', 'depth', 'status', 'created',)
	list_filter = ('status', 'parent', 'depth',)
	search_fields = ('name', 'body',)
	readonly_fields = ('depth',)

	def save_model(self, request, obj, form, change):
		parent = obj.parent
		if parent:
			obj.depth = parent.depth + 1
		else:
			obj.depth = 0  # If no parent, set depth to 0 (top-level comment)
		super().save_model(request, obj, form, change)
