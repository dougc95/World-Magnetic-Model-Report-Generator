import logging
import traceback
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QMessageBox,
    QDateEdit,
    QButtonGroup,
    QApplication,
)
from PyQt6.QtCore import QDate
from src.models.wmm_model import WMMModel
from src.services.wmm_calculator import WMMCalculator
from src.services.excel_generator import ExcelGenerator
from src.utils.date_utils import DateUtils


logger = logging.getLogger(__name__)


class WMMGui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WMM Excel Generator")
        screen = QApplication.primaryScreen()
        screen_size = screen.size()
        screen_width = screen_size.width()
        screen_height = screen_size.height()
        window_width = 800
        window_height = 300
        center_x = int((screen_width - window_width) / 2)
        center_y = int((screen_height) / 2)
        self.setGeometry(center_x, center_y, window_width, window_height)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Create input fields, labels, and buttons
        self.txt_lat = QLineEdit()
        self.txt_lon = QLineEdit()
        self.txt_alt = QLineEdit()
        self.txt_step_days = QLineEdit("1")
        self.txt_output_file = QLineEdit()

        # Calendar
        self.txt_start_date = QDateEdit()
        self.txt_end_date = QDateEdit()
        self.txt_start_date.setDate(QDate.currentDate())
        self.txt_end_date.setDate(QDate.currentDate())

        # Buttons
        btn_generate = QPushButton("Generate")
        btn_generate.clicked.connect(self.on_generate)

        # Create radio buttons groups
        self.lat_group = QButtonGroup(self)
        self.lon_group = QButtonGroup(self)
        self.alt_group = QButtonGroup(self)

        # Add radio buttons
        self.rb_north = QRadioButton("North")
        self.rb_south = QRadioButton("South")
        self.rb_east = QRadioButton("East")
        self.rb_west = QRadioButton("West")
        self.rb_km = QRadioButton("Meters")
        self.rb_ft = QRadioButton("Feet")

        # Add radio buttons to groups
        self.lat_group.addButton(self.rb_north)
        self.lat_group.addButton(self.rb_south)
        self.lon_group.addButton(self.rb_east)
        self.lon_group.addButton(self.rb_west)
        self.alt_group.addButton(self.rb_km)
        self.alt_group.addButton(self.rb_ft)

        self.rb_north.setChecked(True)
        self.rb_east.setChecked(True)
        self.rb_km.setChecked(True)

        # Create layouts
        lat_layout = QHBoxLayout()
        lat_layout.addWidget(QLabel("Latitude:"))
        lat_layout.addWidget(self.txt_lat)
        lat_layout.addWidget(self.rb_north)
        lat_layout.addWidget(self.rb_south)

        lon_layout = QHBoxLayout()
        lon_layout.addWidget(QLabel("Longitude:"))
        lon_layout.addWidget(self.txt_lon)
        lon_layout.addWidget(self.rb_east)
        lon_layout.addWidget(self.rb_west)

        alt_layout = QHBoxLayout()
        alt_layout.addWidget(QLabel("Altitude:"))
        alt_layout.addWidget(self.txt_alt)
        alt_layout.addWidget(self.rb_km)
        alt_layout.addWidget(self.rb_ft)

        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("Start Date:"))
        date_layout.addWidget(self.txt_start_date)
        date_layout.addWidget(QLabel("End Date:"))
        date_layout.addWidget(self.txt_end_date)

        step_layout = QHBoxLayout()
        step_layout.addWidget(QLabel("Step (days):"))
        step_layout.addWidget(self.txt_step_days)

        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("Output File:"))
        output_layout.addWidget(self.txt_output_file)

        # Add layouts to main layout
        main_layout.addLayout(lat_layout)
        main_layout.addLayout(lon_layout)
        main_layout.addLayout(alt_layout)
        main_layout.addLayout(date_layout)
        main_layout.addLayout(step_layout)
        main_layout.addLayout(output_layout)
        main_layout.addWidget(btn_generate)

    def on_generate(self):
        try:
            # Get input values from text fields
            lat = float(self.txt_lat.text())
            lon = float(self.txt_lon.text())
            alt = float(self.txt_alt.text())
            start_date = self.txt_start_date.date().toString("yyyy-MM-dd")
            end_date = self.txt_end_date.date().toString("yyyy-MM-dd")
            step_days = int(self.txt_step_days.text())
            output_file = self.txt_output_file.text()

            # Adjust latitude based on radio button selection
            if self.rb_south.isChecked():
                lat = -lat

            # Adjust longitude based on radio button selection
            if self.rb_west.isChecked():
                lon = -lon

            # Adjust altitude based on radio button selection
            if self.rb_ft.isChecked():
                alt = alt * 0.3048780487804878 / 1000  # Convert feet to meters

            # Generate date range
            dates = DateUtils.date_range(start_date, end_date, step_days)

            # Create ExcelGenerator instance
            excel_generator = ExcelGenerator(output_file)
            excel_generator.generate_header()

            # Perform calculations and add data to Excel
            for date in dates:
                model = WMMModel(latitude=lat, longitude=lon, altitude=alt, date=date)

                WMMCalculator.calculate(model)
                next_model = WMMCalculator.calculate_next_year(model)
                variation = WMMCalculator.calculate_variation(model, next_model)
                excel_generator.add_data(model, variation)

            # Save the Excel file
            excel_generator.save()

            # Show completion message
            QMessageBox.information(
                self, "Complete", "Excel file generated successfully!"
            )
        except Exception as e:
            logger.error(f'{e}')
            logger.error(f'Full traceback:\n{traceback.format_exc()}')
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
