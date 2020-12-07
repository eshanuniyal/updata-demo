from FormRecognizer import FormRecognizer
import pair_data
import csv
import os
from PyQt5.QtWidgets import QWidget, QPushButton, QFileDialog, QLineEdit, QLabel, QDialog, QGroupBox, QCheckBox, QDateTimeEdit, QComboBox, QGridLayout, QFormLayout
from PyQt5.QtCore import QDateTime, QThread

def datapoint(name):
    for datapoint in pair_data.PAIRS:
        if datapoint.key() == name:
            return datapoint

class FormProcessor(QThread):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def run(self):
        self.parent.recognizer.extract_pairs()

class GUI(QWidget):
    def __init__(self):
        super().__init__()  # initializes the QWidget
        self.init_UI()

    def init_UI(self):
        self.setWindowTitle('Updata Demo')  # title
        # self.process_file()  # UNCOMMENT
        self.init_geo()                     # geometry
        self.init_input()                   # path field and browse button
        self.show()                         # displays the QWidget

    def init_geo(self):
        self.setGeometry(200, 200, 600, 145)

    def init_input(self):
        # create instruction label
        self.file_select_label = QLabel("Please enter the path to the file or select by clicking on Browse:", self)
        self.file_select_label.move(25, 25)
        # create path field
        self.path_field = QLineEdit(self)
        self.path_field.move(25, 45)
        self.path_field.resize(450, 25)
        self.path_field.setPlaceholderText("Enter path")
        # create browse button
        self.browse_btn = QPushButton('Browse', self)
        self.browse_btn.move(500, 45)
        self.browse_btn.resize(75, 25)
        # create file browser
        self.init_browser()

        # create OK and Cancel buttons
        self.file_select_process = QPushButton("Process", self)
        self.file_select_process.move(500, 95)
        self.file_select_process.resize(75, 25)
        self.file_select_process.clicked.connect(self.process_file)

        self.file_select_cancel = QPushButton("Cancel", self)
        self.file_select_cancel.move(400, 95)
        self.file_select_cancel.resize(75, 25)
        self.file_select_cancel.clicked.connect(self.close)

    def init_browser(self):
        # create file browser
        self.file_browser = QFileDialog(self, "Select a PDF file")
        self.browse_btn.clicked.connect(self.get_file)  # open browser when click on "Browse" button
        self.file_browser.fileSelected.connect(self.path_field.setText)  # fill path field when a path is selected

    def get_file(self):
        path = self.file_browser.getOpenFileName(self, 'Select PDF file', '', 'PDF Files (*.pdf)')[0]
        # print(path)
        self.path_field.setText(path)
        
    def process_file(self):
        # slot connected to self.file_select_ok.clicked signal
        self.file_path = self.path_field.text()  # regardless of whether path_field was filled or browser was used, path should be in path_field
        
        # check whether path exists
        try:
            f = open(self.file_path, "rb")
            f.close()
        except FileNotFoundError:
            self.file_select_label.setText("File not found. Please try again.")
            self.file_select_label.setStyleSheet("color: red;")
            return
        except:
            self.file_select_label.setText("Could not read file. Please try again.")
            self.file_select_label.setStyleSheet("color: red;")

        # path exists, continue processing
        os.chdir(os.path.dirname(self.file_path))
        # update UI elements
        self.file_select_label.setText("Processing...")
        self.file_select_label.setStyleSheet("color: green;")
        self.path_field.setReadOnly(True)
        self.path_field.setStyleSheet(
            "color: #808080;"
            "background-color: #F0F0F0;"
        )
        self.browse_btn.setEnabled(False)
        self.browse_btn.setStyleSheet(
            "color: #808080;"
            "background-color: #F0F0F0;"
        )

        # calling recognizer and extracting pairs
        self.recognizer = FormRecognizer(self.file_path)
        self.recognizer_thread = FormProcessor(self)
        self.recognizer_thread.finished.connect(self.open_form_window)
        self.recognizer_thread.start()
 
        # self.pairs = self.recognizer.extract_pairs()  # UNCOMMENT
        # self.pairs = {'Assessment Type': "Virtual", 'Assessment Level': 'Housing needs assessment', 'Pronouns': 'she/her/hers', 'Client Name / HMIS ID': "31416", 'HMIS Consent signed': 'Yes', 'Date consented': datetime.date(2020, 4, 8), 'Assessment Location': 'Pasadena', 'Social Security Number': 2357111317, 'Quality of SSN': "Approximate or partial SSN reported", 'Last Name': 'Smith', 'Middle Name': "J.", 'Suffix': "Jr.", 'Maiden Name': 'Doe', 'First Name': 'Jane', 'Alias': 'V', 'Quality of Name': 'Full name reported', 'Date of Birth': datetime.date(2000, 5, 9), 'DOB - Score': 1, 'Quality of DOB': "Client refused", 'Gender': "Female", 'Ethnicity': 'Data not collected', 'Race': "Asian", 'Primary Language': "Greek"}
        # self.pairs = {datapoint.key(): None for datapoint in pair_data.PAIRS}

    def open_form_window(self):
        self.hide()
        self.recognizer_thread.quit()
        self.form_window = FormWindow(self.recognizer.pairs)

    # def closeEvent(self, event):
    #     if hasattr(self, "recognizer_thread"):
    #         self.recognizer_thread.quit()



class FormWindow(QDialog):

    profiles = {
        "Assessment Profile": [
            "Client Name / HMIS ID",
            "HMIS Consent signed",
            "Date consented",
            "Assessment Location",
            "Assessment Type",
            "Assessment Level"
        ],
        "Personal Profile": [
            "Social Security Number",
            "Quality of SSN",
            "Last Name",
            "Middle Name",
            "Suffix",
            "Maiden Name",
            "First Name",
            "Alias",
            "Quality of Name",
            "Date of Birth",
            "DOB - Score",
            "Quality of DOB",
            "Gender",
            "Pronouns",
            "Ethnicity",
            "Race",
            "Primary Language"
        ]
    }

    def __init__(self, pairs):
        super().__init__()
        self.pairs = pairs
        self.fields = {}
        self.labels = {}
        self.init_UI()

    def init_UI(self):
        self.setWindowTitle("Updata Demo")
        self.init_geo()
        self.init_btns()
        self.show()

    def init_btns(self):
                # -----------------------------------------------------------------
        # creating assessment profile box
        self.assessment_profile_box = QGroupBox("Assessment Profile", self)
        self.fields["Client Name / HMIS ID"] = QLineEdit(self)
        self.fields["HMIS Consent signed"] = QCheckBox(self)
        self.fields["Date consented"] = QDateTimeEdit(self)
        self.fields["Date consented"].setDisplayFormat("MM/dd/yyyy")
        self.fields["Assessment Location"] = QLineEdit(self)
        self.fields["Assessment Type"] = QComboBox(self)
        self.fields["Assessment Level"] = QComboBox(self)
        self.create_form("Assessment Profile", self.assessment_profile_box)
        
        # -----------------------------------------------------------------
        # creating assessment profile box
        self.personal_profile_box = QGroupBox("Personal Profile", self)
        self.fields["Social Security Number"] = QLineEdit(self)
        self.fields["Quality of SSN"] = QComboBox(self)
        self.fields["Last Name"] = QLineEdit(self)
        self.fields["Middle Name"] = QLineEdit(self)
        self.fields["Suffix"] = QLineEdit(self)
        self.fields["Maiden Name"] = QLineEdit(self)
        self.fields["First Name"] = QLineEdit(self)
        self.fields["Alias"] = QLineEdit(self)
        self.fields["Quality of Name"] = QComboBox(self)
        self.fields["Date of Birth"] = QDateTimeEdit(self)
        self.fields["Date of Birth"].setDisplayFormat("MM/dd/yyyy")
        self.fields["DOB - Score"] = QCheckBox(self)
        self.fields["Quality of DOB"] = QComboBox(self)
        self.fields["Gender"] = QComboBox(self)
        self.fields["Pronouns"] = QLineEdit(self)
        self.fields["Ethnicity"] = QComboBox(self)
        self.fields["Race"] = QComboBox(self)
        self.fields["Primary Language"] = QComboBox(self)
        self.create_form("Personal Profile", self.personal_profile_box)

        # create export, cancel buttons
        self.export_button = QPushButton("Export")
        self.cancel_button = QPushButton("Cancel")
        self.export_button.clicked.connect(self.extract)
        self.cancel_button.clicked.connect(self.close)

        # add export, cancel buttons
        button_widget = QWidget(self)
        button_layout = QGridLayout(self)
        button_layout.addWidget(self.cancel_button, 1, 1)
        button_layout.addWidget(self.export_button, 1, 2)
        button_widget.setLayout(button_layout)
        self.mainLayout.addWidget(button_widget)
        

        self.insert_info()

    def insert_info(self):
        # inserting information
        for name, field in self.fields.items():
            if type(field) is QComboBox:
                field.addItem("")
                field.addItems(datapoint(name).value_types())
                if self.pairs[name] is not None:
                    field.setCurrentText(self.pairs[name])
            elif type(field) is QLineEdit:
                if self.pairs[name] is not None:
                    field.setText(str(self.pairs[name]))
            elif type(field) is QDateTimeEdit:
                if self.pairs[name] is not None:
                    field.setDate(self.pairs[name])
            elif type(field) is QCheckBox:
                value = False
                if name == "HMIS Consent signed" and self.pairs[name] == 'Yes':
                    value = True
                elif name == "DOB - Score" and self.pairs[name] == 1:
                    value = True
                field.setChecked(value)

    def init_geo(self):
        self.setGeometry(200, 200, 600, 600)
        self.mainLayout = QGridLayout(self)
            
    def create_form(self, profile_type, groupbox):
        layout = QFormLayout(self)
        for field in self.profiles[profile_type]:
            self.labels[field] = QLabel(field)
            layout.addRow(self.labels[field], self.fields[field])
        groupbox.setLayout(layout)
        self.mainLayout.addWidget(groupbox)

    def paintEvent(self, event):
        can_export = True

        # validating information
        for name, field in self.fields.items():
            missing_value = False

            if type(field) is QComboBox:
                if field.currentText() == "":
                    missing_value = True
            elif type(field) is QLineEdit:
                if field.text() == "":
                    missing_value = True
            elif type(field) is QDateTimeEdit:
                if field.dateTime() == QDateTime(2000, 1, 1, 0, 0):
                    missing_value = True
            elif type(field) is QCheckBox:
                if not field.isChecked():
                    missing_value = True

            if missing_value:
                if datapoint(name).is_req():
                    self.labels[name].setStyleSheet("color: red;")
                    can_export = False
                elif datapoint(name).req() == pair_data.ReqTypes.SOFT_REQ:
                    self.labels[name].setStyleSheet("color: darkorange;")
            else:
                self.labels[name].setStyleSheet("color: black;")

        if can_export:
            self.export_button.setEnabled(True)
        else:
            self.export_button.setEnabled(False)

    def extract(self):
        for name, field in self.fields.items():
            value = ""
            if type(field) is QComboBox:
                value = field.currentText()
            elif type(field) is QLineEdit:
                value = field.text()
            elif type(field) is QDateTimeEdit:
                value = field.dateTime().toString(field.displayFormat())
            self.pairs[name] = value
        
        self.write_to_csv()
        

    def write_to_csv(self):
        keys = [datapoint.key() for datapoint in pair_data.PAIRS]
        values = [self.pairs[key] for key in keys]
        for val, idx in enumerate(values):
            if val is None:
                values[idx] = ""

        # write to csv file named output_file
        with open("out.csv", "w", newline = "") as outfile:
            writer = csv.writer(outfile, delimiter=',')
            writer.writerow(keys)
            writer.writerow(values)
        
        self.export_button.setText("Exported!")