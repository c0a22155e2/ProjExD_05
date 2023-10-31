import sys
import pygame as pg

class tyari():

    def __init__(self,num: int ,xy:tuple[int,int]):

        img0 = pg.transform.rotozoom(pg.image.load(f"ex03/fig/{num}.png"), 0, 2.0)
        img = pg.transform.flip(img0, True, False)  # デフォルトのこうかとん（右向き）
        self.imgs = {  # 0度から反時計回りに定義
            0: img,  # 右
            1: pg.transform.rotozoom(img, 45, 1.0),  # 右上
            -1: pg.transform.rotozoom(img, -45, 1.0),  # 右下
        }
        self.img = self.imgs[0]
        self.rct = self.img.get_rect()
        self.rct.center = xy


    def change_img(self, num: int, screen: pg.Surface):

        self.img = pg.transform.rotozoom(pg.image.load(f"ex05/fig/{num}.png"), 0, 2.0)
        screen.blit(self.img, self.rct)
        

    def update(self, screen: pg.Surface):

        self.rct.move_ip(0,0)
        screen.blit(self.img, self.rct)


def main():
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((800, 600))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("ex05/figs/bg.png")
    bg_img2 = pg.transform.flip(bg_img, True ,False)
    bird = tyari(0,(400,300))
    tmr = 0
    x = tmr
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return
        
        screen.blit(bg_img, [0-x, 0])
        screen.blit(bg_img2, [1297-x,0])
        screen.blit(bg_img, [2594-x, 0])
        pg.display.update()
        bird.update(screen)
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