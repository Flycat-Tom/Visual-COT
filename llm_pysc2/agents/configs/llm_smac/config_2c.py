# Copyright 2024, LLM-PySC2 Contributors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from llm_pysc2.agents.configs.config import ProtossAgentConfig
from llm_pysc2.lib.llm_action import *


class ConfigSmac_2c(ProtossAgentConfig):

  def __init__(self):
    super(ConfigSmac_2c, self).__init__()
    self.ENABLE_INIT_STEPS = False
    self.ENABLE_AUTO_WORKER_MANAGE = False
    self.ENABLE_AUTO_WORKER_TRAINING = False

    # self.LLM_SIMULATION_TIME = 0
    # self.MAX_LLM_QUERY_TIMES = 5
    # self.MAX_LLM_WAITING_TIME = 10
    # self.MAX_LLM_RUNTIME_ERROR_TIME = 30
    # self.MAX_LLM_DECISION_FREQUENCY = 1
    # self.MAX_NUM_ACTIONS = 3

    self.AGENTS_ALWAYS_DISABLE = []
    self.AGENTS = {
      'CombatGroupSmac': {
        'describe': "Please analyze the situation based on the visual information provided, make informed decisions, and ensure our victory." ,
        'llm': {
          'basic_prompt': self.basic_prompt,
          'translator_o': self.translator_o,
          'translator_a': self.translator_a,
          'img_fea': self.ENABLE_IMAGE_FEATURE,
          'img_rgb': self.ENABLE_IMAGE_RGB,
          'model_name': self.model_name,
          'api_base': self.api_base,
          'api_key': self.api_key,

          'screen_rgb_prompt':'',
          # 'screen_rgb_prompt': '''
          #           Analyze the image from the following four angles:
          #
          # 1. **Unit Identification**:
          #    - Distinguish between friendly and enemy units based on color.
          #    - Use grid coordinates to locate both sides' units.
          #
          # 2. **Tactical Analysis**:
          #    - Assess whether our units are on higher ground or in an advantageous position.
          #    - Based on this, decide whether to attack, retreat, or hold the position.
          #
          # 3. **Action Decision**:
          #    - Prioritize attacking the nearest enemy unit based on positions and distances.
          #    - Monitor for enemy reinforcements and decide whether to retreat or continue attacking.
          #
          # 4. **Skill Usage**:
          #    - Use unit skills (control, support, etc.) wisely to maximize tactical effectiveness.
          #
          # Once the analysis is complete, generate specific action commands for each team unit based on the observations and apply them.
          # ''',
        },
        'team': [
          {'name': 'Colossus-1', 'unit_type': [units.Protoss.Colossus],
           'game_group': 1, 'select_type': 'group'},
          # {'name': 'Colossus-2', 'unit_type': [units.Protoss.Colossus],
          #  'game_group': 2, 'select_type': 'group'},
        ],
        'action': {
          units.Protoss.Colossus: PROTOSS_BASIC_ACTION_SMAC2,
        },
      },
    }
