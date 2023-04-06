#!/bin/bash

DATA_DIR=data
DISP=False

echo "Generating dataset... Folder: $DATA_DIR"

# You can parallelize these depending on how much resources you have

#############################
## Language-Conditioned Tasks

TASKS='put-blocks-on-bottom-side-of-table put-blocks-on-closest-corner put-blocks-on-different-corners'

for task in $TASKS
    do
        python cliport/demos.py n=1000 task=$task mode=train data_dir=$DATA_DIR disp=$DISP &
        python cliport/demos.py n=100  task=$task mode=val   data_dir=$DATA_DIR disp=$DISP &
        python cliport/demos.py n=100  task=$task mode=test  data_dir=$DATA_DIR disp=$DISP &
    done
echo "Finished Tasks."


