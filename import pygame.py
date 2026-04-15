import pygame 
import random 
import math 

pygame.init()

ANCHO =  700
ALTO = 500


ventana = pygame.display.set_mode((ANCHO,ALTO))
pygame.display.set_caption("Black jack") 

reloj = pygame.time.Clock()

verde = (34,120,60)
blanco = (255,255,255)
negro = (0,0,0)
rojo = (180,30,30)
amarillo = (220,180,50)
gris = (150,150,150)
verdebtn = (30,140,80)

fuente_normal = pygame.font.SysFont("Arial", 20 )
fuente_grande = pygame.font.SysFont("Arial", 30, bold = True  )

diler = []
jugador = []
sistema = []

victorias = 0
derrotas = 0 
empates = 0

estado = "inicio"

mensaje = ""
color_mensaje = blanco 
tiempo_sistema = 0 

agresividad = 0
umbral = 17 

def fondo(superficie,x,y,angulo,longitud,profundidad,color_base):

    if profundidad == 0 or longitud < 2:

        return 
    
    x1 = x + int(math.cos(math.radians(angulo)) * longitud)
    y1 = y - int(math.sin(math.radians(angulo)) * longitud) 

    brillo = min(255,40 + profundidad * 18)
    color = (0, brillo, int(brillo * 0.4 ))
    grosor = max(1, profundidad//2)
    pygame.draw.line(superficie, color,(x,y),(x1,y1),grosor )

    fondo(superficie, x1, y1, angulo + 30, int(longitud * 0.65 ), profundidad - 1, color_base)
    fondo(superficie, x1, y1, angulo - 30, int(longitud * 0.65 ), profundidad - 1, color_base)

def generar_fondo ():

    n = pygame.Surface((ANCHO,ALTO),pygame.SRCALPHA)
    n.fill((0,0,0,0))

    fondo(n, 60, ALTO - 10, 90, 55, 7, verde)
    fondo(n, ANCHO - 60, ALTO - 10, 90, 55, 7, verde)

    return n 

fon = generar_fondo()

def masos():

    palos = ["♠", "♥", "♦", "♣"] 
    valores = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
    jun = [(b,p) for p in palos for b in valores ]
    random.shuffle(jun) 

    return jun 

def calcular_cartas (carta):

    if carta in ("J","Q","K"):

        return 10 
    
    elif carta == "A":

        return 11 
    
    else:

        return int(carta)
    

def ases(mano_jugador):

    if not mano_jugador: 

        return 0 
    
    cabeza, * resto = mano_jugador
    b, _ = cabeza 

    return (1 if b == "A" else 0 ) + ases(resto)

def sumar_mano(mano):

    if not mano:

        return 0 
    
    cabeza, * resto = mano 
    b, _ = cabeza 
    
    return calcular_cartas(b) + sumar_mano(resto)

def ajuste_ases(total_mano, ases_totales):

    if total_mano <= 21 or ases_totales == 0:

        return total_mano 
    
    return ajuste_ases(total_mano - 10, ases_totales - 1 )

def valor_mano(mano_jugador):

    total_carta = sumar_mano(mano_jugador)
    total_ases = ases(mano_jugador) 

    return ajuste_ases(total_carta,total_ases)

def dibujar_cartas(carta,x,y,oculta = False):

    if oculta == True:
        
        color_cartas = (40,100,60)

    else:

        color_cartas = blanco

    pygame.draw.rect(ventana, color_cartas, (x,y,60,85), border_radius = 6)    
    pygame.draw.rect(ventana, gris, (x,y,60,85), 1 , border_radius = 6)
    
    if not oculta:

        b, p = carta
        
        if p in ("♥", "♦"):

            color_texto = rojo 
        
        else:
            
            color_texto = negro 

        l = fuente_normal.render(b, True, color_texto)
        k = fuente_normal.render(p, True, color_texto)

        ventana.blit(l,(x + 5, y + 5))
        ventana.blit(k,(x + 5, y + 25))

        h = fuente_grande.render(p, True, color_texto)

        ventana.blit(h,(x + 30 - h.get_width()//2, y + 42 - h.get_height()//2)) 

def botones(texto, x, y, activo = True):

    if activo:

        color_boton = verdebtn
    
    else: 

        color_boton = (20,70,40)
    
    pygame.draw.rect(ventana, color_boton, (x,y,140,38), border_radius = 7)
    pygame.draw.rect(ventana, blanco if activo else gris, (x,y,140,38), 1,  border_radius = 7)
    
    b = fuente_normal.render(texto, True, blanco if activo else gris)
    ventana.blit(b, (x + 70 - b.get_width()//2, y + 19 - b.get_height()//2))

def texto(mensaje, x, y, color = blanco, grande = False):

    if grande: 

        g = fuente_grande

    else: 

        g = fuente_normal
    
    ventana.blit(g.render(mensaje, True, color ), (x,y))

def nueva_partida():

    global diler,jugador,sistema,estado,mensaje,tiempo_sistema,umbral,agresividad 

    diler = masos() 
    jugador = [diler.pop(),diler.pop()]
    sistema = [diler.pop(),diler.pop()]
    estado = "jugando"
    mensaje = ""
    tiempo_sistema = 0 


    if agresividad >= 3: 

        umbral = 18 
    
    elif agresividad <= -2:

        umbral = 16 

    else:

        umbral = 17 
    
def terminar_juego(resultado):

    global victorias, derrotas, empates,estado,mensaje,color_mensaje

    cal_mano = valor_mano(jugador)
    mano_sistema = valor_mano(sistema)
    estado = "resultado"

    if resultado == "gana_jugador":

        victorias += 1

        mensaje = f"ganaste: tu{cal_mano},  sistema {mano_sistema}"
        color_mensaje = blanco

    elif resultado == "gana_sistema":

        derrotas += 1 

        mensaje =f"perdiste: tu {cal_mano}, sistema {mano_sistema}"
        color_mensaje = blanco 
    
    else:

        empates += 1

        mensaje = f"empate: tu {cal_mano}, sistema {mano_sistema}"
        color_mensaje = blanco 
    
corriendo = True 

while corriendo:

    dt = reloj.tick(60) 

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:

            corriendo = False
        
        if evento.type == pygame.MOUSEBUTTONDOWN:

            mx, my = evento.pos 

            if estado in ("inicio", "resultado"):

                if pygame.Rect(20, ALTO - 55,140, 138 ).collidepoint(mx,my):

                    nueva_partida()
                
            if estado == "jugando":

                if pygame.Rect(175,ALTO - 55,140, 38).collidepoint(mx,my):

                    jugador.append(diler.pop())

                    t = valor_mano(jugador)

                    if t > 15:

                        agresividad += 1 

                    if t > 21:

                        terminar_juego("gana_sistema")
                    
                    elif t == 21:

                        estado = "turno_sistema"

                if pygame.Rect(330,ALTO - 55,140, 38).collidepoint(mx,my):

                    if valor_mano(jugador) <= 15: 

                        agresividad -= 1 
                    
                    estado = "turno_sistema"
    
    if estado == "turno_sistema":

        tiempo_sistema += dt 

        if tiempo_sistema >= 800:

            tiempo_sistema = 0 

            j = valor_mano(sistema)

            if j < umbral:

                sistema.append(diler.pop())

                if valor_mano(sistema) > 21:

                    terminar_juego("gana_jugador")

            else: 

                d = valor_mano(jugador)
                s = valor_mano(sistema)

                if d > s: 

                    terminar_juego ("gana_jugador")

                elif d < s: 

                    terminar_juego("gana_sistema")
                
                else:

                    terminar_juego("empate")

    ventana.fill(verdebtn)
    ventana.blit(fon,(0,0))
    texto("Blackjack",10,8,blanco,grande = True)
    texto("sistema cibernetico ", 10, 50, (180,230,200))

    for i, carta in enumerate(sistema):

        oculta = (i == 1 and estado == "jugando")
        dibujar_cartas(carta,10 + i * 70, 75, oculta = oculta )
    
    if sistema:

        a = valor_mano(sistema)
        w = f"total:{a}" if estado != "jugando" else "total:?"
        
        texto(w,10 + len(sistema) * 70 + 10, 90 )
    
    pygame.draw.line(ventana,(20,90,50),(0,235),(ANCHO,235),2) 
    texto("jugador",10 , 245,(180,230,200))

    for i, carta in enumerate(jugador):

        dibujar_cartas(carta,10 + i * 70, 268  )

    if jugador:

        q = valor_mano(jugador)
        r = (60,200,100) if q == 21 else (220,70,70) if q > 21 else blanco

        texto (f"total {q}", 10 + len(jugador)* 70 + 10, 280, r ) 
    
    texto("Resultados:",  ANCHO-175, 50, amarillo)
    texto(f"Victorias: {victorias}", ANCHO-175, 78,  (60, 200, 100))
    texto(f"Derrotas:  {derrotas}",  ANCHO-175, 102, (220, 70, 70))
    texto(f"Empates:   {empates}",   ANCHO-175, 126, (220, 180, 50))
    texto(f"Umbral Autonomo: {umbral}", ANCHO-175, 155, (100, 200, 255))

    if estado == "turno_sistema": 

        h = valor_mano(sistema)
        texto(f"sistema {h}(umbral{umbral})", 10,205,(100,200,255))
    
    if estado == "resultado" and mensaje:

        texto(mensaje,ANCHO//2 - 160, ALTO//2 - 55, color_mensaje, grande = True) 
    
    en_inicio = estado in ("inicio", "resultado")
    en_juego  = estado == "jugando"
    botones("Nueva partida", 20,  ALTO-55, activo=en_inicio)
    botones("Pedir carta",   175, ALTO-55, activo=en_juego)
    botones("Plantarse",     330, ALTO-55, activo=en_juego)

    pygame.display.flip()

pygame.quit()
