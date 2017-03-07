from django.http import HttpResponseRedirect
from django.contrib import admin
from django.contrib.admin.sites import site
from apps.custom_admin.widgets import VerboseForeignKeyRawIdWidget, VerboseManyToManyRawIdWidget

admin.site.disable_action('delete_selected')


class SortableAdmin(admin.ModelAdmin):
    # Make instances reorderable
    list_editable = ('position',)
    list_display = ('position', )

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.16/jquery-ui.min.js',
            'js/django-admin-sortable.js',)


class SortableAdminMixin(object):

    # Make instances reorderable
    # list_editable = ('position',)
    # list_display = ('position', )

    class Media:
        js = (
            'admin/js/django-admin-sortable.js',
        )

        css = {
            'all': ('admin/css/admin-sortable-fix.css',)
        }


class ReadOnlyAdmin(admin.ModelAdmin):
    readonly_fields = []

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + \
               [field.name for field in obj._meta.fields]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ReadOnlyTabularInline(admin.TabularInline):
    extra = 0
    can_delete = False
    editable_fields = []
    readonly_fields = []
    exclude = []

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + \
               [field.name for field in self.model._meta.fields
                if field.name not in self.editable_fields and
                   field.name not in self.exclude]

    def has_add_permission(self, request):
        return False


class ButtonableAdmin(admin.ModelAdmin):
    """
    https://djangosnippets.org/snippets/1016/

    A subclass of this admin will let you add buttons (like history) in the
    change view of an entry.

    ex.
    class FooAdmin(ButtonableModelAdmin):
       ...

       def bar(self, obj):
          obj.bar()
       bar.short_description='Example button'

       buttons = [ bar ]

    you can then put the following in your admin/change_form.html template:

       {% block object-tools %}
       {% if change %}{% if not is_popup %}
       <ul class="object-tools">
       {% for button in buttons %}
          <li><a href="{{ button.func_name }}/">{{ button.short_description }}</a></li>
       {% endfor %}
       <li><a href="history/" class="historylink">History</a></li>
       {% if has_absolute_url %}<li><a href="../../../r/{{ content_type_id }}/{{ object_id }}/" class="viewsitelink">View on site</a></li>{% endif%}
       </ul>
       {% endif %}{% endif %}
       {% endblock %}


            dodgyville (on November 1, 2011):
            I found this snippet (and arvid's 1.2 updates) very helpful. However, it does not work in 1.3 due to the the change to "Callables in templates" (see the 1.3 changelist docs). This means the items in buttons are being evaluated in the template for loop, so func_name and short_description are not available since "button" is now automatically "button()".

            My quick workaround:

            In FooAdmin: Instead of:
            buttons = [bar]
            use:
            buttons = [(bar.func_name, bar.short_description), ]

            In arvid's get_urls use but[0] instead of but.func_name

            And in the template use button.0 and button.1 instead of button.func_name and button.short_description

    """

    buttons = []
    change_form_template = 'custom_admin/change_form.html'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['buttons'] = self.buttons
        return self.changeform_view(request, object_id, form_url, extra_context)

    def button_view_dispatcher(self, request, object_id, command):
        obj = self.model._default_manager.get(pk=object_id)
        return getattr(self, command)(request, obj) or HttpResponseRedirect(request.META['HTTP_REFERER'])

    def get_urls(self):
        # Todo: Needs to be rewritten so we can actually reverse the url. Take a look at AsSULoginMixin.
        from django.conf.urls import patterns, url
        from functools import update_wrapper

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)

            return update_wrapper(wrapper, view)

        result = patterns(
            '',
            *(url(r'^(\d+)/(%s)/$' % but[0], wrap(self.button_view_dispatcher)) for but in self.buttons)
        ) + super(ButtonableAdmin, self).get_urls()

        return result

    def get_info(self):
        return self.model._meta.app_label, self.model._meta.model_name


"""
Check https://djangosnippets.org/snippets/2217/
"""


class ImprovedRawIdFields(admin.ModelAdmin):
    raw_id_managers = None

    def get_manager(self, db_field):
        managers = self.raw_id_managers or {}
        return managers.get(db_field, '')

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in self.raw_id_fields:
            kwargs.pop("request", None)
            type = db_field.rel.__class__.__name__
            if type == "ManyToOneRel":
                kwargs['widget'] = VerboseForeignKeyRawIdWidget(db_field.rel, site, self.get_manager(db_field.name))
            elif type == "ManyToManyRel":
                kwargs['widget'] = VerboseManyToManyRawIdWidget(db_field.rel, site)
            return db_field.formfield(**kwargs)
        return super(ImprovedRawIdFields, self).formfield_for_dbfield(db_field, **kwargs)


class AddFormMixin(admin.ModelAdmin):
    """
    A ModelAdmin that uses a different form class when adding an object.
    http://reliablybroken.com/b/2009/01/using-separate-forms-for-adding-and-changing-in-djangos-admin/
    """
    add_form = None

    def get_add_form(self):
        if not self.add_form:
            raise NotImplemented("add_form not defined")
        return self.add_form

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            return self.get_add_form()
        else:
            return super(AddFormMixin, self).get_form(request, obj, **kwargs)