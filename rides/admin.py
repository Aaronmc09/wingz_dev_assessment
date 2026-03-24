from django.contrib import admin

from rides.models import Ride, RideEvent


class RideEventInline(admin.TabularInline):
    model = RideEvent
    extra = 1
    fields = ('description', 'created_at')
    readonly_fields = ('id_ride_event',)


@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = ('id_ride', 'status', 'rider_name', 'driver_name', 'pickup_time')
    list_filter = ('status', 'pickup_time')
    search_fields = (
        'id_rider__first_name', 'id_rider__last_name', 'id_rider__email',
        'id_driver__first_name', 'id_driver__last_name', 'id_driver__email',
    )
    list_select_related = ('id_rider', 'id_driver')
    raw_id_fields = ('id_rider', 'id_driver')
    date_hierarchy = 'pickup_time'
    inlines = [RideEventInline]

    fieldsets = (
        (None, {'fields': ('status', 'id_rider', 'id_driver', 'pickup_time')}),
        ('Pickup Location', {'fields': ('pickup_latitude', 'pickup_longitude')}),
        ('Dropoff Location', {'fields': ('dropoff_latitude', 'dropoff_longitude')}),
    )

    @admin.display(description='Rider')
    def rider_name(self, obj):
        return str(obj.id_rider)

    @admin.display(description='Driver')
    def driver_name(self, obj):
        return str(obj.id_driver)


@admin.register(RideEvent)
class RideEventAdmin(admin.ModelAdmin):
    list_display = ('id_ride_event', 'id_ride', 'description', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('description', 'id_ride__id_ride')
    list_select_related = ('id_ride',)
    raw_id_fields = ('id_ride',)
    date_hierarchy = 'created_at'
