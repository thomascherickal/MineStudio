from minestudio.simulator import MinecraftSim
from minestudio.simulator.callbacks import RecordCallback, SpeedTestCallback, CommandsCallback, DemonstrationCallback
from minestudio.models import GrootPolicy, load_groot_policy
from minestudio.benchmark.utility.read_conf import convert_yaml_to_callbacks
from minestudio.inference import EpisodePipeline, MineGenerator, InfoBaseFilter

import ray
import numpy as np
import av
import os
from functools import partial
from rich import print

if __name__ == '__main__':
    ray.init()

    resolution = (224, 224)
    
    file_path = "/home/zhwang/workspace/MineStudio/minestudio/benchmark/task_configs/simple/collect_wood.yaml"
    commands_callback, task_callback = convert_yaml_to_callbacks(file_path)
    print(f'Task: {task_callback}')
    print(f'Init commands: {commands_callback}')

    env_generator = partial(
        MinecraftSim,
        obs_size = resolution,
        preferred_spawn_biome = "forest", 
        callbacks = [
            RecordCallback(record_path = "./output", fps = 30, frame_type="pov"),
            SpeedTestCallback(50),
            CommandsCallback(commands_callback),
            DemonstrationCallback("collect_wood")
        ]
    )

    agent_generator = partial(
        load_groot_policy,
        ckpt_path = "/home/zhwang/Desktop/zhancun/jarvisbase/pretrained/groot.ckpt"
    )

    worker_kwargs = dict(
        env_generator=env_generator, 
        agent_generator=agent_generator,
        num_max_steps=1200,
        num_episodes=2,
        tmpdir="./output",
        image_media="h264",
    )

    pipeline = EpisodePipeline(
        episode_generator=MineGenerator(
            num_workers=4,
            num_gpus=0.25,
            max_restarts=3,
            **worker_kwargs, 
        ), 
        episode_filter=InfoBaseFilter(
            key="mine_block",
            val="log",
            num=1,
        ),
    )
    summary = pipeline.run()
    print(summary)