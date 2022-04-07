## Zion trust setup

There are about 2 phases in the trust setup progress:

we use similar method of contributing as in phase1: https://github.com/weijiekoh/perpetualpowersoftau/.

And our phase2 is based on https://github.com/kobigurk/phase2-bn254


## Procedure
There is a coordinator and multiple participants. The ceremony occurs in sequential rounds. Each participant performs one or more rounds at a time. The coordinator decides the order in which the participants act. There can be an indefinite number of rounds.

The ceremony starts with the coordinator picking a response file from the phase 1 ceremony. The coordinator uses this to generate the initial parameters for all circuits in the phase 2 ceremony.

The participants download these parameters, run a computation to produce new parameters, and send it to the coordinator.

## Instructions for Participants
All participants please follow [these instructions](./participants.md).

## Instructions for Coordinators
Coordinators shall follow [these instructions](./coordinator.md);

## constraint num

| block size | constraint num| exp (2) |
| :--------:| :----------:| :---------:|
| 8 | 786688 | 20 |
| 32 | 3008304 | 22 |
| 64 | 5951760 |  23 |
| 128 | 11838672 | 24 |
| 256 | 23612496 | 25 |
| 512 | 47160144 | 26 |