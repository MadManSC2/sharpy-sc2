from typing import Dict


from sharpy.managers.combat2 import Action, GenericMicro, CombatModel
from sc2 import AbilityId, UnitTypeId
from sc2.position import Point2
from sc2.unit import Unit

high_priority: Dict[UnitTypeId, int] = {
    # Terran
    UnitTypeId.SIEGETANK: 8,
    UnitTypeId.SIEGETANKSIEGED: 10,  # sieged tanks are much higher priority than unsieged
    UnitTypeId.WIDOWMINE: 8,
    UnitTypeId.WIDOWMINEBURROWED: 10,
    UnitTypeId.MULE: 3,
    UnitTypeId.SCV: 10,  # prioritize scv because they'll continue repairing otherwise
    UnitTypeId.GHOST: 1,
    UnitTypeId.REAPER: 4,
    UnitTypeId.MARAUDER: 6,
    UnitTypeId.MARINE: 2,
    UnitTypeId.CYCLONE: 5,
    UnitTypeId.HELLION: 2,
    UnitTypeId.HELLIONTANK: 3,
    UnitTypeId.THOR: 7,
    UnitTypeId.VIKINGFIGHTER: 5,
    UnitTypeId.MISSILETURRET: 1,
    UnitTypeId.BUNKER: 2,
    UnitTypeId.MEDIVAC: -1,
    UnitTypeId.VIKINGASSAULT: -1,
    UnitTypeId.LIBERATORAG: -1,
    UnitTypeId.LIBERATOR: -1,
    UnitTypeId.RAVEN: -1,
    UnitTypeId.BATTLECRUISER: -1,
    UnitTypeId.BANSHEE: -1,

    # Zerg
    UnitTypeId.DRONE: 2,
    UnitTypeId.ZERGLING: 3,
    UnitTypeId.BANELING: 4,
    UnitTypeId.ULTRALISK: 7,
    UnitTypeId.QUEEN: 5,
    UnitTypeId.ROACH: 6,
    UnitTypeId.RAVAGER: 8,
    UnitTypeId.HYDRALISK: 4,
    UnitTypeId.HYDRALISKBURROWED: 7,
    UnitTypeId.LURKERMP: 9,
    UnitTypeId.LURKERMPBURROWED: 9,
    UnitTypeId.INFESTOR: 5,
    UnitTypeId.INFESTEDTERRAN: 1,
    UnitTypeId.BROODLORD: -1,
    UnitTypeId.MUTALISK: -1,
    UnitTypeId.CORRUPTOR: -1,

    UnitTypeId.LARVA: -1,
    UnitTypeId.EGG: -1,
    UnitTypeId.LOCUSTMP: -1,

    # Protoss
    UnitTypeId.SENTRY: 5,
    UnitTypeId.PROBE: 2,
    UnitTypeId.HIGHTEMPLAR: 6,
    UnitTypeId.DARKTEMPLAR: 9,
    UnitTypeId.ADEPT: 4,
    UnitTypeId.ZEALOT: 4,
    UnitTypeId.STALKER: 7,
    UnitTypeId.IMMORTAL: 9,
    UnitTypeId.COLOSSUS: 10,
    UnitTypeId.ARCHON: 5,
    UnitTypeId.WARPPRISM: -1,
    UnitTypeId.PHOENIX: -1,
    UnitTypeId.CARRIER: -1,
    UnitTypeId.VOIDRAY: -1,
    UnitTypeId.TEMPEST: -1,
    UnitTypeId.INTERCEPTOR: -1,
    UnitTypeId.CHANGELINGZEALOT: -1,

    UnitTypeId.SHIELDBATTERY: 1,
    UnitTypeId.PHOTONCANNON: 5,
    UnitTypeId.PYLON: 2,

}


class MicroImmortals(GenericMicro):
    def __init__(self, knowledge):
        super().__init__(knowledge)
        self.prio_dict = high_priority

    def unit_solve_combat(self, unit: Unit, current_command: Action) -> Action:
        if self.engage_ratio < 0.25 and self.can_engage_ratio < 0.25:
            return current_command

        return super().unit_solve_combat(unit, current_command)
