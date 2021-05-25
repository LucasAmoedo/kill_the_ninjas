from constants import (
    BULLET_COLLISION_TYPE,
    NINJA_COLLISION_TYPE,
    PLAYER_COLLISION_TYPE
)


class CollisionHandler:
    def __init__(self, space):
        self.space = space

    def add_handlers_to_space(self):

        def handle_bullet_ninja_collision(arbiter, space, data):
            _, ninja_shape = arbiter.shapes
            ninja = ninja_shape.body.reference
            ninja.hit_points -= 1

            return True

        def handle_player_ninja_collision(arbiter, space, data):
            _, player_shape = arbiter.shapes
            player_shape.body.reference.hit_points -= 1

            return True

        bullet_ninja_collision_handler = self.space.add_collision_handler(
            BULLET_COLLISION_TYPE,
            NINJA_COLLISION_TYPE
        )

        bullet_ninja_collision_handler.begin = handle_bullet_ninja_collision

        player_ninja_collision_handler = self.space.add_collision_handler(
            NINJA_COLLISION_TYPE,
            PLAYER_COLLISION_TYPE
        )

        player_ninja_collision_handler.begin = handle_player_ninja_collision
