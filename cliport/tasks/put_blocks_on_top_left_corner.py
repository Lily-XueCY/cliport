import numpy as np
from cliport.tasks.task import Task
from cliport.utils import utils

import pybullet as p
import random

class PutBlockOnTopLeftCorner(Task):
    """put-blocks-on-top-right-corner"""

    def __init__(self):
        super().__init__()
        self.max_steps = 10
        self.lang_template = "put the {pick} block on the top left corner."
        self.task_completed_desc = "done puting block."

    def reset(self, env):
        super().reset(env)

        # Add base.
        zone_size = (0.08, 0.08, 0)
        rotation = utils.eulerXYZ_to_quatXYZW((0, 0, 0))
        zone_pose = ((0.75-0.04, 0.5-0.04, 0), rotation)


        # Block colors.
        color_names = self.get_colors()

        # Shuffle the block colors.
        random.shuffle(color_names)
        colors = [utils.COLORS[cn] for cn in color_names]

        # Add blocks.
        objs = []
        # sym = np.pi / 2
        block_size = (0.04, 0.04, 0.04)
        block_urdf = 'stacking/block.urdf'
        targs = []
        
#         block_pose = self.get_random_pose(env, block_size)
#         first_p1 = block_pose[1]
#         targ = ((0.25+0.02, 0.5-0.02, block_pose[0][2]), first_p1)
#         targs.append(targ)
#         block_id = env.add_object(block_urdf, block_pose)
#         p.changeVisualShape(block_id, -1, rgbaColor=colors[0] + [1])
#         objs.append((block_id, (np.pi / 2, None)))
        for i in range(0, 4):
#             print(color_names[i])
            block_pose = self.get_random_pose(env, block_size)
#             targ = ((0.25+0.02, 0.5-0.02, block_pose[0][2]), first_p1)
#             print(block_pose)
#             print(targ)
#             targs.append(targ)
            block_id = env.add_object(block_urdf, block_pose)
            p.changeVisualShape(block_id, -1, rgbaColor=colors[i] + [1])
            objs.append((block_id, (np.pi / 2, None)))
            obj_pts=dict()
            obj_pts[block_id] = self.get_box_object_points(block_id)
            self.goals.append(([objs[i]], np.ones((1, 1)), [zone_pose], True, False,
                           'zone', (obj_pts, [(zone_pose, zone_size)]), 1 / 4))

    def get_colors(self):
        return utils.TRAIN_COLORS if self.mode == 'train' else utils.EVAL_COLORS