import pygame
import math
import sys
import random

def create_guassian(width, height, sigma=1, color=pygame.Vector3(1, 1, 1)):
    
    surf = pygame.surface.Surface((int(width), int(height))).convert_alpha()
    for y in range(width):
        for x in range(height):
            r2 = (x - width/2)**2 + (y - height/2)**2
            g = math.exp(-0.5*r2/(sigma**2))
            c = color.copy()
            # a = g
            a = g/5
            c *= 255
            
            surf.set_at((x, y), (int(c.x), int(c.y), int(c.z), int(a*255)))
                
    return surf

class Particle:

    def __init__(self, pos, size, lifetime, velocity, surf, parent_system):
        self.pos = pos
        self.lifetime = lifetime
        self.age = 0
        self.size = size
        self.velocity = velocity
        self.parent_system = parent_system

        self.surf = surf

        # randomize the lifetime and the velocity a bit
        t = random.random()
        self.lifetime = self.lifetime*(1 - t) + t*(self.lifetime + self.lifetime*0.5)

        t = random.random()
        self.velocity = self.velocity*(1 - t) + t*(self.velocity + self.velocity*0.1)
    
    def update(self, delta):
        self.pos += delta*self.velocity
        self.age += delta
        if self.age >= self.lifetime:
            self.parent_system.remove_particle(self)
        
        t = self.age/self.lifetime
        self.surf.set_alpha(int(255*(1 - t)))

    def draw(self):
        surf = pygame.display.get_surface()
        surf.blit(self.surf, (int(self.pos.x - self.size.x/2), int(self.pos.y - self.size.y/2)))

class ParticleSystem:

    def __init__(self, n, pos, lifetime=1, color=pygame.Vector3(0, 0, 0)):
        self.n = n
        self.e_t = 1/n
        self.t = 0
        self.particles = []
        self.pos = pos
        self.g_surf = create_guassian(50, 50, sigma=6, color=color)
        self.lifetime = lifetime

    def emit(self, delta):
        self.t += delta
    
        new_particles = []
        while self.t > self.e_t:
            new_particle = Particle(
                pos=self.pos, 
                size=pygame.Vector2(50, 50),
                lifetime=self.lifetime,
                velocity=100*pygame.Vector2(0.3*(random.random() - random.random()), -1).normalize(),
                surf=self.g_surf,
                parent_system=self)
            self.particles.append(new_particle)
            self.t -= self.e_t

    
    def update(self, delta):
        self.emit(delta)
        for particle in self.particles:
            particle.update(delta)

    def draw(self):
        for particle in self.particles:
            particle.draw()
    
    def remove_particle(self, particle):
        i = self.particles.index(particle)
        del self.particles[i]

def main():

    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Particle System")

    particle_system_1 = ParticleSystem(100, [100, 300])
    particle_system_2 = ParticleSystem(100, [200, 300], color=pygame.Vector3(.9, 0.3, 0))
    particle_system_3 = ParticleSystem(100, [300, 300], color=pygame.Vector3(0, 0, 1))
    particle_system_4 = ParticleSystem(100, [400, 300], color=pygame.Vector3(0, 1, 0))

    clock = pygame.time.Clock()
    delta = 0
    times = 0
    while True:
        clock.tick()
        fps = clock.get_fps()
        if times%50 == 0:
            print(f"fps: {fps}")
        times += 1
        if fps:
            delta = 1/fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        particle_system_1.update(delta)
        particle_system_2.update(delta)
        particle_system_3.update(delta)
        particle_system_4.update(delta)
        
        screen.fill((100, 100, 100))
        particle_system_1.draw()
        particle_system_2.draw()
        particle_system_3.draw()
        particle_system_4.draw()
        pygame.display.update()

if __name__ == "__main__":
    main()