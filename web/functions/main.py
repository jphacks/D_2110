from flask import jsonify
import symmetryshift.create_biological_structure_unit as assembler
import tempfile
import os
from google.cloud import storage as gcs
import logging
import uuid


def create_assembly(pdb_code):
    tmp_dir = tempfile.mkdtemp()
    # input_filename = os.path.join(tmp_dir, "tmp_in.pdb")
    output_filename = os.path.join(tmp_dir, "tmp_out.pdb")
    structure = assembler.get_biological_assembly_from_pdb_code(pdb_code)
    assembler.save_structure(structure, output=output_filename)
    return output_filename


def upload_assembly(filename):
    project_id = os.environ["GCP_PROJECT"]
    bucket_id = os.environ["ROTATED_PDB_FILE_BUCKECT_ID"]
    client = gcs.Client(project_id)
    bucket = client.get_bucket(bucket_id)
    blob_gcs = bucket.blob(uuid.uuid1())
    blob_gcs.upload_from_filename(filename)
    download_url = blob_gcs._get_download_url()
    return download_url


def fetch_biological_assembly(request):
    data = request.get_json()
    try:
        pdb_code = data["pdb_code"]
        if type(pdb_code) != str or len(pdb_code) != 4:
            raise ValueError(f"pdb code must be 4 char. Input is {pdb_code}")
        filename = create_assembly(pdb_code)
        download_url = upload_assembly(filename)
        data = {"message": "ok", "download_url": download_url}
        return jsonify(data)
    except ValueError as err:
        logging.error(err)
        return jsonify({"message": "pdb code must be 4 char"}), 500
    except Exception as err:
        logging.error(err)
        return jsonify({"message": "Unexpected error occur"}), 500
