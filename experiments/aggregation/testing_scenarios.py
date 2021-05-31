"""
The testing scenarios recommended by Eliseo.
It describe environments with two aggregation sites.
The agents start in random positions of the bounded environment (circular shape).
"""
def round_v(pos):
    return [int(round(pos[0])), int(round(pos[1]))]

def experiment0(screensize, outside): # Different sizes | Different locations
    area_loc1 = round_v([screensize[0]/2., screensize[1]/2.])


    if outside:
        scale1 = round_v([screensize[0]*.14, screensize[1]*.14])
    else:
        scale1 = round_v([screensize[0]*.11, screensize[1]*.11])

    bigB1 = False

    return area_loc1, scale1, bigB1


def experiment1(screensize, outside): # Different sizes | Different locations
    area_loc1 = round_v([screensize[0]*.05 + screensize[0]/3.5, screensize[1]*.05 + screensize[1]/3.])
    area_loc2 = round_v([screensize[0]/2., screensize[1]/2.])


    if outside:
        scale1 = round_v([screensize[0]*.14, screensize[1]*.14])
        scale2 = round_v([screensize[0]*.18, screensize[1]*.18])
    else:
        scale1 = round_v([screensize[0]*.11, screensize[1]*.11])
        scale2 = round_v([screensize[0]*.14,screensize[1]*.14])

    bigB1 = False
    bigB2 = True

    return area_loc1, scale1, bigB1, area_loc2, scale2, bigB2


def experiment2(screensize, outside): # Same size | Big | Different locations
    area_loc1 = round_v([screensize[0]*.05 + screensize[0]/3.3, screensize[1]*.05 + screensize[1]/3.])
    area_loc2 = round_v([screensize[0]/2., screensize[1]/2.])

    if outside:
        scale1 = round_v([screensize[0]*.18, screensize[1]*.18])
        scale2 = round_v([screensize[1]*.18, screensize[1]*.18])
    else:
        scale1 = round_v([screensize[0]*.14, screensize[1]*.14])
        scale2 = round_v([screensize[0]*.14, screensize[1]*.14])

    bigB1 = True
    bigB2 = True

    return area_loc1, scale1, bigB1, area_loc2, scale2, bigB2

def experiment3(screensize, outside): # Different sizes |  Symmetric locations
    area_loc1 = round_v([screensize[0]/2. - screensize[0]/4.5, screensize[1]/2.])
    area_loc2 = round_v([screensize[0]/4.5 + screensize[0]/2., screensize[1]/2.])

    if outside:
        scale1 = round_v([screensize[0]*.14, screensize[1]*.14])
        scale2 = round_v([screensize[0]*.18, screensize[1]*.18])
    else:
        scale1 = round_v([screensize[0]*.11,screensize[1]*.11])
        scale2 = round_v([screensize[0]*.14,screensize[1]*.14])

    bigB1 = False
    bigB2 = True

    return area_loc1, scale1, bigB1, area_loc2, scale2, bigB2


def experiment4(screensize, outside): # Equal size |  Symmetric locations
    area_loc1 = round_v([screensize[0]/2. - screensize[0]/4.4, screensize[1]/2.])
    area_loc2 = round_v([screensize[0]/4.4 + screensize[0]/2., screensize[1]/2.])

    if outside:
        scale1 = round_v([screensize[0]*.18, screensize[1]*.18])
        scale2 = round_v([screensize[0]*.18,screensize[1]*.18])
    else:
        scale1 = round_v([screensize[0]*.11, screensize[1]*.11])
        scale2 = round_v([screensize[0]*.11, screensize[1]*.11])

    bigB1 = False
    bigB2 = False

    return area_loc1, scale1, bigB1, area_loc2, scale2, bigB2