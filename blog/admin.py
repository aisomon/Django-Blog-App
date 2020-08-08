from django.contrib import admin
from .models import Author, Article,Category,Comment
# Register your models here.

#for customizing the model(will show search bar in Author), we have to write bellow class
class authorModel(admin.ModelAdmin):
    list_display = ["__str__"]
    search_fields = ["__str__", "detailes"]

    class Meta:
        Model = Author

admin.site.register(Author,authorModel)

#for customizing the model(will show search bar in Article and date of post, and filtering), we have to write bellow class
class articleModel(admin.ModelAdmin):
    list_display = ["__str__","posted_on"]
    search_fields = ["__str__", "detailes"]
    list_filter = ["posted_on", "category"]
    list_per_page = 10

    class Meta:
        Model = Article

admin.site.register(Article,articleModel)


#for customizing the model(will show search bar in Category and date of post, and filtering), we have to write bellow class
class categoryModel(admin.ModelAdmin):
    list_display = ["__str__"]
    search_fields = ["__str__"]
    list_per_page = 10

    class Meta:
        Model = Category
admin.site.register(Category,categoryModel)

#for customizing the model(will show search bar in Category and date of post, and filtering), we have to write bellow class
class commentModel(admin.ModelAdmin):
    list_display = ["__str__"]
    search_fields = ["__str__"]
    list_per_page = 10

    class Meta:
        Model = Comment
admin.site.register(Comment,commentModel)