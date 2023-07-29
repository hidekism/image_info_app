import os
import sys
import json
import concurrent.futures
from pathlib import Path

from PyQt5.QtCore import Qt, QEvent, QFile, QStandardPaths
from PyQt5.QtGui import QClipboard, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.uic import loadUi

from PIL import Image

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', str(Path(__file__).absolute().parent))
    return str(Path(base_path).joinpath(relative_path))

class ImageInfoApp(QMainWindow):
    def __init__(self):
        super(ImageInfoApp, self).__init__()
        loadUi(resource_path('gui.ui'), self)

        # スタイルシートとアイコンの読み込み
        self.load_style_sheet()
        self.setWindowIcon(QIcon(resource_path('usagi.png')))

        # 初期値を設定する
        filename_custom_text = "src=\"{{filename}}\""
        width_custom_text = "width=\"{{width}}\""
        height_custom_text = "height=\"{{height}}\""
        all_custom_text = "<img src=\"{{filename}}\" width=\"{{width}}\" height=\"{{height}}\" alt=\"\" loading=\"lazy\" >"

        self.filename_custom.setPlainText(filename_custom_text)
        self.width_custom.setPlainText(width_custom_text)
        self.height_custom.setPlainText(height_custom_text)
        self.all_custom.setPlainText(all_custom_text)
        self.custom_texts = {
            "filename": filename_custom_text,
            "width": width_custom_text,
            "height": height_custom_text,
            "all": all_custom_text
        }

        self.browseButton.clicked.connect(self.select_directory)
        self.table.cellClicked.connect(self.cell_clicked)


        self.filename_custom.textChanged.connect(self.update_filename_custom_text)
        self.width_custom.textChanged.connect(self.update_width_custom_text)
        self.height_custom.textChanged.connect(self.update_height_custom_text)
        self.all_custom.textChanged.connect(self.update_all_custom_text)

        self.table.viewport().installEventFilter(self)

        self.directory_info = []
        self.load_directory_info_from_file()


    def load_style_sheet(self):
        style_file = QFile(resource_path('style.qss'))
        if style_file.open(QFile.ReadOnly | QFile.Text):
            self.setStyleSheet(str(style_file.readAll(), encoding='utf-8'))
            style_file.close()

    def load_directory(self, directory_path):
        self.directory_info.clear()
        self.directory_info.append(directory_path)
        self.save_directory_info_to_file()

    def get_app_data_dir(self):
        data_dir = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
        os.makedirs(data_dir, exist_ok=True)  # ディレクトリが存在しない場合は作成する
        file_path = os.path.join(data_dir, 'directory_info.json')
        return file_path

    def save_directory_info_to_file(self):
        file_path = self.get_app_data_dir()

        with open(file_path, 'w') as file:
            json.dump(self.directory_info, file)

    def load_directory_info_from_file(self):
        file_path = self.get_app_data_dir()

        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                self.directory_info = json.load(file)
                self.load_directory(self.directory_info[0])
                self.lineEdit.setText(self.directory_info[0])
                self.populate_table(self.directory_info[0])

    def eventFilter(self, source, event):
        if source is self.table.viewport() and event.type() == QEvent.MouseMove:
            pos = event.pos()
            index = self.table.indexAt(pos)
            if index.isValid():
                row = index.row()
                column = index.column()
                cell_text = self.get_replaced_text(row, column)
                self.statusBar.showMessage(cell_text)

        if source is self.table.viewport() and event.type() == QEvent.Leave:
            # マウスがテーブルから出た場合はステータスバーをクリア
            self.statusBar.clearMessage()

        return super(ImageInfoApp, self).eventFilter(source, event)

    def select_directory(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        directory_path = QFileDialog.getExistingDirectory(self, "Select Directory", options=options)
        if directory_path:
            self.lineEdit.setText(directory_path)
            self.populate_table(directory_path)
            self.load_directory(directory_path)
            self.save_directory_info_to_file()

    def populate_table(self, directory_path):
        self.table.clearContents()
        image_files = self.get_image_files(directory_path)
        self.table.setRowCount(len(image_files))

        for row, image_file in enumerate(image_files):
            filename, width, height = image_file
            self.table.setItem(row, 0, QTableWidgetItem(filename))
            self.table.setItem(row, 1, QTableWidgetItem(str(width)))
            self.table.setItem(row, 2, QTableWidgetItem(str(height)))
            self.table.setItem(row, 3, QTableWidgetItem("コピーする"))

    def get_svg_size(self, svg_content):
        renderer = QSvgRenderer()
        renderer.load(svg_content.encode('utf-8'))
        return renderer.defaultSize().width(), renderer.defaultSize().height()

    def get_image_files(self, directory_path):
        image_files = []
        valid_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp', '.svg']  # SVGを追加

        def process_image_file(file_path):
            try:
                if file_path.lower().endswith('.svg'):
                    # エンコーディングを指定してファイルを開く
                    with open(file_path, 'r', encoding='utf-8') as svg_file:
                        width, height = self.get_svg_size(svg_file.read())
                else:
                    img = Image.open(file_path)
                    width, height = img.size
                    img.close()
                return width, height
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                return None

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_path = {executor.submit(process_image_file, str(Path(directory_path, filename))): filename for filename in os.listdir(directory_path)}

            for future in concurrent.futures.as_completed(future_to_path):
                filename = future_to_path[future]
                try:
                    result = future.result()
                    if result:
                        image_files.append((filename, result[0], result[1]))
                except Exception as e:
                    print(f"Error processing {filename}: {e}")

        return sorted(image_files, key=lambda x: x[0].lower())

    def get_replaced_text(self, row, column):
        item = self.table.item(row, column)
        if item is not None:
            if column == 3:  # Clicked on the "一括" column
                filename = self.table.item(row, 0).text()
                width = self.table.item(row, 1).text()
                height = self.table.item(row, 2).text()
                custom_text = self.custom_texts["all"].replace("{{filename}}", filename)
                custom_text = custom_text.replace("{{width}}", width)
                custom_text = custom_text.replace("{{height}}", height)
            else:
                if column == 0 and "{{filename}}" in self.custom_texts["filename"]:
                    custom_text = self.custom_texts["filename"].replace("{{filename}}", item.text())
                elif column == 1 and "{{width}}" in self.custom_texts["width"]:
                    custom_text = self.custom_texts["width"].replace("{{width}}", item.text())
                elif column == 2 and "{{height}}" in self.custom_texts["height"]:
                    custom_text = self.custom_texts["height"].replace("{{height}}", item.text())
                else:
                    custom_text = item.text()
        return custom_text

    def cell_clicked(self, row, column):
        item = self.table.item(row, column)
        if item is not None:
            clipboard = QApplication.clipboard()
            if column == 3:  # Clicked on the "一括" column
                filename = self.table.item(row, 0).text()
                width = self.table.item(row, 1).text()
                height = self.table.item(row, 2).text()
                custom_text = self.custom_texts["all"].replace("{{filename}}", filename)
                custom_text = custom_text.replace("{{width}}", width)
                custom_text = custom_text.replace("{{height}}", height)
                clipboard.setText(custom_text, QClipboard.Clipboard)
            else:
                if column == 0 and "{{filename}}" in self.custom_texts["filename"]:
                    custom_text = self.custom_texts["filename"].replace("{{filename}}", item.text())
                elif column == 1 and "{{width}}" in self.custom_texts["width"]:
                    custom_text = self.custom_texts["width"].replace("{{width}}", item.text())
                elif column == 2 and "{{height}}" in self.custom_texts["height"]:
                    custom_text = self.custom_texts["height"].replace("{{height}}", item.text())
                else:
                    custom_text = item.text()
                clipboard.setText(custom_text, QClipboard.Clipboard)

    def update_filename_custom_text(self):
        self.custom_texts["filename"] = self.filename_custom.toPlainText()

    def update_width_custom_text(self):
        self.custom_texts["width"] = self.width_custom.toPlainText()

    def update_height_custom_text(self):
        self.custom_texts["height"] = self.height_custom.toPlainText()

    def update_all_custom_text(self):
        self.custom_texts["all"] = self.all_custom.toPlainText()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F5:
            # F5キーが押された場合は一覧を更新する処理を実行
            self.load_directory(self.directory_info[0])
            self.lineEdit.setText(self.directory_info[0])
            self.populate_table(self.directory_info[0])
        elif event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_R:
            # Ctrl+Rが押された場合も一覧を更新する処理を実行
            self.load_directory(self.directory_info[0])
            self.lineEdit.setText(self.directory_info[0])
            self.populate_table(self.directory_info[0])
        else:
            super(ImageInfoApp, self).keyPressEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageInfoApp()
    window.setWindowTitle("Image Info App")
    window.show()
    sys.exit(app.exec_())
