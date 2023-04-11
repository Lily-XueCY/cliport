#!/bin/bash

DATA_DIR=data
DISP=False

echo "Generating dataset... Folder: $DATA_DIR"

# You can parallelize these depending on how much resources you have

#############################
## Language-Conditioned Tasks

# TASKS='put-blocks-on-bottom-side-of-table put-blocks-on-closest-corner put-blocks-on-different-corners'
TASKS='put-blocks-on-bottom-left-corner put-blocks-on-top-right-corner put-blocks-on-bottom-side-of-table'

for task in $TASKS
    do
        python cliport/demos.py n=1000 task=$task mode=train data_dir=$DATA_DIR disp=$DISP &
        python cliport/demos.py n=100  task=$task mode=val   data_dir=$DATA_DIR disp=$DISP &
        python cliport/demos.py n=100  task=$task mode=test  data_dir=$DATA_DIR disp=$DISP &
    done
echo "Finished Tasks."

# python cliport/train.py train.task=multi-language-conditioned-new \
#                         train.agent=cliport \
#                         train.attn_stream_fusion_type=add \
#                         train.trans_stream_fusion_type=conv \
#                         train.lang_fusion_type=mult \
#                         train.n_demos=1000 \
#                         train.n_steps=601000 \
#                         dataset.cache=False \
#                         train.exp_folder=exps \
#                         dataset.type=multi 
# echo "Finished Training."

# python cliport/eval.py model_task=multi-language-conditioned-new \
#                        eval_task=stack-block-pyramid-seq-seen-colors \
#                        agent=cliport \
#                        mode=val \
#                        n_demos=100 \
#                        train_demos=1000 \
#                        checkpoint_type=val_missing \
#                        type=single \
#                        exp_folder=exps 
# echo "Finished Evaluating."
