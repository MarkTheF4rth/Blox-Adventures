def level_one(emptyobj, images, a, b, c):
    print('creating level 1..')
    level = emptyobj()

    level.sequence = 1
    level.level = [[b(), a(), a(), a(), b()],
                    [b(), a(), a(), a(), c()],
                    [b(), a(), a(), a(), b()],
                    [b(), b(), b(), b(), b()]]

    level.images = images

    level.spawn = (1, 3)
    with open('Levels/level1.pkl', 'wb') as output:
            pickle.dump(level, output, pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    from common import StorageObj
    import pickle
    from game import Air_Block
    from game import Normal_Block
    from game import Win_Block

    images = {'block1':'Images/emptyblock.png',
              'block2':'Images/button_active.png',
              'block3':'Images/button_inactive.png'}

    block1 = lambda : Air_Block('block1')
    block2 = lambda : Normal_Block('block2')
    block3 = lambda : Win_Block('block3')

    level_one(StorageObj, images, block1, block2, block3)
