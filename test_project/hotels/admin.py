from django.contrib import admin


from hotels.models import Hotel, Room, Booking, RoomItem, HotelDistance


class RoomInline(admin.TabularInline):
	model = Room


class RoomItemInline(admin.TabularInline):
	model = RoomItem


class HotelAdmin(admin.ModelAdmin):
	inlines = [
		RoomInline,
	]


class RoomAdmin(admin.ModelAdmin):
	inlines = [
		RoomItemInline,
	]


admin.site.register(Hotel, HotelAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(HotelDistance)
admin.site.register(Booking)
