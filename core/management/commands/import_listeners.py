# coding=utf-8
from django.core.management.base import BaseCommand
from core.file_import import ListenerFileFormat, ListenerImportLogic
from core.models import Department, StudyGroup
from normalize_names import Command as NormalizeCommand
import tempfile
import xlrd
import os

class Command(BaseCommand):
    help = "Import data from xls file"
    args = 'filename'

    def handle(self, *args, **options):
        source_filename = args[0]
        source_file = open(source_filename, 'r')
        descriptor, name = tempfile.mkstemp()
        os.fdopen(descriptor, 'wb').write(source_file.read())
        doc = xlrd.open_workbook(name, formatting_info=True)
        format_doc = ListenerFileFormat(doc)

        from dialog import Dialog
        self.dialog = Dialog()
        if format_doc.sheet.ncols >= len(format_doc.cells):
            studygroup = self.select_department_and_group()
            logic = ListenerImportLogic(format_doc, studygroup)

            total = logic.doc.sheet.nrows - logic.doc.start_line

            self.dialog.gauge_start()
            for index, parsed_row in enumerate(logic.doc):
                logic.process_row(index, parsed_row)
                try:
                    text=(u'Импорт: %s' % parsed_row[0][0]).encode('utf-8')
                except IndexError:
                    text = (u'Ошибка').encode('utf-8')
                self.dialog.gauge_update(int(float(index)/total*100),
                    text=text,
                    update_text=True)

            self.dialog.gauge_stop()

            num_errors = len(logic.errors)
            self.dialog.infobox(u'Ошибок %d из %d: ' % (num_errors, total))

        next_cmd = NormalizeCommand()
        next_cmd.handle()


    def select_department_and_group(self):

        retcode, department_id = self.dialog.menu(
            u"Выберите филиал",
            choices=[(str(dep.id), dep.name) for dep in Department.objects.all()]
        )
        department = Department.objects.get(id=department_id)

        retcode, group_id = self.dialog.menu(
            u'Выберите группу',
            choices=[(str(group.id), group.subject.name) for group in department.groups.all()]
        )
        return StudyGroup.objects.get(id=group_id)
