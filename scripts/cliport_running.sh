#!/bin/bash

DISP=False

cd cliport
pip install -r requirements.txt

export CLIPORT_ROOT=$(pwd)
python setup.py develop

echo "Generating dataset... Folder: $DATA_DIR"

# You can parallelize these depending on how much resources you have

#############################
## Language-Conditioned Tasks

TASKS='put-blocks-on-bottom-side-of-table put-blocks-on-closest-corner put-blocks-on-different-corners'

for task in $TASKS
    do
        python cliport/demos.py n=1000 task=$task mode=train disp=$DISP &
        python cliport/demos.py n=100  task=$task mode=val   disp=$DISP &
        python cliport/demos.py n=100  task=$task mode=test  disp=$DISP
        python cliport/train.py train.task=$task \
                        train.agent=cliport \
                        train.attn_stream_fusion_type=add \
                        train.trans_stream_fusion_type=conv \
                        train.lang_fusion_type=mult \
                        train.n_demos=1000 \
                        train.n_steps=201000 \
                        train.exp_folder=exps \
                        dataset.cache=False
        python cliport/eval.py eval_task=$task \
                       agent=cliport \
                       mode=val \
                       n_demos=100 \
                       train_demos=1000 \
                       checkpoint_type=val_missing \
                       exp_folder=exps
        python cliport/eval.py eval_task=$task \
                       agent=cliport \
                       mode=test \
                       n_demos=100 \
                       train_demos=1000 \
                       checkpoint_type=test_best \
                       exp_folder=exps
    done
echo "Finished Tasks."



