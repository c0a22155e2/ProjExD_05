import sys
import random
import pygame as pg

WIDTH = 1297
HEIGHT = 744
vec = pg.math.Vector2
is_jumping = False
character_speed = 5
jump_height = 591
jump_count = 0
character_y=0.73 *HEIGHT

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
        self.on_floor = True
        self.acc = 1
        self.vel= -10
        self.y = 400
        
        



    def change_img(self, num: int, screen: pg.Surface):

        self.img = pg.transform.rotozoom(pg.image.load(f"ex05/fig/{num}.png"), 0, 2.0)
        screen.blit(self.img, self.rct)
        

    def update(self, screen: pg.Surface):

        self.rct.move_ip(0,0)
        screen.blit(self.img, self.rct)
        if self.on_floor:
            return
        self.vel += self.acc
        self.rct.y += self.vel
        if self.rct.y> 400:
            self.rct.y= 400
            self.vel = 0
            self.on_floor = True
        

    def jamp(self):#高さジャンプをするか決める
        
        if self.on_floor:
            self.on_floor=False
            time = 0
            self.vel = -30
    
        
            
            

    
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
    bird = tyari(0,(200,400))
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