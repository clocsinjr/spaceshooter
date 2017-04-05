"""
 Show how to use a sprite backed by a graphic.
 
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
 Explanation video: http://youtu.be/vRB_983kUMc
"""

import math
import random
import time as pytime
import pygame

import global_vars as g
import entity
import images
import sounds
import events
import gui

SIZE_SCALE = 0.8
# Define some colors
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
CYAN = 52223
pygame.init()

# Set the width and height of the screen [width, height]
size = (int(600 * SIZE_SCALE), int(920 * SIZE_SCALE))
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Cloc's Spacex")

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# set buttonrepeating on
pygame.key.set_repeat(1, 10)

pygame.mouse.set_visible(False)



def game_reset():
    g.playerGroup.empty()
    g.pickups.empty()
    g.fProj.empty()
    g.eProj.empty()
    g.enemies.empty()
    
    g.player = entity.player(size)
    g.player.add(g.playerGroup)
    
    g.time = 0
    g.difficulty = 1.0
    g.diffcount = 1
    
def drawEntities():
    # draw player
    g.playerGroup.draw(screen)

    # draw enemies
    g.enemies.draw(screen)

    # draw projectiles
    g.fProj.draw(screen)
    g.eProj.draw(screen)

    g.pickups.draw(screen)

    # draw the blue laserpointer if the player picked up a scope pickup
    if g.player.scopeTime > 0 and g.player.alive:
        start_pos = (g.player.rect[0] + entity.PSIZE, g.player.rect[1])
        end_pos = (g.player.rect[0] + entity.PSIZE, 0)
        pygame.draw.line(screen, CYAN, start_pos, end_pos, 1)


def spawnEnemy(type, x):
    enemy = None
    if type == events.EVENT_FODDER:
        enemy = entity.fodder(size, x, 0)
    elif type == events.EVENT_SINE:
        enemy = entity.sine(size, x, 0)
    elif type == events.EVENT_GRUNT:
        enemy = entity.grunt(size, x, 0)
    elif type == events.EVENT_SENTRY:
        enemy = entity.sentry(size, x, 0)

    enemy.add(g.enemies)


def spawnBuff(type, x):
    buff = None
    if type == events.EVENT_HPUP:
        buff = entity.hpup(size, x, 0)
    elif type == events.EVENT_SCOPE:
        buff = entity.scope(size, x, 0)
    elif type == events.EVENT_AS:
        buff = entity.AS(size, x, 0)
    buff.add(g.pickups)


def handleEvents():
    # add events to the event queues
    events.addEvents(size)

    # check the enemy event queues for tasks and execute them
    for eventType in events.enemySpawn:
        if len(events.enemySpawn[eventType]) == 0:
            continue

        # get coordinates list for this task type
        coords = events.enemySpawn[eventType].pop()

        for x in coords:
            if x is not None:
                spawnEnemy(eventType, x)

    # check the buffs event queues for tasks
    for eventType in events.buffSpawn:
        if len(events.buffSpawn[eventType]) == 0:
            continue
        coords = events.buffSpawn[eventType].pop()
        for x in coords:
            if x is not None:
                spawnBuff(eventType, x)


""" Check for collisions with projectiles. """


def checkCollisions():
    playerhit = False
    # check for collisions between friendly projectiles and enemies
    coldict = pygame.sprite.groupcollide(g.enemies, g.fProj, False, True)

    # keys: enemies hit, values: lists of intersecting projectiles
    if coldict != {}:
        sounds.hitMarker.play(sounds.hitEnemySound)

        # check for all projectiles and enemies for collisions
        for enemyHit in coldict:
            for projs in coldict[enemyHit]:

                # play sounds and adjust stats based on projectiles and Hp
                enemyHit.HP -= projs.DMG
                if enemyHit.HP <= 0.0:
                    sounds.hitMarker.play(sounds.killEnemySound)
                    enemyHit.kill()
                    g.player.score += enemyHit.points

    # check enemy projectile collisions with player
    coldict = pygame.sprite.groupcollide(g.playerGroup, g.eProj, False, True)
    if coldict != {}:
        sounds.playerHit.play(sounds.hitPlayerSound)
        for projs in coldict[g.player]:
            g.player.HP -= projs.DMG
            playerhit = True

    # check enemy entity collisions with player
    coldict = pygame.sprite.groupcollide(g.playerGroup, g.enemies, False, True)
    if coldict != {}:
        sounds.hitMarker.play(sounds.hitEnemySound)
        for enemy in coldict[g.player]:
            g.player.HP -= 10
            playerhit = True

    # check pickup collisions with player
    coldict = pygame.sprite.groupcollide(g.playerGroup, g.pickups, False, True)
    if coldict != {}:
        sounds.pickups.play(sounds.pickupBuff)
        for buff in coldict[g.player]:
            if isinstance(buff, entity.hpup):
                g.player.HP += buff.HP
                if g.player.HP > 100:
                    g.player.HP = 100

            if isinstance(buff, entity.scope):
                g.player.scopeTime = buff.time

            if isinstance(buff, entity.AS):
                g.player.ASTime = buff.time
                g.player.gunCD = 5.0

    # if the player got a killing blow, play a sound and off the player
    if g.player.HP <= 0.0 and playerhit == True:
        sounds.hitMarker.play(sounds.killEnemySound)
        g.player.alive = False
        g.player.kill()


def updatePlayer(keys):
    # check pressed keys
    left = keys[pygame.K_LEFT]
    right = keys[pygame.K_RIGHT]
    fire = keys[pygame.K_SPACE]

    # move player based on keys
    if left and not right:
        g.player.move(entity.PDIRL, size)
    elif right and not left:
        g.player.move(entity.PDIRR, size)
    if not left and not right:
        g.player.move(entity.PDIRN, size)

    # fire projectiles based on key
    if fire and g.player.gunTime == 0:
        sounds.fireChannel.play(sounds.playerFireSound)
        entity.projectile(g.player).add(g.fProj)
        g.player.gunTime = g.player.gunCD

    # check AS buff
    if g.player.ASTime == 0:
        g.player.gunCD = 10
    g.player.updateTimers()


def updateEnemies():
    for enm in g.enemies:
        enm.move()

        isGrunt = isinstance(enm, entity.grunt)
        isSentry = isinstance(enm, entity.sentry)

        if enm.rect[1] > size[1]:
            enm.kill()
        if isGrunt or isSentry:
            enm.gunTime -= 1
            if enm.gunTime <= 0:
                sounds.fireChannel.play(sounds.playerFireSound)
                entity.projectile(enm).add(g.eProj)
                enm.gunTime = enm.gunCD

        if isSentry:
            enm.detFacing(g.player)


def updatePickups():
    for pickup in g.pickups:
        pickup.move()

        if pickup.rect[1] > size[1]:
            pickup.kill()


def updateProjectiles():
    # move projectiles
    for projectile in g.fProj.sprites():
        projectile.moveProjectile()
    for projectile in g.eProj.sprites():
        projectile.moveProjectile()

    # check if friendly projectiles are out of bounds
    for projectile in g.fProj.sprites():
        x = projectile.rect[0]
        y = projectile.rect[1]
        if ((x < 0 or x > size[0]) or (y < 0 or y > size[1])):
            projectile.kill()

    # check if enemy projectiles are out of bounds
    for projectile in g.eProj.sprites():
        x = projectile.rect[0]
        y = projectile.rect[1]
        if ((x < 0 or x > size[0]) or (y < 0 or y > size[1])):
            projectile.kill()


# -------- Main Program Loop -----------
if __name__ == '__main__':
    game_reset()
    
    while not g.done:

        # general input:
        keys = pygame.key.get_pressed()
        menu_key = None
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYUP:
                menu_key = event.key
                if event.key == pygame.K_ESCAPE:
                    pygame.event.clear(pygame.KEYUP)
                    g.paused = not g.paused
        # in-game
        if g.paused != True:
            # --- Game logic should go here
            if g.player.alive:
                updatePlayer(keys)
            updateEnemies()
            updatePickups()
            updateProjectiles()

            checkCollisions()

			# tick every 16 frames
            if g.time % 16 == 0:
                handleEvents()

            if (g.player.score / 250.0) >= g.diffcount:
                g.diffcount += 1
                g.difficulty += 0.10

            # --- Drawing code should go here
            screen.fill(131094)

            drawEntities()


            # --- tick timers

        # when paused:
        else:
            gui.pausemenu.handle(menu_key)

        """ === end else ========================================================== """
        
        gui.drawgui()
        # flip screen
        pygame.display.flip()

        g.time += 1
        clock.tick(FPS)

    # Close the window and quit.
    sounds.hitMarker.play(sounds.killEnemySound)
    pygame.mixer.music.stop()
    pytime.sleep(1)
    pygame.quit()
