import os
import subprocess
import config
import time
from zipfile import ZipFile, ZIP_DEFLATED

def mpc_setup(circuit):
    circuit_filename = config.get_circuit_filename(circuit)
    params_filename = config.get_params_filename(circuit)
    if not os.path.exists(params_filename):
        os.makedirs(os.path.dirname(params_filename), exist_ok=True)
    subprocess.check_call([config.phase2_repo_path + "phase2/target/release/new", circuit_filename, params_filename])
    return params_filename

if __name__ == "__main__":
    start = time.time()
    with ZipFile(config.get_zip_filename(0), 'w', ZIP_DEFLATED) as zip_file:
        circuits = config.get_circuits()
        for idx, circuit in enumerate(circuits):
            print("Circuit " + str(idx+1) + "/" + str(len(circuits)) + ":")

            block = config.generate_block(circuit)
            circuit_filename = config.export_circuit(circuit)
            params_filename = mpc_setup(circuit)

            # Add the params file to the zip file
            zip_file.write(params_filename, os.path.basename(params_filename))

            # delete the files
            os.remove(params_filename)
            os.remove(circuit_filename)
            os.remove(block)

    # calculate the hash of the file
    hash = config.hash_file(config.get_zip_filename(0))
    print("SHA256 hash of the contribution is: " + str(hash))

    end = time.time()
    print("Setup took " + str(end - start) + " seconds.")
