from vpython import *
import time
import numpy as np
dt = 0.01
m = 1
t = 0
r = 0.05
mycolors = [color.red, color.blue, color.green]
dim_x = 10
dim_y = 10
dim_z = 0.1
sim_length = 10000  # frames
max_ptl = 100


def change_size_from_txt():
    try:
        f = open("size.txt", "r")
        lines = f.readlines()
        if len(lines) > 0:
            ball.radius = float(lines[0])
        f.close()
    except e:
        pass


def vec_mag(vec):
    return sqrt(vec.x**2 + vec.y**2)

class Scene:

    def __init__(self):
        self.actors = []
        self.base = box(pos=vector(0, 0, -0.2), size=vector(dim_x, dim_y, dim_z), color=color.white)

    def get_force(self, pos, vel):
        _v = vec_mag(vel)
        _r = vec_mag(pos)
        _mag = 0.998 * (m * _v ** 2) / _r
        return vector(_mag * -pos.x / _r, _mag * -pos.y / _r, vel.z)

    def spawn_pos(self):
        return vector(10*random(), 10*random(), 0)
        pass

    def add_actor(self, id, bd=0):
        c = mycolors[id]
        coord = self.spawn_pos()
        actor = sphere(pos=vector(coord), radius=r, color=c)
        #actor = sphere(pos=vector(1, 0, 0), radius=r, color=c)
        actor.pos = vector(0.1, 0, 0)
        actor.id = id
        actor.count = 1
        actor.vel = vector(0, 1, 0)
        actor.pos_pc = [actor.pos]
        actor.vel_pc = [actor.vel]
        actor.bd = bd
        self.actors.append(actor)

    def precal_pos(self, id = -1):
        if id == -1:
            start = 0
            stop = len(self.actors)
        else:
            start = id
            stop = id + 1
        for j in range(1,sim_length):
            for i in range(start, stop):
                # Recalculate velocity
                # delta_v = a * delta_t
                # delta_v = (F/m) * delta_t
                vel = self.actors[i].vel_pc[j-1]
                pos = self.actors[i].pos_pc[j-1]
                x = pos.x
                y = pos.y
                z = pos.z
                fc = self.get_force(pos, vel)
                dvx = fc.x / m * dt
                dvy = fc.y / m * dt
                vel_new = vector(vel.x + dvx, vel.y + dvy, fc.z)
                scl = vec_mag(vel)/vec_mag(vel_new)
                vel_new = vector(scl*(vel.x + dvx), scl*(vel.y + dvy), fc.z)

                # Advance position
                dx = vel.x * dt + 0.5*fc.x * dt**2
                dy = vel.y * dt + 0.5*fc.y * dt**2
                dz = 0.0005

                #dz = 0
                pos = vector(x + dx, y + dy, z + dz)
                self.actors[i].pos_pc.append(pos)
                self.actors[i].vel_pc.append(vel_new)

    def update_pos_pc(self, tick):
        for i in range(len(self.actors)):
            bd = self.actors[i].bd
            if tick > bd:
                self.actors[i].pos = self.actors[i].pos_pc[tick - bd]
                self.actors[i].vel = self.actors[i].vel_pc[tick - bd]

    def update_pos(self):
        for i in range(len(self.actors)):
            x = self.actors[i].pos.x
            y = self.actors[i].pos.y
            z = self.actors[i].pos.z

            # Recalculate velocity
            # delta_v = a * delta_t
            # delta_v = (F/m) * delta_t
            vel = self.actors[i].vel
            pos = self.actors[i].pos
            fc = self.get_force(pos, vel)
            dvx = fc.x / m * dt
            dvy = fc.y / m * dt
            vel_new = vector(vel.x + dvx, vel.y + dvy, fc.z)
            scl = vec_mag(vel)/vec_mag(vel_new)
            vel_new = vector(scl*(vel.x + dvx), scl*(vel.y + dvy), fc.z)

            # Advance position
            dx = vel.x * dt + 0.5*fc.x * dt**2
            dy = vel.y * dt + 0.5*fc.y * dt**2
            dz = 0.0005

            #dz = 0
            pos = vector(x + dx, y + dy, z + dz)
            self.actors[i].pos = pos
            self.actors[i].vel = vel_new

    def out_of_bounds(self):
        kill = []
        for i in range(len(self.actors)):
            x = self.actors[i].pos.x
            y = self.actors[i].pos.y
            z = self.actors[i].pos.z
            if abs(x) > dim_x/2 or abs(y) > dim_y/2 or abs(z) > 10:
                self.actors[i].radius = 0
                kill.append(i)
        for i in kill:
            del self.actors[i]



if __name__ == "__main__":
    scene = Scene()
    scene.add_actor(1)
    ticks = 0
    scene.precal_pos()
    for i in range(sim_length):
        ticks = ticks + 1
        rnd = int(100 * random())+1
        if ticks % rnd == 0 and len(scene.actors) < max_ptl:
            scene.add_actor(int(3*random()), bd = ticks)
            scene.precal_pos(len(scene.actors)-1)
    ticks = 0
    for frame in range(sim_length):
        ticks = ticks + 1
        scene.update_pos_pc(ticks)
        scene.out_of_bounds()
        rate(100)


    #scene.run()
