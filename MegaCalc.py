from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import ScreenManager, Screen
import math
from datetime import datetime

# Shared helper functions
def is_positive_float(value):
    try:
        return float(value) > 0
    except:
        return False

def to_float(value):
    try:
        return float(value)
    except:
        return 0

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        layout.add_widget(Label(text="Hello! I'm your friendly calculator bot!", font_size=24))
        
        features = [
            ("Simple Interest", "si"),
            ("Compound Interest", "ci"),
            ("BMI", "bmi"),
            ("Loan EMI", "emi"),
            ("Temperature Converter", "temp"),
            ("Unit Converter", "unit"),
            ("Age Calculator", "age"),
            ("SI vs CI Comparison", "compare"),
            ("Scientific Calculator", "sci")
        ]
        
        for name, screen in features:
            btn = Button(text=name, size_hint_y=None, height=50)
            btn.bind(on_release=lambda btn, screen=screen: self.manager.current = screen)
            layout.add_widget(btn)
        
        self.add_widget(layout)

class SimpleInterestScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.inputs = [TextInput(hint_text=h, multiline=False, input_filter="float") for h in ["Principal", "Rate (%)", "Time (years)"]]
        self.result_label = Label(text="", font_size=20)
        self.build_ui("Simple Interest", self.calculate_si)

    def build_ui(self, title, callback):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        layout.add_widget(Label(text=title, font_size=24))
        for i in self.inputs:
            layout.add_widget(i)
        layout.add_widget(Button(text="Calculate", on_release=lambda x: callback()))
        layout.add_widget(self.result_label)
        layout.add_widget(Button(text="Back", on_release=lambda x: self.manager.current = "menu"))
        self.add_widget(layout)

    def calculate_si(self):
        try:
            p, r, t = map(to_float, [i.text for i in self.inputs])
            si = (p * r * t) / 100
            self.result_label.text = f"Simple Interest: {si:.2f}"
        except:
            self.result_label.text = "Invalid input."

class CompoundInterestScreen(SimpleInterestScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.inputs = [TextInput(hint_text=h, multiline=False, input_filter="float") for h in ["Principal", "Rate (%)", "Time (years)"]]
        self.result_label = Label(text="", font_size=20)
        self.clear_widgets()
        self.build_ui("Compound Interest", self.calculate_ci)

    def calculate_ci(self):
        try:
            p, r, t = map(to_float, [i.text for i in self.inputs])
            a = p * ((1 + r/100) ** t)
            ci = a - p
            self.result_label.text = f"Compound Interest: {ci:.2f}\nTotal Amount: {a:.2f}"
        except:
            self.result_label.text = "Invalid input."

class BMIScreen(SimpleInterestScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.inputs = [TextInput(hint_text="Weight (kg)", multiline=False, input_filter="float"),
                       TextInput(hint_text="Height (m)", multiline=False, input_filter="float")]
        self.result_label = Label(text="", font_size=20)
        self.clear_widgets()
        self.build_ui("BMI Calculator", self.calculate_bmi)

    def calculate_bmi(self):
        try:
            weight, height = map(to_float, [i.text for i in self.inputs])
            bmi = weight / (height ** 2)
            status = ("Underweight" if bmi < 18.5 else
                      "Normal" if bmi < 25 else
                      "Overweight" if bmi < 30 else "Obese")
            self.result_label.text = f"BMI: {bmi:.2f} ({status})"
        except:
            self.result_label.text = "Invalid input."

class EMIScreen(SimpleInterestScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.inputs = [TextInput(hint_text="Loan Amount", multiline=False, input_filter="float"),
                       TextInput(hint_text="Annual Rate (%)", multiline=False, input_filter="float"),
                       TextInput(hint_text="Tenure (years)", multiline=False, input_filter="int")]
        self.result_label = Label(text="", font_size=20)
        self.clear_widgets()
        self.build_ui("Loan EMI Calculator", self.calculate_emi)

    def calculate_emi(self):
        try:
            P, annual_rate, years = map(to_float, [i.text for i in self.inputs])
            r = annual_rate / 12 / 100
            n = years * 12
            emi = (P * r * (1 + r) ** n) / ((1 + r) ** n - 1)
            self.result_label.text = f"EMI: {emi:.2f}"
        except:
            self.result_label.text = "Invalid input."

class TemperatureScreen(SimpleInterestScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.input_temp = TextInput(hint_text="Enter Temperature", multiline=False, input_filter="float")
        self.spinner = Spinner(text="Celsius to Fahrenheit",
                               values=("Celsius to Fahrenheit", "Fahrenheit to Celsius", "Celsius to Kelvin", "Fahrenheit to Kelvin"))
        self.result_label = Label(text="", font_size=20)
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        layout.add_widget(Label(text="Temperature Converter", font_size=24))
        layout.add_widget(self.spinner)
        layout.add_widget(self.input_temp)
        layout.add_widget(Button(text="Convert", on_release=lambda x: self.convert()))
        layout.add_widget(self.result_label)
        layout.add_widget(Button(text="Back", on_release=lambda x: self.manager.current = "menu"))
        self.add_widget(layout)

    def convert(self):
        try:
            temp = to_float(self.input_temp.text)
            mode = self.spinner.text
            if mode == "Celsius to Fahrenheit":
                result = temp * 9 / 5 + 32
            elif mode == "Fahrenheit to Celsius":
                result = (temp - 32) * 5 / 9
            elif mode == "Celsius to Kelvin":
                result = temp + 273.15
            elif mode == "Fahrenheit to Kelvin":
                result = (temp - 32) * 5 / 9 + 273.15
            self.result_label.text = f"Result: {result:.2f}"
        except:
            self.result_label.text = "Invalid input."

class UnitConverterScreen(SimpleInterestScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.input_val = TextInput(hint_text="Enter Value", multiline=False, input_filter="float")
        self.spinner = Spinner(text="Meters to Kilometers", values=("Meters to Kilometers", "Kilometers to Miles"))
        self.result_label = Label(text="", font_size=20)
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        layout.add_widget(Label(text="Unit Converter", font_size=24))
        layout.add_widget(self.spinner)
        layout.add_widget(self.input_val)
        layout.add_widget(Button(text="Convert", on_release=lambda x: self.convert()))
        layout.add_widget(self.result_label)
        layout.add_widget(Button(text="Back", on_release=lambda x: self.manager.current = "menu"))
        self.add_widget(layout)

    def convert(self):
        try:
            value = to_float(self.input_val.text)
            mode = self.spinner.text
            if mode == "Meters to Kilometers":
                result = value / 1000
            elif mode == "Kilometers to Miles":
                result = value * 0.621371
            self.result_label.text = f"Result: {result:.2f}"
        except:
            self.result_label.text = "Invalid input."

class AgeCalculatorScreen(SimpleInterestScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.date_input = TextInput(hint_text="DOB (YYYY-MM-DD)", multiline=False)
        self.result_label = Label(text="", font_size=20)
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        layout.add_widget(Label(text="Age Calculator", font_size=24))
        layout.add_widget(self.date_input)
        layout.add_widget(Button(text="Calculate Age", on_release=lambda x: self.calculate_age()))
        layout.add_widget(self.result_label)
        layout.add_widget(Button(text="Back", on_release=lambda x: self.manager.current = "menu"))
        self.add_widget(layout)

    def calculate_age(self):
        try:
            birth_date = datetime.strptime(self.date_input.text, "%Y-%m-%d")
            today = datetime.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            self.result_label.text = f"Age: {age} years"
        except:
            self.result_label.text = "Invalid date format."

class CompareInterestScreen(SimpleInterestScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.inputs = [TextInput(hint_text=h, multiline=False, input_filter="float") for h in ["Principal", "Rate (%)", "Time (years)"]]
        self.result_label = Label(text="", font_size=20)
        self.clear_widgets()
        self.build_ui("Compare SI vs CI", self.compare)

    def compare(self):
        try:
            p, r, t = map(to_float, [i.text for i in self.inputs])
            si = (p * r * t) / 100
            ci = p * ((1 + r / 100) ** t) - p
            self.result_label.text = f"Simple Interest: {si:.2f}\nCompound Interest: {ci:.2f}"
        except:
            self.result_label.text = "Invalid input."

class ScientificCalculatorScreen(SimpleInterestScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.input_val = TextInput(hint_text="Enter Value", multiline=False, input_filter="float")
        self.spinner = Spinner(text="Sine", values=("Sine", "Cosine", "Tangent", "Log10", "Square Root"))
        self.result_label = Label(text="", font_size=20)
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        layout.add_widget(Label(text="Scientific Calculator", font_size=24))
        layout.add_widget(self.spinner)
        layout.add_widget(self.input_val)
        layout.add_widget(Button(text="Calculate", on_release=lambda x: self.calculate()))
        layout.add_widget(self.result_label)
        layout.add_widget(Button(text="Back", on_release=lambda x: self.manager.current = "menu"))
        self.add_widget(layout)

    def calculate(self):
        try:
            val = to_float(self.input_val.text)
            op = self.spinner.text
            if op == "Sine":
                result = math.sin(math.radians(val))
            elif op == "Cosine":
                result = math.cos(math.radians(val))
            elif op == "Tangent":
                result = math.tan(math.radians(val))
            elif op == "Log10":
                result = math.log10(val)
            elif op == "Square Root":
                result = math.sqrt(val)
            self.result_label.text = f"Result: {result:.4f}"
        except:
            self.result_label.text = "Invalid input."

class CalcApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(SimpleInterestScreen(name="si"))
        sm.add_widget(CompoundInterestScreen(name="ci"))
        sm.add_widget(BMIScreen(name="bmi"))
        sm.add_widget(EMIScreen(name="emi"))
        sm.add_widget(TemperatureScreen(name="temp"))
        sm.add_widget(UnitConverterScreen(name="unit"))
        sm.add_widget(AgeCalculatorScreen(name="age"))
        sm.add_widget(CompareInterestScreen(name="compare"))
        sm.add_widget(ScientificCalculatorScreen(name="sci"))
        return sm

if __name__ == '__main__':
    CalcApp().run()
