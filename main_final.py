if True: #podminka jen abych to mohl "sbalit"
    import pygame
    import os
    import pickle #knihovna pro ulozeni jedne promenne, respektive seznamu
    import random

if True:
    #pygame blbosti
    height = 500 #vyska okna
    width = 500 #sirka okna

    pygame.init()
    clock = pygame.time.Clock() #pygame zacne odpocitavat cas
    screen = pygame.display.set_mode((width, height)) #definice okna
    pygame.display.set_caption("Tomova quizohra") #nastavi jmeno okna

    #pressed = pygame.key.get_pressed() #je True pokud je klavesa zmacknuta
    focused = pygame.key.get_focused() #rekne, zda jde na obrazovce videt mys

    #text
    velikost1 = 25 #velikost prvniho fontu
    velikost2 = round(velikost1*0.8) #velikost druheho fontu, zakrouhlena a prevedena na int
    #print(velikost2)
    font1 = pygame.font.SysFont('Calibri', velikost1, True, False) #promenna "font": calibri, velikost pisma a n�co divn�ho
    font2 = pygame.font.SysFont('Calibri', velikost2, True, False) #mensi velikost
    odsazeni = 20

    #barvy
    WHITE = (225, 225, 225)
    BLACK = (0, 0, 0)


    #herni promenne

    #high score
    #high_score = 0
    #pickle.dump(high_score, open("high_score", "wb")) #ulozeni (pokud je potreba vynulovat)
    high_score = pickle.load(open("high_score", "rb")) #nacteni
    #print(high_score)

    first_loop = True #zatim nepouzito
    second_loop = False
    cas_kola = 60*1000 #později je v milisekundách, zde jsou to sekundy vynásobené 1000
    fps = 60
    #fps = 1
    pictures_nqab = 1 #no pictures - 1, pictures in question - 2, in answer - 3, in both - 4
    



def generate_board_mtt(otazka, odpovedi, cislo_otazky, cas, jmeno_slozky, obrazek_nqab):
    screen.fill((0, 0, 0))
    if obrazek_nqab == 1 or obrazek_nqab == 3:
        text = font1.render(otazka, False, WHITE)
        screen.blit(text, (odsazeni, odsazeni)) #tento radek by sel spojit s 
    elif obrazek_nqab == 2 or obrazek_nqab == 4:
        nazev = jmeno_slozky + "/" + otazka
        image = pygame.image.load(nazev)
        pic_height = image.get_height()
        if pic_height > 2*velikost1:
            pic_width = image.get_width()
            image = pygame.transform.scale(image, (int(pic_width*(2*velikost1/pic_height)), 2*velikost1))
        screen.blit(image, (odsazeni, odsazeni))#timto

    if obrazek_nqab == 1 or obrazek_nqab == 2:
        for i in range(len(odpovedi)):
            text = font2.render(odpovedi[i], False, WHITE) #odpovedi[i]
            screen.blit(text, (odsazeni, 3*velikost2*i+100))
    elif obrazek_nqab == 3 or obrazek_nqab == 4:
        for i in range(len(odpovedi)):
            nazev = jmeno_slozky + "/" + odpovedi[i]
            image = pygame.image.load(nazev)
            pic_height = image.get_height()
            if pic_height > 3*velikost2:
                pic_width = image.get_width()
                image = pygame.transform.scale(image, (int(pic_width*(3*velikost2/pic_height)), 3*velikost2))

            screen.blit(image, (odsazeni, 3*velikost2*i+100))

    text = font2.render(str(cislo_otazky), False, WHITE)
    screen.blit(text, (odsazeni, height-1.5*velikost2))

    minuty = cas // 60
    sekundy = cas % 60
    text = font2.render(str(minuty) + " : " + str(sekundy), False, WHITE)
    txt_width, txt_height = font2.size(str(minuty) + " : " + str(sekundy))
    screen.blit(text, (width-odsazeni-txt_width, height-1.5*velikost2))
    
    pygame.display.flip()



def generate_board_end(score, nhs):#nepouzita funkce
    screen.fill((0, 0, 0))
    sez_text = ["Konec hry", "Konecne skore: "+str(score)]
    if nhs:
        sez_text = ["Konec hry", "Nove nejvyssi skore", "Konecne skore: "+str(score)]
    for i in range(len(sez_text)):
        pass
        
        
    text = font1.render("Konec hry", False, WHITE)
    screen.blit(text, (odsazeni, odsazeni))
    text = font2.render("Konečné skore: "+str(score), False, WHITE)
    screen.blit(text, (odsazeni, odsazeni+velikost1*1.5))
    if nhs:
        text = font2.render("Konečné skore: "+str(score), False, WHITE)
        screen.blit(text, (odsazeni, odsazeni+velikost1*1.5))
    

    pygame.display.flip()

def generate_board_seznam(text, seznam):#funkce do okna vypise text, udela odstup a pote zacne vypisovat body ze seznamu, vzdy kazdy element seznamu na novy radek 
    screen.fill((0, 0, 0))#pole "vyplni" cernou
    text = font1.render(text, False, WHITE)
    screen.blit(text, (odsazeni, odsazeni))
    for i in range(len(seznam)):
        text = font2.render(seznam[i], False, WHITE) 
        screen.blit(text, (odsazeni, 1.5*velikost2*i+100))#rozestup mezi radky je půl velikosti fontu
    pygame.display.flip() #aktualizace pole

def display_text():#absolutne netusim proc jsem to psal
    screen.fill((0, 0, 0))
    pygame.display.flip()

def mouse_input():
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                return(pygame.mouse.get_pos())


def minuta_text_text(otazky, high_score, jmeno_slozky, picture_nqab):
    new_high_score = False
    cislo_otazky = 0
    break_loop = True
    pouzite_otazky = []
    nova_otazka = True
    start_time = pygame.time.get_ticks()
    now_time = pygame.time.get_ticks()

    while ((now_time - start_time) <= cas_kola) and break_loop:
        #vygenerovani otazky
        if nova_otazka:
            cislo_otazky += 1

            otazka = random.choice(list(otazky.keys()))
            while otazka in pouzite_otazky:
                otazka = random.choice(list(otazky.keys()))
            pouzite_otazky.append(otazka)
            if len(pouzite_otazky) >= len(list(otazky.keys())):
                pouzite_otazky = [] 

            #vygenerovani odpovedi
            odpovedi = []
            spravna_odpoved = otazky[otazka]
            odpovedi.append(spravna_odpoved)
            for i in range(3):
                odpoved = random.choice(list(otazky.values()))
                while odpoved in odpovedi:
                    odpoved = random.choice(list(otazky.values()))
                odpovedi.append(odpoved)
            random.shuffle(odpovedi)
            spravny_index = odpovedi.index(spravna_odpoved)
            nova_otazka = False
        
        souradnice = mouse_input()
        if souradnice == "quit":
            print("hej")
            break_loop = False
        elif souradnice:
            x, y = souradnice
            if (100+spravny_index*velikost2*3) < y < (100+(spravny_index+1)*velikost2*3):
                nova_otazka = True
            elif 100 < y < 100+4*velikost2*2:
                start_time -= 5*1000

        zbyvajici_cas = 60 - ((now_time-start_time)//1000)

        generate_board_mtt(otazka, odpovedi, cislo_otazky, zbyvajici_cas, jmeno_slozky, picture_nqab)
        now_time = pygame.time.get_ticks()
        clock.tick(fps)
    #konec loopu
    score = cislo_otazky-1
    if score > high_score:
        high_score = score
        pickle.dump(high_score, open("high_score", "wb"))
        new_high_score = True

    sez_text = ["Konecne skore: "+str(score)]
    if new_high_score:
        sez_text = ["Nove nejvyssi skore", "Konecne skore: "+str(score)]
    break_loop = True
    while break_loop:
        generate_board_seznam("Konec hry", sez_text)
        souradnice = mouse_input()
        if bool(souradnice) == True:
            break_loop = False
        clock.tick(fps)
        
def vyber_otazek(nazev_souboru):#jiz nepotrebna
    
    otazky = {}
    file = open(nazev_souboru, "r")
    sez_lines = file.readlines()
    for line in sez_lines:
        dic_key = line.split(":")[0]
        dic_value = line.split(":")[1]
        dic_value = dic_value.split("\n")[0]
        otazky[dic_key] = dic_value
    return(otazky)

def cyklus_vyber_otazek():
    list_files = []
    for x in os.listdir():
        if x.endswith(".txt"):
            jmeno = x.split(".txt")[0]
            list_files.append(jmeno)
    break_loop = True
    vyber = False
    while break_loop:
        generate_board_seznam("Vyberte sadu otazek", list_files)
        souradnice = mouse_input()
        if bool(souradnice) == True:
           
            x, y = souradnice
            
            for i in range(len(list_files)):
                if (100+i*1.5*velikost2) < y < (100+(i+1)*1.5*velikost2):
                    vyber = list_files[i]
                    break_loop = False
                    return(vyber)
        clock.tick(fps)

def create_otazky(nazev):
    otazky = {}
    file_name = nazev + ".txt"
    file = open(file_name, "r")
    sez_lines = file.readlines()
    for line in sez_lines:
        dic_key = line.split(":")[0]
        dic_value = line.split(":")[1]
        dic_value = dic_value.split("\n")[0]
        otazky[dic_key] = dic_value
    file.close()
    return(otazky)

def urci_typ(vychozi_stav, otazky):
    if vychozi_stav == 1 or vychozi_stav == 4:
        return(vychozi_stav, otazky)

    else:
        sez = ["Pictures in questions", "Pictures in answers"]
        break_loop = True
        while break_loop:
            generate_board_seznam("Choose type of game", sez)
            souradnice = mouse_input()
            if bool(souradnice) == True:
                break_loop = False
                x, y = souradnice
                for i in range(len(sez)):
                    if (100+i*1.5*velikost2) < y < (100+(i+1)*1.5*velikost2):
                        vyber = i+2
                        if (vyber == 2 and vychozi_stav == 3) or (vychozi_stav == 3 and vyber == 2):
                            otazky = otoc_dic(otazky)
                        return(vyber, otazky)
def otoc_dic(otazky_2):
    otazky = {}
    for i in list(otazky_2.keys()):
        otazky[otazky_2[i]] = i
    return(otazky)

def urci_vychozi(otazky, nazev_slozky):
    if nazev_slozky not in os.listdir():
        return(1)
    elif nazev_slozky in os.listdir():
        q = list(otazky.keys())[0]
        a = list(otazky.values())[0]
        if "." in q and "." in a:
            return(4)
        elif "." in q:
            return(2)
        elif "." in a:
            return(3)
    else:
        print("chyba ve funkci urci_vychozi")
            
def create_dic(nazev_slozky):
    dic = {}
    dir_list = os.listdir(nazev_slozky+"/")
    for pic in dir_list:
        dic[pic.split(".png")] = pic

def create_txt(nazev_slozky):
    sez = []
    dir_list = os.listdir(nazev_slozky+"/")
    for pic in dir_list:
        dic_key = pic.split(".png")[0]
        if "_" in dic_key:
            dic_key = dic_key.replace("_", " ")
        to_append = dic_key + ":" + pic + "\n"
        sez.append(to_append)
    file = open(nazev_slozky + ".txt", "w")
    file.writelines(sez)
#-------------------------------------------------------------------------------------------------------------------------------

#create_txt("shapes")

jmeno = cyklus_vyber_otazek()
otazky = create_otazky(jmeno)
vychozi_stav = urci_vychozi(otazky, jmeno)
pictures_nqab, otazky = urci_typ(vychozi_stav, otazky)
minuta_text_text(otazky, high_score, jmeno, pictures_nqab)


pygame.quit()
print("konec celeho programu")

