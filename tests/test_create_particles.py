from main import create_particles, particles
from setup import PARTICLE

def test_create_particles_creates_one_particle_correctly():
    particles = []
    create_particles(x=1, y=2, r=4, g=5, b=6, amount = 1)

    # test that one particle was created
    assert len(particles) == 1

    # test that the created particle has the correct values
    created_particle = particles[0]
    assert created_particle.x == 1
    assert created_particle.y == 2

    r, g, b = created_particle.col
    assert r >= 4-5 and r <= 4+5
    assert g >= 5-5 and g <= 5+5
    assert b >= 6-5 and b <= 6+5

def test_create_particles_creates_the_correct_number_of_particles():
    global particles
    particles = []
    create_particles(x=1, y=2, r=4, g=5, b=6, amount = 3)

    # test that one particle was created
    assert len(particles) == 3

def test_example():
    result = 1+1

    assert result==2

# def test_failing_example():
#     result = 1+1

#     assert result==3