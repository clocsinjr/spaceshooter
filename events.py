import random
import pygame

import entity

EVENT_NONE = 0
EVENT_FODDER = 1
EVENT_SINE = 2
EVENT_GRUNT = 3
EVENT_SENTRY = 4

EVENT_HPUP = 5
EVENT_SCOPE = 6
EVENT_AS = 7

enemySpawn = {EVENT_FODDER: [], EVENT_SINE: [],
              EVENT_GRUNT: [], EVENT_SENTRY: []}
buffSpawn = {EVENT_HPUP: [], EVENT_SCOPE: [], EVENT_AS: []}


def addEventFodder(size):
    x = random.randint(entity.RFODDER, size[0] - entity.RFODDER)
    enemySpawn[EVENT_FODDER].append([x])


def addEventSentry(size):
    x = random.randint(entity.RSENTRY, size[0] - entity.RSENTRY)
    enemySpawn[EVENT_SENTRY].append([x])


def addEventSinewave(size):
    # choose an originx that will fit the whole sine wave
    x = random.randint(entity.RSINE + entity.SINEAMP,
                       size[0] - entity.RSINE - entity.SINEAMP)
    num = random.randint(5, 10)
    thisEvent = []
    for i in range(num):
        thisEvent.append([x])

    enemySpawn[EVENT_SINE].extend(thisEvent)


def addEventGrunt(size):
    x = random.randint(entity.RFODDER, size[0] - entity.RFODDER)
    enemySpawn[EVENT_GRUNT].append([x])


def addEventVgrunts(size):
    # origin x to fit the whole V shape
    x = random.uniform(entity.RGRUNT + 128, size[0] - (entity.RGRUNT + 128))

    thisEvent = []
    thisEvent.append([(x - 128), (x + 128)])
    thisEvent.append([None])
    thisEvent.append([(x - 64), (x + 64)])
    thisEvent.append([None])
    thisEvent.append([x])

    enemySpawn[EVENT_GRUNT].extend(thisEvent)


def addEventHPup(size):
    x = random.randint(entity.RFODDER, size[0] - entity.RFODDER)
    buffSpawn[EVENT_HPUP].append([x])


def addEventScope(size):
    x = random.randint(entity.RFODDER, size[0] - entity.RFODDER)
    buffSpawn[EVENT_SCOPE].append([x])


def addEventAS(size):
    x = random.randint(entity.RFODDER, size[0] - entity.RFODDER)
    buffSpawn[EVENT_AS].append([x])


def addEvents(size, difficulty):
    twentieth = (1.0 / 200.0)
    fiftheenth = (1.0 / 150.0)
    twelveth = (1.0 / 120.0)
    tenth = (1.0 / 100.0)

    # add enemy events
    if random.random() < fiftheenth * difficulty:
        type = random.randint(1, 10)
        if len(enemySpawn[EVENT_SINE]) == 0 and type <= 6:
            addEventSinewave(size)
        elif len(enemySpawn[EVENT_GRUNT]) == 0 and type > 6:
            addEventVgrunts(size)

    # add randomly placed fodders and grunts
    timesFodder = timesGrunt = 0
    for i in range(16):
        if random.random() < twelveth * difficulty:
            timesFodder += 1
        if random.random() < twentieth * difficulty:
            timesGrunt += 1
    for j in range(0, timesFodder):
        addEventFodder(size)
    for j in range(0, timesFodder):
        addEventGrunt(size)

    # add randomly placed sentries
    if random.random() < fiftheenth * difficulty:
        addEventSentry(size)

    # add randomly placed scopes, ASes and HPups
    if random.random() < fiftheenth:
        addEventScope(size)
    if random.random() < fiftheenth:
        addEventAS(size)
    if random.random() < fiftheenth * difficulty:
        addEventHPup(size)
