



# The testing scenarios recommended by Eliseo

def experiment1(screensize, outside): # Different sizes | Different locations
    area_loc1 = [55 + screensize[0]/4., 55 + screensize[1]/3.]
    area_loc2 = [screensize[0]/2., screensize[1]/2.]


    if outside:
        scale1 = [130,130]
        scale2 = [160,160]
    else:
        scale1 = [110,110]
        scale2 = [140,140]

    bigB1 = False
    bigB2 = True

    return area_loc1, scale1, bigB1, area_loc2, scale2, bigB2


def experiment2(screensize, outside): # Same size | Big | Different locations
    area_loc1 = [55 + screensize[0]/4., 55 + screensize[1]/3.]
    area_loc2 = [screensize[0]/2., screensize[1]/2.]

    if outside:
        scale1 = [180,180]
        scale2 = [180,180]
    else:
        scale1 = [110,110]
        scale2 = [110,110]

    bigB1 = True
    bigB2 = True

    return area_loc1, scale1, bigB1, area_loc2, scale2, bigB2

def experiment3(screensize, outside): # Different sizes |  Symmetric locations
    area_loc1 = [screensize[0]/2. - screensize[0]/4., screensize[1]/2.]
    area_loc2 = [screensize[0]/4. + screensize[0]/2., screensize[1]/2.]

    if outside:
        scale1 = [140,140]
        scale2 = [180,180]
    else:
        scale1 = [110,110]
        scale2 = [130,130]

    bigB1 = False
    bigB2 = True

    return area_loc1, scale1, bigB1, area_loc2, scale2, bigB2


def experiment4(screensize, outside): # Equal size |  Symmetric locations
    area_loc1 = [screensize[0]/2. - screensize[0]/4.4, screensize[1]/2.]
    area_loc2 = [screensize[0]/4.4 + screensize[0]/2., screensize[1]/2.]

    if outside:
        scale1 = [110,110]
        scale2 = [150,150]
    else:
        scale1 = [90,90]
        scale2 = [110,110]

    bigB1 = True
    bigB2 = True

    return area_loc1, scale1, bigB1, area_loc2, scale2, bigB2