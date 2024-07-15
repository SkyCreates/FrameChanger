base_styles = """
/* Base Styles for All Widgets */
QWidget {
    font-family: 'Segoe UI', sans-serif;
    font-size: 11pt;
    color: #ECF0F1;  /* Light Grey */
    background-color: #2C3E50;  /* Darker Grey */
}

/* Button and Label Styles */
QPushButton, QLabel {
    font-size: 13pt;
    height: 32px;
    border-radius: 5px;
    background-color: #1E90FF;  /* Vibrant Blue */
    color: #FFFFFF;  /* White */
    border: none;
}

QPushButton:hover {
    background-color: #1C86EE;  /* Slightly darker blue for hover */
}

/* Input Field and List View Styles */
QLineEdit, QComboBox, QListView, QRadioButton, QCheckBox {
    font-size: 12pt;
    height: 32px;
    border-radius: 5px;
    background-color: #34495E;  /* Darker input fields */
    color: #ECF0F1;  /* Light Grey text */
    border: 2px solid #1E90FF;  /* Vibrant Blue border */
}

/* ComboBox Drop-down Arrow Styles */
QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 20px;
    border-left-width: 1px;
    border-left-color: darkgray;
    border-left-style: solid;
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
}

QComboBox::down-arrow {
    width: 0;  /* Hides the default down arrow */
}

/* RadioButton and CheckBox Indicator Styles */
QRadioButton::indicator:checked, QCheckBox::indicator:checked {
    background-color: #1E90FF;  /* Vibrant Blue */
    border: 2px solid #1E90FF;  /* Vibrant Blue */
}

/* MessageBox Styles */
QMessageBox {
    color: #1E90FF;  /* Vibrant Blue */
}

QMessageBox QLabel {
    color: inherit;
}

/* Tooltip Styles */
QToolTip {
    background-color: #333333;  /* Dark Grey */
    color: #ECF0F1;  /* Light Grey */
    border: 1px solid #1E90FF;  /* Vibrant Blue */
    font-size: 10pt;
    padding: 5px;
}
"""

stylesheets = {
    "Default": base_styles + """
    QWidget {
        background-color: #2C3E50;  /* Darker Grey background for Default theme */
        color: #ECF0F1;  /* Light Grey text for better contrast */
    }
    QPushButton {
        background-color: #1E90FF;  /* Vibrant Blue button color */
        color: #FFFFFF;  /* White text for better visibility */
    }
    QLineEdit, QComboBox, QListView, QRadioButton, QCheckBox {
        background-color: #34495E;  /* Darker input fields */
        color: #ECF0F1;  /* Light Grey text for readability */
        border: 2px solid #1E90FF;  /* Vibrant Blue border */
    }
    QComboBox::down-arrow {
        color: #1E90FF;  /* Vibrant Blue arrow for Default theme */
    }
    QRadioButton::indicator:checked, QCheckBox::indicator:checked {
        background-color: #1E90FF;  /* Vibrant Blue */
    }
    QMessageBox {
        color: #1E90FF;  /* Vibrant Blue text color */
    }
    QMessageBox QLabel {
        color: #ECF0F1;  /* Light Grey text for readability */
    }
    """,


    "Dark": base_styles + """
    QWidget {
        background-color: #1D1D1D;  /* Dark background for Dark theme */
        color: #E0E0E0;  /* Light text color for readability */
    }
    QPushButton {
        background-color: #3399FF;  /* Light blue button for contrast */
    }
    QLineEdit, QComboBox, QListView, QRadioButton, QCheckBox {
        background-color: #2C2C2C;  /* Dark input fields */
        color: #E0E0E0;  /* Light text color */
        border: 2px solid #3399FF;
    }
    QComboBox::down-arrow {
        color: #3399FF;  /* Light blue arrow for Dark theme */
    }
    QRadioButton::indicator:checked, QCheckBox::indicator:checked {
        background-color: #3399FF;
    }
    QMessageBox {
        color: #1D1D1D;
    }
    QMessageBox QLabel {
        color: #E0E0E0;  /* Ensure text is visible */
    }
    """,

    "IMDB": base_styles + """
    QWidget {
        background-color: #2C2C2C;  /* Dark background for IMDB theme */
        color: #F5C518;  /* IMDB yellow text */
    }
    QPushButton {
        background-color: #F5C518;  /* IMDB yellow button */
        color: #2C2C2C;  /* Dark text for contrast */
    }
    QPushButton:hover {
        background-color: #E6B800;  /* Slightly toned down yellow */
    }
    QLineEdit, QComboBox, QListView, QRadioButton, QCheckBox {
        background-color: #2C2C2C;  /* Dark input fields */
        color: #F5C518;  /* IMDB yellow text */
        border: 2px solid #F5C518;
    }
    QComboBox::down-arrow {
        color: #F5C518;  /* IMDB yellow arrow */
    }
    QRadioButton::indicator:checked, QCheckBox::indicator:checked {
        background-color: #F5C518;
    }
    QMessageBox {
        color: #2C2C2C;
    }
    QMessageBox QLabel {
        color: #F5C518;  /* Ensure text is visible */
    }
    """,

    "TMDB": base_styles + """
    QWidget {
        background-color: #081C24;  /* Dark background for TMDB theme */
        color: #01D277;  /* TMDB green text */
    }
    QPushButton {
        background-color: #01B368;  /* TMDB green button */
        color: #081C24;  /* Dark text for contrast */
    }
    QPushButton:hover {
        background-color: #019B57;  /* Subtler hover effect */
    }
    QLineEdit, QComboBox, QListView, QRadioButton, QCheckBox {
        background-color: #0B2E35;  /* Dark input fields */
        color: #01D277;  /* TMDB green text */
        border: 2px solid #01D277;
    }
    QComboBox::down-arrow {
        color: #01D277;  /* TMDB green arrow */
    }
    QRadioButton::indicator:checked, QCheckBox::indicator:checked {
        background-color: #01D277;
    }
    QMessageBox {
        color: #081C24;
    }
    QMessageBox QLabel {
        color: #01D277;  /* Ensure text is visible */
    }
    """,

    "GreyRed": base_styles + """
    QWidget {
        background-color: #2B2B2B;  /* Dark background for GreyRed theme */
        color: #F0F0F0;  /* Light text color */
    }
    QPushButton {
        background-color: #8B0000;  /* Red button */
        color: #F0F0F0;  /* Light text color */
    }
    QPushButton:hover {
        background-color: #5C0000;  /* Darker red on hover */
    }
    QLineEdit, QComboBox, QListView, QRadioButton, QCheckBox {
        background-color: #2B2B2B;  /* Dark input fields */
        color: #F0F0F0;  /* Light text color */
        border: 2px solid #8B0000;
    }
    QComboBox::down-arrow {
        color: #8B0000;  /* Red arrow for GreyRed theme */
    }
    QRadioButton::indicator:checked, QCheckBox::indicator:checked {
        background-color: #8B0000;
    }
    QMessageBox {
        color: #2B2B2B;
    }
    QMessageBox QLabel {
        color: #F0F0F0;  /* Ensure text is visible */
    }
    """
}
