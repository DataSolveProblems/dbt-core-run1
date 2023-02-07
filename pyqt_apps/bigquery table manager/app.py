import os
import sys
from gbq import BQuery
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTabWidget, QComboBox, QListWidget,
							 QHBoxLayout, QVBoxLayout, QFormLayout, QStatusBar, QAbstractItemView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

class AppWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.window_width, self.window_height = 700, 500
		self.setMinimumSize(self.window_width, self.window_height)
		self.setWindowTitle('BigQuery Table Manager by Jie v1')
		self.setWindowIcon(QIcon('bigquery.png'))
		self.setStyleSheet('''
			QWidget {
				font-size: 16px;
			}
		''')

		self.layout = {}
		self.layout['main'] = QVBoxLayout()
		self.setLayout(self.layout['main'])

		self.init_ui()
		self.init_default_values()
		self.init_configure_signals()

	def init_ui(self):
		self.layout['layout'] = QFormLayout()
		self.layout['main'].addLayout(self.layout['layout'])

		self.combo_project = QComboBox()
		self.layout['layout'].addRow(QLabel('Project:'), self.combo_project)

		self.combo_dataset = QComboBox()		
		self.layout['layout'].addRow(QLabel('Dataset:'), self.combo_dataset)

		self.list_table = QListWidget()
		self.list_table.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
		self.layout['layout'].addRow(QLabel('Table:'), self.list_table)

		self.button_delete = QPushButton('&Delete', clicked=self.delete_tables)
		self.button_reset = QPushButton('R&eset', clicked=self.list_table.clearSelection)
		self.button_refresh = QPushButton('&Refresh', clicked=self.update_table_list)
		self.layout['buttons'] = QHBoxLayout()
		self.layout['buttons'].addWidget(self.button_delete)
		self.layout['buttons'].addWidget(self.button_reset)
		self.layout['buttons'].addWidget(self.button_refresh)
		self.layout['layout'].addRow(QLabel(''), self.layout['buttons'])

		self.status_bar = QStatusBar()
		self.status_bar.showMessage('Online')
		self.layout['main'].addWidget(self.status_bar)

	def init_default_values(self):
		self.combo_project.addItems(['sql-for-bigquery', 'dbt-tutorial', 'bigquery-public-data'])

		tables = bquery.list_dataset()
		self.combo_dataset.addItems(tables)

		self.update_table_list()

	def init_configure_signals(self):
		self.combo_dataset.currentIndexChanged.connect(self.update_table_list)

	def update_table_list(self):
		self.list_table.clear()
		selected_dataset = self.combo_dataset.currentText()		

		tables = bquery.list_tables(selected_dataset)
		self.list_table.addItems('{0} ({1})'.format(table[0], table[1]) for table in tables)

	def delete_tables(self):
		items = self.list_table.selectedItems()
		dataset_id = self.combo_dataset.currentText()
		if items:
			for item in items:
				table_id = item.text()[:item.text().find('(')-1]
				bquery.delete_table('{0}.{1}'.format(dataset_id, table_id))
		self.update_table_list()
		self.status_bar.showMessage('Deleted')


if __name__ == "__main__":
	os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'H:\PythonVenv\dbt-core-project-demo\reddit_playground\sql_for_bigquery_service_account.json'
	bquery = BQuery()

	app = QApplication(sys.argv)

	w = AppWindow()
	w.show()
	sys.exit(app.exec())
