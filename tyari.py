import sys
import random
import pygame as pg

WIDTH = 1297
HEIGHT = 744


class tyari():

    def __init__(self,num: int ,xy:tuple[int,int]):
        img0 = pg.transform.rotozoom(pg.image.load(f"ex05/figs/{num}.png"), 0, 1.0)
        img = pg.transform.flip(img0, True, False)  # デフォルトの自転車（右向き）
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
        self.rct.move_ip(0,0)#自転車を描画
        screen.blit(self.img, self.rct)
        

def main():
    pg.display.set_caption("チャリ走DX")
    screen = pg.display.set_mode((WIDTH, HEIGHT))#スクリーンを描画
    clock  = pg.time.Clock()
    bg_img = pg.image.load("ex05/figs/bg.png")
    bg_img2 = pg.transform.flip(bg_img, True ,False)
    bird = tyari(1,(200,HEIGHT *0.68))#自転車を描画
    reverse = False#反転
    tmr = 0
    x = tmr
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return
        if not reverse:#通常状態
          screen.blit(bg_img, [-2594-x, 0])
          screen.blit(bg_img2, [-1297-x, 0])
          screen.blit(bg_img, [0-x, 0])
          screen.blit(bg_img2, [1297-x,0])
          screen.blit(bg_img, [2594-x, 0])
          x += 5
          if x > 2594:
              x = 0
        else:#反転状態
          screen.blit(bg_img, [2594-x, 0])
          screen.blit(bg_img2, [1297-x, 0])
          screen.blit(bg_img, [0-x, 0])
          screen.blit(bg_img2, [-1297-x,0])
          screen.blit(bg_img, [-2594-x, 0])
          x -= 5
          if x < -2594:
              x = 0
        bird.update(screen)
        pg.draw.rect(screen,(255,255,255),(0,HEIGHT*0.8,WIDTH,HEIGHT))#じめんを描画
        pg.display.update()
        tmr += 5        
        clock.tick(1000)
        for event in pg.event.get():
          if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:#スペースで反転
              if reverse:
                reverse = False
              else:
                 reverse = True
          
if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()