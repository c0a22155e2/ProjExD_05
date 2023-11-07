import sys
import random
import pygame as pg

WIDTH = 1297
HEIGHT = 744

#完成版

def check_bound(obj: pg.Rect) -> tuple[bool, bool]:
    yoko, tate = True, True
    if obj.left < 0 or WIDTH < obj.right:  # 横方向のはみ出し判定
        yoko = False
    if obj.top < 0 or HEIGHT < obj.bottom:  # 縦方向のはみ出し判定
        tate = False
    return yoko, tate


class tyari(pg.sprite.Sprite):

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

    def change_img(self, num: int, screen: pg.Surface):

        self.img = pg.transform.rotozoom(pg.image.load(f"ex05/fig/{num}.png"), 0, 2.0)
        screen.blit(self.img, self.rct)
        

    def update(self, screen: pg.Surface):

        self.rct.move_ip(0,0)
        screen.blit(self.img, self.rct)
        

class Coin(pg.sprite.Sprite):
    def __init__(self):
        """
        コイン画像を生成する
        """
        super(Coin, self).__init__()
        #画像をリストに代入する
        self.imgs = list()
        for i in range(1,7):
            self.imgs.append(pg.transform.rotozoom(pg.image.load(f"ex05/coin01_gold01/{i}.png"),0,0.4))
        
        self.index = 0
        self.image = self.imgs[self.index]
        self.rect = self.image.get_rect()
        
    def update(self):
        if self.index >= len(self.imgs):
            self.index = 0
        
        self.image = self.imgs[self.index]
        self.index += 1

class Score:
    """
    コインとチャリンコが接したときにスコアを表示するクラス
    1コイン　= 1ポイント
    """
    def __init__(self):
        self.font = pg.font.Font(None, 50)
        self.color = (0, 0, 255)
        self.score = 0
        self.image = self.font.render(f"Score: {self.score}", 0, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = 100, HEIGHT-50
    
    def score_up(self, add):
        self.score += add
    
    def update(self, screen: pg.Surface):
        self.image = self.font.render(f"Score: {self.score}", 0, self.color)
        screen.blit(self.image, self.rect)
        

def main():
    pg.init()
    pg.display.set_caption("チャリ走DX")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("ex05/figs/bg.png")
    bg_img2 = pg.transform.flip(bg_img, True ,False)
    bird = tyari(0,(200,HEIGHT *0.73))
    tmr = 0
    x = tmr
    coin = Coin()
    coins = pg.sprite.Group()
    score = Score()
    tyaris = pg.sprite.Sprite()
    coin_group = pg.sprite.Group(coin)
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return
            
            for coin in pg.sprite.groupcollide(coins, tyaris, True, True).keys():
                score.score_up(1)
        
        screen.blit(bg_img, [0-x, 0])
        screen.blit(bg_img2, [1297-x,0])
        screen.blit(bg_img, [2594-x, 0])
        bird.update(screen)
        score.update(screen)
        pg.draw.rect(screen,(255,255,255),(0,HEIGHT*0.8,WIDTH,HEIGHT))
        if tmr % 3 == 1:
            coin_group.update()
        coin_group.draw(screen)
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