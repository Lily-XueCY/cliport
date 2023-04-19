"""Put Blocks in Bowl Task."""

import numpy as np
from cliport.tasks.task import Task
from cliport.utils import utils

import random
import pybullet as p


class PutBlockInDifferentBowl(Task):
    """Put Blocks in Bowl base class and task."""

    def __init__(self):
        super().__init__()
        self.max_steps = 10
        self.pos_eps = 0.05
        self.lang_template = "put the {pick} blocks in a {place} bowl"
        self.task_completed_desc = "done placing blocks in bowls."

    def reset(self, env):
        super().reset(env)
#         n_bowls = np.random.randint(2, 4)
#         n_blocks = n_bowls

#         all_color_names = self.get_colors()
#         selected_color_names_bowl = random.sample(all_color_names, n_bowls)
#         bowl_colors = [utils.COLORS[cn] for cn in selected_color_names_bowl]
#         selected_color_names_block = [c for c in utils.COLORS if c not in selected_color_names_bowl]
#         block_colors = [utils.COLORS[cn] for cn in selected_color_names_block]

        n_bowls = np.random.randint(2, 6)
        n_blocks = n_bowls

        all_color_names = self.get_colors()
        selected_color_names = random.sample(all_color_names, n_bowls)
        bowl_colors = [utils.COLORS[cn] for cn in selected_color_names]
        block_colors = bowl_colors


        # Add bowls.
        bowl_size = (0.12, 0.12, 0)
        bowl_urdf = 'bowl/bowl.urdf'
        bowl_poses = []
        for i in range(n_bowls):
            bowl_pose = self.get_random_pose(env, bowl_size)
            bowl_id = env.add_object(bowl_urdf, bowl_pose, 'fixed')
            p.changeVisualShape(bowl_id, -1, rgbaColor=bowl_colors[i] + [1])
            bowl_poses.append(bowl_pose)

        # Add blocks.
        blocks = []
        block_size = (0.04, 0.04, 0.04)
        block_urdf = 'stacking/block.urdf'
        for i in range(n_blocks):
            block_pose = self.get_random_pose(env, block_size)
            block_id = env.add_object(block_urdf, block_pose)
            p.changeVisualShape(block_id, -1, rgbaColor=block_colors[i] + [1])
            blocks.append((block_id, (0, None)))

        # Goal: put each block in a different bowl.
#         self.goals.append((blocks, np.ones((len(blocks), len(bowl_poses))),
#                            bowl_poses, False, True, 'pose', None, 1))
#         self.lang_goals.append(self.lang_template.format(pick=selected_color_names[0],
#                                                          place=selected_color_names[1]))
        for i in range(n_blocks):
            self.goals.append(([blocks[i]], np.ones((1, 1)),
                           [bowl_poses[(i+1)%n_bowls]], False, True, 'pose', None, 1/n_bowls))
            self.lang_goals.append(self.lang_template.format(pick=selected_color_names[i],
                                                         place=selected_color_names[(i+1)%n_bowls]))

        # Only one mistake allowed.
        self.max_steps = len(blocks) + 1

        # Colors of distractor objects.
#         distractor_bowl_colors = [utils.COLORS[c] for c in utils.COLORS if c in selected_color_names]
#         distractor_block_colors = [utils.COLORS[c] for c in utils.COLORS if c not in selected_color_names_bowl and c not in selected_color_names_block]

#         # Add distractors.
#         n_distractors = 0
#         max_distractors = 6
#         while n_distractors < max_distractors:
#             is_block = True
#             urdf = block_urdf if is_block else bowl_urdf
#             size = block_size if is_block else bowl_size
#             colors = distractor_block_colors if is_block else distractor_bowl_colors
#             pose = self.get_random_pose(env, size)
#             if not pose:
#                 continue
#             obj_id = env.add_object(urdf, pose)
#             color = colors[n_distractors % len(colors)]
#             if not obj_id:
#                 continue
#             p.changeVisualShape(obj_id, -1, rgbaColor=color + [1])
#             n_distractors += 1


    def get_colors(self):
#         return utils.TRAIN_COLORS if self.mode == 'train' else utils.EVAL_COLORS
        return utils.TRAIN_COLORS
    
# class PutBlockInDifferentBowlNoPlan(Task):
    
#     def __init__(self):
#         super().__init__()
#         self.max_steps = 10
#         self.pos_eps = 0.05
#         self.lang_template = "put the {pick} blocks in a {place} bowl"
#         self.task_completed_desc = "done placing blocks in bowls."

        
#     def reset(self, env):
#         super().reset(env)
#         n_bowls = np.random.randint(2, 6)
#         n_blocks = n_bowls

#         all_color_names = self.get_colors()
#         selected_color_names = random.sample(all_color_names, n_bowls)
#         bowl_colors = [utils.COLORS[cn] for cn in selected_color_names]
# #         selected_color_names_block = [c for c in utils.COLORS if c not in selected_color_names_bowl]
# #         block_colors = [utils.COLORS[cn] for cn in selected_color_names]
#         block_colors = bowl_colors

#         # Add bowls.
#         bowl_size = (0.12, 0.12, 0)
#         bowl_urdf = 'bowl/bowl.urdf'
#         bowl_poses = []
#         for i in range(n_bowls):
#             bowl_pose = self.get_random_pose(env, bowl_size)
#             bowl_id = env.add_object(bowl_urdf, bowl_pose, 'fixed')
#             p.changeVisualShape(bowl_id, -1, rgbaColor=bowl_colors[i] + [1])
#             bowl_poses.append(bowl_pose)

#         # Add blocks.
#         blocks = []
#         block_size = (0.04, 0.04, 0.04)
#         block_urdf = 'stacking/block.urdf'
#         for i in range(n_blocks):
#             block_pose = self.get_random_pose(env, block_size)
#             block_id = env.add_object(block_urdf, block_pose)
#             p.changeVisualShape(block_id, -1, rgbaColor=block_colors[i] + [1])
#             blocks.append((block_id, (0, None)))

#         # Goal: put each block in a different bowl.
# #         self.goals.append((blocks, np.ones((len(blocks), len(bowl_poses))),
# #                            bowl_poses, False, True, 'pose', None, 1))
# #         self.lang_goals.append(self.lang_template.format(pick=selected_color_names[0],
# #                                                          place=selected_color_names[1]))
# #         for i in range(n_blocks):
#         self.goals.append((blocks, np.ones((len(blocks), len(bowl_poses)))-np.diag(np.ones(n_bowls)),
#                        bowl_poses, False, True, 'pose', None, 1))
#         self.lang_goals.append("Put all the blocks in different color bowls" )

#         # Only one mistake allowed.
#         self.max_steps = len(blocks) + 1
        
#         # Colors of distractor objects.
# #         distractor_bowl_colors = [utils.COLORS[c] for c in utils.COLORS if c == selected_color_names_block[0]]
# #         distractor_block_colors = [utils.COLORS[c] for c in utils.COLORS if c not in selected_color_names_bowl and c not in selected_color_names_block]

# #         # Add distractors.
# #         n_distractors = 0
# #         max_distractors = 2
# #         while n_distractors < max_distractors:
# #             is_block = False
# #             urdf = block_urdf if is_block else bowl_urdf
# #             size = block_size if is_block else bowl_size
# #             colors = distractor_block_colors if is_block else distractor_bowl_colors
# #             pose = self.get_random_pose(env, size)
# #             if not pose:
# #                 continue
# #             obj_id = env.add_object(urdf, pose)
# #             color = colors[n_distractors % len(colors)]
# #             if not obj_id:
# #                 continue
# #             p.changeVisualShape(obj_id, -1, rgbaColor=color + [1])
# #             n_distractors += 1
            
#     def get_colors(self):
# #         return utils.TRAIN_COLORS if self.mode == 'train' else utils.EVAL_COLORS
#           return utils.TRAIN_COLORS
