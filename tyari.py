import sys
import pygame as pg


class Coin:
    def __init__(self, bird: Tori):
        """
        コイン画像を生成する
        """
        self.imgs = list()
        self.imgs.append(pygame.image.load(f"ex05/coin01_gold01"))
        self.rct = self.img.get_rect()
        
    def update(self, screen: pg.Surface):
        """
        コインを速度に従って移動させる
        """
        self.rct.move_ip(self.vx, self.vy)
        screen.blit(self.img, self.rct)  

def main():
    pg.display.set_caption("チャリ走DX!!!!")
    screen = pg.display.set_mode((800, 600))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("ex05/figs/bg.png")
    bg_img2 = pg.transform.flip(bg_img, True ,False)
    tori = pg.image.load("ex01-20230926/fig/3.png")
    tori1 = pg.transform.flip(tori, True ,False)
    tori2 = pg.transform.rotozoom(tori1, 10,1.0)
    t_list = [tori1 , tori2]
    tmr = 0
    x = tmr
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return
        
        screen.blit(bg_img, [0-x, 0])
        screen.blit(bg_img2, [1297-x,0])
        screen.blit(bg_img, [2594-x, 0])
        screen.blit(t_list[(x//50) %2] , [300,200])
        pg.display.update()
        tmr += 1        
        clock.tick(1000)
        x += 1
        if x > 3200:
            x = 0
if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()