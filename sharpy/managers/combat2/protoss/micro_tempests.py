from typing import Dict

from sc2.ids.effect_id import EffectId
from sc2.position import Point2
from sc2.units import Units
from sharpy.managers.combat2 import MicroStep, Action, MoveType
from sc2 import AbilityId, UnitTypeId
from sc2.unit import Unit

high_priority: Dict[UnitTypeId, int] = {
    # Terran
    UnitTypeId.SIEGETANK: 3,
    UnitTypeId.SIEGETANKSIEGED: 4,
    UnitTypeId.WIDOWMINE: 8,
    UnitTypeId.WIDOWMINEBURROWED: 10,
    UnitTypeId.MULE: 5,
    UnitTypeId.SCV: 5,
    UnitTypeId.GHOST: 8,
    UnitTypeId.REAPER: 4,
    UnitTypeId.MARAUDER: 2,
    UnitTypeId.MARINE: 7,
    UnitTypeId.CYCLONE: 9,
    UnitTypeId.HELLION: 3,
    UnitTypeId.HELLIONTANK: 3,
    UnitTypeId.THOR: 9,
    UnitTypeId.MEDIVAC: 4,
    UnitTypeId.VIKINGFIGHTER: 6,
    UnitTypeId.VIKINGASSAULT: 9,
    UnitTypeId.LIBERATORAG: 6,
    UnitTypeId.LIBERATOR: 8,
    UnitTypeId.RAVEN: 10,
    UnitTypeId.BATTLECRUISER: 10,
    UnitTypeId.BANSHEE: 5,

    UnitTypeId.MISSILETURRET: 8,
    UnitTypeId.BUNKER: 1,

    # Zerg
    UnitTypeId.DRONE: 4,
    UnitTypeId.ZERGLING: 2,
    UnitTypeId.BANELING: 4,
    UnitTypeId.ULTRALISK: 4,
    UnitTypeId.QUEEN: 8,
    UnitTypeId.ROACH: 2,
    UnitTypeId.RAVAGER: 6,
    UnitTypeId.HYDRALISK: 9,
    UnitTypeId.HYDRALISKBURROWED: 7,
    UnitTypeId.LURKERMP: 4,
    UnitTypeId.LURKERMPBURROWED: 4,
    UnitTypeId.INFESTOR: 10,
    UnitTypeId.BROODLORD: 5,
    UnitTypeId.MUTALISK: 8,
    UnitTypeId.CORRUPTOR: 10,
    UnitTypeId.INFESTEDTERRAN: 6,
    UnitTypeId.SPORECRAWLER: 8,

    UnitTypeId.LARVA: -1,
    UnitTypeId.EGG: -1,
    UnitTypeId.LOCUSTMP: -1,

    # Protoss
    UnitTypeId.SENTRY: 6,
    UnitTypeId.PROBE: 4,
    UnitTypeId.HIGHTEMPLAR: 7,
    UnitTypeId.DARKTEMPLAR: 6,
    UnitTypeId.ADEPT: 2,
    UnitTypeId.ZEALOT: 2,
    UnitTypeId.STALKER: 8,
    UnitTypeId.IMMORTAL: 4,
    UnitTypeId.COLOSSUS: 4,
    UnitTypeId.ARCHON: 9,
    UnitTypeId.WARPPRISM: 5,
    UnitTypeId.PHOENIX: 9,
    UnitTypeId.CARRIER: 10,
    UnitTypeId.VOIDRAY: 9,
    UnitTypeId.TEMPEST: 8,
    UnitTypeId.INTERCEPTOR: -1,
    UnitTypeId.CHANGELINGZEALOT: -1,

    UnitTypeId.SHIELDBATTERY: 5,
    UnitTypeId.PHOTONCANNON: 8,
    UnitTypeId.PYLON: 3,
    UnitTypeId.FLEETBEACON: 3,

}


class MicroTempests(MicroStep):
    def __init__(self, knowledge):
        super().__init__(knowledge)
        self.prio_dict = high_priority

    def should_retreat(self, unit: Unit) -> bool:
        if unit.shield_max + unit.health_max > 0:
            health_percentage = (unit.shield + unit.health) / (unit.shield_max + unit.health_max)
        else:
            health_percentage = 0
        if health_percentage < 0.5 or unit.weapon_cooldown < 0:
            # low hp or unit can't attack
            return True

        return False

    def group_solve_combat(self, units: Units, current_command: Action) -> Action:
        return current_command

    def unit_solve_combat(self, unit: Unit, current_command: Action) -> Action:
        if self.engage_ratio < 0.25 and self.can_engage_ratio < 0.25:
            return current_command

        if self.move_type in {MoveType.PanicRetreat, MoveType.DefensiveRetreat}:
            return current_command

        if not unit.is_attacking and self.should_retreat(unit):
            pos = self.pather.find_weak_influence_air(unit.position, 4)
            return Action(pos, False)

        return self.focus_fire(unit, current_command, self.prio_dict)