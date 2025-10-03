from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.clock import Clock
from datetime import datetime
from kivy.uix.image import Image
from kivy.graphics import Color, RoundedRectangle

class StudyTimerWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (None, None)
        self.size = (400, 300)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.3}
        self.padding = [20, 20]
        self.spacing = 15
        
        with self.canvas.before:
            Color(0, 0, 0, 0.8)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[20])
        
        self.name_label = Label(
            text='STUDENT STUDY SESSION',
            font_size='24sp',
            color=(0, 1, 0.5, 1),
            size_hint=(1, 0.2),
            bold=True
        )
        self.timer_label = Label(
            text='00:00:00',
            font_size='60sp',
            color=(0, 1, 0.5, 1),
            size_hint=(1, 0.4),
            bold=True
        )
        
        self.session_info = Label(
            text='Current Session',
            font_size='18sp',
            color=(0, 0.8, 0.4, 1),
            size_hint=(1, 0.2)
        )
        
        controls = BoxLayout(size_hint=(1, 0.2), spacing=15)
        
        button_style = {
            'background_normal': '',
            'font_size': '18sp',
            'bold': True,
            'size_hint': (1, 1)
        }
        
    
        self.start_button = Button(
            text='START',
            background_color=(0, 0.7, 0.3, 1),
            **button_style
        )
        
        self.reset_button = Button(
            text='RESET',
            background_color=(0.7, 0, 0, 1),
            **button_style
        )
        
        controls.add_widget(self.start_button)
        controls.add_widget(self.reset_button)
        
        self.add_widget(self.name_label)
        self.add_widget(self.timer_label)
        self.add_widget(self.session_info)
        self.add_widget(controls)
        
        self.study_time = 0
        self.timer_running = False
        self.session_count = 0
        
        self.start_button.bind(on_press=self.toggle_timer)
        self.reset_button.bind(on_press=self.reset_timer)
        
        self.bind(pos=self.update_rect, size=self.update_rect)
        
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
    
    def toggle_timer(self, instance):
        self.timer_running = not self.timer_running
        if self.timer_running and self.study_time == 0:
            self.session_count += 1
            self.session_info.text = f'Study Session #{self.session_count}'
        
        instance.text = 'PAUSE' if self.timer_running else 'START'
        instance.background_color = (0.7, 0.3, 0, 1) if self.timer_running else (0, 0.7, 0.3, 1)
    
    def reset_timer(self, instance):
        self.study_time = 0
        self.timer_running = False
        self.start_button.text = 'START'
        self.start_button.background_color = (0, 0.7, 0.3, 1)
        self.session_info.text = 'Current Session'
        self.update_display()
    
    def update_display(self):
        hours = self.study_time // 3600
        minutes = (self.study_time % 3600) // 60
        seconds = self.study_time % 60
        self.timer_label.text = f'{hours:02d}:{minutes:02d}:{seconds:02d}'
    
    def update(self, dt):
        if self.timer_running:
            self.study_time += 1
            self.update_display()

class ModernClockWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (None, None)
        self.size = (400, 200)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.7}
        
        with self.canvas.before:
            Color(0, 0, 0, 0.7)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[20])
        
        self.time_label = Label(
            text='00:00:00',
            font_size='80sp',
            color=(0, 1, 0.5, 1),
            size_hint=(1, 0.7),
            bold=True
        )
        
        self.date_label = Label(
            text='',
            font_size='24sp',
            color=(0, 0.8, 0.4, 1),
            size_hint=(1, 0.3)
        )
        
        self.add_widget(self.time_label)
        self.add_widget(self.date_label)
        
        self.bind(pos=self.update_rect, size=self.update_rect)
        
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        
    def update_time(self, time_str, date_str):
        self.time_label.text = time_str
        self.date_label.text = date_str

class MainLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        Window.clearcolor = (0, 0, 0, 1)
        
        self.background = Image(
            source='8bit.gif',
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            anim_delay=0.1
        )
        self.add_widget(self.background)
        
        self.clock_widget = ModernClockWidget()
        self.add_widget(self.clock_widget)
        
        self.timer_widget = StudyTimerWidget()
        self.add_widget(self.timer_widget)
        
        Clock.schedule_interval(self.update_clock, 1)
        Clock.schedule_interval(self.timer_widget.update, 1)
    
    def update_clock(self, dt):
        now = datetime.now()
        current_time = now.strftime('%H:%M:%S')
        current_date = now.strftime('%B %d, %Y')
        self.clock_widget.update_time(current_time, current_date)

class RetroStudy(App):
    def build(self):
        Window.size = (800, 600)
        return MainLayout()

if __name__ == "__main__":
    RetroStudy().run()