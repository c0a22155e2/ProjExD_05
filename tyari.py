import sys
import random
import pygame as pg
import time

WIDTH = 1297
HEIGHT = 744
F_RATE = 24


#完成版
def check_image(vel , flag):
    #第一引数 : チャリンコのy軸移動量
    #第二引数 : 反転しているかどうか
    num = 0

    for i in range(-30,31):
        if abs(vel - i) < 1:
            num = (vel) * -2
            break
    if flag:
        num *= -1
    return num


def check_bound(obj: pg.Rect) -> tuple[bool, bool]:
    yoko, tate = True, True
    if obj.left < 0 or WIDTH < obj.right:  # 横方向のはみ出し判定
        yoko = False
    if obj.top < 0 or HEIGHT < obj.bottom:  # 縦方向のはみ出し判定
        tate = False
    return yoko, tate


class TYARI(pg.sprite.Sprite):

    def __init__(self,num: int ,xy:tuple[int,int]):
        img0 = pg.transform.rotozoom(pg.image.load(f"ex05/figs/tyari/{num}.png"), 0, 0.5)
        img = pg.transform.flip(img0, True, False)  # デフォルトの自転車（右向き）
        
        self.nomal_img = img
        self.img = img
        self.rect = self.img.get_rect()
        self.rect.center = xy
        self.on_floor = True
        self.acc = 1
        self.vel= 0
        self.y = HEIGHT * 0.79

    def update(self, screen: pg.Surface,flag):
        self.img = pg.transform.flip(self.nomal_img ,flag, False) 
        self.img = pg.transform.rotozoom(self.img, check_image(self.vel,flag), 1.0)
        self.rect.move_ip(0,0)#自転車を描画
        screen.blit(self.img, self.rect)
        if self.on_floor:
            return
        self.vel += self.acc
        self.rect.y += self.vel
        if self.rect.y> HEIGHT * 0.79:
            self.rect.y= HEIGHT * 0.79
            self.vel = 0
            self.on_floor = True
        
    def jamp(self):#高さジャンプをするか決める
        
        if self.on_floor:
            self.on_floor=False
            self.vel = -30
                   
    def events(self):
        for event in pg.event.get():
            if event.type == pg.KEYUP:
                TYARI.jamp()



class FLOOR:
    
    def __init__(self,floor_type):
        floor_img = pg.transform.rotozoom(pg.image.load(f"ex05/figs/floor.png"), 0, 1.0)

        self.img = floor_img
        self.map = [1,1,1,1,1,1,1,1,1,1]
        self.coin = [random.randint(1,10) for i in range(200)]
        for i in range(200):
            self.map.append(random.randint(0, 4))
        self.rct = [self.img.get_rect() for i in range(len(self.map))]
            
    def update(self, screen: pg.Surface,x):
        for i in range(len(self.map)):
            self.rct[i].move_ip(0,0)#地面を描画
            if  0< i * 66 - x + 66 < WIDTH:
                if self.map[i] != 0:
                    screen.blit(self.img, (i * 66 - x, HEIGHT-66))
    
    def check_bound(self,num):
        if self.map[(200+num) // 66]== 0:
            return True
        else:
            return False
    
    def finish(self,x,flag):
        num = 0
        if flag:#反転しているとき
            if (x < -200) :
                return 1
        else:
            if (x//66 == len(self.map)-5):
                return 2


class Coin(pg.sprite.Sprite): 
    
    def __init__(self):
        super().__init__()
        """
        コイン画像を生成する
        """
        self.image = pg.transform.rotozoom(pg.image.load(f"ex05/coin01_gold01/1.png"),0,0.2)
        self.rect = self.image.get_rect()
        self.rect.center = 1297, random.randint(200,600)
        self.vy = -0.5
        self.vx = 10
        self.speed = 0.5
            
    def update(self,flag):
        if flag:
            self.rect.move_ip(self.speed*self.vx,-self.vy)
        else:
            self.rect.move_ip(-self.speed*self.vx,-self.vy)
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)

        
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
        self.rect.center = 100, HEIGHT-700
        
    def score_up(self, add):
        self.score += add
    
    def update(self, screen: pg.Surface):
        self.image = self.font.render(f"Score: {self.score}", 0, self.color)
        screen.blit(self.image, self.rect)
        

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
    score = Score()
    coin = Coin()
    coins= pg.sprite.Group()
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
          x -= 5
          if bg < -2*WIDTH:
              bg = 0
        if event.type == pg.KEYDOWN and event.key == pg.K_UP:
              bird.jamp()
        bird.update(screen,reverse)
        floor.update(screen,x)

        if floor.check_bound(x) and bird.on_floor:#ゲームオーバー時の終了画面
            for i in range(HEIGHT):#上から黒い幕が降ってくる
                pg.draw.rect(screen, (0,0,0), (0,0,WIDTH,i+1))
                pg.display.update()
                time.sleep(0.001)
            time.sleep(1)
            font = pg.font.Font(None,300)
            text = font.render("GameOver" , True , (128,128,128))
            screen.blit(text,[100,200])
            pg.display.update()
            time.sleep(2)
            font = pg.font.Font(None,100)
            text = font.render("SCORE : "+ str(score.score) , True , (128,128,128))
            screen.blit(text,[450,500])
            pg.display.update()
            time.sleep(5)
            pg.quit()


        if floor.finish(bg,reverse) == 2:#右端到達時の演出
            font = pg.font.Font(None,200)
            text = font.render("Mode : reverse!!", True , (128,128,128))
            for i in range(15):
                pg.draw.rect(screen, (0,0,0), (0,0,WIDTH,HEIGHT))
                screen.blit(text,[100,200])
                pg.display.update()
                time.sleep(0.1)
                pg.draw.rect(screen, (255,0,0), (0,0,WIDTH,HEIGHT))
                screen.blit(text,[100,200])
                pg.display.update()
                time.sleep(0.01)
            reverse = True

        elif floor.finish(bg,reverse) == 1:#反転後ゴール時の演出
            font = pg.font.Font(None,200)
            for i in range(HEIGHT):
                pg.draw.rect(screen, (171,201,217), (0,HEIGHT-i,WIDTH,HEIGHT))
                pg.display.update()
                time.sleep(0.001)
            for i in range(40):
                text = font.render("Congratulations!!" , True , ((i * 16) %255,(i *16) %255,(i *16) %255))
                screen.blit(text,[50,200])
                pg.display.update()
                time.sleep(0.1)
            text = font.render("Congratulations!!" , True , (128,128,128))
            screen.blit(text,[50,200])
            pg.display.update()
            time.sleep(2)
            font = pg.font.Font(None,100)
            text = font.render("SCORE : "+ str(score.score) , True , (128,128,128))
            screen.blit(text,[450,500])
            pg.display.update()
            time.sleep(5)
            pg.quit()
            reverse = False
        u = (10,11)
        o = 0
        o = random.randint(0,50)
        if o in u:
            coins.add(Coin())
        for coin in pg.sprite.spritecollide(bird, coins, True):
            score.score_up(1)
        coins.update(reverse)
        coins.draw(screen)
        score.update(screen)
        pg.display.update()
        tmr += 1
        clock.tick(1000)
        #for event in pg.event.get():
         # if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:#スペースで反転
          #    if reverse:
           #     reverse = False
            #  else:
             #   reverse = True
if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()