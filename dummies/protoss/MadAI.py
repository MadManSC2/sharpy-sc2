from sc2 import BotAI, UnitTypeId, AbilityId, Race
from sc2.ids.upgrade_id import UpgradeId

from sharpy.knowledges import KnowledgeBot
from sharpy.plans import BuildOrder, Step, SequentialList, StepBuildGas
from sharpy.plans.acts import *
from sharpy.plans.acts.protoss import *
from sharpy.plans.require import *
from sharpy.plans.tactics import *
from sc2.position import Point2
from sc2.constants import RALLY_UNITS

import random
import numpy as np
import time


class GetScoutingData(ActBase):
    def __init__(self):
        super().__init__()
        self.build_order = -1
        self.scout_data = []

    async def start(self, knowledge: 'Knowledge'):
        await super().start(knowledge)

    async def execute(self) -> bool:

        if self.build_order == -1:
            self.scout_data = [
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

            self.build_order = 2 #random.randrange(0, 2)
            print(self.scout_data)
            print(self.build_order)

            if self.build_order == 0:
                await self.ai.chat_send(
                    "(glhf) MadAI v3.0: 2-Base Blink-Stalker BO chosen!"
                )
            elif self.build_order == 1:
                await self.ai.chat_send(
                    "(glhf) MadAI v3.0: 4-Gate Proxy BO chosen!"
                )
            elif self.build_order == 2:
                await self.ai.chat_send(
                    "(glhf) MadAI v3.0: Rush Defend BO chosen!"
                )
            else:
                await self.ai.chat_send(
                    "(glhf) MadAI v3.0: No BO chosen! PANIC!"
                )

            return True
        else:
            return True


class Dt_Harass(ActBase):
    def __init__(self):
        super().__init__()

    async def execute(self) -> bool:
        # Start dark templar attack
        if self.cache.own(UnitTypeId.DARKTEMPLAR).exists:
            dt1 = self.cache.own(UnitTypeId.DARKTEMPLAR)[0]
            self.do(
                dt1(
                    RALLY_UNITS,
                    self.knowledge.enemy_start_location.towards(self.ai.game_info.map_center, random.randrange(-5, -1)),
                )
            )
            enemy_workers = self.knowledge.known_enemy_units.of_type(
                [UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.DRONE, UnitTypeId.MULE])
            for dt in self.cache.own(UnitTypeId.DARKTEMPLAR).idle:
                if self.knowledge.known_enemy_structures.of_type(UnitTypeId.SPORECRAWLER).exists:
                    self.do(
                        dt.attack(
                            self.knowledge.known_enemy_structures.of_type(UnitTypeId.SPORECRAWLER).closest_to(dt.position)
                        )
                    )
                elif enemy_workers.exists:
                    self.do(
                        dt.attack(
                            enemy_workers.closest_to(dt.position)
                        )
                    )
                else:
                    self.do(dt.attack(self.knowledge.enemy_start_location))

        return True


class MadAI(KnowledgeBot):

    def __init__(self):
        super().__init__("MadAI")
        self.proxy_location = None
        self.train_data = []
        self.scout = GetScoutingData()

    async def start(self, knowledge: 'Knowledge'):
        await super().start(knowledge)

    def on_end(self, game_result):
        print("OnGameEnd() was called.")
        if str(game_result) == "Result.Victory":
            print(self.scout.scout_data)
            self.train_data.append(
                [
                    self.scout.build_order,
                    self.scout.scout_data[0][0]+self.scout.scout_data[0][1],
                ]
            )

            np.save("data/{}.npy".format(str(int(time.time()))), np.array(self.train_data))

    async def create_plan(self) -> BuildOrder:
        # Common Start Build Order
        #TODO: Implement more BOs
        #TODO: Build second pylon at reaper ramp against Terran
        return BuildOrder([
            Step(None, ChronoUnitProduction(UnitTypeId.PROBE, UnitTypeId.NEXUS),
                 skip=RequiredUnitExists(UnitTypeId.PROBE, 19, include_pending=True), skip_until=RequiredUnitReady(UnitTypeId.PYLON, 1)),
            SequentialList([
                ActUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS, 14),
                GridBuilding(UnitTypeId.PYLON, 1),
                ActUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS, 15),
                Step(RequiredUnitExists(UnitTypeId.PYLON, 1, include_pending=False), WorkerScout()),
                GridBuilding(UnitTypeId.GATEWAY, 1),
                ActUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS, 16),
                StepBuildGas(1),
                ActUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS, 18),
                GridBuilding(UnitTypeId.PYLON, 2),
                ActUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS, 20),
                StepBuildGas(2),
                ActUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS, 21),
                GridBuilding(UnitTypeId.CYBERNETICSCORE, 1),
                GateUnit(UnitTypeId.ZEALOT, 1),
                ActUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS, 23),
                Step(None, self.scout, skip_until=RequiredUnitExists(UnitTypeId.CYBERNETICSCORE, 1), skip=RequiredUnitReady(UnitTypeId.CYBERNETICSCORE))
            ]),
            Step(lambda k: self.scout.build_order == 0, self.two_base_stalker()),
            Step(lambda k: self.scout.build_order == 1, self.four_gate()),
            Step(lambda k: self.scout.build_order == 2, self.defend()),
            SequentialList([
                PlanZoneDefense(),
                RestorePower(),
                PlanDistributeWorkers(),
            ])
        ])

    def four_gate(self) -> ActBase:
        #TODO: Adapt Unit Composition, Follow-up BO
        natural = self.knowledge.expansion_zones[-3]
        pylon_pos: Point2 = natural.behind_mineral_position_center
        return BuildOrder([
            SequentialList([
                GridBuilding(UnitTypeId.GATEWAY, 2),
                BuildOrder(
                    [
                        AutoPylon(),
                        ActTech(UpgradeId.WARPGATERESEARCH, UnitTypeId.CYBERNETICSCORE),
                        GateUnit(UnitTypeId.STALKER, 1, priority=True),
                        GridBuilding(UnitTypeId.GATEWAY, 3),
                        BuildPosition(UnitTypeId.PYLON, pylon_pos, exact=False,
                                      only_once=True),
                        GridBuilding(UnitTypeId.GATEWAY, 4),
                        [
                            Step(None, ProtossUnit(UnitTypeId.SENTRY, 1),
                                 skip_until=RequiredUnitExists(UnitTypeId.STALKER, 2, include_pending=True)),
                            Step(None, ProtossUnit(UnitTypeId.SENTRY, 2),
                                 skip_until=RequiredUnitExists(UnitTypeId.STALKER, 6, include_pending=True)),
                            Step(None, ProtossUnit(UnitTypeId.STALKER, 50)),
                        ],
                    ])
            ]),
            SequentialList([
                ChronoTech(AbilityId.RESEARCH_WARPGATE, UnitTypeId.CYBERNETICSCORE),
                ChronoUnitProduction(UnitTypeId.STALKER, UnitTypeId.GATEWAY),
            ]),
            SequentialList([
                Step(RequiredUnitReady(UnitTypeId.GATEWAY, 4), PlanZoneGather()),
                Step(RequiredUnitReady(UnitTypeId.STALKER, 4), PlanZoneAttack(12)),
                PlanFinishEnemy(),
            ])
        ])

    def two_base_stalker(self) -> ActBase:
        #TODO: Adapt Unit Composition, Improve Timings
        natural = self.knowledge.expansion_zones[-3]
        pylon_pos: Point2 = natural.behind_mineral_position_center
        return BuildOrder([
            SequentialList([
                ActExpand(2),
                BuildOrder(
                    [
                        AutoPylon(),
                        ActTech(UpgradeId.WARPGATERESEARCH, UnitTypeId.CYBERNETICSCORE),
                        [
                            Step(RequiredUnitExists(UnitTypeId.NEXUS, 2),
                                 ActUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS, 44)),
                            StepBuildGas(3, skip=RequiredGas(300)),
                            StepBuildGas(4, skip=RequiredGas(200)),
                        ],
                        [
                            Step(None, ProtossUnit(UnitTypeId.SENTRY, 1),
                                 skip_until=RequiredUnitExists(UnitTypeId.STALKER, 2, include_pending=True)),
                            Step(None, ProtossUnit(UnitTypeId.SENTRY, 2),
                                 skip_until=RequiredUnitExists(UnitTypeId.STALKER, 6, include_pending=True)),
                            Step(None, ProtossUnit(UnitTypeId.STALKER, 100)),
                        ],
                        [
                            Step(RequiredUnitReady(UnitTypeId.GATEWAY, 3),
                                 BuildPosition(UnitTypeId.PYLON, pylon_pos, exact=False, only_once=True))
                        ],
                        SequentialList([
                            GridBuilding(UnitTypeId.GATEWAY, 4),
                            Step(RequiredUnitReady(UnitTypeId.CYBERNETICSCORE, 1),
                                 GridBuilding(UnitTypeId.TWILIGHTCOUNCIL, 1)),
                            GridBuilding(UnitTypeId.GATEWAY, 6),
                            Step(RequiredUnitReady(UnitTypeId.TWILIGHTCOUNCIL, 1),
                                 ActTech(UpgradeId.BLINKTECH, UnitTypeId.TWILIGHTCOUNCIL)),
                            GridBuilding(UnitTypeId.GATEWAY, 7),
                        ]),

                    ])
            ]),
            SequentialList([
                ChronoTech(AbilityId.RESEARCH_WARPGATE, UnitTypeId.CYBERNETICSCORE),
                ChronoTech(AbilityId.RESEARCH_BLINK, UnitTypeId.TWILIGHTCOUNCIL),
                ChronoUnitProduction(UnitTypeId.STALKER, UnitTypeId.GATEWAY),
            ]),
            SequentialList([
                Step(RequiredUnitReady(UnitTypeId.GATEWAY, 4), PlanZoneGather()),
                Step(RequiredUnitReady(UnitTypeId.STALKER, 4), PlanZoneAttack(12)),
                PlanFinishEnemy(),
            ])
        ])

    def defend(self) -> ActBase:
        #TODO: Placement of Cannons & Batteries more consistant, optimize timeing of Darkshrine
        if self.knowledge.enemy_race == Race.Zerg:
            defensive_position = self.knowledge.expansion_zones[1].mineral_line_center.towards(self.knowledge.expansion_zones[1].behind_mineral_position_center, -10)
        else:
            defensive_position = self.knowledge.base_ramp.top_center.towards(self.knowledge.base_ramp.bottom_center, -4)
        return BuildOrder([
            SequentialList([
                GridBuilding(UnitTypeId.FORGE, 1),
                Step(RequiredUnitReady(UnitTypeId.CYBERNETICSCORE, 1),
                     BuildPosition(UnitTypeId.SHIELDBATTERY, defensive_position, exact=False, only_once=True)),
                BuildOrder(
                    [
                        AutoPylon(),
                        ActTech(UpgradeId.WARPGATERESEARCH, UnitTypeId.CYBERNETICSCORE),
                        GateUnit(UnitTypeId.STALKER, 1, priority=True),
                        GridBuilding(UnitTypeId.GATEWAY, 2),
                        [
                            Step(None, ProtossUnit(UnitTypeId.SENTRY, 1),
                                 skip_until=RequiredUnitExists(UnitTypeId.STALKER, 2, include_pending=True)),
                            Step(None, ProtossUnit(UnitTypeId.SENTRY, 2),
                                 skip_until=RequiredUnitExists(UnitTypeId.STALKER, 4, include_pending=True)),
                            Step(None, ProtossUnit(UnitTypeId.STALKER, 4)),
                        ],
                        Step(RequiredUnitReady(UnitTypeId.FORGE, 1),
                             BuildPosition(UnitTypeId.PHOTONCANNON, defensive_position, exact=False, only_once=True)),
                        ActDefensiveCannons(1),
                    ])
            ]),
            Step(RequiredUnitReady(UnitTypeId.CYBERNETICSCORE, 1), GridBuilding(UnitTypeId.TWILIGHTCOUNCIL, 1)),
            GridBuilding(UnitTypeId.GATEWAY, 3),
            Step(RequiredUnitReady(UnitTypeId.TWILIGHTCOUNCIL, 1), GridBuilding(UnitTypeId.DARKSHRINE, 1)),
            [
                Step(RequiredUnitReady(UnitTypeId.DARKSHRINE, 1), ProtossUnit(UnitTypeId.DARKTEMPLAR, 4, priority=True),
                     skip_until=RequiredUnitReady(UnitTypeId.DARKSHRINE, 1)),
                Step(None, ProtossUnit(UnitTypeId.ZEALOT, 40)),
            ],
            Step(RequiredUnitReady(UnitTypeId.DARKTEMPLAR, 4), ActTech(UpgradeId.CHARGE, UnitTypeId.TWILIGHTCOUNCIL)),
            SequentialList([
                ChronoTech(AbilityId.RESEARCH_WARPGATE, UnitTypeId.CYBERNETICSCORE),
                ChronoUnitProduction(UnitTypeId.STALKER, UnitTypeId.GATEWAY),
                ChronoAnyTech(0)
            ]),
            SequentialList([
                Dt_Harass(),
                Step(RequiredUnitReady(UnitTypeId.GATEWAY, 4), PlanZoneGather()),
                Step(RequiredUnitReady(UnitTypeId.ZEALOT, 15), PlanZoneAttack(30)),
                PlanFinishEnemy(),
            ])
        ])


class LadderBot(MadAI):
    @property
    def my_race(self):
        return Race.Protoss
