from sc2 import BotAI, UnitTypeId, AbilityId, Race
from sc2.ids.upgrade_id import UpgradeId

from sharpy.knowledges import KnowledgeBot
from sharpy.plans import BuildOrder, Step, SequentialList, StepBuildGas
from sharpy.plans.acts import *
from sharpy.plans.acts.protoss import *
from sharpy.plans.require import *
from sharpy.plans.tactics import *
from sharpy.plans.tactics.protoss import *
from sc2.position import Point2
from sc2.constants import RALLY_UNITS
from sharpy.managers.manager_base import ManagerBase


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

            if self.knowledge.possible_rush_detected:
                enemy_rush = 1
            else:
                enemy_rush = 0

            enemy_pylon_pos = []
            for pylon in range(len(self.knowledge.known_enemy_units(UnitTypeId.PYLON))):
                enemy_pylon_pos.append(self.knowledge.known_enemy_units(UnitTypeId.PYLON)[pylon].position)
            enemy_gateway_pos = []
            for gateway in range(len(self.knowledge.known_enemy_units(UnitTypeId.GATEWAY))):
                enemy_gateway_pos.append(self.knowledge.known_enemy_units(UnitTypeId.GATEWAY)[gateway].position)
            enemy_forge_pos = []
            for forge in range(len(self.knowledge.known_enemy_units(UnitTypeId.FORGE))):
                enemy_forge_pos.append(self.knowledge.known_enemy_units(UnitTypeId.FORGE)[forge].position)
            enemy_cannon_pos = []
            for cannon in range(len(self.knowledge.known_enemy_units(UnitTypeId.PHOTONCANNON))):
                enemy_cannon_pos.append(self.knowledge.known_enemy_units(UnitTypeId.PHOTONCANNON)[cannon].position)
            enemy_depot_pos = []
            for depot in range(len(self.knowledge.known_enemy_units(UnitTypeId.SUPPLYDEPOT))):
                enemy_depot_pos.append(self.knowledge.known_enemy_units(UnitTypeId.SUPPLYDEPOT)[depot].position)
            enemy_depotlow_pos = []
            for depotlow in range(len(self.knowledge.known_enemy_units(UnitTypeId.SUPPLYDEPOTLOWERED))):
                enemy_depotlow_pos.append(
                    self.knowledge.known_enemy_units(UnitTypeId.SUPPLYDEPOTLOWERED)[depotlow].position
                )
            enemy_bunker_pos = []
            for bunker in range(len(self.knowledge.known_enemy_units(UnitTypeId.BUNKER))):
                enemy_bunker_pos.append(self.knowledge.known_enemy_units(UnitTypeId.BUNKER)[bunker].position)
            enemy_barracks_pos = []
            for barracks in range(len(self.knowledge.known_enemy_units(UnitTypeId.BARRACKS))):
                enemy_barracks_pos.append(self.knowledge.known_enemy_units(UnitTypeId.BARRACKS)[barracks].position)
            enemy_factory_pos = []
            for factory in range(len(self.knowledge.known_enemy_units(UnitTypeId.FACTORY))):
                enemy_factory_pos.append(self.knowledge.known_enemy_units(UnitTypeId.FACTORY)[factory].position)
            enemy_pool_pos = []
            for pool in range(len(self.knowledge.known_enemy_units(UnitTypeId.SPAWNINGPOOL))):
                enemy_pool_pos.append(self.knowledge.known_enemy_units(UnitTypeId.SPAWNINGPOOL)[pool].position)
            enemy_spine_pos = []
            for spine in range(len(self.knowledge.known_enemy_units(UnitTypeId.SPINECRAWLER))):
                enemy_spine_pos.append(self.knowledge.known_enemy_units(UnitTypeId.SPINECRAWLER)[spine].position)

            if len(self.knowledge.known_enemy_units(UnitTypeId.PYLON)) >= 1:
                pylon1_pos = enemy_pylon_pos[0][0] + enemy_pylon_pos[0][1]
            else:
                pylon1_pos = 0
            if len(self.knowledge.known_enemy_units(UnitTypeId.PYLON)) >= 2:
                pylon2_pos = enemy_pylon_pos[1][0] + enemy_pylon_pos[1][1]
            else:
                pylon2_pos = 0
            if len(self.knowledge.known_enemy_units(UnitTypeId.PYLON)) >= 3:
                pylon3_pos = enemy_pylon_pos[2][0] + enemy_pylon_pos[2][1]
            else:
                pylon3_pos = 0
            if len(self.knowledge.known_enemy_units(UnitTypeId.GATEWAY)) >= 1:
                gate1_pos = enemy_gateway_pos[0][0] + enemy_gateway_pos[0][1]
            else:
                gate1_pos = 0
            if len(self.knowledge.known_enemy_units(UnitTypeId.GATEWAY)) >= 2:
                gate2_pos = enemy_gateway_pos[1][0] + enemy_gateway_pos[1][1]
            else:
                gate2_pos = 0
            if len(self.knowledge.known_enemy_units(UnitTypeId.FORGE)) >= 1:
                forge1_pos = enemy_forge_pos[0][0] + enemy_forge_pos[0][1]
            else:
                forge1_pos = 0
            if len(self.knowledge.known_enemy_units(UnitTypeId.PHOTONCANNON)) >= 1:
                cannon1_pos = enemy_cannon_pos[0][0] + enemy_cannon_pos[0][1]
            else:
                cannon1_pos = 0
            if len(self.knowledge.known_enemy_units(UnitTypeId.PHOTONCANNON)) >= 2:
                cannon2_pos = enemy_cannon_pos[1][0] + enemy_cannon_pos[1][1]
            else:
                cannon2_pos = 0
            if len(self.knowledge.known_enemy_units(UnitTypeId.PHOTONCANNON)) >= 3:
                cannon3_pos = enemy_cannon_pos[2][0] + enemy_cannon_pos[2][1]
            else:
                cannon3_pos = 0
            if len(self.knowledge.known_enemy_units(UnitTypeId.PHOTONCANNON)) >= 4:
                cannon4_pos = enemy_cannon_pos[3][0] + enemy_cannon_pos[3][1]
            else:
                cannon4_pos = 0
            if len(self.knowledge.known_enemy_units(UnitTypeId.SUPPLYDEPOT)) >= 1:
                depot1_pos = enemy_depot_pos[0][0] + enemy_depot_pos[0][1]
            else:
                depot1_pos = 0
            if len(self.knowledge.known_enemy_units(UnitTypeId.SUPPLYDEPOT)) >= 2:
                depot2_pos = enemy_depot_pos[1][0] + enemy_depot_pos[1][1]
            else:
                depot2_pos = 0
            if len(self.knowledge.known_enemy_units(UnitTypeId.SUPPLYDEPOT)) >= 3:
                depot3_pos = enemy_depot_pos[2][0] + enemy_depot_pos[2][1]
            else:
                depot3_pos = 0
            if len(self.knowledge.known_enemy_units(UnitTypeId.SUPPLYDEPOTLOWERED)) >= 1:
                depotlow1_pos = enemy_depotlow_pos[0][0] + enemy_depotlow_pos[0][1]
            else:
                depotlow1_pos = 0
            if len(self.knowledge.known_enemy_units(UnitTypeId.SUPPLYDEPOTLOWERED)) >= 2:
                depotlow2_pos = enemy_depotlow_pos[1][0] + enemy_depotlow_pos[1][1]
            else:
                depotlow2_pos = 0
            if len(self.knowledge.known_enemy_units(UnitTypeId.SUPPLYDEPOTLOWERED)) >= 3:
                depotlow3_pos = enemy_depotlow_pos[2][0] + enemy_depotlow_pos[2][1]
            else:
                depotlow3_pos = 0
            if len(self.knowledge.known_enemy_units(UnitTypeId.BUNKER)) >= 1:
                bunker1_pos = enemy_bunker_pos[0][0] + enemy_bunker_pos[0][1]
            else:
                bunker1_pos = 0
            if len(self.knowledge.known_enemy_units(UnitTypeId.BARRACKS)) >= 1:
                barracks1_pos = enemy_barracks_pos[0][0] + enemy_barracks_pos[0][1]
            else:
                barracks1_pos = 0
            if len(self.knowledge.known_enemy_units(UnitTypeId.BARRACKS)) >= 2:
                barracks2_pos = enemy_barracks_pos[1][0] + enemy_barracks_pos[1][1]
            else:
                barracks2_pos = 0
            if len(self.knowledge.known_enemy_units(UnitTypeId.BARRACKS)) >= 3:
                barracks3_pos = enemy_barracks_pos[2][0] + enemy_barracks_pos[2][1]
            else:
                barracks3_pos = 0
            if len(self.knowledge.known_enemy_units(UnitTypeId.FACTORY)) >= 1:
                factory1_pos = enemy_factory_pos[0][0] + enemy_factory_pos[0][1]
            else:
                factory1_pos = 0
            if len(self.knowledge.known_enemy_units(UnitTypeId.SPAWNINGPOOL)) >= 1:
                pool1_pos = enemy_pool_pos[0][0] + enemy_pool_pos[0][1]
            else:
                pool1_pos = 0
            if len(self.knowledge.known_enemy_units(UnitTypeId.SPINECRAWLER)) >= 1:
                spine1_pos = enemy_spine_pos[0][0] + enemy_spine_pos[0][1]
            else:
                spine1_pos = 0
            if len(self.knowledge.known_enemy_units(UnitTypeId.SPINECRAWLER)) >= 2:
                spine2_pos = enemy_spine_pos[1][0] + enemy_spine_pos[1][1]
            else:
                spine2_pos = 0

            self.scout_data = [
                self.knowledge.enemy_start_location,
                enemy_rush,
                self.knowledge.enemy_units_manager.enemy_worker_count,
                len(self.knowledge.known_enemy_units(UnitTypeId.NEXUS)),
                len(self.knowledge.known_enemy_units(UnitTypeId.PYLON)),
                len(self.knowledge.known_enemy_units(UnitTypeId.GATEWAY)),
                len(self.knowledge.known_enemy_units(UnitTypeId.CYBERNETICSCORE)),
                len(self.knowledge.known_enemy_units(UnitTypeId.ASSIMILATOR)),
                len(self.knowledge.known_enemy_units(UnitTypeId.PHOTONCANNON)),
                len(self.knowledge.known_enemy_units(UnitTypeId.BUNKER)),
                len(self.knowledge.known_enemy_units(UnitTypeId.FORGE)),
                len(self.knowledge.known_enemy_units(UnitTypeId.COMMANDCENTER)),
                len(self.knowledge.known_enemy_units(UnitTypeId.ORBITALCOMMAND)),
                len(self.knowledge.known_enemy_units(UnitTypeId.SUPPLYDEPOT)),
                len(self.knowledge.known_enemy_units(UnitTypeId.SUPPLYDEPOTLOWERED)),
                len(self.knowledge.known_enemy_units(UnitTypeId.BARRACKS)),
                len(self.knowledge.known_enemy_units(UnitTypeId.TECHLAB)),
                len(self.knowledge.known_enemy_units(UnitTypeId.REACTOR)),
                len(self.knowledge.known_enemy_units(UnitTypeId.REFINERY)),
                len(self.knowledge.known_enemy_units(UnitTypeId.FACTORY)),
                len(self.knowledge.known_enemy_units(UnitTypeId.HATCHERY)),
                len(self.knowledge.known_enemy_units(UnitTypeId.SPINECRAWLER)),
                len(self.knowledge.known_enemy_units(UnitTypeId.SPAWNINGPOOL)),
                len(self.knowledge.known_enemy_units(UnitTypeId.ROACHWARREN)),
                len(self.knowledge.known_enemy_units(UnitTypeId.EXTRACTOR)),
                self.knowledge.enemy_units_manager.unit_count(UnitTypeId.ZEALOT),
                self.knowledge.enemy_units_manager.unit_count(UnitTypeId.STALKER),
                self.knowledge.enemy_units_manager.unit_count(UnitTypeId.MARINE),
                self.knowledge.enemy_units_manager.unit_count(UnitTypeId.REAPER),
                self.knowledge.enemy_units_manager.unit_count(UnitTypeId.ZERGLING),
                self.knowledge.enemy_units_manager.unit_count(UnitTypeId.ROACH),
                pylon1_pos,
                pylon2_pos,
                pylon3_pos,
                gate1_pos,
                gate2_pos,
                forge1_pos,
                cannon1_pos,
                cannon2_pos,
                cannon3_pos,
                cannon4_pos,
                depot1_pos,
                depot2_pos,
                depot3_pos,
                depotlow1_pos,
                depotlow2_pos,
                depotlow3_pos,
                bunker1_pos,
                barracks1_pos,
                barracks2_pos,
                barracks3_pos,
                factory1_pos,
                pool1_pos,
                spine1_pos,
                spine2_pos,
                self.knowledge.game_analyzer.enemy_mineral_income,
                self.knowledge.game_analyzer.enemy_gas_income,
                self.knowledge.game_analyzer.enemy_power.power,
                self.knowledge.game_analyzer.enemy_predict_power.power,
                self.knowledge.game_analyzer.our_power.power,
                self.knowledge.enemy_army_predicter.own_value,
                self.knowledge.enemy_army_predicter.enemy_value,
                self.knowledge.enemy_army_predicter.enemy_mined_minerals,
                self.knowledge.enemy_army_predicter.enemy_mined_gas,
            ]

            self.build_order = random.randrange(0, 3)
            print(self.scout_data)

            if self.build_order == 0:
                await self.ai.chat_send(
                    "(glhf) MadAI v3.0: 2-Base Robo BO chosen!"
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
                    self.knowledge.expansion_zones[-1].mineral_line_center,
                )
            )
            if len(self.cache.own(UnitTypeId.DARKTEMPLAR)) > 1:
                dt2 = self.cache.own(UnitTypeId.DARKTEMPLAR)[1]
                self.do(
                    dt2(
                        RALLY_UNITS,
                        self.knowledge.expansion_zones[-2].mineral_line_center,
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
            result = 1
        else:
            result = 0

        self.train_data.append(
            [
                result,
                self.scout.build_order,
                self.scout.scout_data[0][0]+self.scout.scout_data[0][1],
                self.scout.scout_data[1],
                self.scout.scout_data[2],
                self.scout.scout_data[3],
                self.scout.scout_data[4],
                self.scout.scout_data[5],
                self.scout.scout_data[6],
                self.scout.scout_data[7],
                self.scout.scout_data[8],
                self.scout.scout_data[9],
                self.scout.scout_data[10],
                self.scout.scout_data[11],
                self.scout.scout_data[12],
                self.scout.scout_data[13],
                self.scout.scout_data[14],
                self.scout.scout_data[15],
                self.scout.scout_data[16],
                self.scout.scout_data[17],
                self.scout.scout_data[18],
                self.scout.scout_data[19],
                self.scout.scout_data[20],
                self.scout.scout_data[21],
                self.scout.scout_data[22],
                self.scout.scout_data[23],
                self.scout.scout_data[24],
                self.scout.scout_data[25],
                self.scout.scout_data[26],
                self.scout.scout_data[27],
                self.scout.scout_data[28],
                self.scout.scout_data[29],
                self.scout.scout_data[30],
                self.scout.scout_data[31],
                self.scout.scout_data[32],
                self.scout.scout_data[33],
                self.scout.scout_data[34],
                self.scout.scout_data[35],
                self.scout.scout_data[36],
                self.scout.scout_data[37],
                self.scout.scout_data[38],
                self.scout.scout_data[39],
                self.scout.scout_data[40],
                self.scout.scout_data[41],
                self.scout.scout_data[42],
                self.scout.scout_data[43],
                self.scout.scout_data[44],
                self.scout.scout_data[45],
                self.scout.scout_data[46],
                self.scout.scout_data[47],
                self.scout.scout_data[48],
                self.scout.scout_data[49],
                self.scout.scout_data[50],
                self.scout.scout_data[51],
                self.scout.scout_data[52],
                self.scout.scout_data[53],
                self.scout.scout_data[54],
                self.scout.scout_data[55],
                self.scout.scout_data[56],
                self.scout.scout_data[57],
                self.scout.scout_data[58],
                self.scout.scout_data[59],
                self.scout.scout_data[60],
                self.scout.scout_data[61],
                self.scout.scout_data[62],
                self.scout.scout_data[63],
            ]
        )
        print(self.train_data)

        np.save("data/{}_first.npy".format(str(int(time.time()))), np.array(self.train_data))

    async def create_plan(self) -> BuildOrder:
        # Common Start Build Order
        #TODO: Implement more BOs
        #TODO: Build second pylon at reaper ramp against Terran
        #TODO: Gather in front of enemy base (Deathball) before attack
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
            Step(lambda k: self.scout.build_order == 0, self.two_base_robo()),
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
        random_location = random.randrange(0, 2)
        if random_location == 0:
            natural = self.knowledge.expansion_zones[-3]
            pylon_pos: Point2 = natural.mineral_line_center.towards(
                    self.knowledge.expansion_zones[-3].behind_mineral_position_center, -5)
        else:
            pylon_pos = self.knowledge.ai.game_info.map_center.towards(self.knowledge.ai.enemy_start_locations[0],
                                                                   17).position
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

    def two_base_robo(self) -> ActBase:
        #TODO: Adapt Unit Composition, Archons as follow-up after first push (ActArchon)
        return BuildOrder([
            SequentialList([
                ActExpand(2),
                BuildOrder(
                    [
                        ActTech(UpgradeId.WARPGATERESEARCH, UnitTypeId.CYBERNETICSCORE),
                        GateUnit(UnitTypeId.STALKER, 1),
                        Step(RequiredUnitExists(UnitTypeId.NEXUS, 2), ActUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS, 24)),
                    ]),
                GridBuilding(UnitTypeId.ROBOTICSFACILITY, 1),
                GateUnit(UnitTypeId.SENTRY, 1),
                Step(RequiredUnitExists(UnitTypeId.NEXUS, 2), ActUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS, 25)),
                GridBuilding(UnitTypeId.PYLON, 3),
                GridBuilding(UnitTypeId.GATEWAY, 2),
                Step(RequiredUnitExists(UnitTypeId.NEXUS, 2), ActUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS, 26)),
                BuildOrder(
                    [
                        GateUnit(UnitTypeId.SENTRY, 2),
                        Step(RequiredUnitExists(UnitTypeId.NEXUS, 2), ActUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS, 30)),
                        GridBuilding(UnitTypeId.PYLON, 4),
                        SequentialList([
                            Step(RequiredUnitReady(UnitTypeId.SENTRY, 1), HallucinatedPhoenixScout()),
                            Step(RequiredUnitReady(UnitTypeId.SENTRY, 1), PlanHallucination()),
                        ])
                    ]),
                Step(RequiredUnitReady(UnitTypeId.ROBOTICSFACILITY, 1), ProtossUnit(UnitTypeId.IMMORTAL, 1)),
                GateUnit(UnitTypeId.ZEALOT, 3),
                GridBuilding(UnitTypeId.GATEWAY, 3),
                Step(RequiredUnitExists(UnitTypeId.NEXUS, 2), ActUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS, 32)),
                Step(RequiredUnitReady(UnitTypeId.IMMORTAL, 1), ProtossUnit(UnitTypeId.OBSERVER, 1)),
                StepBuildGas(3),
                Step(RequiredUnitReady(UnitTypeId.CYBERNETICSCORE, 1), GridBuilding(UnitTypeId.TWILIGHTCOUNCIL, 1)),
                Step(RequiredUnitExists(UnitTypeId.NEXUS, 2), ActUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS, 34)),
                Step(RequiredUnitReady(UnitTypeId.ROBOTICSFACILITY, 1), ProtossUnit(UnitTypeId.IMMORTAL, 2)),
                GateUnit(UnitTypeId.SENTRY, 4),
                GridBuilding(UnitTypeId.GATEWAY, 4),
                Step(RequiredUnitReady(UnitTypeId.IMMORTAL, 1), ActTech(UpgradeId.CHARGE, UnitTypeId.TWILIGHTCOUNCIL)),
                StepBuildGas(4),
            ]),
            BuildOrder(
                [
                    AutoPylon(),
                    Step(RequiredUnitExists(UnitTypeId.NEXUS, 2), ActUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS, 44)),
                    Step(RequiredUnitReady(UnitTypeId.IMMORTAL, 3),
                         ProtossUnit(UnitTypeId.WARPPRISM, 1, priority=True)),
                    Step(RequiredUnitReady(UnitTypeId.ROBOTICSFACILITY, 1),
                         ProtossUnit(UnitTypeId.IMMORTAL, 20, priority=True)),
                    Step(RequiredUnitReady(UnitTypeId.ROBOTICSFACILITY, 1), ProtossUnit(UnitTypeId.ZEALOT, 7),
                         skip=RequiredUnitExists(UnitTypeId.TWILIGHTCOUNCIL, 1)),
                    Step(RequiredUnitReady(UnitTypeId.SENTRY, 4), ProtossUnit(UnitTypeId.ZEALOT, 50)),

                ]),
            SequentialList([
                ChronoTech(AbilityId.RESEARCH_WARPGATE, UnitTypeId.CYBERNETICSCORE),
                ChronoUnitProduction(UnitTypeId.IMMORTAL, UnitTypeId.ROBOTICSFACILITY),
                Step(RequiredUnitReady(UnitTypeId.TWILIGHTCOUNCIL, 1), ChronoAnyTech(0),
                     skip=RequiredUnitReady(UnitTypeId.IMMORTAL, 3)),
            ]),
            SequentialList([
                PlanZoneGather(),
                Step(RequiredTechReady(UpgradeId.CHARGE, 0.9), PlanZoneAttack(12)),
                PlanFinishEnemy(),
            ])
        ])

    def defend(self) -> ActBase:
        #TODO: Morph DTs into Archons if detected, Proxy-Pylon for DTs only, Follow-Up
        if self.knowledge.enemy_race == Race.Zerg:
            defensive_position1 = self.knowledge.expansion_zones[1].mineral_line_center.towards(
                self.knowledge.expansion_zones[1].behind_mineral_position_center, -12)
            defensive_position2 = self.knowledge.expansion_zones[1].mineral_line_center.towards(
                self.knowledge.expansion_zones[1].behind_mineral_position_center, -14)
        else:
            defensive_position1 = self.knowledge.base_ramp.top_center.towards(self.knowledge.base_ramp.bottom_center, -4)
            defensive_position2 = self.knowledge.base_ramp.top_center.towards(self.knowledge.expansion_zones[1].mineral_line_center, 4)
        return BuildOrder([
            SequentialList([
                GridBuilding(UnitTypeId.FORGE, 1),
                BuildOrder(
                    [
                        Step(RequiredUnitReady(UnitTypeId.CYBERNETICSCORE, 1),
                             BuildPosition(UnitTypeId.SHIELDBATTERY, defensive_position1, exact=False, only_once=True)),
                        ActTech(UpgradeId.WARPGATERESEARCH, UnitTypeId.CYBERNETICSCORE),
                        GateUnit(UnitTypeId.STALKER, 1),
                    ]),
                Step(RequiredUnitReady(UnitTypeId.FORGE, 1),
                     BuildPosition(UnitTypeId.PHOTONCANNON, defensive_position1, exact=False, only_once=True)),
                Step(RequiredUnitReady(UnitTypeId.FORGE, 1),
                     BuildPosition(UnitTypeId.PHOTONCANNON, defensive_position2, exact=False, only_once=True)),
                Step(RequiredUnitReady(UnitTypeId.CYBERNETICSCORE, 1), GridBuilding(UnitTypeId.TWILIGHTCOUNCIL, 1)),
                GateUnit(UnitTypeId.SENTRY, 1),
                GridBuilding(UnitTypeId.PYLON, 3),
                GridBuilding(UnitTypeId.GATEWAY, 2),
                Step(RequiredUnitReady(UnitTypeId.TWILIGHTCOUNCIL, 1), GridBuilding(UnitTypeId.DARKSHRINE, 1)),
                BuildOrder(
                    [
                        GateUnit(UnitTypeId.SENTRY, 2),
                        GateUnit(UnitTypeId.ZEALOT, 3),
                        GridBuilding(UnitTypeId.GATEWAY, 3),
                        SequentialList([
                            Step(RequiredUnitReady(UnitTypeId.SENTRY, 1), HallucinatedPhoenixScout()),
                            Step(RequiredUnitReady(UnitTypeId.SENTRY, 1), PlanHallucination()),
                        ])
                    ]),
            ]),
            [
                AutoPylon(),
                Step(RequiredUnitReady(UnitTypeId.DARKSHRINE, 1), ProtossUnit(UnitTypeId.DARKTEMPLAR, 3, priority=True),
                     skip_until=RequiredUnitReady(UnitTypeId.DARKSHRINE, 1)),
                Step(RequiredUnitReady(UnitTypeId.DARKSHRINE, 1), ProtossUnit(UnitTypeId.ZEALOT, 40)),
                Step(RequiredUnitReady(UnitTypeId.DARKSHRINE, 1), ProtossUnit(UnitTypeId.SENTRY, 5)),
            ],
            SequentialList([
                Step(RequiredUnitReady(UnitTypeId.DARKTEMPLAR, 3), ActTech(UpgradeId.CHARGE, UnitTypeId.TWILIGHTCOUNCIL)),
                Step(RequiredUnitReady(UnitTypeId.DARKTEMPLAR, 3), ActTech(UpgradeId.PROTOSSGROUNDWEAPONSLEVEL1, UnitTypeId.FORGE)),
            ]),
            SequentialList([
                ChronoTech(AbilityId.RESEARCH_WARPGATE, UnitTypeId.CYBERNETICSCORE),
                ChronoUnitProduction(UnitTypeId.STALKER, UnitTypeId.GATEWAY),
                ChronoAnyTech(0)
            ]),
            SequentialList([
                Step(None, PlanZoneGather(), skip=RequiredUnitReady(UnitTypeId.DARKSHRINE, 1)),
                Step(RequiredUnitReady(UnitTypeId.DARKSHRINE, 1), Dt_Harass()),
                Step(RequiredTechReady(UpgradeId.CHARGE), PlanZoneGather()),
                Step(RequiredTechReady(UpgradeId.CHARGE), PlanZoneAttack(10)),
                PlanFinishEnemy(),
            ])
        ])

    def two_base_stalker(self) -> ActBase:
        #TODO: Adapt Unit Composition, Improve Timings, Hallu-Phoenix-Scout
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

class LadderBot(MadAI):
    @property
    def my_race(self):
        return Race.Protoss
