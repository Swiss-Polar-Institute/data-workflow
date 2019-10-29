from django.db import models
from data_core.models import CreateModify, File, AbstractFile


class Batch(CreateModify):
    """Increasing number used to identify a selection of files that were added to be deleted in one go."""
    number = models.IntegerField(help_text='Integer used to represent a batch', null=False, blank=False)

    def __str__(self):
        return self.number


class FileToBeDeleted(CreateModify):
    """Files listed ready for deletion from buckets."""
    batch = models.ForeignKey(Batch, help_text='Batch of file added', on_delete=models.PROTECT)
    file = models.ForeignKey(File, help_text='File that has been added to this table', on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = 'Files to be deleted'

    def __str__(self):
        return '{} - {}'.format(self.batch, self.file)


class DeletedFile(AbstractFile):
    """Files that have been deleted from a bucket."""
    pass


class MarkFilesDeleteCommand(CreateModify):
    """Record of the commands used to mark files to be deleted and to which batch of files they correspond."""

    batch = models.ForeignKey(Batch, help_text='Batch of files to which the command relates', on_delete=models.PROTECT)
    command = models.CharField(help_text='Command used to add files to be deleted', max_length=500, blank=False, null=False)

    class Meta:
        verbose_name_plural = 'Commands marking files for deletion'

    def __str__(self):
        return '{} - {}'.format(self.batch, self.command)