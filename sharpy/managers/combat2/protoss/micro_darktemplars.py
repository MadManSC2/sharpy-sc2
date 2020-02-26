from typing import Dict

from sharpy.managers.combat2 import MicroStep, Action, MoveType, NoAction
from sc2.ids.buff_id import BuffId
from sc2 import UnitTypeId
from sc2.unit import Unit
from sc2.units import Units

high_priority: Dict[UnitTypeId, int] = {

    # Terran
    UnitTypeId.MEDIVAC: -1,
    UnitTypeId.VIKINGASSAULT: -1,
    UnitTypeId.LIBERATORAG: -1,
    UnitTypeId.LIBERATOR: -1,
    UnitTypeId.RAVEN: -1,
    UnitTypeId.BATTLECRUISER: -1,
    UnitTypeId.BANSHEE: -1,
    UnitTypeId.MULE: 9,
    UnitTypeId.SCV: 8,
    UnitTypeId.MISSILETURRET: 10,
    UnitTypeId.MARINE: 5,

    # Zerg
    UnitTypeId.LARVA: -1,
    UnitTypeId.EGG: -1,
    UnitTypeId.LOCUSTMP: -1,
    UnitTypeId.BROODLORD: -1,
    UnitTypeId.MUTALISK: -1,
    UnitTypeId.CORRUPTOR: -1,
    UnitTypeId.DRONE: 8,
    UnitTypeId.SPORECRAWLER: 10,
    UnitTypeId.SPORECRAWLERUPROOTED: 9,
    UnitTypeId.INFESTOR: 5,

    # Protoss
    UnitTypeId.WARPPRISM: -1,
    UnitTypeId.PHOENIX: -1,
    UnitTypeId.CARRIER: -1,
    UnitTypeId.VOIDRAY: -1,
    UnitTypeId.TEMPEST: -1,
    UnitTypeId.INTERCEPTOR: -1,
    UnitTypeId.CHANGELINGZEALOT: -1,
    UnitTypeId.SENTRY: 6,
    UnitTypeId.PROBE: 9,
    UnitTypeId.HIGHTEMPLAR: 7,
    UnitTypeId.PHOTONCANNON: 10,
    UnitTypeId.PYLON: 8,

}


class MicroDarktemplars(MicroStep):
    def __init__(self, knowledge):
        super().__init__(knowledge)
        self.prio_dict = high_priority

    def group_solve_combat(self, units: Units, current_command: Action) -> Action:
        if self.engage_ratio > 0.5 and self.closest_group:
            if self.ready_to_attack_ratio > 0.8 or self.closest_group_distance < 2:
                return Action(self.closest_group.center, True)
            if self.ready_to_attack_ratio < 0.25:
                return Action(self.closest_group.center, True)
            return Action(self.closest_group.center.towards(self.center, -3), False)
        # if self.engage_percentage == 0
        return current_command

    def unit_solve_combat(self, unit: Unit, current_command: Action) -> Action:

        return current_command
