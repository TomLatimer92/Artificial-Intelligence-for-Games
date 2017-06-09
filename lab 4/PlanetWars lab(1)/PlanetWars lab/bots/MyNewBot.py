class MyNewBot(object):

    def update(self, gameinfo):

        for g in gameinfo.not_my_planets:
            # print(gameinfo.my_planets)
            src = max(gameinfo.my_planets.values(), key=lambda p: p.num_ships)
            #Find a target planet with the minimum number of ships.
            dest = min(gameinfo.not_my_planets.values(), key=lambda p: p.num_ships)
            #OR, (alternatively), use an inverse proportional maximum search...
            # dest = max(gameinfo.not_my_planets.values(), key=lambda p: 1.0 / (1 + p.num_ships))
            gameinfo.planet_order(src, dest, src.num_ships)
