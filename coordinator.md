# Instructions for the Coordinator
link the git resposity(https://github.com/CortexFoundation/zion) under the trust_setup folder(in the same folder with phase2-bn254).
and then go to the zion/build to make the tool.


Due to the max block size we may use is 512, exp is 2 ^26, so we could 
change the REQUIRED_POWER in phase2-bn254/powersoftau/src/small_bn256/mod.rs from 28 to 26.

Next, go into phase2-bn254 and build the rust programs:
```bash
cd powersoftau && cargo build --release && \
cd ../phase2 && cargo build --release && \
cd ../zion
```

Stay in the folder `phase2-bn254/zion` from now on to run all commands.
Download the response of the latest participant from [phase 1](https://github.com/weijiekoh/perpetualpowersoftau/) into `phase2-bn254/loopring`. Rename the file to `response`.

A final contribution is needed with a [beacon](https://github.com/ZcashFoundation/powersoftau-attestations/tree/master/0088). The beacon we use is the hash of Bitcoin block #602168: `00000000000000000013a0dab9d26be0353108f6eb5a2be6ac389986296607c7`, which can be found in `phase2-bn254/powersoftau/src/bin/beacon_constrained.rs`:

```
// Update the number of iterations: We use 2^37 iterations

// Place block hash here (block number #564321)
let mut cur_hash: [u8; 32] = hex!("0000000000000000000a558a61ddc8ee4e488d647a747fe4dcc362fe2026c620");
```
Recompile with `cargo build --release` in `phase2-bn254/powersoftau` and now run this:

```bash
../powersoftau/target/release/verify_transform_constrained -skipverification && \
mv new_challenge challenge && mv response old_response && \
../powersoftau/target/release/beacon_constrained && \
../powersoftau/target/release/prepare_phase2
```
We're now ready to setup phase 2. Open `config.py` and modify `circuits` with all the circuits that are needed. Once you've done this, create a new branch for the `phase2-bn254` repo and commit your changes to that branch. Make sure all participants checkout that branch when participating.

We can now create the initial parameters:

```
python3 setup.py
```
Once finished the file `loopring_zion_0000.zip` will have been created with the initial parameters for all circuits. share it with other participants.

At this point an indefinite number of participants can contribute.

At any point we can use the parameters to create the verification and proving keys.


If you decide to use a certain contribution, you first have to do another contribution on top of it with [a beacon](https://lists.zfnd.org/pipermail/zapps-wg/2018/000380.html) (just like before with the phase 1 result). To do this a bitcoin hash is used at a certain block height. Publicly share the block height of the block you will use a couple of hours before the block is mined. Once the block is mined put the hash of the block in `phase2-bn254/phase2/src/bin/beacon.rs`:

```
// Update the number of iterations: We use 2^37 iterations

// Place block hash here (block number #564321)
let mut cur_hash: [u8; 32] = hex!("0000000000000000000a558a61ddc8ee4e488d647a747fe4dcc362fe2026c620");
```

Recompile with `cargo build --release` in `phase2-bn254/phase2` and now contribute like this:

```
python3 contribute.py beacon
```

This will generate the contribution that can finally be used to create the verification and proving keys!

```
python3 export_keys.py
```

This will use the latest `zion_mpc_NNNN.zip` file it can find and write the keys to `protocols/packages/loopring_v3/keys`.

