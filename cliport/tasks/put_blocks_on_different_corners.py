import numpy as np
from cliport.tasks.task import Task
from cliport.utils import utils

import pybullet as p
import random

class PutBlockOnDifferentCorner(Task):
    """put-blocks-on-different-corners"""

    def __init__(self):
        super().__init__()
        self.max_steps = 5
        self.lang_template = "put the {pick} block on the {place} corner"
        self.task_completed_desc = "done puting block."

    def reset(self, env):
        super().reset(env)

        # Add base.
#         base_size = (0.05, 0.15, 0.005)
#         base_urdf = 'stacking/stand.urdf'
#         base_pose = self.get_random_pose(env, base_size)
#         env.add_object(base_urdf, base_pose, 'fixed')


        # Block colors.
        n_blocks = 4

        all_color_names = self.get_colors()
        selected_color_names = random.sample(all_color_names, n_blocks)
        colors = [utils.COLORS[cn] for cn in selected_color_names]
        
        corners = [(0.25+0.02, 0.5-0.02, 0.02), (0.75-0.02, 0.5-0.02, 0.02), (0.25+0.02, -0.5+0.02, 0.02), (0.75-0.02, -0.5+0.02, 0.02)] 
        corner_names = ['bottom left', 'top left', 'bottom right', 'top right']

       
        # Add blocks.
        block_size = (0.04, 0.04, 0.04)
        block_urdf = 'stacking/block.urdf'
        blocks = []
        for i in range(4):
            block_pose = self.get_random_pose(env, block_size)
            targ = (corners[i], block_pose[1])
            block_id = env.add_object(block_urdf, block_pose)
            p.changeVisualShape(block_id, -1, rgbaColor=colors[i] + [1])
            blocks.append((block_id, (0, None)))
            self.goals.append(([(block_id, (0, None))], np.ones((1, 1)), [targ],
                               False, True, 'pose', None, 1/4))
            self.lang_goals.append(self.lang_template.format(pick=selected_color_names[i], place=corner_names[i]))
        
        
        # Colors of distractor objects.
        bowl_size = (0.12, 0.12, 0)
        bowl_urdf = 'bowl/bowl.urdf'
        distractor_bowl_colors = [utils.COLORS[c] for c in utils.COLORS if c not in selected_color_names]

        # Add distractors.
        n_distractors = 0
        max_distractors = 6
        while n_distractors < max_distractors:
            is_block = False
            urdf = block_urdf if is_block else bowl_urdf
            size = block_size if is_block else bowl_size
            colors = distractor_block_colors if is_block else distractor_bowl_colors
            pose = self.get_random_pose(env, size)
            if not pose:
                continue
            obj_id = env.add_object(urdf, pose)
            color = colors[n_distractors % len(colors)]
            if not obj_id:
                continue
            p.changeVisualShape(obj_id, -1, rgbaColor=color + [1])
            n_distractors += 1


    def get_colors(self):
        return utils.TRAIN_COLORS if self.mode == 'train' else utils.EVAL_COLORS