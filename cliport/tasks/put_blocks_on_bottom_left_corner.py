import numpy as np
from cliport.tasks.task import Task
from cliport.utils import utils

import pybullet as p
import random

class PutBlockOnBottomLeftCorner(Task):
    """put-blocks-on-bottom-left-corner"""

    def __init__(self):
        super().__init__()
        self.max_steps = 10
        self.lang_template = "put the {pick} block on the bottom left corner."
        self.task_completed_desc = "done puting block."

    def reset(self, env):
        super().reset(env)

        # Add base.
        zone_size = (0.08, 0.08, 0)
        rotation = utils.eulerXYZ_to_quatXYZW((0, 0, 0))
        zone_pose = ((0.25+0.04, 0.5-0.04, 0), rotation)


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

        # Associate placement locations for goals.
#         place_pos = [(0, -0.05, 0.03), (0, 0, 0.03),
#                      (0, 0.05, 0.03), (0, -0.025, 0.08),
#                      (0, 0.025, 0.08), (0, 0, 0.13)]
#         targs = [(utils.apply(base_pose, i), base_pose[1]) for i in place_pos]
    
        # Goal: make bottom row.
#         self.goals.append(([objs[0]], np.ones((1, 1)), [targs[0]],
#                            False, True, 'pose', None, 1 / 4))
#         self.lang_goals.append(self.lang_template.format(pick=color_names[0]))

#         self.goals.append(([objs[1]], np.ones((1, 1)), [targs[1]],
#                            False, True, 'pose', None, 1 / 4))
#         self.lang_goals.append(self.lang_template.format(pick=color_names[1]))

#         self.goals.append(([objs[2]], np.ones((1, 1)), [targs[2]],
#                            False, True, 'pose', None, 1 / 4))
#         self.lang_goals.append(self.lang_template.format(pick=color_names[2]))

#         # Goal: make middle row.
#         self.goals.append(([objs[3]], np.ones((1, 1)), [targs[3]],
#                            False, True, 'pose', None, 1 / 4))
#         self.lang_goals.append(self.lang_template.format(pick=color_names[3]))

#         self.goals.append(([objs[4]], np.ones((1, 1)), [targs[4]],
#                            False, True, 'pose', None, 1 / 6))
#         self.lang_goals.append(self.lang_template.format(pick=color_names[4]))

#         # Goal: make top row.
#         self.goals.append(([objs[5]], np.ones((1, 1)), [targs[5]],
#                            False, True, 'pose', None, 1 / 6))
#         self.lang_goals.append(self.lang_template.format(pick=color_names[5]))

    def get_colors(self):
        return utils.TRAIN_COLORS if self.mode == 'train' else utils.EVAL_COLORS