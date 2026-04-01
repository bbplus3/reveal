import sys
sys.path.insert(0, '.')
from server import app
app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)