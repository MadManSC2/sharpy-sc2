from typing import Dict

from sharpy.general.extended_power import siege
from sharpy.managers.combat2 import Action, MoveType, GenericMicro, CombatModel
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
    UnitTypeId.SCV: 9,  # prioritize scv because they'll continue repairing otherwise
    UnitTypeId.GHOST: 7,
    UnitTypeId.REAPER: 4,
    UnitTypeId.MARAUDER: 4,
    UnitTypeId.MARINE: 3,
    UnitTypeId.CYCLONE: 5,
    UnitTypeId.HELLION: 2,
    UnitTypeId.HELLIONTANK: 3,
    UnitTypeId.THOR: 5,
    UnitTypeId.MEDIVAC: 6,
    UnitTypeId.VIKINGFIGHTER: 5,
    UnitTypeId.VIKINGASSAULT: 5,
    UnitTypeId.LIBERATORAG: 9,
    UnitTypeId.LIBERATOR: 5,
    UnitTypeId.RAVEN: 10,
    UnitTypeId.BATTLECRUISER: 8,
    UnitTypeId.BANSHEE: 9,

    UnitTypeId.MISSILETURRET: 1,
    UnitTypeId.BUNKER: 2,

    # Zerg
    UnitTypeId.DRONE: 4,
    UnitTypeId.ZERGLING: 3,
    UnitTypeId.BANELING: 6,
    UnitTypeId.ULTRALISK: 6,
    UnitTypeId.QUEEN: 5,
    UnitTypeId.ROACH: 6,
    UnitTypeId.RAVAGER: 8,
    UnitTypeId.HYDRALISK: 7,
    UnitTypeId.HYDRALISKBURROWED: 7,
    UnitTypeId.LURKERMP: 9,
    UnitTypeId.LURKERMPBURROWED: 9,
    UnitTypeId.INFESTOR: 10,
    UnitTypeId.BROODLORD: 10,
    UnitTypeId.MUTALISK: 6,
    UnitTypeId.CORRUPTOR: 8,
    UnitTypeId.INFESTEDTERRAN: 1,

    UnitTypeId.LARVA: -1,
    UnitTypeId.EGG: -1,
    UnitTypeId.LOCUSTMP: -1,

    # Protoss
    UnitTypeId.SENTRY: 8,
    UnitTypeId.PROBE: 4,
    UnitTypeId.HIGHTEMPLAR: 10,
    UnitTypeId.DARKTEMPLAR: 9,
    UnitTypeId.ADEPT: 4,
    UnitTypeId.ZEALOT: 4,
    UnitTypeId.STALKER: 5,
    UnitTypeId.IMMORTAL: 9,
    UnitTypeId.COLOSSUS: 10,
    UnitTypeId.ARCHON: 6,
    UnitTypeId.WARPPRISM: 7,
    UnitTypeId.PHOENIX: 3,
    UnitTypeId.CARRIER: 10,
    UnitTypeId.VOIDRAY: 8,
    UnitTypeId.TEMPEST: 9,
    UnitTypeId.INTERCEPTOR: -1,
    UnitTypeId.CHANGELINGZEALOT: -1,

    UnitTypeId.SHIELDBATTERY: 1,
    UnitTypeId.PHOTONCANNON: 1,
    UnitTypeId.PYLON: 2,
    UnitTypeId.FLEETBEACON: 3,

}


class MicroStalkers(GenericMicro):
    def __init__(self, knowledge):
        super().__init__(knowledge)
        self.prio_dict = high_priority

    def unit_solve_combat(self, unit: Unit, current_command: Action) -> Action:
        if self.engage_ratio < 0.25 and self.can_engage_ratio < 0.25:
            return current_command

        if self.cd_manager.is_ready(unit.tag, AbilityId.EFFECT_BLINK_STALKER):
            if self.is_locked_on(unit):
                cyclones = self.enemies_near_by(UnitTypeId.CYCLONE)
                if cyclones:
                    closest_cyclone = cyclones.closest_to(unit)
                    backstep: Point2 = closest_cyclone.position.towards(unit.position, 15)
                    backstep = self.pather.find_weak_influence_ground(backstep, 4)
                    return Action(backstep, False, AbilityId.EFFECT_BLINK_STALKER)

            if self.model == CombatModel.StalkerToSiege and \
                    (self.move_type == MoveType.Assault or self.move_type == MoveType.SearchAndDestroy):
                siege_units = self.enemies_near_by.of_type(siege)
                if siege_units:
                    target = siege_units.closest_to(unit)
                    if target.distance_to(unit) > 6:
                        return Action(target.position, False, AbilityId.EFFECT_BLINK_STALKER)

            if unit.shield_percentage < 0.05:
                # Blink to safety.

                target_pos = unit.position
                if self.closest_group:
                    target_pos = target_pos.towards(self.closest_group.center, -5)

                target = self.pather.find_weak_influence_ground_blink(target_pos, 6)
                if target.distance_to(unit) > 3:
                    return Action(target, False, AbilityId.EFFECT_BLINK_STALKER)

        # If there are SCVs near a bunker kill them with top priority!
        #TODO: Check if the SCVs are repairing
        if self.enemies_near_by(UnitTypeId.BUNKER):
            scvs = self.enemies_near_by(UnitTypeId.SCV)
            if scvs:
                target = scvs.closest_to(unit)
                return Action(target, True)


        return super().unit_solve_combat(unit, current_command)
