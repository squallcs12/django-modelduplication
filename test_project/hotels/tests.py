from django.contrib import admin
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from hotels.models import Hotel, Room, HotelDistance, Booking


class AdminTestCase(TestCase):
	def setUp(self):
		super(AdminTestCase, self).setUp()
		self.user = User.objects.create_superuser('username', 'email@domain.com', 'RandomPassword!@#')
		self.client.login(username='username', password='RandomPassword!@#')


class DuplicateBookAdmin(AdminTestCase):
	def test_see_action(self):
		self.assertTrue(admin.site.get_action('duplicate_models'))


	def test_submit_duplicate_hotel(self):
		hotel = Hotel.objects.create(name="Hotel X")
		room = hotel.room_set.create(name="Room 1")
		distance = hotel.hoteldistance_set.create(name="X Square 1")
		booking = hotel.booking_set.create(total=10)

		response = self.client.post('/admin/hotels/hotel/', data={
			'_selected_action': [hotel.id],
			'action': 'duplicate_models',
		})

		self.assertEqual(Hotel.objects.count(), 2)  # new hotel is duplicated
		self.assertEqual(Room.objects.count(), 2)  # new hotel is duplicated
		self.assertEqual(Booking.objects.count(), 1)  # no new booking duplicated
		
		hotel2 = Hotel.objects.all().order_by('id').last()  # new hotel
		self.assertEqual(hotel2.name, '{} - Duplicated'.format(hotel.name))

		room2 = Room.objects.all().order_by('id').last()  # new room
		self.assertEqual(room2.name, room.name)

	def test_fail_permission_duplicate(self):
		content_types = ContentType.objects.get_for_models(
            Hotel,
        )
		self.user.is_superuser = False
		self.user.user_permissions.add(Permission.objects.get(codename='change_hotel',
                                                              content_type=content_types[Hotel]))
		self.user.save()

		hotel = Hotel.objects.create(name="Hotel X")
		response = self.client.post('/admin/hotels/hotel/', data={
			'_selected_action': [hotel.id],
			'action': 'duplicate_models',
		})
		self.assertEqual(response.status_code, 403)
		self.assertEqual(Hotel.objects.count(), 1)