"""Put Blocks in Bowl Task."""

import numpy as np
from cliport.tasks.task import Task
from cliport.utils import utils

import random
import pybullet as p


class PutBlockInMatchingBowl(Task):
    """Put Blocks in Bowl base class and task."""

    def __init__(self):
        super().__init__()
        self.max_steps = 10
        self.pos_eps = 0.05
        self.lang_template = "put the {pick} blocks in a {place} bowl"
        self.task_completed_desc = "done placing blocks in bowls."

    def reset(self, env):
        super().reset(env)
        n_bowls = np.random.randint(2, 6)
        n_blocks = n_bowls

        all_color_names = self.get_colors()
        selected_color_names = random.sample(all_color_names, n_bowls)
        colors = [utils.COLORS[cn] for cn in selected_color_names]

        # Add bowls.
        bowl_size = (0.12, 0.12, 0)
        bowl_urdf = 'bowl/bowl.urdf'
        bowl_poses = []
        for i in range(n_bowls):
            bowl_pose = self.get_random_pose(env, bowl_size)
            bowl_id = env.add_object(bowl_urdf, bowl_pose, 'fixed')
            p.changeVisualShape(bowl_id, -1, rgbaColor=colors[i] + [1])
            bowl_poses.append(bowl_pose)

        # Add blocks.
        blocks = []
        block_size = (0.04, 0.04, 0.04)
        block_urdf = 'stacking/block.urdf'
        for i in range(n_blocks):
            block_pose = self.get_random_pose(env, block_size)
            block_id = env.add_object(block_urdf, block_pose)
            p.changeVisualShape(block_id, -1, rgbaColor=colors[i] + [1])
            blocks.append((block_id, (0, None)))

        # Goal: put each block in a different bowl.
#         self.goals.append((blocks, np.ones((len(blocks), len(bowl_poses))),
#                            bowl_poses, False, True, 'pose', None, 1))
#         self.lang_goals.append(self.lang_template.format(pick=selected_color_names[0],
#                                                          place=selected_color_names[1]))
        for i in range(n_blocks):
            self.goals.append(([blocks[i]], np.ones((1, 1)),
                           [bowl_poses[i]], False, True, 'pose', None, 1/n_bowls))
            self.lang_goals.append(self.lang_template.format(pick=selected_color_names[i],
                                                         place=selected_color_names[i]))

        # Only one mistake allowed.
        self.max_steps = len(blocks) + 1

#         # Colors of distractor objects.
#         distractor_bowl_colors = [utils.COLORS[c] for c in utils.COLORS if c not in selected_color_names]
#         distractor_block_colors = [utils.COLORS[c] for c in utils.COLORS if c not in selected_color_names]

#         # Add distractors.
#         n_distractors = 0
#         max_distractors = 6
#         while n_distractors < max_distractors:
#             is_block = np.random.rand() > 0.5
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

#     def reward(self):   
#         reward, info = 0, {}



#         if len(self.goals) > 0:
#             # Unpack next goal step.
#             objs, matches, targs, _, _, metric, params, max_reward = self.goals[0]

#             # Evaluate by matching object poses.
#             if metric == 'pose':
#                 step_reward = 0
#                 for i in range(len(objs)):
#                     object_id, (symmetry, _) = objs[i]
#                     pose = p.getBasePositionAndOrientation(object_id)
#                     targets_i = np.argwhere(matches[i, :]).reshape(-1)
#                     for j in targets_i:
#                         target_pose = targs[j]
#                         if self.is_match(pose, target_pose, symmetry):
#                             step_reward += max_reward / len(objs)
#                             break

#             # Evaluate by measuring object intersection with zone.
#             elif metric == 'zone':
#                 zone_pts, total_pts = 0, 0
#                 obj_pts, zones = params
#                 for zone_idx, (zone_pose, zone_size) in enumerate(zones):

#                     # Count valid points in zone.
#                     for obj_idx, obj_id in enumerate(obj_pts):
#                         pts = obj_pts[obj_id]
#                         obj_pose = p.getBasePositionAndOrientation(obj_id)
#                         world_to_zone = utils.invert(zone_pose)
#                         obj_to_zone = utils.multiply(world_to_zone, obj_pose)
#                         pts = np.float32(utils.apply(obj_to_zone, pts))
#                         if len(zone_size) > 1:
#                             valid_pts = np.logical_and.reduce([
#                                 pts[0, :] > -zone_size[0] / 2, pts[0, :] < zone_size[0] / 2,
#                                 pts[1, :] > -zone_size[1] / 2, pts[1, :] < zone_size[1] / 2,
#                                 pts[2, :] < self.zone_bounds[2, 1]])

#                         # if zone_idx == matches[obj_idx].argmax():
#                         zone_pts += np.sum(np.float32(valid_pts))
#                         total_pts += pts.shape[1]
#                 step_reward = max_reward * (zone_pts / total_pts)

#             # Get cumulative rewards and return delta.
#             reward = self.progress + step_reward - self._rewards
#             self._rewards = self.progress + step_reward
#             self.goals.pop(0)
#         if len(self.lang_goals) > 0:
#             self.lang_goals.pop(0)

#         return reward, info
    
#     def done(self):
#         return False

    def get_colors(self):
#         return utils.TRAIN_COLORS if self.mode == 'train' else utils.EVAL_COLORS
        return utils.TRAIN_COLORS