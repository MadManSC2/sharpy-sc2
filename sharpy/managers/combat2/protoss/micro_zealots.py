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

    # Zerg
    UnitTypeId.LARVA: -1,
    UnitTypeId.EGG: -1,
    UnitTypeId.LOCUSTMP: -1,
    UnitTypeId.BROODLORD: -1,
    UnitTypeId.MUTALISK: -1,
    UnitTypeId.CORRUPTOR: -1,

    # Protoss
    UnitTypeId.WARPPRISM: -1,
    UnitTypeId.PHOENIX: -1,
    UnitTypeId.CARRIER: -1,
    UnitTypeId.VOIDRAY: -1,
    UnitTypeId.TEMPEST: -1,
    UnitTypeId.INTERCEPTOR: -1,
    UnitTypeId.CHANGELINGZEALOT: -1,

}


class MicroZealots(MicroStep):
    def __init__(self, knowledge):
        super().__init__(knowledge)
        self.prio_dict = high_priority

    def group_solve_combat(self, units: Units, current_command: Action) -> Action:
        if self.move_type == MoveType.DefensiveRetreat or self.move_type == MoveType.PanicRetreat:
            return current_command

        if self.engage_ratio > 0.25 and self.closest_group:
            if self.ready_to_attack_ratio > 0.25 or self.closest_group_distance < 2:
                return Action(self.closest_group.center, True)
            return Action(self.closest_group.center.towards(self.center, -3), False)
        #if self.engage_percentage == 0
        return current_command

    def unit_solve_combat(self, unit: Unit, current_command: Action) -> Action:
        if unit.has_buff(BuffId.CHARGING):
            return NoAction()

        ground_units = self.enemies_near_by.not_flying
        if not ground_units:
            current_command.is_attack = False
            return current_command
        # if self.knowledge.enemy_race == Race.Protoss:
        #     if self.engage_percentage < 0.25:
        #         buildings = self.enemies_near_by.sorted_by_distance_to(unit)
        #         if buildings:
        #             if buildings.first.health + buildings.first.shield < 200:
        #                 return Action(buildings.first, True)
        #             pylons = buildings(UnitTypeId.PYLON)
        #             if pylons:
        #                 return Action(buildings.first, True)
        return current_command
