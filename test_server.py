import sys
sys.path.insert(0, '.')
from server import app
import json

with app.test_client() as client:
    # Test health
    r1 = client.get('/health')
    print("Health:", r1.status_code, r1.data.decode())

    # Test abuse
    r2 = client.post('/abuse',
        data=json.dumps({'text': 'You are imagining things. You will regret this.'}),
        content_type='application/json'
    )
    print("Abuse:", r2.status_code, r2.data.decode())

    # Test quick
    r3 = client.post('/quick',
        data=json.dumps({'text': 'You are imagining things.'}),
        content_type='application/json'
    )
    print("Quick:", r3.status_code, r3.data.decode())