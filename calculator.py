import sys
import math
import re
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class ScientificCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Casio Scientific Calculator")
        self.setGeometry(100, 100, 400, 600)
        self.setStyleSheet("background-color: #222; color: white;")

        # Layouts
        main_layout = QVBoxLayout()
        grid_layout = QGridLayout()

        # Display
        self.display = QLineEdit()
        self.display.setFont(QFont("Arial", 24))
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setStyleSheet("background: black; color: #0f0; padding: 10px; border: 2px solid #555;")
        main_layout.addWidget(self.display)

        # Buttons layout
        buttons = [
            ('7', '8', '9', 'DEL', 'AC'),
            ('4', '5', '6', '*', '/'),
            ('1', '2', '3', '+', '-'),
            ('0', '.', 'EXP', '(', ')'),
            ('sin', 'cos', 'tan', 'log', 'sqrt'),
            ('pi', 'e', '^', '=', 'ANS')
        ]

        for row_idx, row in enumerate(buttons):
            for col_idx, text in enumerate(row):
                button = QPushButton(text)
                button.setFont(QFont("Arial", 14))
                button.setStyleSheet("background-color: #444; border-radius: 5px; padding: 15px;")
                button.clicked.connect(lambda checked, btn=text: self.buttonClicked(btn))
                grid_layout.addWidget(button, row_idx, col_idx)

        main_layout.addLayout(grid_layout)
        self.setLayout(main_layout)

    def buttonClicked(self, button_text):
        if button_text == "=":
            try:
                expression = self.display.text()
                result = self.evaluateExpression(expression)
                self.display.setText(str(result))
            except Exception as e:
                self.display.setText("Error")

        elif button_text == "AC":
            self.display.clear()
        elif button_text == "DEL":
            self.display.setText(self.display.text()[:-1])
        elif button_text == "EXP":
            self.display.setText(self.display.text() + "e")
        else:
            self.display.setText(self.display.text() + button_text)

    def evaluateExpression(self, expression):
        expression = expression.replace('^', '**')
        expression = expression.replace('pi', str(math.pi))
        expression = expression.replace('e', str(math.e))
        expression = self.handleTrigFunctions(expression)

        try:
            result = eval(expression, {"math": math})
            return result
        except Exception:
            raise ValueError("Invalid expression")

    def handleTrigFunctions(self, expression):
        expression = re.sub(r'sin\((.*?)\)', lambda m: str(self.sin(float(m.group(1)))), expression)
        expression = re.sub(r'cos\((.*?)\)', lambda m: str(self.cos(float(m.group(1)))), expression)
        expression = re.sub(r'tan\((.*?)\)', lambda m: str(self.tan(float(m.group(1)))), expression)
        expression = re.sub(r'log\((.*?)\)', lambda m: str(self.log(float(m.group(1)))), expression)
        expression = re.sub(r'sqrt\((.*?)\)', lambda m: str(self.sqrt(float(m.group(1)))), expression)
        return expression

    def sin(self, x):
        return math.sin(math.radians(x))

    def cos(self, x):
        return math.cos(math.radians(x))

    def tan(self, x):
        x = x % 360
        if x == 90 or x == 270:
            return float('inf')
        return math.tan(math.radians(x))

    def log(self, x):
        if x <= 0:
            raise ValueError("Logarithm undefined for non-positive values")
        return math.log10(x)

    def sqrt(self, x):
        if x < 0:
            raise ValueError("Square root undefined for negative values")
        return math.sqrt(x)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScientificCalculator()
    window.show()
    sys.exit(app.exec())