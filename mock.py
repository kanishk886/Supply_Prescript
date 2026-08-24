import requests

print('Clearing dataset...')
requests.delete('http://localhost:8000/api/dataset/clear')

print('Uploading dataset...')
with open('supply_chain_sample.csv', 'rb') as f:
    res = requests.post('http://localhost:8000/api/dataset/upload', files={'file': f})
    print(res.json())

print('Simulating predictions...')
res = requests.post('http://localhost:8000/api/predictions/batch_simulate')
print(res.json())

print('Generating and executing decisions...')
risks = requests.get('http://localhost:8000/api/predictions/risks').json()
count = 0
for r in risks[:30]:
    sid = r['shipment_id']
    opts = requests.post(f'http://localhost:8000/api/decisions/generate/{sid}').json()
    if opts and isinstance(opts, list) and len(opts) > 0:
        res = requests.post(f'http://localhost:8000/api/decisions/execute?prescription_id={opts[0]["id"]}')
        if res.status_code == 200: 
            count += 1
print(f'Executed {count} decisions.')

print('Reconciling outcomes...')
res = requests.post('http://localhost:8000/api/decisions/mock_reconcile')
print(res.json())
