from django.utils.translation import ungettext_lazy
from django_tables2 import Table


class DashboardTable(Table):
    caption = ungettext_lazy('%d Row', '%d Rows')

    def get_caption_display(self):
        try:
            return self.caption % self.paginator.count
        except TypeError:
            pass
        return self.caption

    class Meta:
        template_name = 'dashboard/table_bootstrap4.html'
        attrs = {'class': 'table table-responsive-sm table-bordered table-striped table-sm'}
