import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
import g4f  # Импортируем библиотеку G4F

# Главная страница приложения
class SimpleScriptApp(App):
    selected_language = "Processing"  # По умолчанию выбран Processing

    def build(self):
        # Основное вертикальное расположение элементов
        layout = BoxLayout(orientation='vertical')

        # Поле ввода кода
        self.code_input = TextInput(
            hint_text="Введите код SimpleScript",
            size_hint=(1, 0.4),
            background_color=(0.2, 0.2, 0.2, 1),
            foreground_color=(1, 1, 1, 1),
            multiline=True
        )
        layout.add_widget(self.code_input)

        # Кнопка "Запустить"
        run_button = Button(
            text="Run",
            size_hint=(1, 0.1),
            background_color=(0.3, 0.7, 0.3, 1)
        )
        run_button.bind(on_press=self.translate_code)
        layout.add_widget(run_button)

        # Выпадающий список для выбора языка
        self.language_dropdown = DropDown()
        for lang in ["Processing", "Python", "Lua"]:
            btn = Button(text=lang, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.language_dropdown.select(btn.text))
            self.language_dropdown.add_widget(btn)
        
        main_button = Button(text="Выберите язык", size_hint=(1, 0.1))
        main_button.bind(on_release=self.language_dropdown.open)
        self.language_dropdown.bind(on_select=lambda instance, x: self.select_language(x))
        layout.add_widget(main_button)

        # Поле вывода переведённого кода
        self.code_output = TextInput(
            hint_text="Здесь появится переведённый код",
            size_hint=(1, 0.4),
            background_color=(0.2, 0.2, 0.2, 1),
            foreground_color=(1, 1, 1, 1),
            multiline=True,
            readonly=True
        )
        layout.add_widget(self.code_output)

        return layout

    # Функция перевода кода
    def translate_code(self, instance):
        try:
            simple_script_code = self.code_input.text.strip()
            
            # Формируем запрос в зависимости от выбранного языка
            language_prompts = {
                "Processing": f"Напиши скрипт на Processing РОВНО как в этом примере...",
                "Python": f"Напиши скрипт на Python РОВНО как в этом примере...",
                "Lua": f"Напиши скрипт на Lua для solar 2d РОВНО как в этом примере..."
            }

            prompt = language_prompts.get(self.selected_language, language_prompts["Processing"])
            
            # Отправляем запрос через G4F
            response = g4f.ChatCompletion.create(
                model="gemini-pro",
                messages=[{"role": "user", "content": f"{prompt}\n{simple_script_code}"}]
            )

            translated_code = response
            self.code_output.text = translated_code
        
        except Exception as e:
            self.code_output.text = f"Произошла ошибка: {e}"

    # Выбор языка
    def select_language(self, language):
        self.selected_language = language
        print(f"Выбранный язык: {language}")

# Запуск приложения
if __name__ == "__main__":
    SimpleScriptApp().run()
