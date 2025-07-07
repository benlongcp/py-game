import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        # Create widgets
        self.label = QLabel("Type something below:")
        self.textbox = QLineEdit()
        self.button = QPushButton("Submit")

        # Connect button click to a function
        self.button.clicked.connect(self.update_label)

        # Arrange widgets using a vertical layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.textbox)
        layout.addWidget(self.button)

        # Set the layout on the main window
        self.setLayout(layout)
        self.setWindowTitle("My First PyQt App")

    def update_label(self):
        # Get text from the textbox and set it to the label
        user_text = self.textbox.text()
        self.label.setText(f"You said: {user_text}")

# Run the application
app = QApplication(sys.argv)
window = MyApp()
window.show()
sys.exit(app.exec())
