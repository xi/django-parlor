from django.contrib import admin


class TranslatableAdmin(admin.ModelAdmin):
    translation_inline_class = admin.TabularInline

    def get_inlines(self, request, obj):
        class TranslationInline(self.translation_inline_class):
            model = self.model().translations.model
            min_num = 2
            extra = 0
        return [
            TranslationInline,
            *super().get_inlines(request, obj),
        ]
