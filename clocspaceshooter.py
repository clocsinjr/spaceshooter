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

import entity
import images
import sounds
import events
import gui

# Define some colors
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
CYAN = 52223
pygame.init()

# Set the width and height of the screen [width, height]
size = (int(600 * 1.0), int(920 * 1.0))
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Cloc's Spacex")

# Loop until the user clicks the close button.
done = False
paused = False
inmenu = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# set buttonrepeating on
pygame.key.set_repeat(1, 10)

pygame.mouse.set_visible(False)

# original gamestate:
playerGroup = pygame.sprite.Group()
pickups = pygame.sprite.Group()
fProj = pygame.sprite.Group()
eProj = pygame.sprite.Group()
enemies = pygame.sprite.Group()

player = entity.player(size)
player.add(playerGroup)

time = 0
difficulty = 1.4
diffcount = 1

pause_selected = 0
mainmenu_selected = 0

def drawEntities():
    # draw player
    playerGroup.draw(screen)

    # draw enemies
    enemies.draw(screen)

    # draw projectiles
    fProj.draw(screen)
    eProj.draw(screen)

    pickups.draw(screen)

    if player.scopeTime > 0 and player.alive:
        start_pos = (player.rect[0] + entity.PSIZE, player.rect[1])
        end_pos = (player.rect[0] + entity.PSIZE, 0)
        pygame.draw.line(screen, CYAN, start_pos, end_pos, 1)


def drawgui():
    scoretxt = scorefont.render("Score: " + str(player.score), False, WHITE)
    screen.blit(scoretxt, (scorex, scorey))

    hptxt = scorefont.render("HP: " + str(player.HP) + "/ 100", False, WHITE)
    screen.blit(hptxt, (hpx, hpy))

    difftext = scorefont.render("Difficulty: " + str(difficulty), False, WHITE)
    screen.blit(difftext, (diffx, diffy))

    hpbarlim = hpbarlen * (player.HP / 100.0) + 1
    hpbarlim2 = hpbarlen * ((100 - player.HP) / 100.0)

    if player.HP > 0.0:
        pygame.draw.rect(screen, GREEN, [hpbarxmin, hpbarymin, hpbarlim, 30])

    if player.HP < 100.0:
        pygame.draw.rect(
            screen, RED, [hpbarlim + hpbarxmin, hpbarymin, hpbarlim2, 30])


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

    enemy.add(enemies)


def spawnBuff(type, x):
    buff = None
    if type == events.EVENT_HPUP:
        buff = entity.hpup(size, x, 0)
    elif type == events.EVENT_SCOPE:
        buff = entity.scope(size, x, 0)
    elif type == events.EVENT_AS:
        buff = entity.AS(size, x, 0)
    buff.add(pickups)


def handleEvents():
    # add events to the event queues
    events.addEvents(size, difficulty)

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
    coldict = pygame.sprite.groupcollide(enemies, fProj, False, True)

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
                    player.score += enemyHit.points

    # check enemy projectile collisions with player
    coldict = pygame.sprite.groupcollide(playerGroup, eProj, False, True)
    if coldict != {}:
        sounds.playerHit.play(sounds.hitPlayerSound)
        for projs in coldict[player]:
            player.HP -= projs.DMG
            playerhit = True

    # check enemy entity collisions with player
    coldict = pygame.sprite.groupcollide(playerGroup, enemies, False, True)
    if coldict != {}:
        sounds.hitMarker.play(sounds.hitEnemySound)
        for enemy in coldict[player]:
            player.HP -= 10
            playerhit = True

    # check pickup collisions with player
    coldict = pygame.sprite.groupcollide(playerGroup, pickups, False, True)
    if coldict != {}:
        sounds.pickups.play(sounds.pickupBuff)
        for buff in coldict[player]:
            if isinstance(buff, entity.hpup):
                player.HP += buff.HP
                if player.HP > 100:
                    player.HP = 100

            if isinstance(buff, entity.scope):
                player.scopeTime = buff.time

            if isinstance(buff, entity.AS):
                player.ASTime = buff.time
                player.gunCD = 5.0

    # if the player got a killing blow, play a sound and off the player
    if player.HP <= 0.0 and playerhit == True:
        sounds.hitMarker.play(sounds.killEnemySound)
        player.alive = False
        player.kill()


def updatePlayer(keys):
    # check pressed keys
    left = keys[pygame.K_LEFT]
    right = keys[pygame.K_RIGHT]
    fire = keys[pygame.K_SPACE]

    # move player based on keys
    if left and not right:
        player.move(entity.PDIRL, size)
    elif right and not left:
        player.move(entity.PDIRR, size)
    if not left and not right:
        player.move(entity.PDIRN, size)

    # fire projectiles based on key
    if fire and player.gunTime == 0:
        sounds.fireChannel.play(sounds.playerFireSound)
        entity.projectile(player).add(fProj)
        player.gunTime = player.gunCD

    # check AS buff
    if player.ASTime == 0:
        player.gunCD = 10
    player.updateTimers()


def updateEnemies():
    for enm in enemies:
        enm.move()

        isGrunt = isinstance(enm, entity.grunt)
        isSentry = isinstance(enm, entity.sentry)

        if enm.rect[1] > size[1]:
            enm.kill()
        if isGrunt or isSentry:
            enm.gunTime -= 1
            if enm.gunTime <= 0:
                sounds.fireChannel.play(sounds.playerFireSound)
                entity.projectile(enm).add(eProj)
                enm.gunTime = enm.gunCD

        if isSentry:
            enm.detFacing(player)


def updatePickups():
    for pickup in pickups:
        pickup.move()

        if pickup.rect[1] > size[1]:
            pickup.kill()


def updateProjectiles():
    # move projectiles
    for projectile in fProj.sprites():
        projectile.moveProjectile()
    for projectile in eProj.sprites():
        projectile.moveProjectile()

    # check if friendly projectiles are out of bounds
    for projectile in fProj.sprites():
        x = projectile.rect[0]
        y = projectile.rect[1]
        if ((x < 0 or x > size[0]) or (y < 0 or y > size[1])):
            projectile.kill()

    # check if enemy projectiles are out of bounds
    for projectile in eProj.sprites():
        x = projectile.rect[0]
        y = projectile.rect[1]
        if ((x < 0 or x > size[0]) or (y < 0 or y > size[1])):
            projectile.kill()


# -------- Main Program Loop -----------
if __name__ == '__main__':
    while not done:

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
                    paused = not paused
        # in-game
        if paused != True:
            # --- Game logic should go here
            if player.alive:
                updatePlayer(keys)
            updateEnemies()
            updatePickups()
            updateProjectiles()

            checkCollisions()

			# tick every 16 frames
            if time % 16 == 0:
                handleEvents()

            if (player.score / 500.0) >= diffcount:
                diffcount += 1
                difficulty *= 1.4

            # --- Drawing code should go here
            screen.fill(131094)

            drawEntities()
            gui.drawgui(player, difficulty)

            # --- tick timers

        # when paused:
        else:
            r_pause = gui.handle_pausemenu(menu_key, pause_selected)
            
            if r_pause['selected'] != None:
                pause_selected = r_pause['selected']
            elif r_pause['done'] != None:
                done = True
            elif  r_pause['pause'] != None:
                paused = not paused
            gui.draw_pausescreen(pause_selected)

        """ === end else ========================================================== """

        # flip screen
        pygame.display.flip()

        time += 1
        clock.tick(FPS)

    # Close the window and quit.
    sounds.hitMarker.play(sounds.hitEnemySound)
    pygame.mixer.music.stop()
    pytime.sleep(1)
    pygame.quit()
