import kivy 

from kivy.app import App
from kivy.uix.layout import Layout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

from custom_bluetooth import Bluetooth


class Timer(GridLayout):

	FONT_SIZE = '50'

	def __init__(self, screen_manager, recv_stream, send_stream, **kwargs):  
		super(Timer, self).__init__(**kwargs)

		self.recv_stream, self.send_stream = recv_stream, send_stream

		self.screen_manager = screen_manager
 
		self.rows = 6

		self.back_to_main_btn = Button(text ='Back to main', font_size = '50', size_hint_y=None, size=(50, 100))
		self.set_timer_btn = Button(text ='Set timer', font_size = '50')
		self.h_text = TextInput(text ='hours', size=(50, 50))
		self.m_text = TextInput(text ='minutes', size=(50, 50))
		self.s_text = TextInput(text ='seconds', size=(50, 50))
		
		self.back_to_main_btn.bind(on_press = self.back_to_main)

		self.set_timer_btn.bind(on_press = self.set_timer)

		self.add_widget(self.back_to_main_btn)

		self.add_widget(Label(text ='Timer', font_size = self.FONT_SIZE))
		self.add_widget(self.h_text)
		self.add_widget(self.m_text)
		self.add_widget(self.s_text)

		self.add_widget(self.set_timer_btn)

		
	def set_timer(self, instance):
		hours = int(self.h_text.text) if self.h_text.text != 'hours' else 0
		minutes = int(self.m_text.text) if self.m_text.text != 'minutes' else 0
		seconds = int(self.s_text.text) if self.s_text.text != 'seconds' else 0

		seconds = seconds + (minutes * 60) + (hours * 60  * 60) 

		print(seconds)

		print(f'{seconds}'.encode())

		self.send_stream.write(f'{seconds}'.encode())
		print('Timer started!')
		self.send_stream.flush()

	def back_to_main(self, root):
	 	self.screen_manager.current = 'Main'


class TimerScreen(Screen):
	def __init__(self, **kwargs): 
		super(TimerScreen, self).__init__(**kwargs)


class Feed(GridLayout):

	FONT_SIZE = '50'

	def __init__(self, screen_manager, send_stream, recv_stream, **kwargs): 
		super(Feed, self).__init__(**kwargs)

		self.recv_stream, self.recv_stream = recv_stream, send_stream

		self.screen_manager = screen_manager
 
		self.rows = 5

		self.back_to_main_btn = Button(text ='Back to main', font_size = '50', size_hint_y=None, size=(50, 100))
		
		self.back_to_main_btn.bind(on_press = self.back_to_main)

		self.add_widget(self.back_to_main_btn)

		self.add_widget(Label(text ='Select feed options: ', font_size = '50'))

		self.low_btn = Button(text ='low', font_size = '50', size_hint_y=None, size=(50, 200))
		self.medium_btn = Button(text ='medium', font_size = '50', size_hint_y=None, size=(50, 200))
		self.big_btn = Button(text ='high', font_size = '50', size_hint_y=None, size=(50, 200))

		self.add_widget(self.low_btn)
		self.add_widget(self.medium_btn)
		self.add_widget(self.big_btn)

		self.low_btn.bind(on_press = self.on_low_btn)
		self.medium_btn.bind(on_press = self.on_medium_btn)
		self.big_btn.bind(on_press = self.on_big_btn)

	def back_to_main(self, root):
		self.screen_manager.current = 'Main'

	def on_low_btn(self, instance):
		self.send_stream.write('1'.encode())
		print('gave low portion to a pet')
		self.send_stream.flush()

	def on_medium_btn(self, instance):
		self.send_stream.write('2'.encode())
		print('gave medium portion to a pet')
		self.send_stream.flush()

	def on_big_btn(self, instance):
		self.send_stream.write('3'.encode())
		print('gave big portion to a pet')
		self.send_stream.flush()


class FeedScreen(Screen):
	def __init__(self, **kwargs): 
		super(FeedScreen, self).__init__(**kwargs)


class Main(GridLayout):

	FONT_SIZE = '50'

	def __init__(self, screen_manager, **kwargs): 
		super(Main, self).__init__(**kwargs)

		self.screen_manager = screen_manager
 
		self.rows = 2

		self.timer_screen_btn = Button(text ='Timer', font_size = self.FONT_SIZE)
		self.feed_screen_btn = Button(text ='Feed now', font_size = self.FONT_SIZE)

		self.timer_screen_btn.bind(on_press=self.timer_screen)
		self.feed_screen_btn.bind(on_press=self.feed_screen)

		self.add_widget(self.timer_screen_btn)
		self.add_widget(self.feed_screen_btn)


	def timer_screen(self, root):
		self.screen_manager.current = 'Timer'

	def feed_screen(self, root):
		self.screen_manager.current = 'Feed'


class MainScreen(Screen):
	def __init__(self, **kwargs): 
		super(MainScreen, self).__init__(**kwargs)


class WidgetApp(App):

	def __init__(self, **kwargs):
		super(WidgetApp, self).__init__(**kwargs)

		self.bluetooth = Bluetooth('ilya-Vostro-15-3568')

		recv_stream, send_stream = self.bluetooth.get_socket_stream()

		self.sm = ScreenManager(transition = SlideTransition())
		self.main_screen = MainScreen(name='Main')
		self.timer_screen = TimerScreen(name='Timer')
		self.feed_screen = FeedScreen(name='Feed')

		self.main_screen.add_widget(Main(self.sm))
		self.timer_screen.add_widget(Timer(self.sm, recv_stream, send_stream))
		self.feed_screen.add_widget(Feed(self.sm, recv_stream, send_stream))

		self.sm.add_widget(self.main_screen)
		self.sm.add_widget(self.timer_screen)
		self.sm.add_widget(self.feed_screen)

		self.sm.current = 'Main'

	def build(self):
		return self.sm

WidgetApp().run()