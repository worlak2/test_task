from django.contrib import admin
import csv
from django.http import HttpResponse
# Register your models here.
from office_world.models import Person, VoteModel, VoteUser


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('fio', 'name', 'patronymic', 'age',)
    list_display_links = ('fio', 'name', 'patronymic', 'age')
    search_fields = ('fio', 'name', 'patronymic')


@admin.register(VoteModel)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_start', 'date_end', 'max_vote')


@admin.register(VoteUser)
class UserVote(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('user', 'vote', 'vote_count')
    actions = ["export_as_csv"]
