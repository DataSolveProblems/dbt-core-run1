import os
from google.cloud import bigquery

class BQuery:
	def __init__(self):
		self.client = bigquery.Client(project='sql-for-bigquery')

	def list_dataset(self):
		datasets = self.client.list_datasets()
		return [dataset.dataset_id for dataset in datasets]

	def list_tables(self, dataset_id):
		tables = self.client.list_tables(dataset_id)
		return [(table.table_id, table.table_type) for table in tables]

	def delete_table(self, table_id):
		self.client.delete_table(table_id, not_found_ok=True)
		

if __name__ == '__main__':
	os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service_account_pyqt_manager.json'	
	bquery = BQuery()
	tables = bquery.client.list_tables('JJ')
	for table in tables:
		# print(dir(table))
		print(table.table_type)

