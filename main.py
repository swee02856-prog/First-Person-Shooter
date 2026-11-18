from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

player = FirstPersonController()
player.y += 2

viewmodelarm = Entity(parent=camera, model='models/arm.obj', color=color.peach, position=(1.1, -1, 0.5), scale=0.3)
gun = Entity(parent=camera, model='models/gun.obj',color=color.black,position=(1.5, -1, 2), scale=0.8)
gun_start_y = gun.y
gun_start_x = gun.x
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

def enemyshoot():
    if not enemy1.enabled:
        return
    invoke(enemyshoot, delay=2)
    direction = Vec3(player.x - enemy1.x, 0, player.z - enemy1.z).normalized()
    bullet = Entity(model="cube",color=color.yellow,scale=0.2, position=enemy1.position)
    def move_bullet():
        bullet.position += direction * 5 * time.dt
    bullet.update = move_bullet

def input(key):
    if key == 'left mouse down':
        shoot()

def update():
    global recoil
    if enemydead == False:
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
 
Sky()


enemy1 = Entity(model='cube',color=color.red,scale=2,position=(0, 1, 5), collider='box')
enemy1.health = 100
enemyshoot()
enemydead = False

floor = Entity(model='plane',scale=20,color=color.green,collider='box')

wall1 = Entity(model='cube', scale=(20, 3, 1), position=(0, 1.5,10), color=color.gray, collider='box')
wall2 = Entity(model='cube',scale=(20, 3, 1),position=(0, 1.5, -10),color=color.gray,collider='box')
wall3 = Entity(model='cube',scale=(1, 3, 20),position=(10, 1.5, 0),color=color.gray,collider='box')
wall4 = Entity(model='cube',scale=(1, 3, 20),position=(-10, 1.5, 0),color=color.gray,collider='box')

app.run()