import sys
import random
import pygame as pg

WIDTH = 1297
HEIGHT = 744
vec = pg.math.Vector2

#完成版

class tyari():

    def __init__(self,num: int ,xy:tuple[int,int]):

        img0 = pg.transform.rotozoom(pg.image.load(f"ex05/figs/{num}.png"), 0, 2.0)
        img = pg.transform.flip(img0, True, False)  # デフォルトのこうかとん（右向き）
        self.imgs = {  # 0度から反時計回りに定義
            0: img,  # 右
            1: pg.transform.rotozoom(img, 45, 1.0),  # 右上
            -1: pg.transform.rotozoom(img, -45, 1.0),  # 右下
        }
        self.img = self.imgs[0]
        self.rct = self.img.get_rect()
        self.rct.center = xy
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)



    def change_img(self, num: int, screen: pg.Surface):

        self.img = pg.transform.rotozoom(pg.image.load(f"ex05/fig/{num}.png"), 0, 2.0)
        screen.blit(self.img, self.rct)
        

    def update(self, screen: pg.Surface):

        self.rct.move_ip(0,0)
        screen.blit(self.img, self.rct)
        self.acc = vec(0, 0.5)
        keys = pg.key.get_pressed()

    def jamp(self):
        print(0.8*HEIGHT)
        if self.rct.bottom == 591:
            self.rct.move_ip(0,-20)
            
        

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pg.Surface((w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
class Game:
    def __init__(self):
        # ゲームを初期化
        self.running = True
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.all_sprites = None
        self.platforms = None
        self.playing = False

        self.player = None
    def events(self):
        for event in pg.event.get():
            if event.type == pg.KEYUP:
                tyari.jamp()



def main():
    pg.display.set_caption("チャリ走DX")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("ex05/figs/bg.png")
    bg_img2 = pg.transform.flip(bg_img, True ,False)
    bird = tyari(0,(200,HEIGHT *0.73))
    tmr = 0
    x = tmr
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return
            if event.type == pg.KEYDOWN and event.key == pg.K_UP:
                bird.jamp()
        screen.blit(bg_img, [0-x, 0])
        screen.blit(bg_img2, [1297-x,0])
        screen.blit(bg_img, [2594-x, 0])
        bird.update(screen)
        pg.draw.rect(screen,(255,255,255),(0,HEIGHT*0.8,WIDTH,HEIGHT))
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