import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QStackedLayout,
    QDesktopWidget, QRadioButton, QTextEdit, QCheckBox, QFileDialog, QButtonGroup, QComboBox, QFormLayout, QSpinBox,
    QMessageBox, QLineEdit, QScrollArea
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
from methods import Encode

class EncodingWindow(QWidget):
    def __init__(self, file_data, encode_letter, parent=None):
        super().__init__()
        try:
            self.setWindowTitle("编码")
            self.resize(1600, 1200)

            self.file_data = file_data  # Binary array from loaded file
            self.encode_letter = encode_letter  # Encoding letter selected in EncodeWindow

            # Main layout
            main_layout = QVBoxLayout()

            # Select encoding method
            encoding_method_label = QLabel("Select Encoding Method")
            encoding_method_label.setFont(QFont("Arial", 12))
            main_layout.addWidget(encoding_method_label)

            self.encoding_method_combobox = QComboBox()
            self.encoding_method_combobox.addItems(["DNA Fountain", "YYC", "HybridCode", "HEDGES", "6-Huffman", "8-Huffman"])
            main_layout.addWidget(self.encoding_method_combobox)

            # Set encoding constraints
            constraints_label = QLabel("Set Encoding Constraints")
            constraints_label.setFont(QFont("Arial", 12))
            main_layout.addWidget(constraints_label)

            constraints_form = QFormLayout()
            self.gc_content_spinbox = QSpinBox()
            self.gc_content_spinbox.setRange(40, 60)  # Example GC content range (40%-60%)
            self.gc_content_spinbox.setValue(50)
            constraints_form.addRow("GC Content (%)", self.gc_content_spinbox)

            self.homopolymer_limit_spinbox = QSpinBox()
            self.homopolymer_limit_spinbox.setRange(1, 6)  # Example homopolymer limit range
            self.homopolymer_limit_spinbox.setValue(4)
            constraints_form.addRow("Homopolymer Limit", self.homopolymer_limit_spinbox)

            # Display results
            result_label = QLabel("Encoded Sequence")
            result_label.setFont(QFont("Arial", 12))
            main_layout.addWidget(result_label)

            self.result_text = QTextEdit()
            self.result_text.setReadOnly(True)
            main_layout.addWidget(self.result_text)

            # Encode button
            encode_button = QPushButton("Run Encoding")
            encode_button.setFont(QFont("Arial", 12))
            encode_button.clicked.connect(self.perform_encoding)
            main_layout.addWidget(encode_button)

            download_button = QPushButton("Download as FASTA")
            download_button.setFont(QFont("Arial", 12))
            download_button.clicked.connect(self.download_fasta)
            main_layout.addWidget(download_button)

            self.setLayout(main_layout)

            # Placeholder for encoded sequences
            self.encoded_sequences = []

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error during window initialization: {e}")

    def perform_encoding(self):
        # Example encoding logic (replace with actual implementation)
        selected_method = self.encoding_method_combobox.currentText()
        gc_content = self.gc_content_spinbox.value()
        homopolymer_limit = self.homopolymer_limit_spinbox.value()
        encoded_sequence = Encode(self.file_data, self.encode_letter, selected_method)
        encoded_sequence = f"Encoding performed using {selected_method}..."
        # Format results for display
        result_text = f"Encoding Method: {selected_method}\n"
        result_text += f"GC Content: {gc_content}%\n"
        result_text += f"Homopolymer Limit: {homopolymer_limit}\n\n"
        result_text += "\n".join(self.encoded_sequences)
        self.result_text.setPlainText(result_text)

    def download_fasta(self):
        """Save encoded sequences to a FASTA file."""
        if not self.encoded_sequences:
            QMessageBox.warning(self, "Warning", "No encoded sequences to save.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Save as FASTA", "", "FASTA Files (*.fasta)")
        if not file_path:
            return

        try:
            with open(file_path, "w") as fasta_file:
                fasta_file.write("\n".join(self.encoded_sequences))
            QMessageBox.information(self, "Success", "Encoded sequences saved successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save file: {e}")

class EncodeWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("编码方案")
        self.resize(1600, 1200)

        # Initialize variables to store user input
        self.file_path = None
        self.selected_method = None
        self.file_data = None

        # Main layout
        main_layout = QVBoxLayout()

        # Title
        title_label = QLabel("选择编码文件")
        title_label.setFont(QFont("Arial", 12))
        main_layout.addWidget(title_label)

        # Upload file section
        self.file_path_label = QLabel("移动文件到此处或点击”浏览“来选择文件")
        self.file_path_label.setFont(QFont("Arial", 14))
        self.file_path_label.setStyleSheet(
            "border: 2px dashed #007BFF; padding: 40px; color: #007BFF; background-color: #F8F9FA;"
        )
        self.file_path_label.setAlignment(Qt.AlignCenter)
        self.file_path_label.setAcceptDrops(True)  # Enable drag-and-drop
        main_layout.addWidget(self.file_path_label)

        # Connect drag and drop events
        self.file_path_label.dragEnterEvent = self.drag_enter_event
        self.file_path_label.dropEvent = self.drop_event

        # Browse button
        browse_button = QPushButton("浏览")
        browse_button.setFont(QFont("Arial", 14))
        browse_button.setStyleSheet("background-color: #007BFF; color: white; padding: 10px;")
        browse_button.clicked.connect(self.browse_file)
        main_layout.addWidget(browse_button)

        # Select encode molecules
        molecules_label = QLabel("选择编码字母")
        molecules_label.setFont(QFont("Arial", 12))
        main_layout.addWidget(molecules_label)

        # Molecule selection layout
        molecules_layout = QHBoxLayout()

        # First column (ATCG)
        column1_layout = QVBoxLayout()
        column1_label = QLabel("天然碱基")
        column1_label.setFont(QFont("Arial", 12))
        column1_label.setAlignment(Qt.AlignLeft)
        column1_layout.addWidget(column1_label, alignment=Qt.AlignLeft)

        atcg_radio = QRadioButton("A, T, C, G")
        column1_layout.addWidget(atcg_radio, alignment=Qt.AlignTop)

        molecules_layout.addLayout(column1_layout)

        # Second column (PZ, BS, PZBS)
        column2_layout = QVBoxLayout()
        column2_label = QLabel("非天然碱基")
        column2_label.setFont(QFont("Arial", 12))
        column2_label.setAlignment(Qt.AlignLeft)
        column2_layout.addWidget(column2_label, alignment=Qt.AlignLeft)

        pz_radio = QRadioButton("P, Z")
        bs_radio = QRadioButton("B, S")
        pzbs_radio = QRadioButton("P, Z+B, S")
        column2_layout.addWidget(pz_radio)
        column2_layout.addWidget(bs_radio)
        column2_layout.addWidget(pzbs_radio)

        molecules_layout.addLayout(column2_layout)

        # Third column (5mC, 6mA, 5mC+6mA)
        column3_layout = QVBoxLayout()
        column3_label = QLabel("修饰碱基")
        column3_label.setFont(QFont("Arial", 12))
        column3_label.setAlignment(Qt.AlignLeft)
        column3_layout.addWidget(column3_label, alignment=Qt.AlignLeft)

        m5c_radio = QRadioButton("5mC")
        m6a_radio = QRadioButton("6mA")
        m5c6a_radio = QRadioButton("5mC+6mA")
        column3_layout.addWidget(m5c_radio)
        column3_layout.addWidget(m6a_radio)
        column3_layout.addWidget(m5c6a_radio)

        molecules_layout.addLayout(column3_layout)

        main_layout.addLayout(molecules_layout)

        # Button groups for each column
        self.column1_group = QButtonGroup(self)
        self.column1_group.addButton(atcg_radio)

        self.column2_group = QButtonGroup(self)
        self.column2_group.addButton(pz_radio)
        self.column2_group.addButton(bs_radio)
        self.column2_group.addButton(pzbs_radio)

        self.column3_group = QButtonGroup(self)
        self.column3_group.addButton(m5c_radio)
        self.column3_group.addButton(m6a_radio)
        self.column3_group.addButton(m5c6a_radio)

        # Connect selection change to a method
        self.column1_group.buttonClicked.connect(self.update_selection)
        self.column2_group.buttonClicked.connect(self.update_selection)
        self.column3_group.buttonClicked.connect(self.update_selection)

        # Label to display selected options
        self.selection_label = QLabel("已选择的编码字母:  ")
        self.selection_label.setFont(QFont("Arial", 12))
        self.selection_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.selection_label)

        # Select encoding method
        encoding_method_label = QLabel("选择编码方法")
        encoding_method_label.setFont(QFont("Arial", 12))
        main_layout.addWidget(encoding_method_label)

        self.encoding_method_combobox = QComboBox()
        self.encoding_method_combobox.addItems(
            ["DNA Fountain", "YYC", "HybridCode", "HEDGES", "6-Huffman", "8-Huffman"])
        self.encoding_method_combobox.setFont(QFont("Arial", 12))
        self.encoding_method_combobox.setMinimumHeight(60)  # 设置最小高度为 40 像素
        main_layout.addWidget(self.encoding_method_combobox)

        # Run button
        encode_button = QPushButton("开始编码")
        encode_button.setFont(QFont("Arial", 12))
        encode_button.setFixedSize(140, 60)
        encode_button.setStyleSheet("color: white; background-color: #007BFF; border-radius: 10px;")
        encode_button.clicked.connect(self.launch_encoding_window)

        main_layout.addWidget(encode_button, alignment=Qt.AlignCenter)

        # Footer (底边栏)
        footer = QWidget()
        footer.setStyleSheet("background-color: black;")  # 设置背景为黑色
        footer.setFixedHeight(100)
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(10, 5, 10, 5)  # 设置内边距
        footer_label = QLabel(
            "本平台受国家重点研发计划”生物与信息融合专项“：”基于多类型生物分子的新一代超高密度信息存储技术研发“资助开发。\n"
                              "华中科技大学人工智能与自动化学院，图像信息处理与智能控制重点实验室，湖北，武汉，430074。\n"
                              "联系方式: zixiaozhang@hust.edu.cn, m202373753@hust.edu.cn"
        )
        footer_label.setAlignment(Qt.AlignCenter)
        footer_label.setFont(QFont("Arial", 10))
        footer_label.setStyleSheet("color: white;")  # 设置文字为白色
        footer_layout.addWidget(footer_label)
        footer.setLayout(footer_layout)

        # 将底边栏添加到主布局
        main_layout.addWidget(footer)

        self.setLayout(main_layout)

    def browse_file(self):
        """Opens a file dialog to select a file."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)")
        if file_path:
            self.file_path = file_path
            self.file_path_label.setText(f"Loaded file: {file_path}")
            with open(file_path, "rb") as f:
                self.file_data = f.read()

    def drag_enter_event(self, event):
        """Handles drag enter event to verify if the dragged item is a file."""
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def drop_event(self, event):
        """Handles drop event to load the dropped file."""
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            self.file_path = file_path
            self.file_path_label.setText(f"Loaded file: {file_path}")
            with open(file_path, "rb") as f:
                self.file_data = f.read()

    def update_selection(self):
        """Update the selection label when an option is selected."""
        column1_selection = self.get_checked_button_text(self.column1_group)
        column2_selection = self.get_checked_button_text(self.column2_group)
        column3_selection = self.get_checked_button_text(self.column3_group)

        selected_text = (
            f"Selected: {column1_selection}, {column2_selection}, {column3_selection}"
        )
        self.selection_label.setText(selected_text)

    @staticmethod
    def get_checked_button_text(button_group):
        """Get the text of the selected button in the button group."""
        checked_button = button_group.checkedButton()
        return checked_button.text() if checked_button else "None"

    def launch_encoding_window(self):
        """Launch EncodingWindow with the selected parameters."""
        if self.file_data is None:
            QMessageBox.warning(self, "Warning", "Please load a file before proceeding.")
            return

        encode_letter = self.encoding_letter_combobox.currentText()
        if not encode_letter:  # 检查是否有选择
            QMessageBox.warning(self, "Warning", "Please select an encoding letter.")
            return
            # 调试信息
        print(f"Launching EncodingWindow with file_data of size: {len(self.file_data)} bytes")
        print(f"Encoding letter: {encode_letter}")

        try:
            encoding_window = EncodingWindow(self.file_data, encode_letter, self)
            encoding_window.show()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to launch EncodingWindow: {e}")

class SimulateWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("模拟")
        self.resize(1600, 1200)

        self.file_path = None

        # Main layout
        main_layout = QVBoxLayout()

        load_label = QLabel("上传编码文件")
        load_label.setFont(QFont("Arial", 12))
        main_layout.addWidget(load_label)

        # Step 1: Load FASTA file
        self.file_path_label = QLabel("移动文件到此处或点击”浏览“来选择文件")
        self.file_path_label.setFont(QFont("Arial", 14))
        self.file_path_label.setStyleSheet(
            "border: 2px dashed #FF8C00; padding: 40px; color: #FF8C00; background-color: #F8F9FA;"
        )
        self.file_path_label.setAlignment(Qt.AlignCenter)
        self.file_path_label.setAcceptDrops(True)  # Enable drag-and-drop
        main_layout.addWidget(self.file_path_label)

        # Connect drag and drop events
        self.file_path_label.dragEnterEvent = self.drag_enter_event
        self.file_path_label.dropEvent = self.drop_event

        # Browse button
        browse_button = QPushButton("浏览")
        browse_button.setFont(QFont("Arial", 14))
        browse_button.setStyleSheet("background-color: #FF8C00; color: white; padding: 10px;")
        browse_button.clicked.connect(self.browse_file)
        main_layout.addWidget(browse_button)

        # Step 2: Select DNA storage simulation process
        simulation_label = QLabel("选择模拟存储流程")
        simulation_label.setFont(QFont("Arial", 14))
        main_layout.addWidget(simulation_label)

        self.process_comboboxes = {}
        processes = ["合成", "保存", "测序"]
        for process in processes:
            process_label = QLabel(f"{process} 技术")
            process_label.setFont(QFont("Arial", 14))
            main_layout.addWidget(process_label)

            combobox = QComboBox()
            combobox.addItems(self.get_methods_for_process(process))
            combobox.setFont(QFont("Arial", 12))
            combobox.setMinimumHeight(60)  # 设置最小高度
            main_layout.addWidget(combobox)

            self.process_comboboxes[process] = combobox

        # Step 3: Run simulation
        run_button = QPushButton("开始模拟")
        run_button.setFont(QFont("Arial", 12))
        run_button.setFixedSize(140, 60)
        run_button.setStyleSheet("color: white; background-color: #FF8C00; border-radius: 10px;")
        run_button.clicked.connect(self.run_simulation)
        main_layout.addWidget(run_button, alignment=Qt.AlignCenter)

        # Step 4: Display and download results
        result_label = QLabel("模拟结果")
        result_label.setFont(QFont("Arial", 12))
        main_layout.addWidget(result_label)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        main_layout.addWidget(self.result_text)

        download_button = QPushButton("下载模拟结果文件")
        download_button.setFont(QFont("Arial", 12))
        download_button.setFixedSize(220, 60)
        download_button.setStyleSheet("color: white; background-color: #FF8C00; border-radius: 10px;")
        download_button.clicked.connect(self.download_simulated_fasta)
        main_layout.addWidget(download_button, alignment=Qt.AlignCenter)

        # Placeholder for simulation results
        self.simulated_fasta = None

        self.setLayout(main_layout)

    def browse_file(self):
        """Opens a file dialog to select a file."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)")
        if file_path:
            self.file_path = file_path
            self.file_path_label.setText(f"Loaded file: {file_path}")

    def drag_enter_event(self, event):
        """Handles drag enter event to verify if the dragged item is a file."""
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def drop_event(self, event):
        """Handles drop event to load the dropped file."""
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            self.file_path = file_path
            self.file_path_label.setText(f"Loaded file: {file_path}")

    def get_methods_for_process(self, process):
        """Return a list of methods for a given process."""
        methods = {
            "合成": ["ErrASE", "HT-Electrochemical", "Inkjet", "None"],
            "保存": ["Cold Storage", "Room Temperature Storage", "None"],
            "测序": ["Nanopore", "Illumina", "PacBio", "None"]
        }
        return methods.get(process, [])

    def run_simulation(self):
        """Run the simulation based on the selected methods."""
        file_path = self.file_path_edit.text()
        if not file_path:
            QMessageBox.warning(self, "Warning", "Please load a FASTA file before running the simulation.")
            return

        try:
            selected_methods = {process: combobox.currentText() for process, combobox in
                                self.process_comboboxes.items()}
            # Example simulation logic
            self.simulated_fasta = f"Simulated results based on:\n{selected_methods}\n"
            self.simulated_fasta += f"Original file: {file_path}"
            self.result_text.setPlainText(self.simulated_fasta)
            QMessageBox.information(self, "Success", "Simulation completed successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Simulation failed: {e}")

    def download_simulated_fasta(self):
        """Save simulated FASTA results."""
        if not self.simulated_fasta:
            QMessageBox.warning(self, "Warning", "No simulation results to download.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Save Simulated FASTA", "", "FASTA Files (*.fasta)")
        if not file_path:
            return

        try:
            with open(file_path, "w") as fasta_file:
                fasta_file.write(self.simulated_fasta)
            QMessageBox.information(self, "Success", "Simulated FASTA file saved successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save file: {e}")

class DecodeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("解码")
        self.resize(1600, 1200)

        # Main layout
        main_layout = QVBoxLayout()

        # Step 1: Load DNA file
        load_label = QLabel("上传序列文件")
        load_label.setFont(QFont("Arial", 12))
        main_layout.addWidget(load_label)

        # Upload file section
        self.file_path_label = QLabel("拖动文件到此处或点击“浏览”来选择文件")
        self.file_path_label.setFont(QFont("Arial", 14))
        self.file_path_label.setStyleSheet(
            "border: 2px dashed #20B2AA; padding: 40px; color: #20B2AA; background-color: #F8F9FA;"
        )
        self.file_path_label.setAlignment(Qt.AlignCenter)
        self.file_path_label.setAcceptDrops(True)  # Enable drag-and-drop
        main_layout.addWidget(self.file_path_label)

        # Connect drag and drop events
        self.file_path_label.dragEnterEvent = self.drag_enter_event
        self.file_path_label.dropEvent = self.drop_event

        # Browse button
        browse_button = QPushButton("浏览")
        browse_button.setFont(QFont("Arial", 14))
        browse_button.setStyleSheet("background-color: #20B2AA; color: white; padding: 10px;")
        browse_button.clicked.connect(self.browse_file)
        main_layout.addWidget(browse_button)

        # Drag and drop functionality
        self.setAcceptDrops(True)

        # Step 2: Select encoding letter
        encoding_letter_label = QLabel("选择序列文件的编码字母")
        encoding_letter_label.setFont(QFont("Arial", 14))
        main_layout.addWidget(encoding_letter_label)

        self.encoding_letter_combobox = QComboBox()
        self.encoding_letter_combobox.addItems(["A, T, C, G", "ATCGPZ", "ATCGBS", "A,T,C,G,P,Z,B,S", "A,T,C,G,5mC,6mA"])  # Example encoding letters
        self.encoding_letter_combobox.setFont(QFont("Arial", 12))
        self.encoding_letter_combobox.setMinimumHeight(60)  # 设置最小高度
        main_layout.addWidget(self.encoding_letter_combobox)

        # Step 3: Select encoding method
        encoding_method_label = QLabel("选择序列文件的编码方法")
        encoding_method_label.setFont(QFont("Arial", 14))
        main_layout.addWidget(encoding_method_label)

        self.encoding_method_combobox = QComboBox()
        self.encoding_method_combobox.addItems(["DNA Fountain", "YYC", "HybridCode", "6-Huffman", "8-Huffman"])
        self.encoding_method_combobox.setFont(QFont("Arial", 12))
        self.encoding_method_combobox.setMinimumHeight(60)  # 设置最小高度
        main_layout.addWidget(self.encoding_method_combobox)

        # Step 4: Start decoding
        decode_button = QPushButton("开始解码")
        decode_button.setFont(QFont("Arial", 12))
        decode_button.setFixedSize(140, 60)
        decode_button.setStyleSheet("color: white; background-color: #20B2AA; border-radius: 10px;")
        decode_button.clicked.connect(self.start_decoding)
        main_layout.addWidget(decode_button, alignment=Qt.AlignCenter)

        '''# Step 5: Results display
        results_label = QLabel("解码结果")
        results_label.setFont(QFont("Arial", 12))
        main_layout.addWidget(results_label)

        self.data_recovery_rate_label = QLabel("数据恢复率: N/A")
        self.data_recovery_rate_label.setFont(QFont("Arial", 10))
        main_layout.addWidget(self.data_recovery_rate_label)

        self.base_error_rate_label = QLabel("Base Error Rate: N/A")
        self.base_error_rate_label.setFont(QFont("Arial", 10))
        main_layout.addWidget(self.base_error_rate_label)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        main_layout.addWidget(self.result_text)'''

        # Placeholder for visualization
        visualization_label = QLabel("解码结果可视化分析")
        visualization_label.setFont(QFont("Arial", 12))
        main_layout.addWidget(visualization_label)

        self.visualization_widget = QTextEdit()  # Replace with an actual visualization widget if available
        self.visualization_widget.setReadOnly(True)
        main_layout.addWidget(self.visualization_widget)

        # Placeholder for decoding results
        self.decoded_file_content = None

        # Step 6: Download decoded file
        download_button = QPushButton("下载解码文件")
        download_button.setFont(QFont("Arial", 12))
        download_button.setFixedSize(220, 60)
        download_button.setStyleSheet("color: white; background-color: #20B2AA; border-radius: 10px;")
        download_button.clicked.connect(self.download_decoded_file)
        main_layout.addWidget(download_button, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)

    def browse_file(self):
        """Opens a file dialog to select a file."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)")
        if file_path:
            self.file_path = file_path
            self.file_path_label.setText(f"Loaded file: {file_path}")

    def drag_enter_event(self, event):
        """Handles drag enter event to verify if the dragged item is a file."""
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def drop_event(self, event):
        """Handles drop event to load the dropped file."""
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            self.file_path = file_path
            self.file_path_label.setText(f"Loaded file: {file_path}")

    def start_decoding(self):
        """Start the decoding process."""
        file_path = self.file_path_edit.text()
        if not file_path:
            QMessageBox.warning(self, "Warning", "Please load a DNA file before starting the decoding.")
            return

        try:
            # Retrieve selected encoding parameters
            encode_letter = self.encoding_letter_combobox.currentText()
            encode_method = self.encoding_method_combobox.currentText()

            # Example decoding logic (replace with actual implementation)
            self.decoded_file_content = f"Decoding completed with:\nEncoding Letter: {encode_letter}\nEncoding Method: {encode_method}\n"
            self.decoded_file_content += f"Loaded file: {file_path}\nDecoded content here..."

            # Update results
            self.result_text.setPlainText(self.decoded_file_content)
            self.data_recovery_rate_label.setText("Data Recovery Rate: 95%")  # Example value
            self.base_error_rate_label.setText("Base Error Rate: 2%")  # Example value

            # Example visualization (replace with actual graph or chart)
            self.visualization_widget.setPlainText("Visualization placeholder. Replace with an actual chart.")

            QMessageBox.information(self, "Success", "Decoding completed successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Decoding failed: {e}")

    def download_decoded_file(self):
        """Save the decoded file."""
        if not self.decoded_file_content:
            QMessageBox.warning(self, "Warning", "No decoded file to download.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Save Decoded File", "", "Text Files (*.txt);;All Files (*)")
        if not file_path:
            return

        try:
            with open(file_path, "w") as file:
                file.write(self.decoded_file_content)
            QMessageBox.information(self, "Success", "Decoded file saved successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save file: {e}")

class TutorialWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("帮助")
        self.resize(1600, 1200)

        # Main layout
        main_layout = QVBoxLayout()

        # Top Navigation Bar
        nav_bar = QWidget()
        nav_bar.setStyleSheet("background-color: #130066;")
        nav_bar.setFixedHeight(100)

        nav_layout = QHBoxLayout()
        nav_layout.setContentsMargins(10, 10, 10, 10)
        nav_layout.setSpacing(20)  # 设置栏目之间的间距

        # Navigation buttons
        name_label = QLabel("MMDNA")
        # MBio-Storage
        name_label.setFont(QFont("Arial", 22, QFont.Bold))
        name_label.setStyleSheet("color: orange;")
        nav_layout.addWidget(name_label)

        # Navigation items (uniform size with hover effect)
        nav_items = [
            {"text": "主页", "action": None},  # Home 目前无点击事件
            {"text": "编码", "action": self.open_encode_window},  # Encode 打开新窗口
            {"text": "模拟", "action": self.open_simulate_window},  # Simulate
            {"text": "解码", "action": self.open_decode_window},  # Decode 打开新窗口
            {"text": "帮助", "action": self.open_tutorial_window},  # Tutorial
        ]

        for item in nav_items:
            button = QPushButton(item["text"])
            button.setFont(QFont("Arial", 18))
            button.setCursor(Qt.PointingHandCursor)  # 鼠标悬停时显示手型
            button.setStyleSheet(
                """
                QPushButton {
                    color: white; 
                    background-color: #130066; 
                    border: none;
                }
                QPushButton:hover {
                    background-color: #4C0099;  /* 鼠标悬停时背景变浅蓝 */
                }
                """
            )
            if item["action"]:
                button.clicked.connect(item["action"])  # 连接对应槽函数
            nav_layout.addWidget(button)

        nav_bar.setLayout(nav_layout)
        main_layout.addWidget(nav_bar)

        # Introduction Section
        introduction_layout = QVBoxLayout()
        introduction_layout.setContentsMargins(50, 20, 50, 0)  # 设置左右间距

        # Scrollable Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(50, 20, 50, 20)

        # Title1
        title_label = QLabel("多类型生物分子信息存储编解码平台介绍\n")
        title_label.setFont(QFont("Arial", 26, QFont.Bold))
        title_label.setStyleSheet("color: black;")
        scroll_layout.addWidget(title_label, alignment=Qt.AlignCenter)
        scroll_content.setLayout(scroll_layout)

        # Description Text
        description_label = QLabel(
            "      多类型生物分子信息存储编解码平台是面向多类型生物分子信息存储研究开发的全流程一体化平台，由编码、模拟和解码等主要模块组成。"
            "本平台提供了多样化的编码方案设计，用户可以根据需求选择多种生物分子的组合来设计编码字母表。"
            "以下部分将详细介绍本平台的使用方法，来帮助用户快速入手进行多类型生物分子信息存储的研究。"
            "此外，我们还介绍了功能模块中所用到的主要方法和相关技术，并在结尾提供了对应的参考文献。\n"
        )
        description_label.setFont(QFont("Arial", 14))
        description_label.setAlignment(Qt.AlignLeft)
        description_label.setWordWrap(True)
        scroll_layout.addWidget(description_label)

        encode_titile = QLabel("一、编码\n")
        encode_titile.setFont(QFont("Arial", 14, QFont.Bold))
        encode_titile.setStyleSheet("color: black;")
        scroll_layout.addWidget(encode_titile)

        encode_description = QLabel(
            "编码模块数据加载、编码字母表构建、编码方法选择、运行编码、及结果下载。\n"
            "1.首先通过拖动或浏览本地文件来选择需要编码的数据文件，从而加载到平台中；\n"
            "2. 分别从天然碱基、非天然碱基、修饰碱基中选择所需的编码字母来构建编码字母表；\n"
            "3. 再从编码方法列表中选择合适的编码方法，本平台提供了DNA Fountain、DNA-Aeon、HEDGES、DNA-Aeon、HybridCode、6-Huffman、8-Huffman等多种优秀的编码算法，用户可以根据编码字母表和编码需求来选择对应的编码算法；\n"
            "4. 点击“开始编码”，后台根据所选编码字母和编码算法将输入的数据文件编码为分子序列；\n"
            "5. 点击“开始下载”，可以将编码得到的生物分子序列文件下载到本地，用于模拟和解码模块。\n"
        )
        encode_description.setFont(QFont("Arial", 14))
        encode_description.setAlignment(Qt.AlignLeft)
        encode_description.setWordWrap(True)
        scroll_layout.addWidget(encode_description)

        simulate_titile = QLabel("二、模拟\n")
        simulate_titile.setFont(QFont("Arial", 14, QFont.Bold))
        simulate_titile.setStyleSheet("color: black;")
        scroll_layout.addWidget(simulate_titile)

        simulate_description = QLabel(
            "模拟模块分别包括：加载序列文件、存储流程及对应技术选择、模拟结果、及结果下载。\n"
            "1. 首先通过拖动或浏览本地文件来选择编码得到的序列文件，从而加载到平台中；\n"
            "2. 选择信息存储模拟流程，分别包括合成技术、保存技术、测序技术，每个流程都包含了多种该流程可用的技术。此外，每个流程中还提供了忽略选项，用户可以根据需求来选择一种或多种存储流程；\n"
            "3. 点击“开始模拟”，后台根据所选存储流程和相应技术来构建错误模型，为输入的序列文件引入错误，模拟分子信息存储过程的真实情况；\n"
            "4. 点击“开始下载”，可以将模拟得到的生物分子序列文件下载到本地，用于解码模块以及错误分析。\n"

        )
        simulate_description.setFont(QFont("Arial", 14))
        simulate_description.setAlignment(Qt.AlignLeft)
        simulate_description.setWordWrap(True)
        scroll_layout.addWidget(simulate_description)

        decode_titile = QLabel("三、解码\n")
        decode_titile.setFont(QFont("Arial", 14, QFont.Bold))
        decode_titile.setStyleSheet("color: black;")
        scroll_layout.addWidget(decode_titile)

        decode_description = QLabel(
            "解码模块分别包括：加载序列文件、编码字母和编码方法选择、序列解码、及结果下载。\n"
            "1. 首先通过拖动或浏览本地文件来选择需要解码的序列文件，从而加载到平台中；\n"
            "2. 选择该序列文件所用的编码字母和编码方法；"
            "3. 点击“开始解码”，后台根据所选编码字母和编码方法将序列文件中生物分子解码为数据，并恢复为原始文件；\n"
            "4. 点击“开始下载”，将解码得到的数据文件下载本地，可以用于比对分析DNA存储前后文件的变化。\n"

        )
        decode_description.setFont(QFont("Arial", 14))
        decode_description.setAlignment(Qt.AlignLeft)
        decode_description.setWordWrap(True)
        scroll_layout.addWidget(decode_description)

        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

        # Footer (底边栏)
        footer = QWidget()
        footer.setStyleSheet("background-color: black;")  # 设置背景为黑色
        footer.setFixedHeight(100)
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(10, 0, 10, 0)  # 设置内边距
        footer_label = QLabel("本平台受国家重点研发计划”生物与信息融合专项“：”基于多类型生物分子的新一代超高密度信息存储技术研发“资助开发。\n"
                              "华中科技大学人工智能与自动化学院，图像信息处理与智能控制重点实验室，湖北，武汉，430074。\n"
                              "联系方式: zixiaozhang@hust.edu.cn, m202373753@hust.edu.cn")
        footer_label.setAlignment(Qt.AlignCenter)
        footer_label.setFont(QFont("Arial", 11))
        footer_label.setStyleSheet("color: white;")  # 设置文字为白色
        footer_layout.addWidget(footer_label)
        footer.setLayout(footer_layout)

        # 将底边栏添加到主布局
        main_layout.addWidget(footer)

        self.setLayout(main_layout)

    def open_encode_window(self):
        """打开编码界面"""
        self.encode_window = EncodeWindow()
        self.encode_window.show()

    def open_simulate_window(self):
        """打开模拟界面"""
        self.simulate_window = SimulateWindow()
        self.simulate_window.show()

    def open_decode_window(self):
        """打开解码界面"""
        self.decode_window = DecodeWindow()
        self.decode_window.show()

    def open_tutorial_window(self):
        """打开介绍界面"""
        self.tutorial_window = TutorialWindow()
        self.tutorial_window.show()

class MBioStorageApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("多类型生物分子信息存储编解码平台")
        self.resize(1600, 1200)

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main layout
        main_layout = QVBoxLayout()

        # Top Navigation Bar
        nav_bar = QWidget()
        nav_bar.setStyleSheet("background-color: #130066;")
        nav_bar.setFixedHeight(100)

        nav_layout = QHBoxLayout()
        nav_layout.setContentsMargins(10, 10, 10, 10)
        nav_layout.setSpacing(20)  # 设置栏目之间的间距

        # Navigation buttons
        name_label = QLabel("MMDNA")
        #MBio-Storage
        name_label.setFont(QFont("Arial", 22, QFont.Bold))
        name_label.setStyleSheet("color: orange;")
        nav_layout.addWidget(name_label)

        # Navigation items (uniform size with hover effect)
        nav_items = [
            {"text": "主页", "action": None},  # Home 目前无点击事件
            {"text": "编码", "action": self.open_encode_window},  # Encode 打开新窗口
            {"text": "模拟", "action": self.open_simulate_window},  # Simulate
            {"text": "解码", "action": self.open_decode_window},  # Decode 打开新窗口
            {"text": "帮助", "action": self.open_tutorial_window},  # Tutorial
        ]

        for item in nav_items:
            button = QPushButton(item["text"])
            button.setFont(QFont("Arial", 18))
            button.setCursor(Qt.PointingHandCursor)  # 鼠标悬停时显示手型
            button.setStyleSheet(
                """
                QPushButton {
                    color: white; 
                    background-color: #130066; 
                    border: none;
                }
                QPushButton:hover {
                    background-color: #4C0099;  /* 鼠标悬停时背景变浅蓝 */
                }
                """
            )
            if item["action"]:
                button.clicked.connect(item["action"])  # 连接对应槽函数
            nav_layout.addWidget(button)

        nav_bar.setLayout(nav_layout)
        main_layout.addWidget(nav_bar)

        # Content Section
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(50, 20, 50, 0)  # 设置左右间距

        #Title
        title_label = QLabel("欢迎使用多类型生物分子信息存储编解码平台\n")
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: black;")  # 设置字体颜色为蓝色
        content_layout.addWidget(title_label)

        # Description Text
        description_label = QLabel(
            "       本平台是面向多类型生物分子信息存储研究开发的编解码一体化平台，实现了将数据信息编码与生物分子序列之间的编码和纠错解码，并提供了生物分子存储全流程的模拟。"
            "本平台主要由编码、模拟和解码三个模块组成。在编码模块中，我们提供了天然核酸、非天然核酸以及修饰碱基等多种类型的生物分子作为编码字母，用户可以根据研究需求来选择多种不同的碱基来构建编码字母表。"
            "并且，我们针对不同的编码字母组合提供了对应的多种编码方法，实现了多样化的多类型生物分子信息存储。"
            "本平台提供了较为完整的生物分子存储过程的模拟，包括：合成、存储、PCR扩增、测序等，可以通过选择特定环节来更精准的研究多类型生物分子的存储过程。"
        )
        description_label.setFont(QFont("Arial", 12))
        description_label.setAlignment(Qt.AlignLeft)
        description_label.setWordWrap(True)
        content_layout.addWidget(description_label)

        # Placeholder for "流程介绍图"
        flowchart_label = QLabel(self)
        flowchart_label.setAlignment(Qt.AlignCenter)  # Center the image
        pixmap = QPixmap("Figure1.png")  # Load the image
        if not pixmap.isNull():
            # Scale the image to 60% of the window width
            scaled_width = int(self.width() * 0.6)
            scaled_pixmap = pixmap.scaled(
                scaled_width, pixmap.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            flowchart_label.setPixmap(scaled_pixmap)
        else:
            flowchart_label.setText("流程图加载失败")  # Error message if image not found
            flowchart_label.setAlignment(Qt.AlignCenter)

        content_layout.addWidget(flowchart_label, alignment=Qt.AlignCenter)

        # Getting Start Button
        start_button = QPushButton("开始")
        start_button.setFont(QFont("Arial", 16))
        start_button.setFixedSize(200, 60)
        start_button.setStyleSheet("color: white; background-color: #9933CC; border-radius: 10px;")
        start_button.clicked.connect(self.open_encode_window)  # 按钮点击事件
        content_layout.addWidget(start_button, alignment=Qt.AlignCenter)

        main_layout.addLayout(content_layout)

        # Footer (底边栏)
        footer = QWidget()
        footer.setStyleSheet("background-color: black;")  # 设置背景为黑色
        footer.setFixedHeight(100)
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(10, 0, 10, 0)  # 设置内边距
        footer_label = QLabel("本平台受国家重点研发计划”生物与信息融合专项“：”基于多类型生物分子的新一代超高密度信息存储技术研发“资助开发。\n"
                              "华中科技大学人工智能与自动化学院，图像信息处理与智能控制重点实验室，湖北，武汉，430074。\n"
                              "联系方式: zixiaozhang@hust.edu.cn, m202373753@hust.edu.cn")
        footer_label.setAlignment(Qt.AlignCenter)
        footer_label.setFont(QFont("Arial", 11))
        footer_label.setStyleSheet("color: white;")  # 设置文字为白色
        footer_layout.addWidget(footer_label)
        footer.setLayout(footer_layout)

        # 将底边栏添加到主布局
        main_layout.addWidget(footer)

        # Set the main layout
        self.central_widget.setLayout(main_layout)

    def open_encode_window(self):
        """打开编码界面"""
        self.encode_window = EncodeWindow()
        self.encode_window.show()

    def open_simulate_window(self):
        """打开模拟界面"""
        self.simulate_window = SimulateWindow()
        self.simulate_window.show()

    def open_decode_window(self):
        """打开解码界面"""
        self.decode_window = DecodeWindow()
        self.decode_window.show()

    def open_tutorial_window(self):
        """打开介绍界面"""
        self.tutorial_window = TutorialWindow()
        self.tutorial_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MBioStorageApp()
    main_window.show()
    sys.exit(app.exec_())
