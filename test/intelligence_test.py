
import sys
sys.path.insert(0,'..')

import intelligence

def test_find_red_pixels():
    assert intelligence.find_red_pixels("data/test.png") == 25
    
def test_find_cyan_pixels():
    assert intelligence.find_cyan_pixels("data/test.png") == 6