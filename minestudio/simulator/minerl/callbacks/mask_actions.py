'''
Date: 2024-11-11 17:37:06
LastEditors: caishaofei-mus1 1744260356@qq.com
LastEditTime: 2024-11-11 17:42:04
FilePath: /MineStudio/minestudio/simulator/minerl/callbacks/mask_actions.py
'''

from minestudio.simulator.minerl.callbacks.callback import MinecraftCallback

class MaskActionsCallback(MinecraftCallback):
    
    def __init__(self, **action_settings):
        super().__init__()
        self.action_settings = action_settings
    
    def before_step(self, sim, action):
        for act, val in self.action_settings.items():
            action[act] = val
        return action