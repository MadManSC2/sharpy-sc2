from sc2 import BotAI, UnitTypeId, Race
from sc2.ids.upgrade_id import UpgradeId

from sharpy.knowledges import KnowledgeBot
from sharpy.plans import BuildOrder, Step, SequentialList, StepBuildGas
from sharpy.plans.acts import *
from sharpy.plans.acts.protoss import *
from sharpy.plans.require import *
from sharpy.plans.tactics import *
from sc2.position import Point2

import random
import numpy as np
import time

scout_data = []
#TODO: Solve it without using a global variable


class GetScoutingData(ActBase):
    def __init__(self):
        super().__init__()
        self.build_order = -1

    async def start(self, knowledge: 'Knowledge'):
        await super().start(knowledge)

    async def execute(self) -> bool:

        global scout_data

        if self.build_order == -1:
            scout_data = [
                self.knowledge.enemy_start_location,
                self.knowledge.enemy_race,
                self.knowledge.possible_rush_detected,
                # self.ai.enemy_structures,
                # self.knowledge.known_enemy_structures,
                self.knowledge.known_enemy_units,
                self.knowledge.known_enemy_workers,
                self.knowledge.lost_units_manager.own_lost_type(UnitTypeId.GATEWAY),
                self.knowledge.game_analyzer.enemy_mineral_income,
                self.knowledge.game_analyzer.enemy_gas_income,
                self.knowledge.game_analyzer.enemy_power.power,
                self.knowledge.game_analyzer.enemy_predict_power.power,
                self.knowledge.game_analyzer.our_power.power,
                self.knowledge.enemy_army_predicter.own_value,
                self.knowledge.enemy_army_predicter.enemy_value,
                self.knowledge.enemy_army_predicter.enemy_mined_minerals,
            ]

            self.build_order = 1 #random.randrange(0, 2)

            print(scout_data)
            print(self.build_order)

            return True
        else:
            return True


class MadAI(KnowledgeBot):

    def __init__(self):
        super().__init__("MadAI")
        self.proxy_location = None
        self.train_data = []
        global scout_data
        self.scout = GetScoutingData()

    async def start(self, knowledge: 'Knowledge'):
        await super().start(knowledge)

    def on_end(self, game_result):
        print("OnGameEnd() was called.")
        if str(game_result) == "Result.Victory":
            print(scout_data)
            self.train_data.append(
                [
                    self.scout.build_order,
                    scout_data[0][0]+scout_data[0][1],
                ]
            )

            np.save("data/{}.npy".format(str(int(time.time()))), np.array(self.train_data))

    async def create_plan(self) -> BuildOrder:
        # Common Start Build Order
        #TODO: Improve timings to meet: https://lotv.spawningtool.com/build/87940/
        return BuildOrder([
            Step(None, ChronoUnitProduction(UnitTypeId.PROBE, UnitTypeId.NEXUS),
                 skip=RequiredUnitExists(UnitTypeId.PROBE, 40, include_pending=True), skip_until=RequiredUnitExists(UnitTypeId.ASSIMILATOR, 1)),
            SequentialList([
                ActUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS, 14),
                GridBuilding(UnitTypeId.PYLON, 1),
                Step(RequiredUnitExists(UnitTypeId.PYLON, 1, include_pending=False), WorkerScout()),
                ActUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS, 16),
                StepBuildGas(1),
                GridBuilding(UnitTypeId.GATEWAY, 1),
                GridBuilding(UnitTypeId.CYBERNETICSCORE, 1),
                ActUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS, 18),
                Step(None, self.scout, skip_until=RequiredUnitReady(UnitTypeId.CYBERNETICSCORE, 1),
                     skip=RequiredUnitExists(UnitTypeId.STALKER, 1, include_pending=True)),
            ]),
            Step(lambda k: self.scout.build_order == 0, self.two_base_stalker()),
            Step(lambda k: self.scout.build_order == 1, self.four_gate()),
            SequentialList([
                PlanZoneDefense(),
                RestorePower(),
                PlanDistributeWorkers(),
                PlanZoneGather(),
                Step(RequiredUnitReady(UnitTypeId.GATEWAY, 4), PlanZoneAttack(4)),
                PlanFinishEnemy(),
            ])
        ])

    def four_gate(self) -> ActBase:
        #TODO: Improve Timings, Chrono Warpgate, Gather at Proxy-Pylon, Add 1-2 Sentries
        self.knowledge.print(f"4-Gate", "Build")
        natural = self.knowledge.expansion_zones[-3]
        pylon_pos: Point2 = natural.behind_mineral_position_center
        return BuildOrder([
            SequentialList([
                GridBuilding(UnitTypeId.GATEWAY, 2),
                BuildPosition(UnitTypeId.PYLON, pylon_pos, exact=False,
                              only_once=True),
                BuildOrder(
                    [
                        AutoPylon(),
                        ActUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS, 20),
                        ActTech(UpgradeId.WARPGATERESEARCH, UnitTypeId.CYBERNETICSCORE),
                        GridBuilding(UnitTypeId.GATEWAY, 3),
                        ActUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS, 22),
                        [
                            ProtossUnit(UnitTypeId.STALKER, 50),
                            ProtossUnit(UnitTypeId.ZEALOT, 50),
                            ProtossUnit(UnitTypeId.SENTRY, 10)
                        ],
                        StepBuildGas(2),
                        Step(RequiredUnitExists(UnitTypeId.CYBERNETICSCORE, 1), GridBuilding(UnitTypeId.GATEWAY, 4))
                    ])
            ]),
            ChronoUnitProduction(UnitTypeId.STALKER, UnitTypeId.GATEWAY)
        ])

    def two_base_stalker(self) -> ActBase:
        #TODO: Add Proxy-Pylon, Chrono Tech, Research Blink, Add 1-2 Sentries with Guardian Shield
        self.knowledge.print(f"2-Base Stalker", "Build")
        return BuildOrder([
            SequentialList([
                ActExpand(2),
                ActUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS, 21),
                StepBuildGas(2),
                ActUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS, 22),
                GridBuilding(UnitTypeId.PYLON, 1),
                BuildOrder(
                    [
                        AutoPylon(),
                        ActTech(UpgradeId.WARPGATERESEARCH, UnitTypeId.CYBERNETICSCORE),
                        [
                            ActUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS, 22),
                            Step(RequiredUnitExists(UnitTypeId.NEXUS, 2),
                                 ActUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS, 44)),
                            StepBuildGas(3, skip=RequiredGas(300))
                        ],
                        [
                            GateUnit(UnitTypeId.STALKER, 100)
                        ],
                        [
                            GridBuilding(UnitTypeId.GATEWAY, 7),
                            StepBuildGas(4, skip=RequiredGas(200)),
                        ]
                    ])
            ]),
        ])


class LadderBot(MadAI):
    @property
    def my_race(self):
        return Race.Protoss
