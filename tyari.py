import sys
import random
import pygame as pg

WIDTH = 1297
HEIGHT = 744

#完成版

class TYARI:

    def __init__(self,num: int ,xy:tuple[int,int]):
        img = pg.transform.rotozoom(pg.image.load(f"ex05/figs/tyari/{num}.png"), 0, 0.5)
        img = pg.transform.flip(img, True, False)  # デフォルトの自転車（右向き）
        self.imgs = {  # 0度から反時計回りに定義
            0: img,  # 右
            1: pg.transform.flip(img, True, False),
            2: pg.transform.rotozoom(img, 45, 1.0),  # 右上
            3: pg.transform.rotozoom(img, -45, 1.0),  # 右下

        }
        self.img = self.imgs[0]
        self.rct = self.img.get_rect()
        self.rct.center = xy

    def change_img(self, num: int, screen: pg.Surface):
        self.img = self.imgs[num]
        screen.blit(self.img, self.rct)

    def update(self, screen: pg.Surface):
        self.rct.move_ip(0,0)#自転車を描画
        screen.blit(self.img, self.rct)


class FLOOR:
    
    def __init__(self,floor_type):
        floor_img = pg.transform.rotozoom(pg.image.load(f"ex05/figs/floor.png"), 0, 1.0)

        self.img = floor_img
        self.map = [random.randint(0, 4) for i in range(200)]
        self.rct = [self.img.get_rect() for i in range(len(self.map))]
            
    def update(self, screen: pg.Surface,x):

        for i in range(len(self.map)):
            self.rct[i].move_ip(0,0)#地面を描画
            if  0< i * 66 - x + 66 < WIDTH:
                if self.map[i] != 0:
                    screen.blit(self.img, (i * 66 - x, HEIGHT-66))
    
    def check_bound(self,num):
        if self.map[(200+num) // 66]== 0:
            return 1
        else:
            return 0

    

def main():
    pg.display.set_caption("チャリ走DX")
    screen = pg.display.set_mode((WIDTH, HEIGHT))#スクリーンを描画
    clock  = pg.time.Clock()
    bg_img1 = pg.image.load("ex05/figs/bg.png")
    bg_img2 = pg.transform.flip(bg_img1, True ,False)
    bg_imgs = [bg_img1,bg_img2]
    bird = TYARI(1,(200,HEIGHT*0.85))#自転車を描画
    floor = FLOOR(1)
    reverse = False#反転
    tmr = 0
    bg = tmr
    x = tmr
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return
        for i in range(-2,3):
            screen.blit(bg_imgs[i%2] , [-bg-i*WIDTH, 0])#背景を5枚描画

        if not reverse:#通常状態
          bg += 5
          x += 5
          if bg > WIDTH * 2:
              bg = 0
        else:#反転状態
          bg -= 5
          bird.rct.move_ip(0,-2)
          x -= 5
          if bg < -2*WIDTH:
              bg = 0
        bird.update(screen)
        floor.update(screen,x)
        font = pg.font.Font(None,55)
        text = font.render(str(floor.check_bound(x)) , True , (255,255,255))
        screen.blit(text,[100,100])
        pg.display.update()
        tmr += 1     
        clock.tick(1000)
        for event in pg.event.get():
          if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:#スペースで反転
              if reverse:
                reverse = False
                bird.change_img(0,screen)
              else:
                 reverse = True
                 bird.change_img(1,screen)
          
if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()