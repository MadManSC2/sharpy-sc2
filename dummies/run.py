import sc2, sys, random
from ladder import run_ladder_game
from protoss.MadAI import LadderBot
from sc2 import Race, Difficulty
from sc2.player import Bot, Computer

bot = LadderBot()
race = bot.my_race
protoss_bot = Bot(race, bot)


def main():
    if "--LadderServer" in sys.argv:
        # Ladder game started by LadderManager
        print("Starting ladder game...")
        result, opponentid = run_ladder_game(protoss_bot)
        print(result, " against opponent ", opponentid)
    else:
        # Local game
        print("Starting local game...")
        maps = [
            'Acropolis LE',
            'DiscoBloodbath LE',
            'Ephemeron LE',
            'Triton LE',
            'WintersGate LE',
            'WorldofSleepers LE',
            'Thunderbird LE'
        ]

        races = [
            Race.Protoss,
            Race.Terran,
            Race.Zerg
        ]

        selected_map = random.randrange(0, 7)
        race = 0 # random.randrange(0, 3)
        sc2.run_game(sc2.maps.get(maps[selected_map]), [
            Bot(Race.Protoss, bot),
            Computer(races[race], Difficulty.VeryHard)
        ], realtime=False)


if __name__ == '__main__':
    main()
