from django.db import models
from data_core.models import CreateModify, File, AbstractFile


class FileToBeDeleted(CreateModify):
    batch = models.IntegerField(null=False, blank=False)
    file = models.ForeignKey(File, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = 'Files to be deleted'


class DeletedFile(AbstractFile):
    pass