from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

player = FirstPersonController()
player.y += 2

def shoot():
    hit = raycast(camera.world_position, camera.forward,distance=100)
    if hit.hit:
        if hasattr(hit.entity, 'health'):
            hit.entity.health -= 25
            print(f"You hit for {hit.entity.health} damage")

            if hit.entity.health <= 0:
                print(f"You killed {hit.entity}")
                destroy(hit.entity)

def enemyshoot():
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
    enemy1.look_at(player)
    enemy1.rotation_x = 0
    enemy1.rotation_z = 0
enemy1 = Entity(model='cube',color=color.red,scale=2,position=(0, 1, 5), collider='box')
enemy1.health = 100
enemyshoot()

floor = Entity(model='plane',scale=20,color=color.green,collider='box')

wall1 = Entity(model='cube', scale=(20, 3, 1), position=(0, 1.5,10), color=color.gray, collider='box')
wall2 = Entity(model='cube',scale=(20, 3, 1),position=(0, 1.5, -10),color=color.gray,collider='box')
wall3 = Entity(model='cube',scale=(1, 3, 20),position=(10, 1.5, 0),color=color.gray,collider='box')
wall4 = Entity(model='cube',scale=(1, 3, 20),position=(-10, 1.5, 0),color=color.gray,collider='box')

app.run()