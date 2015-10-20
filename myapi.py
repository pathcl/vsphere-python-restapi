from flask import Flask, request, jsonify
from werkzeug.contrib.cache import MemcachedCache

import methods
app = Flask(__name__)


# Defines cache object
CACHE_TIMEOUT = 3000
cache = MemcachedCache(['127.0.0.1:11211'])


class cached(object):

    def __init__(self, timeout=None):
        self.timeout = timeout or CACHE_TIMEOUT

    def __call__(self, f):
        def decorator(*args, **kwargs):
            response = cache.get(request.path)
            if response is None:
                response = f(*args, **kwargs)
                cache.set(request.path, response, self.timeout)
            return response
        return decorator


@app.route('/')
def index():
    return 'HAI!'


@app.route('/vms/<host>/', methods=['GET'])
@cached()
def get_vms(host):
    return jsonify(vm=methods.get_all_vm_info(host))


"""
@app.route('/vms/<uuid>/', methods=['GET', 'PUT', 'DELETE'])
def get_vm(uuid):
    if request.method == 'DELETE':
        return methods.delete_vm_from_server(uuid)
    elif request.method == 'PUT':
        specs = request.get_json()
        return methods.change_vm_stats(uuid, specs)
    else:
        return jsonify(methods.find_vm_by_uuid(uuid))
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
