from flask import jsonify
import symmetryshift.create_biological_structure_unit as assembler
import tempfile
import os
from google.cloud import storage as gcs
import logging


def create_assembly(pdb_code, work_dir):
    # input_filename = os.path.join(work_dir, "tmp_in.pdb")
    output_filename = os.path.join(work_dir, f"{pdb_code}_assembled.pdb")
    structure = assembler.get_biological_assembly_from_pdb_code(pdb_code)
    assembler.save_structure(structure, output=output_filename)
    return output_filename


def upload_assembly(filename, pdb_code):
    project_id = os.environ["PROJECT_ID"]
    bucket_id = os.environ["ROTATED_PDB_FILE_BUCKECT_ID"]
    client = gcs.Client(project_id)
    bucket = client.get_bucket(bucket_id)

    file_id = f"{pdb_code}_assembled.pdb"
    blob_gcs = bucket.blob(file_id)
    blob_gcs.upload_from_filename(filename, content_type="text/plain")
    download_url = f"https://storage.googleapis.com/{bucket_id}/{file_id}"
    return download_url


def upload_original(filename, pdb_code):
    project_id = os.environ["PROJECT_ID"]
    bucket_id = os.environ["ORIGINAL_PDB_FILE_BUCKECT_ID"]
    client = gcs.Client(project_id)
    bucket = client.get_bucket(bucket_id)

    file_id = f"{pdb_code}.pdb"
    blob_gcs = bucket.blob(file_id)
    blob_gcs.upload_from_filename(filename, content_type="text/plain")
    download_url = f"https://storage.googleapis.com/{bucket_id}/{file_id}"
    return download_url


def fetch_biological_assembly(request):
    # CORS enable
    # fmt: off
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST",
        "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept"
    }
    # fmt: on
    if request.method == "OPTIONS":
        return ("", 204, headers)

    data = request.get_json()
    tmp_dir = tempfile.mkdtemp()
    os.chdir(tmp_dir)
    try:
        pdb_code = data["pdb_code"]
        if type(pdb_code) != str or len(pdb_code) != 4:
            raise ValueError(f"pdb code must be 4 char. Input is {pdb_code}")
        assembly_filename = create_assembly(pdb_code, tmp_dir)
        assembly_url = upload_assembly(assembly_filename, pdb_code)
        original_filename = os.path.join(tmp_dir, pdb_code, f"pdb{pdb_code}.ent")
        original_url = upload_original(original_filename, pdb_code)
        data = {
            "message": "ok",
            "assembly_url": assembly_url,
            "original_url": original_url,
        }
        return jsonify(data), 200, headers
    except FileNotFoundError as err:
        logging.error(err)
        return jsonify(
            {
                "message": "Requested PDB code does not exist"
                "or were not submited as a PDB file format."
            },
            410,
            headers,
        )
    except OSError as err:
        logging.error(err)
        return jsonify(
            {
                "message": "Requested PDB code does not exist"
                "or were not submited as a PDB file format."
            },
            410,
            headers,
        )
    except ValueError as err:
        logging.error(err)
        return jsonify({"message": str(err)}), 500, headers
    except Exception as err:
        logging.error(err)
        return jsonify({"message": "Unexpected error occur"}), 500, headers
