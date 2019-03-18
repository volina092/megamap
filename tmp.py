import pygame


pygame.init()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4: #скроллим вверх
                #smth
                pass
            if event.button == 5: #скроллим вниз
                #smth
                pass
            
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_LEFT]:
                #smth
                pass       
            if keystate[pygame.K_RIGHT]:
                #smth
                pass
            if keystate[pygame.K_UP]:
                #smth
                pass
            if keystate[pygame.K_DOWN]:
                #smth
                pass