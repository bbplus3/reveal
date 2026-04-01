import sys
sys.path.insert(0, '.')
from server import app
for rule in app.url_map.iter_rules():
    print(rule, rule.methods)