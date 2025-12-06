# Adapted from https://github.com/nicespoon/retro-adsb-radar
# Modified for ESP32 MicroPython from RPi Python

from cydr import CYD
import utime
import random

from ui_components_map import RadarScope, DataTable, SampleAircraft, _cfg, BRIGHT_GREEN, BLACK

cyd = CYD(display_width=320, display_height=240, rotation=90)
fb = cyd.display
fb.clear(BLACK)

# sample aircraft dataset
def rand_pos():
    return random.uniform(-0.5, 0.5)

ac1 = SampleAircraft(callsign="ALFA01", lat=rand_pos(), lon=rand_pos(), track=45, speed=250, altitude=12000, distance=5.0, is_military=False)
ac2 = SampleAircraft(callsign="BRAVO2", lat=rand_pos(), lon=rand_pos(), track=270, speed=120, altitude=8000, distance=8.2, is_military=True)
ac3 = SampleAircraft(callsign="CHAR3", lat=rand_pos(), lon=rand_pos(), track=180, speed=350, altitude=30000, distance=12.5, is_military=False)

radar = RadarScope(fb, center_x=120, center_y=80, radius=70, font=None)
table = DataTable(fb, x=4, y=170, width=312, height=66, font=None)

def fetch_your_data():
    return [ac1, ac2, ac3]

# single update
def single_update():
    aircraft_list = fetch_your_data()
    fb.clear(BLACK)
    now = utime.ticks_ms()
    radar.draw(aircraft_list)
    table.draw(aircraft_list, status="OK", last_update_ticks_ms=now)
    return now

# In a loop you would refresh periodically:
def main_loop():
    while True:
        now = single_update()
        utime.sleep_ms(10000)

# The module calls the CYD display API directly (no runtime guessing). It expects fb to be cyd.display,
# which provides methods such as: draw_lines, draw_line, draw_pixel, fill_circle, fill_rectangle,
# draw_rectangle, draw_text (with font), and draw_text8x8.

single_update

