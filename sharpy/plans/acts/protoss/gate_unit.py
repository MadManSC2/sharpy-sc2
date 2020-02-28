import numpy as np

from sharpy.plans.acts import ActUnit, ActWarpUnit
from sc2 import BotAI, UnitTypeId, AbilityId, Race
from sc2.ids.upgrade_id import UpgradeId


class GateUnit(ActUnit):
    def __init__(self, unit_type: UnitTypeId = UnitTypeId.STALKER, to_count: int = 9999, priority: bool = False, only_once: bool = False):
        super().__init__(unit_type, UnitTypeId.GATEWAY, to_count, priority)
        self.only_once = only_once
        self.warp = ActWarpUnit(unit_type, to_count)

        self.ideal_zealot_ratio = 0
        self.ideal_stalker_ratio = 0
        self.ideal_sentry_ratio = 0
        self.current_zealot_ratio = 0
        self.current_stalker_ratio = 0
        self.current_sentry_ratio = 0

        self.counterTable = [
            # Zerg (Supply, Zealot ratio, Stalker ratio, Sentry ratio)
            [0.5, 0, 1, 0],  # Baneling
            [0.5, 1, 0, 0],  # Zergling
            [2, 0.75, 0.1, 0.15],  # Hydralisk
            [2, 0, 0.9, 0.1],  # Mutalisk
            [6, 0, 1, 0],  # Ultralisk
            [2, 0, 0.9, 0.1],  # Roach
            [2, 0.2, 0.8, 0],  # Infestor
            [2, 0.5, 0.4, 0],  # Queen
            [3, 0.5, 0.5, 0],  # Ravager
            [3, 0, 1, 0],  # Lurker
            [2, 0, 1, 0],  # Corruptor
            [3, 0, 1, 0],  # Viper
            [2, 0.2, 0.8, 0],  # Broodlord
            [3, 0.4, 0.5, 0.1],  # Swarmhost
            [2, 0.3, 0.7, 0],  # Spinecrawler

            # Protoss (Supply, Zealot ratio, Stalker ratio, Sentry ratio)
            [2, 0.8, 0.2, 0],  # Zealot
            [2, 0, 0.9, 0.1],  # Stalker
            [2, 0.75, 0.1, 0.15],  # Adept
            [2, 0.3, 0.6, 0.1],  # Sentry
            [4, 0.9, 0, 0.1],  # Immortal
            [4, 0, 0.95, 0.05],  # Voidray
            [2, 0, 1, 0],  # Phoenix
            [6, 0, 1, 0],  # Colossus
            [4, 0, 1, 0],  # Tempest
            [2, 1, 0, 0],  # High Templar
            [3, 0, 1, 0],  # Disruptor
            [2, 0, 1, 0],  # Dark Templar
            [4, 0, 1, 0],  # Archon
            [2, 0.3, 0.7, 0],  # Photoncannon
            [3, 0, 1, 0],  # Oracle
            [6, 0, 0.85, 0.15],  # Carrier

            # Terran (Supply, Zealot ratio, Stalker ratio, Sentry ratio)
            [1, 0, 0.85, 0.15],  # Marine
            [1, 0, 1, 0],  # Reaper
            [2, 0.9, 0, 0.1],  # Marauder
            [2, 0, 0.95, 0.05],  # Ghost
            [2, 0, 1, 0],  # Hellion
            [2, 0, 1, 0],  # Widowmine
            [3, 0.8, 0.2, 0],  # Cyclone
            [3, 1, 0, 0],  # Siegetank
            [6, 1, 0, 0],  # Thor
            [2, 0, 1, 0],  # Viking
            [2, 0, 1, 0],  # Medivac
            [3, 0, 1, 0],  # Liberator
            [2, 0, 1, 0],  # Ravon
            [3, 0, 1, 0],  # Banshee
            [6, 0, 1, 0],  # Battlecruiser
        ]

    def get_unit_count(self) -> int:
        count = super().get_unit_count()

        if self.only_once:
            count += self.knowledge.lost_units_manager.own_lost_type(self.unit_type)
        return count

    async def start(self, knowledge: 'Knowledge'):
        await self.warp.start(knowledge)
        await super().start(knowledge)

    async def execute(self) -> bool:
        # First, check if there even is at least one warpgate, which is not on cooldown
        for wg in self.ai.structures(UnitTypeId.WARPGATE).ready:
            abilities = await self.ai.get_available_abilities(wg)
            if AbilityId.WARPGATETRAIN_ZEALOT in abilities:
                # Compute the ideal ratio of gate units against every race composition based on the counter table above
                if self.knowledge.enemy_race == Race.Zerg:
                    ba = self.knowledge.enemy_units_manager.unit_count(UnitTypeId.BANELING) * self.counterTable[0][0]
                    ze = self.knowledge.enemy_units_manager.unit_count(UnitTypeId.ZERGLING) * self.counterTable[1][0]
                    hy = self.knowledge.enemy_units_manager.unit_count(UnitTypeId.HYDRALISK) * self.counterTable[2][0]
                    mu = self.knowledge.enemy_units_manager.unit_count(UnitTypeId.MUTALISK) * self.counterTable[3][0]
                    ul = self.knowledge.enemy_units_manager.unit_count(UnitTypeId.ULTRALISK) * self.counterTable[4][0]
                    ro = self.knowledge.enemy_units_manager.unit_count(UnitTypeId.ROACH) * self.counterTable[5][0]
                    ie = (self.knowledge.enemy_units_manager.unit_count(UnitTypeId.INFESTOR) + self.knowledge.enemy_units_manager.unit_count(UnitTypeId.INFESTORBURROWED)) * self.counterTable[6][0]
                    qu = self.knowledge.enemy_units_manager.unit_count(UnitTypeId.QUEEN) * self.counterTable[7][0]
                    ra = self.knowledge.enemy_units_manager.unit_count(UnitTypeId.RAVAGER) * self.counterTable[8][0]
                    lu = self.knowledge.enemy_units_manager.unit_count(UnitTypeId.LURKER) * self.counterTable[9][0]
                    co = self.knowledge.enemy_units_manager.unit_count(UnitTypeId.CORRUPTOR) * self.counterTable[10][0]
                    vi = self.knowledge.enemy_units_manager.unit_count(UnitTypeId.VIPER) * self.counterTable[11][0]
                    br = self.knowledge.enemy_units_manager.unit_count(UnitTypeId.BROODLORD) * self.counterTable[12][0]
                    sw = (self.knowledge.enemy_units_manager.unit_count(UnitTypeId.SWARMHOSTMP) + self.knowledge.enemy_units_manager.unit_count(UnitTypeId.SWARMHOSTBURROWEDMP)) * self.counterTable[13][0]
                    sp = self.knowledge.enemy_units_manager.unit_count(UnitTypeId.SPINECRAWLER) * self.counterTable[14][0]

                    if (ba + ze + hy + mu + ul + ro + ie + qu + ra + lu + co + vi + br + sw + sp) > 0:
                        self.ideal_zealot_ratio = (ba * self.counterTable[0][1] + ze * self.counterTable[1][1] +
                                                   hy * self.counterTable[2][1] + mu * self.counterTable[3][1] +
                                                   ul * self.counterTable[4][1] + ro * self.counterTable[5][1] +
                                                   ie * self.counterTable[6][1] + qu * self.counterTable[7][1] +
                                                   ra * self.counterTable[8][1] + lu * self.counterTable[9][1] +
                                                   co * self.counterTable[10][1] + vi * self.counterTable[11][1] +
                                                   br * self.counterTable[12][1] + sw * self.counterTable[13][1] +
                                                   sp * self.counterTable[14][1]) / \
                                                  (ba + ze + hy + mu + ul + ro + ie + qu + ra + lu + co + vi + br + sw + sp)

                        self.ideal_stalker_ratio = (ba * self.counterTable[0][2] + ze * self.counterTable[1][2] +
                                                    hy * self.counterTable[2][2] + mu * self.counterTable[3][2] +
                                                    ul * self.counterTable[4][2] + ro * self.counterTable[5][2] +
                                                    ie * self.counterTable[6][2] + qu * self.counterTable[7][2] +
                                                    ra * self.counterTable[8][2] + lu * self.counterTable[9][2] +
                                                    co * self.counterTable[10][2] + vi * self.counterTable[11][2] +
                                                    br * self.counterTable[12][2] + sw * self.counterTable[13][2] +
                                                    sp * self.counterTable[14][2]) / \
                                                   (ba + ze + hy + mu + ul + ro + ie + qu + ra + lu + co + vi + br + sw + sp)

                        self.ideal_sentry_ratio = (ba * self.counterTable[0][3] + ze * self.counterTable[1][3] +
                                                   hy * self.counterTable[2][3] + mu * self.counterTable[3][3] +
                                                   ul * self.counterTable[4][3] + ro * self.counterTable[5][3] +
                                                   ie * self.counterTable[6][3] + qu * self.counterTable[7][3] +
                                                   ra * self.counterTable[8][3] + lu * self.counterTable[9][3] +
                                                   co * self.counterTable[10][3] + vi * self.counterTable[11][3] +
                                                   br * self.counterTable[12][3] + sw * self.counterTable[13][3] +
                                                   sp * self.counterTable[14][3]) / \
                                                  (ba + ze + hy + mu + ul + ro + ie + qu + ra + lu + co + vi + br + sw + sp)
                    else:
                        self.ideal_zealot_ratio = 0.3
                        self.ideal_stalker_ratio = 0.65
                        self.ideal_sentry_ratio = 0.05

                elif self.knowledge.enemy_race == Race.Protoss:
                    ze = self.knowledge.enemy_units_manager.unit_count(UnitTypeId.ZEALOT) * self.counterTable[15][0]
                    st = self.knowledge.enemy_units_manager.unit_count(UnitTypeId.STALKER) * self.counterTable[16][0]
                    ad = self.knowledge.enemy_units_manager.unit_count(UnitTypeId.ADEPT) * self.counterTable[17][0]
                    se = self.knowledge.enemy_units_manager.unit_count(UnitTypeId.SENTRY) * self.counterTable[18][0]
                    im = self.knowledge.enemy_units_manager.unit_count(UnitTypeId.IMMORTAL) * self.counterTable[19][0]
                    vo = self.knowledge.enemy_units_manager.unit_count(UnitTypeId.VOIDRAY) * self.counterTable[20][0]
                    ph = self.knowledge.enemy_units_manager.unit_count(UnitTypeId.PHOENIX) * self.counterTable[21][0]
                    co = self.knowledge.enemy_units_manager.unit_count(UnitTypeId.COLOSSUS) * self.counterTable[22][0]
                    te = self.knowledge.enemy_units_manager.unit_count(UnitTypeId.TEMPEST) * self.counterTable[23][0]
                    hi = self.knowledge.enemy_units_manager.unit_count(UnitTypeId.HIGHTEMPLAR) * self.counterTable[24][0]
                    di = self.knowledge.enemy_units_manager.unit_count(UnitTypeId.DISRUPTOR) * self.counterTable[25][0]
                    da = self.knowledge.enemy_units_manager.unit_count(UnitTypeId.DARKTEMPLAR) * self.counterTable[26][0]
                    ar = self.knowledge.enemy_units_manager.unit_count(UnitTypeId.ARCHON) * self.counterTable[27][0]
                    pc = self.knowledge.enemy_units_manager.unit_count(UnitTypeId.PHOTONCANNON) * self.counterTable[28][0]
                    oc = self.knowledge.enemy_units_manager.unit_count(UnitTypeId.ORACLE) * self.counterTable[29][0]
                    ca = self.knowledge.enemy_units_manager.unit_count(UnitTypeId.CARRIER) * self.counterTable[30][0]

                    if (ze + st + ad + se + im + vo + ph + co + te + hi + di + da + ar + pc + oc + ca) > 0:
                        self.ideal_zealot_ratio = (ze * self.counterTable[15][1] + st * self.counterTable[16][1] +
                                                   ad * self.counterTable[17][1] + se * self.counterTable[18][1] +
                                                   im * self.counterTable[19][1] + vo * self.counterTable[20][1] +
                                                   ph * self.counterTable[21][1] + co * self.counterTable[22][1] +
                                                   te * self.counterTable[23][1] + hi * self.counterTable[24][1] +
                                                   di * self.counterTable[25][1] + da * self.counterTable[26][1] +
                                                   ar * self.counterTable[27][1] + pc * self.counterTable[28][1] +
                                                   oc * self.counterTable[29][1] + ca * self.counterTable[30][1]) / \
                                                  (ze + st + ad + se + im + vo + ph + co + te + hi + di + da + ar + pc + oc + ca)

                        self.ideal_stalker_ratio = (ze * self.counterTable[15][2] + st * self.counterTable[16][2] +
                                                    ad * self.counterTable[17][2] + se * self.counterTable[18][2] +
                                                    im * self.counterTable[19][2] + vo * self.counterTable[20][2] +
                                                    ph * self.counterTable[21][2] + co * self.counterTable[22][2] +
                                                    te * self.counterTable[23][2] + hi * self.counterTable[24][2] +
                                                    di * self.counterTable[25][2] + da * self.counterTable[26][2] +
                                                    ar * self.counterTable[27][2] + pc * self.counterTable[28][2] +
                                                    oc * self.counterTable[29][2] + ca * self.counterTable[30][2]) / \
                                                   (ze + st + ad + se + im + vo + ph + co + te + hi + di + da + ar + pc + oc + ca)

                        self.ideal_sentry_ratio = (ze * self.counterTable[15][3] + st * self.counterTable[16][3] +
                                                   ad * self.counterTable[17][3] + se * self.counterTable[18][3] +
                                                   im * self.counterTable[19][3] + vo * self.counterTable[20][3] +
                                                   ph * self.counterTable[21][3] + co * self.counterTable[22][3] +
                                                   te * self.counterTable[23][3] + hi * self.counterTable[24][3] +
                                                   di * self.counterTable[25][3] + da * self.counterTable[26][3] +
                                                   ar * self.counterTable[27][3] + pc * self.counterTable[28][3] +
                                                   oc * self.counterTable[29][3] + ca * self.counterTable[30][3]) / \
                                                  (ze + st + ad + se + im + vo + ph + co + te + hi + di + da + ar + pc + oc + ca)
                    else:
                        self.ideal_zealot_ratio = 0.3
                        self.ideal_stalker_ratio = 0.65
                        self.ideal_sentry_ratio = 0.05

                elif self.knowledge.enemy_race == Race.Terran:
                    ma = self.knowledge.enemy_units_manager.unit_count(UnitTypeId.MARINE) * self.counterTable[31][0]
                    re = self.knowledge.enemy_units_manager.unit_count(UnitTypeId.REAPER) * self.counterTable[32][0]
                    mr = self.knowledge.enemy_units_manager.unit_count(UnitTypeId.MARAUDER) * self.counterTable[33][0]
                    gh = self.knowledge.enemy_units_manager.unit_count(UnitTypeId.GHOST) * self.counterTable[34][0]
                    he = (self.knowledge.enemy_units_manager.unit_count(UnitTypeId.HELLION) + self.knowledge.enemy_units_manager.unit_count(UnitTypeId.HELLIONTANK)) * self.counterTable[35][0]
                    wi = self.knowledge.enemy_units_manager.unit_count(UnitTypeId.WIDOWMINE) * self.counterTable[36][0]
                    cy = self.knowledge.enemy_units_manager.unit_count(UnitTypeId.CYCLONE) * self.counterTable[37][0]
                    si = (self.knowledge.enemy_units_manager.unit_count(UnitTypeId.SIEGETANK) + self.knowledge.enemy_units_manager.unit_count(UnitTypeId.SIEGETANKSIEGED)) * self.counterTable[38][0]
                    th = self.knowledge.enemy_units_manager.unit_count(UnitTypeId.THOR) * self.counterTable[39][0]
                    vi = (self.knowledge.enemy_units_manager.unit_count(UnitTypeId.VIKINGASSAULT) + self.knowledge.enemy_units_manager.unit_count(UnitTypeId.VIKINGFIGHTER)) * self.counterTable[40][0]
                    me = self.knowledge.enemy_units_manager.unit_count(UnitTypeId.MEDIVAC) * self.counterTable[41][0]
                    li = self.knowledge.enemy_units_manager.unit_count(UnitTypeId.LIBERATOR) * self.counterTable[42][0]
                    ra = self.knowledge.enemy_units_manager.unit_count(UnitTypeId.RAVEN) * self.counterTable[43][0]
                    ba = self.knowledge.enemy_units_manager.unit_count(UnitTypeId.BANSHEE) * self.counterTable[44][0]
                    bc = self.knowledge.enemy_units_manager.unit_count(UnitTypeId.BATTLECRUISER) * self.counterTable[45][0]

                    if (ma + re + mr + gh + he + wi + cy + si + th + vi + me + li + ra + ba + bc) > 0:
                        self.ideal_zealot_ratio = (ma * self.counterTable[31][1] + re * self.counterTable[32][1] +
                                                   mr * self.counterTable[33][1] + gh * self.counterTable[34][1] +
                                                   he * self.counterTable[35][1] + wi * self.counterTable[36][1] +
                                                   cy * self.counterTable[37][1] + si * self.counterTable[38][1] +
                                                   th * self.counterTable[39][1] + vi * self.counterTable[40][1] +
                                                   me * self.counterTable[41][1] + li * self.counterTable[42][1] +
                                                   ra * self.counterTable[43][1] + ba * self.counterTable[44][1] +
                                                   bc * self.counterTable[45][1]) / \
                                                  (ma + re + mr + gh + he + wi + cy + si + th + vi + me + li + ra + ba + bc)

                        self.ideal_stalker_ratio = (ma * self.counterTable[31][2] + re * self.counterTable[32][2] +
                                                    mr * self.counterTable[33][2] + gh * self.counterTable[34][2] +
                                                    he * self.counterTable[35][2] + wi * self.counterTable[36][2] +
                                                    cy * self.counterTable[37][2] + si * self.counterTable[38][2] +
                                                    th * self.counterTable[39][2] + vi * self.counterTable[40][2] +
                                                    me * self.counterTable[41][2] + li * self.counterTable[42][2] +
                                                    ra * self.counterTable[43][2] + ba * self.counterTable[44][2] +
                                                    bc * self.counterTable[45][2]) / \
                                                   (ma + re + mr + gh + he + wi + cy + si + th + vi + me + li + ra + ba + bc)

                        self.ideal_sentry_ratio = (ma * self.counterTable[31][3] + re * self.counterTable[32][3] +
                                                   mr * self.counterTable[33][3] + gh * self.counterTable[34][3] +
                                                   he * self.counterTable[35][3] + wi * self.counterTable[36][3] +
                                                   cy * self.counterTable[37][3] + si * self.counterTable[38][3] +
                                                   th * self.counterTable[39][3] + vi * self.counterTable[40][3] +
                                                   me * self.counterTable[41][3] + li * self.counterTable[42][3] +
                                                   ra * self.counterTable[43][3] + ba * self.counterTable[44][3] +
                                                   bc * self.counterTable[45][3]) / \
                                                  (ma + re + mr + gh + he + wi + cy + si + th + vi + me + li + ra + ba + bc)
                    else:
                        self.ideal_zealot_ratio = 0.3
                        self.ideal_stalker_ratio = 0.65
                        self.ideal_sentry_ratio = 0.05

                else:
                    self.ideal_zealot_ratio = 0.3
                    self.ideal_stalker_ratio = 0.65
                    self.ideal_sentry_ratio = 0.05

                # Determine the current gateway unit ratio
                if len(self.cache.own(UnitTypeId.ZEALOT)) + len(self.cache.own(UnitTypeId.STALKER)) + len(self.cache.own(UnitTypeId.SENTRY)) > 0:
                    own_total = len(self.cache.own(UnitTypeId.ZEALOT)) + len(self.cache.own(UnitTypeId.STALKER)) + len(self.cache.own(UnitTypeId.SENTRY))
                    self.current_zealot_ratio = len(self.cache.own(UnitTypeId.ZEALOT)) / own_total
                    self.current_stalker_ratio = len(self.cache.own(UnitTypeId.STALKER)) / own_total
                    self.current_sentry_ratio = len(self.cache.own(UnitTypeId.SENTRY)) / own_total

                # Compare the ideal unit ratio with the current and choose to build the unit that is the furthest away from its ideal ratio
                build = np.argmax([round(self.ideal_zealot_ratio-self.current_zealot_ratio, 2),
                                   round(self.ideal_stalker_ratio-self.current_stalker_ratio, 2),
                                   round(self.ideal_sentry_ratio-self.current_sentry_ratio, 2)])

                if build == 0:
                    self.unit_type = UnitTypeId.ZEALOT
                elif build == 1:
                    self.unit_type = UnitTypeId.STALKER
                else:
                    self.unit_type = UnitTypeId.SENTRY

                if self.ai.already_pending_upgrade(UpgradeId.WARPGATERESEARCH) >= 1:
                    if self.is_done:
                        return True
                    # Ensure that unit types are the same, python please some proper setters and getters?!?
                    self.warp.to_count = self.to_count
                    self.warp.unit_type = self.unit_type
                    return await self.warp.execute()

        return await super().execute()
