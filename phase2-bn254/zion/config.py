import os.path
import os   
import hashlib
import json
import subprocess
from dataclasses import dataclass

# Set this to the folder containing the phase2 repo
phase2_repo_path = "../../phase2-bn254/"

# Set this to the folder containing the phase2 repo
zion_repo_path = "../../zion/"

# Do the mpc for the following circuits
circuits = [[0, True, [8,16,32,64]]]

# Set this to the folder containing the phase2 repo
tool_executable = zion_repo_path + "build/tool"

@dataclass
class Circuit:
    block_type: int
    block_size: int
    onchain_data_availability:bool

def base_name(circuit: Circuit):
    return "all_" + str(circuit.block_size)


def get_block_filename(circuit):
    return "blocks/block_meta_" + base_name(circuit) + ".json"


def get_circuit_filename(circuit):
    return "circuits/circuit_" + base_name(circuit) + ".json"


def get_params_filename(circuit):
    return "params/params_" + base_name(circuit) + ".params"


def get_old_params_filename(circuit):
    return "old_params/params_" + base_name(circuit) + ".params"


def get_bellman_vk_filename(circuit):
    return "bellman_keys/" + base_name(circuit) + "_vk.json"


def get_bellman_pk_filename(circuit):
    return "bellman_keys/" + base_name(circuit) + "_pk.json"


def get_vk_filename(circuit):
    return "keys/" + base_name(circuit) + "_vk.json"


def get_pk_filename(circuit):
    return "keys/" + base_name(circuit) + "_pk.raw"


def get_zip_filename(index):
    str_index = str(index)
    while len(str_index) < 4:
        str_index = "0" + str_index
    return "zion_mpc_" + str_index + ".zip"


def find_latest_contribution_index():
    index = 1000
    while index >= 0:
        if os.path.isfile(get_zip_filename(index)):
            return index
        index -= 1
    raise ValueError("Could not find any contribution!")


def hash_file(filename):
    hash = hashlib.sha256()
    with open(filename, "rb") as f:
        for block in iter(lambda: f.read(4096), b""):
            hash.update(block)
        return "0x" + hash.hexdigest()


def get_circuits():
    circuit_list = []
    for block_permutations in circuits:
        block_type = block_permutations[0]
        onchain_data_availability = block_permutations[1]
        for block_size in block_permutations[2]:
            circuit_list.append(Circuit(block_type, block_size, onchain_data_availability))
    return circuit_list


@dataclass
class Block:
    block_type: int
    block_size: int
    onchain_data_availability:bool


def generate_block(circuit: Circuit):
    block = Block(circuit.block_type, circuit.block_size, circuit.onchain_data_availability)
    blockJson = json.dumps(
        block, default=lambda o: o.__dict__, sort_keys=True, indent=4
    )

    block = get_block_filename(circuit)
    if not os.path.exists(block):
        os.makedirs(os.path.dirname(block), exist_ok=True)
    
    with open(block, "w+") as f:
        f.write(blockJson)

    return block


def export_circuit(circuit: Circuit):
    block = get_block_filename(circuit)
    circuit_filename = get_circuit_filename(circuit)
    if not os.path.exists(circuit_filename):
        os.makedirs(os.path.dirname(circuit_filename), exist_ok=True)
    subprocess.check_call(
        [tool_executable, "-exportcircuit", block, circuit_filename]
    )
    return circuit_filename
