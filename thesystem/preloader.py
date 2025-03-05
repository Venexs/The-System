import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.abspath(os.path.join(current_dir, '../../'))

sys.path.insert(0, project_root)

import thesystem.system

top_images = [f"thesystem/top_bar/dailyquest.py{str(i).zfill(4)}.png" for i in range(2, 501, 2)]
bottom_images = [f"thesystem/bottom_bar/{str(i).zfill(4)}.png" for i in range(2, 501, 2)]

default_top_preloaded_images = thesystem.system.preload_images(top_images, (695, 39))
default_bottom_preloaded_images = thesystem.system.preload_images(bottom_images, (702, 36))

message_top_preloaded_images = thesystem.system.preload_images(top_images, (715, 41))
message_bottom_preloaded_images = thesystem.system.preload_images(bottom_images, (715, 41))

high_long_top_preloaded_images = thesystem.system.preload_images(top_images, (488, 38))
high_long_bottom_preloaded_images = thesystem.system.preload_images(bottom_images, (488, 33))

demon_castle_top_preloaded_images = thesystem.system.preload_images(top_images, (1229, 47))
demon_castle_bottom_preloaded_images = thesystem.system.preload_images(bottom_images, (1229, 47))






