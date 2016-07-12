from flask import Flask, request, jsonify
import methods

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome to the VMware REST API!'

@app.route('/<host>/vms/', methods=['GET', 'POST'])
def get_vms(host):
    if request.method == 'POST':
        specs = request.get_json()
        return jsonify(vm=methods.create_new_vm(specs))
    else:
        return jsonify(vm=methods.get_all_vm_info(host))


@app.route('/vms/<uuid>/', methods=['GET', 'PUT', 'DELETE'])
def get_vm(uuid):
    if request.method == 'DELETE':
        return methods.delete_vm_from_server(uuid)
    elif request.method == 'PUT':
        specs = request.get_json()
        return methods.change_vm_stats(uuid, specs)
    else:
        return jsonify(methods.find_vm_by_uuid(uuid))


if __name__ == '__main__':
    app.run(debug=True)
