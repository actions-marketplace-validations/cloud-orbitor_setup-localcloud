"""Real Google SDK readback against the SDK environment exported by the action."""
import os
import uuid
from google.cloud import storage, pubsub_v1, firestore

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

db = firestore.Client(project=project)
document = db.collection('qualification').document(suffix)
document.set({'message': payload.decode()})
assert document.get().to_dict()['message'] == payload.decode()
document.delete()
db.close()
print('Firestore: write, readback and cleanup passed')
