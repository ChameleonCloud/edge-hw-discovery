from flask import Flask, jsonify
from doniclient.v1.client import Client as DoniClient
from keystoneauth1.adapter import Adapter
from openstack.connection import Connection

app = Flask(__name__)

@app.route('/devices', methods=['GET'])
def get_devices_info():
    try:
        # Fetch data from the DONI API
        conn = Connection(cloud="chi_edge")

        doni_client = DoniClient(Adapter(session=conn.session,service_type="inventory",interface="public"))

        devices_data = doni_client.export()

        # Extract required information from each device
        devices_info = []
        for device in devices_data:
            device_info = {
                "device_name": device["name"],
                "device_type": device["properties"].get("machine_name", ""),
                "owning_project": device["project_id"],
                "supported_device_profiles": device["properties"].get("device_profiles", [])
            }
            devices_info.append(device_info)

        # Return the extracted information in JSON format
        return jsonify(devices_info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)