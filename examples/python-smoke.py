"""Real Google SDK readback against the SDK environment exported by the action."""
import os
import uuid
from google.cloud import storage, pubsub_v1, bigquery
from google.api_core.client_options import ClientOptions
from google.auth.credentials import AnonymousCredentials

project = os.environ['GOOGLE_CLOUD_PROJECT']
suffix = uuid.uuid4().hex[:12]
payload = b'LocalCloud GitHub Marketplace qualification'

gcs = storage.Client(project=project)
bucket = gcs.create_bucket(f'ci-{suffix}')
blob = bucket.blob('qualification.txt')
blob.upload_from_string(payload)
assert blob.download_as_bytes() == payload
blob.delete()
bucket.delete()
print('Cloud Storage: upload, readback and cleanup passed')

publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()
topic = publisher.topic_path(project, f'ci-{suffix}')
subscription = subscriber.subscription_path(project, f'ci-{suffix}')
publisher.create_topic(request={'name': topic})
subscriber.create_subscription(request={'name': subscription, 'topic': topic})
publisher.publish(topic, payload).result(timeout=20)
messages = subscriber.pull(request={'subscription': subscription, 'max_messages': 1}, timeout=20).received_messages
assert len(messages) == 1 and messages[0].message.data == payload
subscriber.acknowledge(request={'subscription': subscription, 'ack_ids': [messages[0].ack_id]}, timeout=20)
subscriber.delete_subscription(request={'subscription': subscription})
publisher.delete_topic(request={'topic': topic})
subscriber.close()
publisher.stop()
print('Pub/Sub: publish, pull, acknowledgement and cleanup passed')

# BigQuery's SDK requires an explicit local endpoint and anonymous credentials.
bq = bigquery.Client(
    project=project,
    credentials=AnonymousCredentials(),
    client_options=ClientOptions(api_endpoint=os.environ['BIGQUERY_EMULATOR_HOST']),
)
rows = list(bq.query('SELECT 1 AS ok', timeout=20).result(timeout=20))
assert rows[0].ok == 1
dataset = f'{project}.ci_{suffix}'
bq.create_dataset(bigquery.Dataset(dataset), timeout=20)
table = bq.create_table(
    bigquery.Table(f'{dataset}.messages', schema=[bigquery.SchemaField('message', 'STRING')]),
    timeout=20,
)
assert not bq.insert_rows_json(table, [{'message': payload.decode()}], timeout=20)
rows = list(bq.query(f'SELECT message FROM `{project}.ci_{suffix}.messages`', timeout=20).result(timeout=20))
assert [row.message for row in rows] == [payload.decode()]
bq.delete_dataset(dataset, delete_contents=True, timeout=20)
bq.close()
print('BigQuery: dataset/table creation, row insertion, SQL readback and cleanup passed')
