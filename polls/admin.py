from django.contrib import admin
from polls.models import Question,Choice
# Register your models here.
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information',{'fields':['pub_date']})
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    #这样做添加了一个“过滤器”侧边栏，允许人们以 pub_date 字段来过滤列表：
    list_filter = ['pub_date']
    #增加搜索框
    search_fields = ['question_text']
admin.site.register(Question,QuestionAdmin)
