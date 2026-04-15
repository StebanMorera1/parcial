import pygame #libreria interfas grafica 
import random #libreria genera azar
import math  #libreria matematica (fractal)

pygame.init() # se activan todos los modulos de pygame 

#definición de las medidas de la pantalla 
ANCHO =  700
ALTO = 500

#se crea la venta principal, siendo esta la interfaz de salida 
ventana = pygame.display.set_mode((ANCHO,ALTO))
pygame.display.set_caption("Black jack") 

reloj = pygame.time.Clock() #se regulan los ciclos de tiempo 

# definición de colores 
verde = (34,120,60)
blanco = (255,255,255)
negro = (0,0,0)
rojo = (180,30,30)
amarillo = (220,180,50)
gris = (150,150,150)
verdebtn = (30,140,80)

#se carga tipografia 
fuente_normal = pygame.font.SysFont("Arial", 20 )
fuente_grande = pygame.font.SysFont("Arial", 30, bold = True  )

diler = []  #almacena los datos de los mazos de las cartas 
jugador = [] #Registro del estado del jugador 
sistema = [] #Registro del estado del sistema (sistema cibernetico )

#contadores de resultados (retroalimentación )
victorias = 0
derrotas = 0 
empates = 0


estado = "inicio" #la variable controla la fase 

mensaje = ""  #canal de comunicación con el usuario 
color_mensaje = blanco 
tiempo_sistema = 0 #temporizador interno que simula el pensamiento del sistema 

#adaptación 
agresividad = 0  #riesgo dependiendo del historial de jugadas 
umbral = 17     #punto de decision 

#se genera función encargada del fondo (fractal,complejidad y recursividad )
def fondo(superficie,x,y,angulo,longitud,profundidad,color_base): 

    if profundidad == 0 or longitud < 2: #condición de parada 

        return 
    #calculo de las siguentes coordenadas (transformación lineal )
    x1 = x + int(math.cos(math.radians(angulo)) * longitud) 
    y1 = y - int(math.sin(math.radians(angulo)) * longitud) 

    #variación de color y brillo dependiendo de la profundidad 
    brillo = min(255,40 + profundidad * 18)
    color = (0, brillo, int(brillo * 0.4 ))
    grosor = max(1, profundidad//2)
    pygame.draw.line(superficie, color,(x,y),(x1,y1),grosor )#dibujo del segmento 

    #se llama la función a si misma con cambios 
    fondo(superficie, x1, y1, angulo + 30, int(longitud * 0.65 ), profundidad - 1, color_base) #izquierda 
    fondo(superficie, x1, y1, angulo - 30, int(longitud * 0.65 ), profundidad - 1, color_base) #derecha 

def generar_fondo ():
    #se crea una superficie independiente para el fondo 
    n = pygame.Surface((ANCHO,ALTO),pygame.SRCALPHA)
    n.fill((0,0,0,0)) #fondo transparente 
    
    #se generan dos figuras fractales en los extremos 
    fondo(n, 60, ALTO - 10, 90, 55, 7, verde)
    fondo(n, ANCHO - 60, ALTO - 10, 90, 55, 7, verde)

    return n 

fon = generar_fondo() # almacenamiento del resultado de la recusividad 

#logica de infomación, se procesaran los datos 
def masos(): 

    palos = ["♠", "♥", "♦", "♣"] 
    valores = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
    jun = [(b,p) for p in palos for b in valores ] #se generan todas las combinaciones posibles 
    random.shuffle(jun) #reordena los elementos de la lista aleatoriamente 

    return jun 
#en esta función se traducen los simbolos a valores numericos 
def calcular_cartas (carta):

    if carta in ("J","Q","K"): 

        return 10 
    
    elif carta == "A":

        return 11 
    
    else:

        return int(carta)
    
#conteo de elementos ases 
def ases(mano_jugador):

    if not mano_jugador: 

        return 0 
    
    cabeza, * resto = mano_jugador #se divide el sistema en partes 
    b, _ = cabeza 
   
    # Suma 1 si es As, y continúa procesando el resto de la lista
    return (1 if b == "A" else 0 ) + ases(resto)



def sumar_mano(mano):

    if not mano:

        return 0 
    
    cabeza, * resto = mano 
    b, _ = cabeza 
    
    return calcular_cartas(b) + sumar_mano(resto)

#retroalimentació
def ajuste_ases(total_mano, ases_totales): # se busca el control para evitar el colapso 

    if total_mano <= 21 or ases_totales == 0: #si el valor es estable el sistema no hace nada 

        return total_mano 
    
    return ajuste_ases(total_mano - 10, ases_totales - 1 ) # si hay un exeso este reduce en 10 y reevalua 

#suma y ajusta para obtener el estado real del sistema 
def valor_mano(mano_jugador):

    total_carta = sumar_mano(mano_jugador)
    total_ases = ases(mano_jugador) 

    return ajuste_ases(total_carta,total_ases)

#función de interfaz 
def dibujar_cartas(carta,x,y,oculta = False): # representación visual  de las cartas en el espacio de la ventana 

    if oculta == True: 
        
        color_cartas = (40,100,60)

    else:

        color_cartas = blanco

    #se dibuja la forma base de las cartas 
    pygame.draw.rect(ventana, color_cartas, (x,y,60,85), border_radius = 6)    
    pygame.draw.rect(ventana, gris, (x,y,60,85), 1 , border_radius = 6)
    
    if not oculta:

        b, p = carta #se extrae valor y palo 
        
        if p in ("♥", "♦"): 

            color_texto = rojo  #le da el color rojo por su palo 
        
        else:
            
            color_texto = negro  #si no son "♥", "♦" les pone color negro 

        l = fuente_normal.render(b, True, color_texto)
        k = fuente_normal.render(p, True, color_texto)

        ventana.blit(l,(x + 5, y + 5))
        ventana.blit(k,(x + 5, y + 25))

        h = fuente_grande.render(p, True, color_texto) #el icono central sera mas grande 

        ventana.blit(h,(x + 30 - h.get_width()//2, y + 42 - h.get_height()//2)) 

#creación de los elementos de entrada interactivos 
def botones(texto, x, y, activo = True):

    if activo:

        color_boton = verdebtn # color principal 
    
    else: 

        color_boton = (20,70,40) # color apagado si no se usa 

    pygame.draw.rect(ventana, color_boton, (x,y,140,38), border_radius = 7) # Dibuja el cuerpo del botón (rectángulo con bordes redondeados)
    pygame.draw.rect(ventana, blanco if activo else gris, (x,y,140,38), 1,  border_radius = 7)# Dibuja el borde del botón (blanco si está activo, gris si no)
    
    #centra el texto dentro del boton 
    b = fuente_normal.render(texto, True, blanco if activo else gris)
    ventana.blit(b, (x + 70 - b.get_width()//2, y + 19 - b.get_height()//2))

#función para escribir texto en la ventana 
def texto(mensaje, x, y, color = blanco, grande = False):

# elige entre dos tamaños de fuente 
    if grande: 

        g = fuente_grande

    else: 

        g = fuente_normal
    
    ventana.blit(g.render(mensaje, True, color ), (x,y))


#logica del juego 
def nueva_partida():

    
    global diler,jugador,sistema,estado,mensaje,tiempo_sistema,umbral,agresividad # se reinician la variables para una nueva partida 

    diler = masos()  #genera un nuevo mazo de juego 
    jugador = [diler.pop(),diler.pop()] # entrega dos cartas al jugador 
    sistema = [diler.pop(),diler.pop()] #entrega dos cartas al sistema 
    estado = "jugando" #cambia el estado del juego 
    mensaje = ""
    tiempo_sistema = 0  #reinicia el temporizador para las decisiones del sistema 

    #Ajusta el 'umbral' (límite para plantarse) basado en la agresividad acumulada
    if agresividad >= 3: 

        umbral = 18 #el sistema se arriegara mas 
    
    elif agresividad <= -2:

        umbral = 16 #el sistema se mantiene conservador 

    else:

        umbral = 17 # comportamiento estandar 
    
#finalización de ronda 
def terminar_juego(resultado): # se actualizan estadisticas y se muestra mensaje de final 

    global victorias, derrotas, empates,estado,mensaje,color_mensaje

    cal_mano = valor_mano(jugador) #suma total de puntos del jugador 
    mano_sistema = valor_mano(sistema) #suma total del sistema 
    estado = "resultado" #cambia el estado para mostrar botones 

    #conteo de marcador 
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

#bucle principal 
while corriendo:

    dt = reloj.tick(60)  #controlador de fotogramas y del tiempo transcurrido 

    for evento in pygame.event.get(): #se gestionan los eventos mause/teclado

        if evento.type == pygame.QUIT:

            corriendo = False
        
        if evento.type == pygame.MOUSEBUTTONDOWN:

            mx, my = evento.pos #coordenadas del click 

            if estado in ("inicio", "resultado"): # Click en "Nueva partida" (Solo si el juego no ha empezado o ya terminó)

                if pygame.Rect(20, ALTO - 55,140, 138 ).collidepoint(mx,my):

                    nueva_partida()
            
            #acciones durante el turno del jugador   
            if estado == "jugando":

                if pygame.Rect(175,ALTO - 55,140, 38).collidepoint(mx,my): # si se pulsa en pedir carta 

                    jugador.append(diler.pop()) # se le quita uno a la mano del diler 

                    t = valor_mano(jugador)

                    if t > 15: # Si el jugador arriesga con valores altos, el sistema  se vuelve más agresivo

                        agresividad += 1 

                    if t > 21: # jugador se pasa 

                        terminar_juego("gana_sistema")
                    
                    elif t == 21: # Blackjack automático, pasa el turno

                        estado = "turno_sistema"
                #se da click en plantase 
                if pygame.Rect(330,ALTO - 55,140, 38).collidepoint(mx,my):

                    if valor_mano(jugador) <= 15: 

                        agresividad -= 1 # Si el jugador se planta con poco, el sistema será precavido
                    
                    estado = "turno_sistema"
    
    #LOGICA DEL SISTEMA 
    if estado == "turno_sistema":

        tiempo_sistema += dt #temporizador para que el sistema no juegue instantaneamente 

        if tiempo_sistema >= 800: #espera unos segundos entre acciones 

            tiempo_sistema = 0 

            j = valor_mano(sistema)

            if j < umbral: # Si el sistema tiene menos puntos que su 'umbral', pide carta

                sistema.append(diler.pop())

                if valor_mano(sistema) > 21: # sistema pierde por pasarse 

                    terminar_juego("gana_jugador")

            else:  #si el sistema no se pasa se planta y se comparan puntuaciones 

                d = valor_mano(jugador) 
                s = valor_mano(sistema)

                if d > s: 

                    terminar_juego ("gana_jugador")

                elif d < s: 

                    terminar_juego("gana_sistema")
                
                else:

                    terminar_juego("empate")
    #dibujo en pantalla 
    ventana.fill(verdebtn) #fondo verde 
    ventana.blit(fon,(0,0))#imagen de fondo
    texto("Blackjack",10,8,blanco,grande = True)
    texto("sistema cibernetico ", 10, 50, (180,230,200))

    #dibujo de cartas del sistema 
    for i, carta in enumerate(sistema):

        oculta = (i == 1 and estado == "jugando") #oculta la segunda carta del sistema si el jugador sigue decidiendo 
        dibujar_cartas(carta,10 + i * 70, 75, oculta = oculta )
    
    #muestra el puntaje del sistema 
    if sistema:

        a = valor_mano(sistema)
        w = f"total:{a}" if estado != "jugando" else "total:?"
        
        texto(w,10 + len(sistema) * 70 + 10, 90 )
    # Línea divisoria y sección del jugador
    pygame.draw.line(ventana,(20,90,50),(0,235),(ANCHO,235),2) 
    texto("jugador",10 , 245,(180,230,200))
    # Dibujar cartas del jugador y su puntaje
    for i, carta in enumerate(jugador):

        dibujar_cartas(carta,10 + i * 70, 268  )

    if jugador:

        q = valor_mano(jugador)
        r = (60,200,100) if q == 21 else (220,70,70) if q > 21 else blanco # Cambia el color del texto si llega a 21 (verde) o se pasa (rojo)

        texto (f"total {q}", 10 + len(jugador)* 70 + 10, 280, r ) 
    
    #panel de estadisticas que se encuentran a la derecha 
    texto("Resultados:",  ANCHO-175, 50, amarillo)
    texto(f"Victorias: {victorias}", ANCHO-175, 78,  (60, 200, 100))
    texto(f"Derrotas:  {derrotas}",  ANCHO-175, 102, (220, 70, 70))
    texto(f"Empates:   {empates}",   ANCHO-175, 126, (220, 180, 50))
    texto(f"Umbral Autonomo: {umbral}", ANCHO-175, 155, (100, 200, 255))

    if estado == "turno_sistema": 

        h = valor_mano(sistema)
        texto(f"sistema {h}(umbral{umbral})", 10,205,(100,200,255))
    

    if estado == "resultado" and mensaje: # Mostrar mensaje de victoria/derrota en el centro

        texto(mensaje,ANCHO//2 - 160, ALTO//2 - 55, color_mensaje, grande = True) 
    
    # Dibujar los botones de acción
    en_inicio = estado in ("inicio", "resultado")
    en_juego  = estado == "jugando"
    botones("Nueva partida", 20,  ALTO-55, activo=en_inicio)
    botones("Pedir carta",   175, ALTO-55, activo=en_juego)
    botones("Plantarse",     330, ALTO-55, activo=en_juego)

    pygame.display.flip()# Actualizar pantalla

pygame.quit()#inicia el juego 
