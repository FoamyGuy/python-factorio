from factorio import blueprints as factblue
from factblue.blueprints import EncodedBlob
import json
import copy
import sys

try:
    from Tkinter import Tk
    tk_available = True
except ImportError:
    tk_available = False
    pass
 
verbose_mode = False
if "-v" in sys.argv or "--verbose" in sys.argv:
    verbose_mode = True

if "-h" in sys.argv or "--help" in sys.argv:
    print("""factorio-text-generator
-------------------------
Input text to the tool and it will generate a blueprint
string that contains your text written with concrete
letters.

Example simple usage:
    python factorio-text-generator.py "hello world"

Options:
---------
-h   Show help
-v   Verbose output
-c   Copy blueprint to clipboard (requires Tkinter)""")
    quit()
    
    
alphabet_sprites = EncodedBlob.from_exchange_string(str("0eNqd29Fu2zAMBdB/0XMGmLJkKfmVoQ9dZwwG0rRosmFFkH9fuzbAHrbBp0/FOtpwySuK95I8py/77/Pj03I4pd05LXcPh2PafT6n4/LtcLt//d3p+XFOu7Sc5vu0SYfb+9d/vdjdPc2nOV02aTl8nX+mXVxuNum07Oe3Fzw+HJfT8nB4fcXL/37KwyY9v/yM4fK3t/z7gS3ad7RvaF/RvqD9iPYZ7cPs8fX49egcjNVaKMT23TWBD2zRfjR7/Jxq5vjxqw9udPVmR2929GY3b3bz5vvbV7++qXsauqehe5q5p5l7moGtIdgmvFauD2zRvqN9Q/uK9gXtR7TPGgCzx9fj16NzMFaroVD0pBcFc0EwFwRzQTAXBHNB8BRLVcWwVgxrxbBWLG8Wg2b5CDQRN+txOSryRwTyiMAcEZgjAnM0YI6GtBFLjKzuz+j+jO7P6P6Ml1zGSy7jJZcRDtngkA0O2Q5vxsMbip5A9ASiJxA9gdEKi1ZYtAIPrwolgcJHoJARKByECQdh1D6Q2g92VgY7K0p1O8YWmXE3JHQ7h91w0y3HdkJNpzPYqVLrBEik/8r+m8WoWYyaHW1TCkwoaHSuUSaY0OtI4pHDI2WeyOtGmCeK0UTJtKLTqzm9mtOrlZTVKspqya5SSCulr0oHqdpBUkkDBQTUD4zfG703um5svdidoXQua6sNO23YaMM+G7bZsMuGTTbssWGLjbJAtn6cteOsG0dHI1t9r+QTuSQKBcYMjRhKnh7MLdbbtk619Z0H8SD1kInZGa8bKD8jZA2xpn2Y8kHoJnCH5BM6CHi32dVmNxslZMqZlDKxJMMek3WYrL9kxaHVhoVyWqFroVAGtB4XlbRUoxYHlYFkLQKRF1ZCoJHISrEh1lYlX1YJZJVAVrklK8URRRUbvDAFxhQVElRITyE5hYYPSHqZKI4oSdo4kumXpkeSHNkkjiRdNokjjUM1iiM2I0z97xQZmrgjdZ7E+S6VpQn5gYxM23ph48/YBAwjiNgyDCOUYZPPYQQU25dBhFV75dgqx863NbJ1SgSHRHCGA0c4bMIiiKrZOEaQdhbEA3WOCseocCrKhpx0+hFnB8MIXhjDC6N4OMdoY4w64owTzjjgjPPKOK6M08o4rIyzyjF9IEz2KfZ3rnUiFvRhNfrV3L5mLV6wiMXdkbCiFzdNbHNEt45w6ehq3sw8k/laPdOqU1zNw808XMzDvTxcy8OtvEzVqa3w2Qbf/xb4bjZv66K7P7ZLN+nH/HT8/fxUSp62Y8ktXy6/AKnaeWM="))

alphabet_obj = json.loads(alphabet_sprites.to_json_string())

if verbose_mode:
    #print (json.dumps(alphabet_obj, indent=4, sort_keys=True))
    print("num of tiles in spritesheet blueprint:")
    print(len(alphabet_obj['blueprint']['tiles']))

sprite_size = 5

x_coords = []
y_coords = []

for tile in alphabet_obj['blueprint']['tiles']:
    x_coords.append(tile['position']['x'])
    y_coords.append(tile['position']['y'])

    
max_x = max(x_coords)
min_x = min(x_coords)
max_y = max(y_coords)
min_y = min(y_coords)

if verbose_mode:
    total_rect_size = (max(x_coords) * 2 + 1, max(y_coords) * 2 + 1)
    print("total rect size of spritesheet:")
    print(total_rect_size)

def shift_tiles(tiles, x=0, y=0):
    for tile in tiles:
        tile['position']['x'] = tile['position']['x'] + x
        tile['position']['y'] = tile['position']['y'] + y
    return tiles

def to_clipboard(txt):
    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(txt)
    r.update() # now it stays on the clipboard after the window is closed
    r.destroy()
    


def get_sprite_tiles(x, y):
    top_left_of_sheet = (min_x , max_y)
    bottom_right_of_sheet = (max_x, min_y)
    #print("top left of sheet: %s" % (top_left_of_sheet,))
    #print("bottom right of sheet: %s" % (bottom_right_of_sheet,))
    
    x_edge_of_sprite = top_left_of_sheet[0] + (x-1) * 6
    y_edge_of_sprite = top_left_of_sheet[1] - (y-1) * 6
    top_left_of_sprite = (x_edge_of_sprite , y_edge_of_sprite)
    bottom_right_of_sprite = (
        top_left_of_sprite[0]+ (sprite_size-1), 
        top_left_of_sprite[1]- (sprite_size-1)
    )
    
    if verbose_mode:
        print("top left of sprite:")
        print(top_left_of_sprite)
        print("bottom right of sprite:")
        print(bottom_right_of_sprite)
        print("")
    
    sprite_tiles = []
    
    for tile in alphabet_obj['blueprint']['tiles']:
        if verbose_mode:
            print("(%s, %s)" % (tile['position']['x'], tile['position']['y']))
        if tile['position']['x'] <= bottom_right_of_sprite[0]:
            if tile['position']['x'] >= top_left_of_sprite[0]:
                if tile['position']['y'] <= top_left_of_sprite[1]:
                    if tile['position']['y'] >= bottom_right_of_sprite[1]:
                        new_tile = copy.deepcopy(tile)
                        new_tile['position']['x'] = new_tile['position']['x'] - (top_left_of_sprite[0]+2)
                        new_tile['position']['y'] = new_tile['position']['y'] - (bottom_right_of_sprite[1]+2)
                        if verbose_mode:
                            print("new tile:")
                            print(new_tile)
                        sprite_tiles.append(new_tile)
    
    
    return(sprite_tiles)

# Build the alpha bet dict like {'a': (1,4)...}
alphabet_dict = {}
x = 1
y = 4
from string import ascii_lowercase
for c in ascii_lowercase:
    alphabet_dict [c] = (x,y)
    
    if x < 7:
        x += 1
    elif x == 7:
        x = 1
        y-= 1

if verbose_mode:        
    print ("alphabet dict")
    print (alphabet_dict)

def make_string_blueprint_tiles(txt):
    string_tiles = []
    blueprint_x_size = len(txt)*6 - 1
    if verbose_mode:
        print("blueprint x size:")
        print(blueprint_x_size)
    for i, letter in enumerate(txt):
        if letter in alphabet_dict.keys():
            shift = -(blueprint_x_size/2) + 6*i
            shifted_tiles = shift_tiles(get_sprite_tiles(alphabet_dict[letter][0], alphabet_dict[letter][1]), x=shift)
            string_tiles.extend(shifted_tiles)
    return string_tiles


string_tiles = make_string_blueprint_tiles(sys.argv[-1])

if verbose_mode:
    print("string tiles:")
    print(string_tiles)

    
sprite_obj = copy.deepcopy(alphabet_obj)
sprite_obj['blueprint']['tiles'] = string_tiles

sprite_blb = EncodedBlob.from_json_string(json.dumps(sprite_obj))

print(sprite_blb.to_exchange_string())

if "-c" in sys.argv or "--copy" in sys.argv:
    if tk_available:
        to_clipboard(sprite_blb.to_exchange_string())
    else:
        print ("copy to clipboard requires Tkinter")
