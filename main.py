from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import basic_lighting_shader
import random

app = Ursina()
Entity.default_shader = basic_lighting_shader
Sky()

player = FirstPersonController()
playerhealth = 100
playerhitbox = Entity(parent=player, model='models/bean.obj', scale=(0.75), visible=False, collider='box')
player.ignore_list.append(playerhitbox) # hitbox ignores player character
PlayerHealthText = Text(text=f"HP: {playerhealth}",position=(-0.6, -0.35), scale=(4.5))

viewmodelarm = Entity(parent=camera, model='models/arm.obj', color=color.peach, position=(1.1, -1, 0.5), scale=0.3)
gun = Entity(parent=camera, model='models/gun.obj',color=color.black,position=(1.5, -1, 2), scale=0.8)
gun_start_x = gun.x
gun_start_y = gun.y
gun_start_z = gun.z

gamestarted = False
recoil = 0
aiming = False

def shoot():
    '''Player raycast shooting system, every click input shoots a raycast
    towards player cursor and makes sure that it only deals damage towards enemies
    '''
    global recoil
    recoil = 0.5
    hit = raycast(camera.world_position, camera.forward,distance=100)
    if hit.hit:
        if hasattr(hit.entity, 'health'):
            hit.entity.health -= 25
            print(f"You hit for {hit.entity.health} damage")

            if hit.entity.health <= 0:
                print(f"You killed {hit.entity}")
                hit.entity.disable()
                invoke(respawnenemy, delay=1)

def enemy1shoot():
    '''enemy shooting mechanic, every two seconds the enemy shoots a projectile
    that if hit deals 10 damage to the player
    '''
    invoke(enemy1shoot, delay=2)
    if enemy1.enabled and gamestarted:    
        direction = Vec3((player.position + Vec3(0, 1.5, 0)) - enemy1.position).normalized()
        bullet = Entity(model="cube",color=color.yellow,scale=0.2, position=enemy1.position, collider='box')
        def move_bullet():
            '''Bullet velocity mechanic which shoots towards current
            player position and gets destroyed after 6 seconds or after
            inside player vector
            '''
            bullet.position += direction * 5 * time.dt
            if distance(bullet.position, player.position + Vec3(0, 1.5, 0)) < 0.8:
                playerHit()
                bullet.disable()
                destroy(bullet)
        bullet.update = move_bullet
        destroy(bullet, delay=6)

def respawnenemy():
    '''When this function is called, Enemy1 is randomly respawned anywhere on the xy
    axis of the floor plane
    '''
    enemy1.enable()
    enemy1.health = 100
    enemy1.position = (random.uniform(-8, 8), 2.0, random.uniform(-8, 8))

def input(key):
    if not gamestarted:
        return
    if key == 'left mouse down':
        shoot()
    if key == 'right mouse down':
        ads()
    if key == 'right mouse up':
        unads()

def ads():
    '''brings gun viewmodel and arm towards the center of the screen when the player
    holds down right click
    '''
    global gun_start_x, gun_start_y, gun_start_z, aiming
    aiming = True
    gun_start_x = 0.65
    gun_start_y = -0.72
    gun_start_z = 1.3 
    viewmodelarm.position = 0, -0.6, -0.2
    viewmodelarm.scale = 0.20

def unads():
    '''moves gun back to starting position when player releases right click
    '''
    global gun_start_x, gun_start_y, gun_start_z, aiming
    aiming = False
    gun_start_x = 1.5
    gun_start_y = -1
    gun_start_z = 2
    viewmodelarm.position = 1.1, -1, 0.5
    viewmodelarm.scale = 0.3

def update():
    '''functions as a while loop. It updates all entities, objects, & inputs every tick
    '''
    global recoil
    death()
    PlayerHealthText.text = f"HP: {playerhealth}"
    if enemy1.enabled:
        enemy1.look_at(player)
        enemy1.rotation_x = 0
        enemy1.rotation_z = 0
    MOVING = (held_keys['w'] or held_keys['s'] or held_keys['a'] or held_keys['d'])
    recoil = lerp(recoil, 0, 10 * time.dt) # makes gun go down after recoil
    if aiming:
        bob_speed = 2
        bob_amount = 0.01
    elif MOVING:
        bob_speed = 6
        bob_amount = 0.1
    else:
        bob_speed = 2
        bob_amount = 0.05
    gun.y = gun_start_y + sin(time.time() * bob_speed) * bob_amount
    gun.z = gun_start_z - recoil
    gun.x = gun_start_x

def playerHit():
    '''If enemy bullet touches the Player Vector, the player loses
    health
    '''
    global playerhealth
    playerhealth -= 100
    print("You lost 10 hp!")

enemy1 = Entity(model='models/bean.obj',color=color.white,scale=0.75,position=(0, 2, 5), collider='box')
enemy1shoot()
enemy1.health = 100

floor = Entity(model='plane',scale=20,color=color.green,collider='box')

wall1 = Entity(model='cube', scale=(20, 3, 1), position=(0, 1.5,10), color=color.gray, collider='box')
wall2 = Entity(model='cube',scale=(20, 3, 1),position=(0, 1.5, -10),color=color.gray,collider='box')
wall3 = Entity(model='cube',scale=(1, 3, 20),position=(10, 1.5, 0),color=color.gray,collider='box')
wall4 = Entity(model='cube',scale=(1, 3, 20),position=(-10, 1.5, 0),color=color.gray,collider='box')

title = Text(text='Fps Gaem', origin=(0, 0), y=0.25, scale=3)
startbutton = Button(text='start!?', scale=(0.25, 0.1), y=-0.05)

def spawn_point():
    player.x = 0
    player.z = 0

def start_game():
    '''When Player launches the game the cursor is unlocked, the player
    is given the option to manually start the game
    '''
    spawn_point()
    redscreen.disable()
    gun.enable()
    viewmodelarm.enable()
    camera.rotation_z = 0
    global gamestarted, playerhealth
    playerhealth = 100
    gamestarted = True
    title.disable()
    startbutton.disable()
    restartbutton.disable()
    player.enable()
    mouse.locked = True

def game_over():
    '''When this function is called, the game gives the player
    the option to restart or exit the game
    '''
    redscreen.enable()
    camera.animate('rotation_z', 70)
    camera.animate_y(-0.5)
    viewmodelarm.disable()
    gun.disable()
    global gamestarted
    gamestarted = False
    player.disable()
    mouse.locked = False
    restartbutton.enable()

def death():
    '''when this function is called, the game checks if Playerhealth is less than
    or equal to 0, if true it calls for the game_over function
    '''
    if playerhealth <= 0 and gamestarted:
        game_over()

mouse.locked = False
player.disable()

redscreen = Entity(parent=camera.ui,model='quad',scale=(3,3), color=Color(1, 0, 0, 0.5), enabled=False)
restartbutton = Button(text='Restart!?', scale=(0.25, 0.1), y=-0.05)
restartbutton.disable()
restartbutton.on_click = start_game
startbutton.on_click = start_game

sun=DirectionalLight(shadows=False)
sun.look_at(Vec3(1, -1, 1))
app.run()