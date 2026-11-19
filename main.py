from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

player = FirstPersonController()
playerhealth = 100
playerhitbox = Entity(parent=player, model='models/bean.obj', scale=(0.75), visible=False, collider='box')
player.ignore_list.append(playerhitbox)
PlayerHealthText = Text(text=f"HP: {playerhealth}",position=(-0.6, -0.35), scale=(4.5))


viewmodelarm = Entity(parent=camera, model='models/arm.obj', color=color.peach, position=(1.1, -1, 0.5), scale=0.3)
gun = Entity(parent=camera, model='models/gun.obj',color=color.black,position=(1.5, -1, 2), scale=0.8)
gun_start_x = gun.x
gun_start_y = gun.y
gun_start_z = gun.z

recoil = 0

def shoot():
    global recoil
    recoil = 0.5
    hit = raycast(camera.world_position, camera.forward,distance=100)
    if hit.hit:
        if hasattr(hit.entity, 'health'):
            hit.entity.health -= 25
            print(f"You hit for {hit.entity.health} damage")

            if hit.entity.health <= 0:
                enemydead = True
                print(f"You killed {hit.entity}")
                hit.entity.disable()
                invoke(respawnenemy, delay=1)

def enemyshoot():
    invoke(enemyshoot, delay=2)
    if enemy1.enabled:    
        direction = Vec3((player.position + Vec3(0, 1.5, 0)) - enemy1.position).normalized()
        bullet = Entity(model="cube",color=color.yellow,scale=0.2, position=enemy1.position, collider='box')
        def move_bullet():
            bullet.position += direction * 5 * time.dt
            if distance(bullet.position, player.position + Vec3(0, 1.5, 0)) < 0.8:
                playerHit()
                bullet.disable()
                destroy(bullet)
        bullet.update = move_bullet
        destroy(bullet, delay=6)

def respawnenemy():
    enemy1.enable()
    enemy1.health = 100
    enemy1.position = (random.uniform(-8, 8), 2.0, random.uniform(-8, 8))

def input(key):
    if key == 'left mouse down':
        shoot()
    if key == 'right mouse down':
        ads()

def ads():
    global gun_start_x, gun_start_y, gun_start_z
    gun_start_x = 0.65
    gun_start_y = -0.75
    gun_start_z = 1.3 
    viewmodelarm.position = (0.1, -0.9, -0.2)

def update():
    global recoil
    if enemy1.enabled:
        enemy1.look_at(player)
        enemy1.rotation_x = 0
        enemy1.rotation_z = 0
    MOVING = (held_keys['w'] or held_keys['s'] or held_keys['a'] or held_keys['d'])
    recoil = lerp(recoil, 0, 10 * time.dt) # makes gun go down after recoil
    if MOVING:
        bob_speed = 6
        bob_amount = 0.1
    else:
        bob_speed = 2
        bob_amount = 0.05
    gun.y = gun_start_y + sin(time.time() * bob_speed) * bob_amount
    gun.z = gun_start_z - recoil
    gun.x = gun_start_x
 
def playerHit():
    global playerhealth
    playerhealth -= 10
    PlayerHealthText.text = f"HP: {playerhealth}"
    print("You lost 10 hp!")
Sky()

enemy1 = Entity(model='models/bean.obj',color=color.white,scale=0.75,position=(0, 2, 5), collider='box')
enemyshoot()
enemy1.health = 100
enemydead = False

floor = Entity(model='plane',scale=20,color=color.green,collider='box')

wall1 = Entity(model='cube', scale=(20, 3, 1), position=(0, 1.5,10), color=color.gray, collider='box')
wall2 = Entity(model='cube',scale=(20, 3, 1),position=(0, 1.5, -10),color=color.gray,collider='box')
wall3 = Entity(model='cube',scale=(1, 3, 20),position=(10, 1.5, 0),color=color.gray,collider='box')
wall4 = Entity(model='cube',scale=(1, 3, 20),position=(-10, 1.5, 0),color=color.gray,collider='box')

app.run()