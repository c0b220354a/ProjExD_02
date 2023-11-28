import sys
import random
import pygame as pg

WIDTH, HEIGHT = 1600, 900

delta={
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,+5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(+5,0), 
}  #練習3:キーリストを作成

def check_bound(rct: pg.Rect) -> tuple[bool,bool]:
    """
    オブジェクトが画面内or画面外を判定し、真理値タプルを返す関数
    引数 rct:工科トンor爆弾surfaceのRect
    戻り値:横方向、縦方向はみ出し判定結果(画面内:True/画面外:False)
    """
    yoko,tate = True,True
    if rct.left<0 or WIDTH < rct.right:
        yoko = False
    if rct.top<0 or HEIGHT < rct.bottom:
        tate = False
    return (yoko,tate)


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_img2=pg.image.load("ex02/fig/8.png")  #泣いているこうかとん
    kk_img2 = pg.transform.rotozoom(kk_img2, 0, 2.0)
    kk_img_f=pg.transform.flip(kk_img,True,False)
    kk_imgs = {(+5,0):kk_img_f,  # 右方向のこうかとん
               (+5,-5):pg.transform.rotozoom(kk_img_f,45,1.0),  #右上方向のこうかとん
               (0,-5):pg.transform.rotozoom(kk_img_f,90,1.0),  #上方向のこうかとん
               (+5,+5):pg.transform.rotozoom(kk_img_f,-45,1.0),  #右下方向のこうかとん
               (0,+5):pg.transform.rotozoom(kk_img_f,-90,1.0),  #下方向のこうかとん
               (-5,+5):pg.transform.rotozoom(kk_img,45,1.0),  #左下方向のこうかとん
               (-5,0):kk_img,  # 左方向のこうかとん
               (-5,-5):pg.transform.rotozoom(kk_img,-45,1.0),  #左上方向のこうかとん
               }
    kk_img=kk_imgs[+5,0]
    bb_imags=[]
    bb_img = pg.Surface((20,20))  # 練習1:透明なSurfaceを作る
    bb_img.set_colorkey((0,0,0))
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)  #練習1:透明なSurfaceの中に赤い円を作る
    bb_imags.append(bb_img)
    bb_rct = bb_img.get_rect()  # 練習1: 爆弾surfaceを抽出
    kk_rct = kk_img.get_rect()  # 練習3: 工科とんを抽出
    kk_rct.center= 900,400
    bb_rct.centerx = random.randint(0,WIDTH)
    bb_rct.centery = random.randint(0,HEIGHT)
    accs = [a for a in range(1,11)]  # 加速度のリストを作る
    vx,vy = +5,-5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return

        if kk_rct.colliderect(bb_rct):
            screen.blit(kk_img2,kk_rct)
            pg.display.update()
            print("Game Over")
            return
        
        key_lst=pg.key.get_pressed()
        sum_mv=[0,0]

        for k,tpl in delta.items():
            if key_lst[k]:  #練習3　キーが押されたら
                sum_mv[0]+=tpl[0]
                sum_mv[1]+=tpl[1]

        kk_0 = 0  #こうかとんの画像の切り替えに必要
        kk_1 = 0  #こうかとんの画像の切り替えに必要

        for k, mv in delta.items(): 
            if key_lst[k]:  # キーが押されたら
                kk_0 = kk_0 + mv[0]  # kk_0に左右のキーの数値を格納 
                kk_1 = kk_1 + mv[1]  # kk_1に上下のキーの数値を格納
        
        if kk_0 != 0 or kk_1 != 0:  # 飛ぶ方向に従ってこうかとん画像を切り替える
            kk_img = kk_imgs[kk_0, kk_1]  # kk_imgに切り替える画像を代入

        screen.blit(kk_img, kk_rct)
        screen.blit(bg_img, [0, 0])
        kk_rct.move_ip(sum_mv[0],sum_mv[1])

        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])

        avx,avy=vx*accs[min(tmr//500,9)],vy*accs[min(tmr//500,9)]  #tmrの値に応じてスピードを決める
        screen.blit(kk_img,kk_rct)  #練習3: 工科トンの移動
        bb_rct.move_ip(avx,avy)  #練習2 爆弾を移動させる
        yoko,tate = check_bound(bb_rct)
        if not yoko:  # 横方向にはみ出たら
            vx *= -1

        if not tate:
            vy *= -1

        bb_rct.move_ip(vx,vy)
        screen.blit(bb_img,bb_rct)
        pg.display.update()
        tmr += 100  #爆弾を早くするために100にする
        clock.tick(10)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()