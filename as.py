import pygame as pg
import sys

ANCHO = 300
ALTO = 300
LINEA_ANCHO = 15
FILAS_TABLERO = 3
COLUMNAS_TABLERO = 3
TAMANO_CASILLA = ANCHO // COLUMNAS_TABLERO
RADIO_CIRCULO = TAMANO_CASILLA // 3
OFFSET_CRUZ = 50
ANCHO_CRUZ = 25
FPS = 30

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)

pg.init()

pantalla = pg.display.set_mode((ANCHO, ALTO))
pg.display.set_caption("Tres en Raya")

fuente_grande = pg.font.Font(None, 36)
fuente_pequena = pg.font.Font(None, 24)

def mostrar_texto(texto, x, y, fuente):
    texto_superficie = fuente.render(texto, True, BLANCO)
    pantalla.blit(texto_superficie, (x, y))

def dibujar_menu():
    pantalla.fill(NEGRO)
    mostrar_texto("TRES EN RAYA", 50, 50, fuente_grande)

    mostrar_texto("Selecciona tu símbolo:", 50, 150, fuente_pequena)

    pg.draw.rect(pantalla, ROJO, (50, 200, 100, 50))
    pg.draw.rect(pantalla, AZUL, (150, 200, 100, 50))

    mostrar_texto("X", 85, 215, fuente_grande)
    mostrar_texto("O", 185, 215, fuente_grande)

def dibujar_tablero():
    pantalla.fill(NEGRO)
    dibujar_lineas()
    dibujar_figuras()

def dibujar_lineas():
    pg.draw.line(pantalla, BLANCO, (0, TAMANO_CASILLA), (ANCHO, TAMANO_CASILLA), LINEA_ANCHO)
    pg.draw.line(pantalla, BLANCO, (0, 2 * TAMANO_CASILLA), (ANCHO, 2 * TAMANO_CASILLA), LINEA_ANCHO)
    pg.draw.line(pantalla, BLANCO, (TAMANO_CASILLA, 0), (TAMANO_CASILLA, ALTO), LINEA_ANCHO)
    pg.draw.line(pantalla, BLANCO, (2 * TAMANO_CASILLA, 0), (2 * TAMANO_CASILLA, ALTO), LINEA_ANCHO)

def dibujar_figuras():
    for fila in range(FILAS_TABLERO):
        for col in range(COLUMNAS_TABLERO):
            if tablero[fila][col] == 1:
                pg.draw.circle(pantalla, ROJO, (col * TAMANO_CASILLA + TAMANO_CASILLA // 2, fila * TAMANO_CASILLA + TAMANO_CASILLA // 2), RADIO_CIRCULO, LINEA_ANCHO)
            elif tablero[fila][col] == 2:
                texto_superficie = fuente_grande.render("X", True, AZUL)
                texto_superficie = pg.transform.scale(texto_superficie, (TAMANO_CASILLA-30, TAMANO_CASILLA-30))
                text_rect = texto_superficie.get_rect(center=(col * TAMANO_CASILLA + TAMANO_CASILLA // 2, fila * TAMANO_CASILLA + TAMANO_CASILLA // 2))
                pantalla.blit(texto_superficie, text_rect)

def inicializar_tablero():
    return [[0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]]

def esta_tablero_lleno(tablero):
    for fila in range(FILAS_TABLERO):
        for col in range(COLUMNAS_TABLERO):
            if tablero[fila][col] == 0:
                return False
    return True

def hay_ganador(tablero, jugador):
    for i in range(FILAS_TABLERO):
        if all(casilla == jugador for casilla in tablero[i]):
            return True
    for j in range(COLUMNAS_TABLERO):
        if all(tablero[i][j] == jugador for i in range(FILAS_TABLERO)):
            return True
    if all(tablero[i][i] == jugador for i in range(FILAS_TABLERO)):
        return True
    if all(tablero[i][FILAS_TABLERO - i - 1] == jugador for i in range(FILAS_TABLERO)):
        return True
    return False

def test_terminal(tablero):
    return hay_ganador(tablero, 1) or hay_ganador(tablero, 2) or esta_tablero_lleno(tablero)

def acciones(tablero):
    movimientos = []
    for fila in range(FILAS_TABLERO):
        for col in range(COLUMNAS_TABLERO):
            if tablero[fila][col] == 0:
                movimientos.append((fila, col))
    return movimientos

def resultado(tablero, accion, jugador):
    fila, col = accion
    nuevo_tablero = [fila[:] for fila in tablero]
    nuevo_tablero[fila][col] = jugador
    return nuevo_tablero

def utilidad(tablero):
    if hay_ganador(tablero, simbolo_maquina):
        return -1
    elif hay_ganador(tablero, simbolo_jugador):
        return 1
    elif esta_tablero_lleno(tablero):
        return 0
    else:
        return None

def mejor_movimiento(tablero):
    mejor_movimiento = None
    mejor_eval = float('inf')
    for accion in acciones(tablero):
        eval = minimax(resultado(tablero, accion, simbolo_maquina), True)
        if eval < mejor_eval:
            mejor_eval = eval
            mejor_movimiento = accion
    return mejor_movimiento

def minimax(tablero, maximizando_jugador):
    if test_terminal(tablero):
        return utilidad(tablero)

    if maximizando_jugador:
        max_eval = float('-inf')
        for accion in acciones(tablero):
            eval = minimax(resultado(tablero, accion, simbolo_jugador), False)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for accion in acciones(tablero):
            eval = minimax(resultado(tablero, accion, simbolo_maquina), True)
            min_eval = min(min_eval, eval)
        return min_eval

def jugador(tablero):
    count_X = sum(fila.count(simbolo_jugador) for fila in tablero)
    count_O = sum(fila.count(simbolo_maquina) for fila in tablero)
    if count_X <= count_O:
        return simbolo_jugador
    else:
        return simbolo_maquina

def mostrar_resultado(resultado_texto):
    pantalla.fill(NEGRO)
    mostrar_texto(resultado_texto, 50, 50, fuente_grande)
    pg.draw.rect(pantalla, BLANCO, (100, 200, 100, 50))
    mostrar_texto("Volver al Menú", 105, 215, fuente_pequena)

estado_juego = "MENU"
simbolo_jugador = None
simbolo_maquina = None
tablero = None

ejecutando = True
while ejecutando:
    for evento in pg.event.get():
        if evento.type == pg.QUIT:
            ejecutando = False
            pg.quit()
            sys.exit()
        
        if estado_juego == "MENU":
            if evento.type == pg.MOUSEBUTTONDOWN:
                mouseX, mouseY = pg.mouse.get_pos()
                if 50 <= mouseX <= 150 and 200 <= mouseY <= 250:
                    simbolo_jugador = 2
                    simbolo_maquina = 1
                    tablero = inicializar_tablero()
                    estado_juego = "JUGANDO"
                elif 150 <= mouseX <= 250 and 200 <= mouseY <= 250:
                    simbolo_jugador = 1
                    simbolo_maquina = 2
                    tablero = inicializar_tablero()
                    estado_juego = "JUGANDO"
        
        elif estado_juego == "JUGANDO":
            if evento.type == pg.MOUSEBUTTONDOWN or simbolo_maquina == jugador(tablero):
                if simbolo_jugador == jugador(tablero):
                    mouseX, mouseY = pg.mouse.get_pos()
                    if not test_terminal(tablero):
                        fila = mouseY // TAMANO_CASILLA
                        columna = mouseX // TAMANO_CASILLA
                        if tablero[fila][columna] == 0:
                            tablero = resultado(tablero, (fila, columna), simbolo_jugador)
                            if test_terminal(tablero):
                                if utilidad(tablero) == 1:
                                    resultado_texto = "Ganaste"
                                elif utilidad(tablero) == -1:
                                    resultado_texto = "Perdiste"
                                else:
                                    resultado_texto = "Empate"
                                estado_juego = "RESULTADO"
                else:
                    if not test_terminal(tablero):
                        movimiento = mejor_movimiento(tablero)
                        tablero = resultado(tablero, movimiento, simbolo_maquina)
                        if test_terminal(tablero):
                            if utilidad(tablero) == 1:
                                resultado_texto = "Ganaste"
                            elif utilidad(tablero) == -1:
                                resultado_texto = "Perdiste"
                            else:
                                resultado_texto = "Empate"
                            estado_juego = "RESULTADO"

        elif estado_juego == "RESULTADO":
            if evento.type == pg.MOUSEBUTTONDOWN:
                mouseX, mouseY = pg.mouse.get_pos()
                if 100 <= mouseX <= 200 and 200 <= mouseY <= 250:
                    estado_juego = "MENU"

    if estado_juego == "MENU":
        dibujar_menu()

    elif estado_juego == "JUGANDO":
        dibujar_tablero()
        dibujar_figuras()

    elif estado_juego == "RESULTADO":
        mostrar_resultado(resultado_texto)

    pg.display.update()
    pg.time.Clock().tick(FPS)
