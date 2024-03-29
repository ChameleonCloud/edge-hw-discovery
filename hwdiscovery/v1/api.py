import os
from flask import Flask, jsonify
from doniclient.v1.client import Client as DoniClient
from keystoneauth1.adapter import Adapter
from openstack.connection import Connection

app = Flask(__name__)

@app.route('/devices', methods=['GET'])
def get_devices_info():
    try:
        # Fetch data from the DONI API
        # conn = Connection(cloud="chi_edge")
        conn = Connection(
            region_name=os.environ.get("EDGE_OS_REGION_NAME"),
            auth_type=os.environ.get("EDGE_OS_AUTH_TYPE"),
            auth_url=os.environ.get("EDGE_OS_AUTH_URL"),
            auth={
                'application_credential_id': os.environ.get("EDGE_OS_APPLICATION_CREDENTIAL_ID"),
                'application_credential_secret': os.environ.get("EDGE_OS_APPLICATION_CREDENTIAL_SECRET"),
            })

        doni_client = DoniClient(Adapter(session=conn.session,service_type="inventory",interface="public"))

        devices_data = doni_client.export()

        # Extract required information from each device
        devices_info = []
        for device in devices_data:
            print(device['properties'])
            device_info = {
                "device_name": device["name"],
                "uuid": device["uuid"],
                "device_type": device["properties"].get("machine_name", ""),
                "owning_project": device["project_id"],
                "supported_device_profiles": device["properties"].get("device_profiles", []),
                "authorized_projects": device["properties"].get("authorized_projects", ["all"]),
            }
            devices_info.append(device_info)

        # Return the extracted information in JSON format
        return jsonify(devices_info)
    except Exception as e:
        raise(e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)