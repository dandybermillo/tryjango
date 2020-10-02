from django import template
from django.template import Context


register = template.Library()


class TableNode(template.Node):
    template_name = "fx/table.html"

    def __init__(self, table):
        self.table = template.Variable(table)

    def render(self, context):
        table = self.table.resolve(context)
        # print(f" ----table = self.table.resolve(context) :{table}")
        
        t = template.loader.get_template( table.template_name)
        context = {'table': table}
        return t.render(context)


@register.tag
def render_table(parser, token):
    try:
        tag, table = token.split_contents()
    except ValueError:
        msg = '%r tag requires a single arguments' % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)
    return TableNode(table)