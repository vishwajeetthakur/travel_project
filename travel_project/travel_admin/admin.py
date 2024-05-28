from django.contrib import admin
from .models import User, TravelPlan, Bookings
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserModelAdmin(BaseUserAdmin):
  # The fields to be used in displaying the User model.
  # These override the definitions on the base UserModelAdmin
  # that reference specific fields on auth.User.
  list_display = ('id', 'email', 'name',  'is_admin')
  list_filter = ('is_admin',)
  fieldsets = (
      ('User Credentials', {'fields': ('email', 'password')}),
      ('Personal info', {'fields': ('name',)}),
      ('Permissions', {'fields': ('is_admin',)}),
  )
  # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
  # overrides get_fieldsets to use this attribute when creating a user.
  add_fieldsets = (
      (None, {
          'classes': ('wide',),
          'fields': ('email', 'name', 'password1', 'password2'),
      }),
  )
  search_fields = ('email',)
  ordering = ('email', 'id')
  filter_horizontal = ()

class TravelPlanAdmin(admin.ModelAdmin):
    list_display = ['id', 'destination', 'cost', 'description']   # Display all fields in the admin interface

class BookingsAdmin(admin.ModelAdmin):
    # class Meta:
    #     fields = '__all__'  # Display all fields in the admin interface
    list_display = ['id', 'user_id', 'travel_plan_id']


# Now register the new UserModelAdmin...
admin.site.register(User, UserModelAdmin)
admin.site.register(TravelPlan, TravelPlanAdmin)
admin.site.register(Bookings, BookingsAdmin)