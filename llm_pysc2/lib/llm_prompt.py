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


class BasePrompt:

    def __init__(self):
        self.sp = ''
        self.eip = ''
        self.eop = ''
        self.screen_img_rgb_prompt = ''
        self.screen_img_fea_prompt = ''
        self.minimap_img_rgb_prompt = ''
        self.minimap_img_fea_prompt = ''


class CombatGroupPrompt(BasePrompt):

    def __init__(self, name, log_id, config):
        super(CombatGroupPrompt, self).__init__()
        self.name = name
        self.config = config
        self.log_id = log_id

        # Part 1
        self.sp = f"""
    1. Role Description
     You are a {self.config.AGENTS[self.name]['describe']}.
     In this mission, your primary objective is to leverage the Colossus's ability to traverse between high and low terrain to counter the numerical advantage of 32 Zerglings. Your top priority is to capitalize on this mobility advantage, maneuvering between the two terrains to delay the Zerglings' approach, engage in ranged attacks on pursuing Zerglings, and ensure the survival of the Colossus.

    2.Map Information

      2.1 Coordinate System:
    - The screen coordinate system is a 2D grid with a range of [0, 256] × [0, 256].
    - Each grid cell measures 32 × 32 pixels, resulting in a total of 8 × 8 = 64 grid cells.
    - The origin point (0, 0) is at the top-left corner, while (256, 256) is at the bottom-right corner.

      2.2 Terrain Information:  
    - Pathway (connecting the high ground and low ground):  
      The map consists of an upper platform (high ground) and a lower platform (low ground), connected by a narrow pathway on the left side.

    - High Ground (light green area):  
      The high ground is characterized by light green grass textures and is located on the upper platform.

    - Low Ground (dark gray area):  
      The low ground is characterized by dark gray concrete textures and is located on the lower platform.

    - Impassable Area (black background):  
      The edges of the map consist of a black background, which is impassable. The Colossus must avoid entering these areas.

    - Cliff (light gray vertical surface):  
      The cliff separates the high ground and low ground. The Colossus can freely traverse the cliff, but Zerglings can only access the high ground through the narrow pathway on the left.  
      Only the boundary between the high ground and low ground is considered a cliff; other deep red boundaries are impassable edges of the map.

    - Boundary:  
      The boundaries between the high ground and the black background, as well as between the low ground and the black background, are considered impassable edges of the map.  
      The boundaries are represented by deep red lines on the map.

    3. Key Victory Points:
      3.1 Maintain Maximum Attack Range:
        - Ideally, the Colossus should stay within its maximum attack range (range 7) to fully utilize its long-range attack advantage while minimizing the risk of melee attacks from enemies.
      3.2 Focus Fire on Dense Enemy Clusters:
        - Target the center of the densest enemy groups to maximize splash damage and quickly reduce enemy numbers.
      3.3 Cliff Barrier Delay Effect：

        The Cliff Barrier Delay Effect refers to leveraging the terrain characteristics of cliffs, where enemy units cannot directly cross the cliff, while allied units can freely traverse it. This forces the enemy to take a detour when transitioning between high and low ground, buying time for allied units to reposition, cool down weapons, and strike effectively.

        - When enemies are heavily concentrated on the high ground: 
          - If allied units are also on the high ground but risk being surrounded, it is recommended to retreat to the bottom-right low ground. This utilizes the cliff as a barrier to delay enemy pursuit, enabling ranged attacks on the enemies while maintaining battlefield control.

        - When enemies are heavily concentrated on the low ground: 
          - If allied units are also on the low ground but risk being surrounded, it is recommended to retreat to the top-right high ground. The cliff barrier forces enemies to take a detour, providing time for allied units to reposition and counterattack effectively.

   4. Decision Process  
    Based on the observed data of the Colossus and Zerglings, as well as the RGB image of the screen, use the following decision rules to determine action priorities: 

    4.1 Condition Assessment Rules:  

    - IS_HIGH_GROUND:  
      - Criteria: If the Colossus is on the green high ground (above the cliff, with a clear boundary from the low ground), set to True; otherwise, set to False.  
      - Basis: Determined by verifying the Colossus's position in the green area via RGB image and observation data.  

    - IS_ZERG_HIGH_GROUND:  
      - Criteria: If the Zerglings are on the green high ground (above the cliff, with a clear boundary from the low ground), set to True; otherwise, set to False.  
      - Basis: Determined by analyzing the Zerglings' positions via RGB image.  

    - IS_ZERG_NEAR:  
      - Criteria: If at least 5 Zerglings are within the attack range (≤7) or attempting to surround the Colossus, set to True; otherwise, set to False.  
      - Basis: Determined through observation data (distance and position) and RGB image analysis.  

    - IS_AT_CLIFF:  
      - Condition: If the Colossus is near the edge of a cliff, the condition is True; otherwise, it is False. It is important to distinguish between a cliff and a boundary. When the Colossus is near the red boundary line, it is not considered a cliff. A cliff is the transitional area between the highland and the lowland.  
      - Determination Basis: This is analyzed through the RGB image and the positional information of the Colossus. 

    - IS_COLOSSUS_WEAPON_COOLDOWN:
        - Condition: If the Colossus's weapon cooldown time is greater than 0, the condition is True; otherwise, it is False.  
        - Determination Basis: This is determined by analyzing the Colossus's weapon cooldown time.

    - IS_COLOSSUS_HEALTH_LOW:  
        - Condition: If the Colossus's health is below 60%, this condition is True; otherwise, it is False.  
        - Determination Basis: Determined by observing the Colossus's health.  

    4.2 Action Decision Rules

    - Special Scenarios：
     rule1 ：As long as the weapon is in cooldown, the priority of movement actions is higher than attack actions. Movement > Attack.
     rule2：When the Colossus is about to be surrounded by enemies, regardless of the weapon's status, it should prioritize moving to escape the encirclement.
     rule3：Early Game Phase (<6s), at the start of the game, the Colossus should prioritize moving to the right to increase the distance from the narrow pathway on the left and wait for all Zerglings to reach the high ground. During this phase, movement takes priority over attacking.

    - Situation 1: The Colossus and Zerglings are in different areas

      - Weapon not on cooldown (IS_COLOSSUS_WEAPON_COOLDOWN = False):
        - Priority: Attack. The Colossus should immediately attack enemies, leveraging its ranged advantage to maximize damage.
      - Weapon on cooldown (IS_COLOSSUS_WEAPON_COOLDOWN = True):
        - Priority: Move. The Colossus should create distance from the enemies to avoid being approached and attack once the weapon cooldown ends.

    - Situation 2: The Colossus and Zerglings are in the same area

      - Enemies are near and about to attack (IS_ZERG_NEAR = True, Zerglings approaching):
        - Priority: Move. Regardless of whether the weapon is on cooldown, the Colossus should immediately retreat, quickly creating distance from the enemies to avoid being surrounded. This ensures it can fully leverage its ranged advantage and avoid the disadvantage of close combat. Once out of danger, it can then look for opportunities to counterattack.

      - Enemies are not near (IS_ZERG_NEAR = False):
        - Weapon not on cooldown (IS_COLOSSUS_WEAPON_COOLDOWN = False):
          - Priority: Attack. The Colossus should take the opportunity to attack enemies and weaken their forces.
        - Weapon on cooldown (IS_COLOSSUS_WEAPON_COOLDOWN = True):
          - Priority: Move. The Colossus should reposition to maintain a safe distance while waiting for the weapon cooldown to end.

    - Situation 3 ：When IS_COLOSSUS_HEALTH_LOW = True:
        -Priority Strategy:
            - Avoid direct engagement with Zerglings and maintain maximum attack range.
            - Utilize terrain advantages and adopt hit-and-run tactics, moving flexibly between high and low ground.
            - Priority: Movement > Attack

  5 Integrated Strategy and Decision Framework
    1. Strategy Suggestions

        1.1 Common Game Strategies
            - At the start of the game, the Colossus should first move to the right, keeping its Y-coordinate stable while gradually increasing its X-coordinate. This allows the Colossus to maintain distance from the Zerglings climbing up to the high ground and remain positioned on the high ground to wait for most Zerglings to pass through the narrow pathway on the left. This maneuver prevents the Colossus from descending to the low ground too early, avoiding the risk of being surrounded by Zerglings that have not yet reached the high ground.
            - Once most enemy units have entered the high ground, the Colossus should increase its Y-coordinate to retreat to the low ground via the cliff, avoiding encirclement by Zerglings on the high ground.

        1.2 Emergency Response Strategies:
            - If encircled on the high ground, the Colossus should drastically increase the Y-coordinate to quickly escape the high ground and retreat to the low ground.
            - If encircled on the low ground, the Colossus should drastically decrease the Y-coordinate to quickly escape the low ground and retreat to the high ground.

    2. Movement and Attack Decision

        2.1 When Movement Is Required:

        - Phase Judgment:  
          - Determine the current phase based on game time and the positions of both allied and enemy units.  

        - Evaluate Priorities:  
          - Decide if movement takes priority over attacking (e.g., prioritize movement when the weapon is on cooldown or there is high risk).  

         - Analyze Enemy Movements:  
          - Observe the Zerglings’ movements to predict their attack paths.  
          - Use the RGB image and the Cliff Barrier Delay Effect to choose the safest movement path (e.g., move down-right or up-right).  

        - Analyze Movement Along X and Y Axes:  
          - X-Axis Movement:  
            - Increase X value (move right): Create distance from the left-side pathway and maintain horizontal spacing from Zerglings.  
            - Decrease X value (move left): Rarely recommended unless repositioning to a strategic location.  
          - Y-Axis Movement:  
            - Decrease Y value (move upward): Retreat from the low ground to the high ground, leveraging the cliff to block enemies.  
            - Increase Y value (move downward): Retreat from the high ground to the low ground to delay enemy advances.  


        2.2 When Attacking Is Required:

        - Target Selection:  
          - Prioritize the densest groups of enemies to maximize splash damage.  
          - Focus fire on high-health enemy units that pose the greatest threat to the Colossus.  

        - Determine the Best Attack Point:  
          - Aim for the densest clusters of Zerglings to reduce their numbers and weaken their combat strength.  

  6.Analysis:
    In your response, please follow the format outlined in the example output, including section titles, numbering, and the terminology used. Ensure that you use the same variable names and terms specified in the decision process and chain of thought.

    The output should include:

      1. Decision Process

         1.1 Condition Assessment:

           - `IS_COLOSSUS_HIGH_GROUND = True/False`
           - `IS_ZERGLING_HIGH_GROUND = True/False`
           - `IS_ZERGLING_NEAR_COLOSSUS = True/False`
           - `IS_COLOSSUS_AT_CLIFF = True/False`
           - `IS_COLOSSUS_WEAPON_COOLDOWN = True/False`
           - `IS_COLOSSUS_HEALTH_LOW = True/False'

         1.2 Action Decision Rules Brief Recap
             - Special Scenario： 
               - When the weapon is on cooldown: Move > Attack  
               - When encirclement is imminent, prioritize movement to escape, regardless of weapon cooldown status.
               - Early game (<6s), prioritize moving right to distance from the left pathway and wait for Zerglings on the high ground; movement > attack.            

            - Scenario 1: The Colossus and Zerglings are in different areas  
               - Weapon not on cooldown: Prioritize attacking, leveraging range advantage to maximize damage.  
               - Weapon on cooldown: Prioritize moving to create distance, then attack after cooldown ends.

            - Scenario 2: The Colossus and Zerglings are in the same area  
               - Enemies are close: Prioritize moving to avoid melee combat, then counterattack.  
               - Enemies are not close:  
                 - Weapon not on cooldown: Prioritize attacking to weaken enemy forces.  
                 - Weapon on cooldown: Prioritize moving to maintain a safe distance.  

            - Scenario 3: The Colossus is low on health (IS_COLOSSUS_HEALTH_LOW = True)  
               - Enemies are close:  
                 - Prioritize moving to avoid direct engagement, leveraging terrain to create distance and delay pursuit.  
                 - Once a safe position is reached, counterattack cautiously while maintaining maximum attack range.  
               - Enemies are not close:  
                 - Weapon not on cooldown: Focus on targeting the densest enemy clusters from a safe position to reduce their numbers.  
                 - Weapon on cooldown: Continue repositioning to maintain distance and avoid being flanked.  

         1.3 Judgment Based on 4.2 Action Decision Rules:

            -Provide movement and attack priorities, e.g., attack > move or move > attack.
            -Note:
                -Special rules, Scenario 1, Scenario 2, or Scenario 3 should align with only one scenario that best fits the current situation.
                -Always prioritize special rules (such as weapon cooldown or imminent encirclement). If none apply, proceed to select an action rule based on Scenario 1, Scenario 2, or Scenario 3.

      2 Integrated Strategy and Decision Framework

        2.1 Strategy Suggestions

       - Current Phase Determination:
           Dynamically determine the strategy based on time, the Colossus’s position, and Zergling distribution. Key factors include time range, the Colossus’s X/Y coordinates, and enemy movement trends.            

       - Consider Common Action Recommendations::

        - Early Game Observation Phase: Initially, keep the X-coordinate steady while gradually increasing the Y-coordinate to monitor enemy movements. Utilize the Colossus’s range advantage to weaken enemy forces.
        - Emergency Evacuation Phase:
            - Encircled on High Ground: The Colossus should drastically increase the Y-coordinate to quickly retreat to the low ground and escape the encirclement.
            - Encircled on Low Ground: The Colossus should drastically decrease the Y-coordinate to swiftly return to the high ground and avoid threats.
        - Late-Game Kite-and-Pull Phase: In the late game, the Colossus should maneuver flexibly near the cliff, leveraging the terrain to force enemy repositioning. Focus on ranged attacks to weaken enemy forces and maintain control of the battlefield.

        2.2 Movement Decision Analysis

        - Enemy Approach Path Prediction:  
          Analyze the primary approach paths of enemy units and identify potential threats.  

        - Movement Target Suggestions:  
          List multiple candidate movement points, including defensive positions on the high ground, safe retreat points on the low ground, and avoidance points.  
          Specify the most suitable movement target (e.g., a safe spot on the high ground or near the cliff on the low ground).  
          Explain the reasoning behind the selection (e.g., reducing the risk of being surrounded or gaining a better position for attacks).  

        2.3 Attack Decision Analysis

        - Target Prioritization:  
          Prioritize attacking dense enemy clusters to maximize splash damage.  
          If threatening units are approaching, prioritize targeting those closest to the Colossus to ensure its safety.  

        - Attack Target Selection:  
          Identify multiple candidate attack points (e.g., the center of a dense enemy group or the closest group to the Colossus).  
          Specify the optimal attack point and provide reasoning (e.g., to maximize damage or avoid being overwhelmed).


    7.Action Output：
        Team Colossus-1:
          Action steps.
    """

        self.eip = \
            """
        Game Info
          Time: 0:05

        Team Colossus-1 Info:
          Team minimap position: [31, 27]
          Controlled Team Units:
                Unit: Colossus, Tag: 0x100000001, ScreenPos: [150, 123], Health: 350 (100%), Weapon Cooldown Time: 0.91s 
          Nearby Enemy Units:
                Unit: Zergling, Tag: 0x1002c0001, ScreenPos: [52, 164], Distance: 10, Health: 6 (17%)
                Unit: Zergling, Tag: 0x100180001, ScreenPos: [79, 159], Distance: 7, Health: 35 (100%)
                Unit: Zergling, Tag: 0x100440001, ScreenPos: [112, 140], Distance: 4, Health: 35 (100%)
                Unit: Zergling, Tag: 0x100640001, ScreenPos: [38, 176], Distance: 12, Health: 21 (60%)
                Unit: Zergling, Tag: 0x100700001, ScreenPos: [52, 178], Distance: 11, Health: 35 (100%)
                Unit: Zergling, Tag: 0x100780001, ScreenPos: [42, 169], Distance: 11, Health: 6 (17%)
                Unit: Zergling, Tag: 0x100540001, ScreenPos: [49, 171], Distance: 11, Health: 35 (100%)
                Unit: Zergling, Tag: 0x100500001, ScreenPos: [91, 146], Distance: 6, Health: 35 (100%)
                Unit: Zergling, Tag: 0x100800001, ScreenPos: [83, 147], Distance: 7, Health: 35 (100%)
                Unit: Zergling, Tag: 0x100280001, ScreenPos: [96, 151], Distance: 6, Health: 21 (60%)
                Unit: Zergling, Tag: 0x1000c0001, ScreenPos: [59, 162], Distance: 9, Health: 35 (100%)
                Unit: Zergling, Tag: 0x100040001, ScreenPos: [93, 157], Distance: 6, Health: 35 (100%)
                Unit: Zergling, Tag: 0x100340001, ScreenPos: [67, 172], Distance: 9, Health: 35 (100%)
                Unit: Zergling, Tag: 0x1001c0001, ScreenPos: [72, 161], Distance: 8, Health: 6 (17%)
                Unit: Zergling, Tag: 0x100600001, ScreenPos: [76, 152], Distance: 7, Health: 35 (100%)
                Unit: Zergling, Tag: 0x100140001, ScreenPos: [86, 162], Distance: 7, Health: 35 (100%)
                Unit: Zergling, Tag: 0x1004c0001, ScreenPos: [117, 145], Distance: 3, Health: 35 (100%)
                Unit: Zergling, Tag: 0x100400001, ScreenPos: [66, 164], Distance: 9, Health: 21 (60%)
                Unit: Zergling, Tag: 0x100200001, ScreenPos: [78, 166], Distance: 8, Health: 35 (100%)
                Unit: Zergling, Tag: 0x100240001, ScreenPos: [104, 144], Distance: 5, Health: 35 (100%)
                Unit: Zergling, Tag: 0x100100001, ScreenPos: [59, 172], Distance: 10, Health: 35 (100%)
                Unit: Zergling, Tag: 0x1003c0001, ScreenPos: [86, 154], Distance: 7, Health: 6 (17%)
                Unit: Zergling, Tag: 0x100480001, ScreenPos: [46, 159], Distance: 11, Health: 35 (100%)
                Unit: Zergling, Tag: 0x1006c0001, ScreenPos: [69, 155], Distance: 8, Health: 35 (100%)
                Unit: Zergling, Tag: 0x100580001, ScreenPos: [59, 154], Distance: 9, Health: 6 (17%)
                Unit: Zergling, Tag: 0x100740001, ScreenPos: [130, 134], Distance: 2, Health: 35 (100%)
                Unit: Zergling, Tag: 0x1005c0001, ScreenPos: [97, 142], Distance: 5, Health: 35 (100%)
                Unit: Zergling, Tag: 0x100380001, ScreenPos: [39, 183], Distance: 12, Health: 35 (100%)
                Unit: Zergling, Tag: 0x100080001, ScreenPos: [106, 151], Distance: 5, Health: 35 (100%)
                Unit: Zergling, Tag: 0x100300001, ScreenPos: [124, 137], Distance: 2, Health: 35 (100%)

            Relevant Knowledge:
                Protoss.Colossus
                    The large quad-legged vehicle fires lasers in a splash pattern well-suited to destroying swarms of weaker units. This unit can also traverse differences in terrain height due to its long legs, and will appear to step over ledges and other obstacles due to the inverse kinematics system.
                    Unit properties: ['ground', 'air', 'armored', 'massive', 'mechanical']
                    Weapon info: Attack Range 7, target: ['ground'], anti: ['light'], DPS(damage per second) 13, DPS-anti 20
                    Unit abilities:

                Zerg.Zergling
                    Fast but weak melee attacker ideal for swarming attacks in large numbers.
                    Unit properties: ['ground', 'light', 'biological']
                    Weapon info: Attack Range 1, target: ['ground'], DPS(damage per second) 10


            Valid Actions:
                Team Colossus-1 Valid Actions:
                    <Attack_Unit(tag)>
                    <Move_Screen(screen)>

            Action Args:
                (1) tag: tag refers to a hexadecimal number, shape as 0x000000000.
                (2) screen: screen refers to a screen coordinate, shape as [x, y], where x and y range from 0 to 256.
                (3) minimap: minimap refers to a minimap coordinate, shape as [x, y], where x and y range from 0 to 64.

            For example, when you want to use an action like <Action_Name(tag, screen)>, you should output like <Action_Name(0x100580001, [37, 55])>; when you want to use an action like <Action_Name(screen)>, you should output like <Action_Name([66, 78])>. Make sure to see whether an action uses screen coordinates or minimap coordinates. If an action name is XXXX_Screen, it uses screen coordinates; if an action name is XXXX_Minimap, it uses minimap coordinates.

            Last Step Actions:
                Team Colossus-1:
                    <Move_Screen([160, 130])>
                    <Attack_Unit(0x1007c0001)>
                    <Attack_Unit(0x100740001)>

            You need to confirm whether the previous action finished executing, and based on this, determine whether to continue the old strategy or immediately take other actions.

            Give each team no more than 2 actions, among which activity release should usually before move and attack.
            Now, start generating your analysis and actions:
            """

        self.eop = \
            """
Analysis:

1. Decision Process

    1.1 Condition Assessment

        - IS_COLOSSUS_HIGH_GROUND = True
           The Colossus is currently on the high ground, confirmed via the image and coordinates.
        - IS_ZERGLING_HIGH_GROUND = True
           Zerglings are primarily concentrated on the high ground, in the same area as the Colossus.
        - IS_ZERGLING_NEAR_COLOSSUS = True
           Multiple Zerglings are close to the Colossus and within its attack range (≤7), posing an immediate threat.
        - IS_COLOSSUS_AT_CLIFF = False
           The Colossus is near the red boundary of the map, not near the cliff (the border between green and gray areas).
        - IS_COLOSSUS_WEAPON_COOLDOWN = True
           The weapon is on cooldown and cannot immediately attack enemy units.
        - IS_COLOSSUS_HEALTH_LOW = False  
           The Colossus's health is at 100%, with no low-health threat.

    1.2 Action Decision Rules 

     Decision basis:
        1. Special Rules:
            - When the weapon is on cooldown, movement takes precedence over attack.
            - When surrounded or under close threat, prioritize movement to escape danger.

        2. Scenario Analysis:
            - Current scenario: The Colossus and Zerglings are in the same area, with Zerglings approaching the Colossus:
                - The weapon is currently on cooldown, and the large number of fast-approaching Zerglings necessitates movement to avoid being surrounded and to create safe distance.
            - Terrain condition:
                - Being close to the red boundary of the map limits the Colossus’s maneuverability, further highlighting the importance of movement.

    1.3 Judgment Based on Action Decision Rules
    - Prioritize matching the special rule: Weapon cooldown (Move > Attack). The current scenario matches the special rule, prioritizing movement to retreat, avoid being surrounded, and gain time for the weapon cooldown.
    - Move > Attack
        The high ground space is insufficient, and with enemies advancing and the weapon on cooldown, the Colossus must immediately retreat to the low ground, using the cliff to delay Zergling pursuit and buy time for the cooldown.                   

2. Integrated Strategy and Decision Framework

    2.1 Strategy Suggestions

       Current Strategy: Emergency Retreat to Low Ground
        - The Colossus and Zerglings are both on the high ground. Given the large number of enemies and their proximity, the situation is critical.
        - The Colossus must quickly retreat to the low ground (gray area), using the cliff barrier to delay Zerglings' pursuit. This retreat will buy time for the weapon to cool down and create a safe distance to regain battlefield control.                

    2.2 Movement Decision Analysis

     -Enemy Approach Path Prediction
        - Zerglings are advancing from the left pathway on the high ground, attempting to encircle the Colossus.
        - If the Colossus does not retreat immediately, it risks being cornered near the red boundary, losing space to maneuver.

     - Movement Target Suggestions
        - Retreat directly to screen coordinates [160, 200], a safe area near the cliff on the low ground.
        - Crossing the cliff to the low ground will delay Zerglings' pursuit, providing more survival space and reducing the risk of melee attacks.

     - Reason:
        - Directly retreating to the low ground avoids encirclement by Zerglings. The cliff barrier delays enemy pursuit, ensuring the Colossus's safety.

    2.3 Attack Decision Analysis

        - Target Prioritization:
            - Once the weapon cooldown ends, prioritize attacking the nearest Zerglings to reduce immediate threats and maximize splash damage.

        - Attack Target Selection:
            - The closest Zerglings (e.g., Zergling, Tag: 0x1004c0001 and 0x100740001) pose a direct threat to the Colossus.
            - After repositioning on the low ground, prioritize attacking dense clusters of pursuing Zerglings.

3 .Actions:
    Team Colossus-1:
        <Move_Screen([160, 200])> # Retreat directly from the high ground to the low ground, avoiding Zergling encirclement and using the cliff to delay pursuit.
        <Attack_Unit(0x1004c0001)> # After the weapon cooldown ends, prioritize attacking the nearest Zergling to reduce the threat.
        <Attack_Unit(0x100740001)> # Continue attacking other nearby Zerglings, using splash damage to weaken the enemy forces.
                """

        # Part 2
        if self.config.ENABLE_COMMUNICATION:
            self.sp += \
                """
                4.Communication Output
                  If there is Available Communicate Target, you should keep communicating with them by Communication functions. For example, if 'Commander' and 'CombatGroup4' in Available Communicate Target, you can output as:

                  Communications:
                    <MessageTo(Commander, '''xxxxxxxxxx''')>
                    <MessageTo(CombatGroup4, '''xxxxxxxxxx''')>
                """
            self.eip += \
                """
                Communication:
                  From Commander: 
                    Your task is to attack the enemy workers of an enemy base near minimap [48,32]. Intelligence shows that two enemy Queens are located on the minimap [44,32]. Try to avoid being detected by enemy Queens before arriving.

                Available Communication Tragets:
                  Commander: Protoss military supreme commander. Responsible for making macro decision through communication, and controls nexus for massrecall for tactical objectives.
                Available Communication Functions:
                  <MessageTo(AgentName, message)>
                  <MessageTo(ChannelName, message)>
                  <ListenTo(ChannelName)>
                Args explanation:
                  (1)AgentName: refers to a name mentioned in Available Communication Tragets.
                  (2)ChannelName: shape as Channel-i, i refers to an integer.
                  (2)message: any text wrapped between ''' and '''.
                """
            self.eop += \
                """
                Communications:
                    <MessageTo(Commander, '''Copy that, we have arrived enemy base, and started attack enemy workers''')>
                """

        # Part 3
        self.eip += \
            f"""
Give each team no more than {self.config.MAX_NUM_ACTIONS} actions.
Now, start generating your analysis and actions:
"""


class CommanderPrompt(BasePrompt):  # TODO: Design a prompt specifically for the supreme military commander
    def __init__(self, name, log_id, config):
        super(CombatGroupPrompt, self).__init__()
        self.name = name
        self.config = config
        self.log_id = log_id
        # self.sp = ''
        # self.eip = ''
        # self.eop = ''


class DeveloperPrompt(BasePrompt):  # TODO: Design a prompt specifically for the supreme logistics commander
    def __init__(self, name, log_id, config):
        super(CombatGroupPrompt, self).__init__()
        self.name = name
        self.config = config
        self.log_id = log_id
        # self.sp = ''
        # self.eip = ''
        # self.eop = ''


PROTOSS_FACTORY = {
    'default': CombatGroupPrompt,
    'commander': CommanderPrompt,
    'developer': DeveloperPrompt,
}
TERRAN_FACTORY = {}
ZERG_FACTORY = {}

FACTORY = {
    'protoss': PROTOSS_FACTORY,
    'terran': TERRAN_FACTORY,
    'zerg': ZERG_FACTORY,
}

if __name__ == "__main__":
    from llm_pysc2.agents.configs.config import ProtossAgentConfig

    config = ProtossAgentConfig()
    prompt = CombatGroupPrompt('CombatGroup1', log_id=0, config=config)

    print("--" * 25 + "System Prompt" + "--" * 25)
    print(prompt.sp)
    print("--" * 25 + "Example Input Prompt" + "--" * 25)
    print(prompt.eip)
    print("--" * 25 + "Example Output Prompt" + "--" * 25)
    print(prompt.eop)

    # print("=====" * 10)
    # # 从 FACTORY 中获取种族工厂字典
    # race_factory = FACTORY['protoss']
    # # 从种族工厂字典中获取提示词类
    # prompt_class = race_factory['default']
    #
    # # 准备实例化所需的参数
    # name = 'CombatGroup1'  # 代理名称
    # log_id = 0  # 日志 ID
    # config = ProtossAgentConfig()  # 配置对象，根据需要导入和实例化
    #
    # # 实例化提示词类
    # prompt_instance = prompt_class(name, log_id, config)
    # # 访问提示词内容
    # system_prompt = prompt_instance.sp
    # example_input_prompt = prompt_instance.eip
    # example_output_prompt = prompt_instance.eop
    #
    # # 输出或使用提示词
    # print(system_prompt)
    # print(example_input_prompt)
    # print(example_output_prompt)

