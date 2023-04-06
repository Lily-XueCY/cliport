#!/bin/bash

DATA_DIR=data
DISP=False

echo "Training... Folder: $DATA_DIR"

# You can parallelize these depending on how much resources you have

#############################
## Language-Conditioned Tasks

TASKS='put-blocks-on-bottom-side-of-table put-blocks-on-closest-corner put-blocks-on-different-corners'
for task in $TASKS
    do
        python cliport/train.py train.task=$task \
                        train.agent=cliport \
                        train.attn_stream_fusion_type=add \
                        train.trans_stream_fusion_type=conv \
                        train.lang_fusion_type=mult \
                        train.n_demos=1000 \
                        train.n_steps=201000 \
                        train.exp_folder=exps \
                        dataset.cache=False
    done
echo "Finished Training."




