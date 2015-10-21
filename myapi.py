from flask import Flask, request, jsonify
from werkzeug.contrib.cache import MemcachedCache

import methods
app = Flask(__name__)


# Defines cache object
CACHE_TIMEOUT = 30
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


@app.route('/vms/<host>/', methods=['GET', 'POST'])
# @cached()
def get_vms(host):
    if request.method == 'POST':
        specs = request.get_json()
        return jsonify(vm = methods.create_new_vm(host, specs))
    else:
        return jsonify(vm = methods.get_all_vm_info(host))


@app.route('/vms/<host>/<uuid>/', methods=['GET', 'PUT', 'DELETE'])
def get_vm(host, uuid):
    if request.method == 'DELETE':
        return methods.delete_vm_from_server(host, uuid)
    elif request.method == 'PUT':
        specs = request.get_json()
        return methods.change_vm_stats(host, uuid, specs)
    else:
        return jsonify(vm=methods.find_vm_by_uuid(host, uuid))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
