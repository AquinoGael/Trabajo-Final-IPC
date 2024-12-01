import pygame
import sys
import time

# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana
largo, alto = 800, 600
blanco = (255, 255, 255)

screen = pygame.display.set_mode((largo, alto))
pygame.display.set_caption("Turbo Track")

# Clock setup
clock = pygame.time.Clock()
def manejar_eventos(salir=True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if salir and (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN):
            return True
    return False

# Función para renderizar texto con contorno
def renderizar_texto_con_contorno(texto, fuente, color_texto, color_contorno, pos):
    text_surf = fuente.render(texto, True, color_contorno)
    rect = text_surf.get_rect(center=pos)
    for dx in (-2, 2):
        for dy in (-2, 2):
            screen.blit(fuente.render(texto, True, color_contorno), (rect.x + dx, rect.y + dy))
    screen.blit(fuente.render(texto, True, color_texto), rect)

def pantalla_de_inicio():
    
    fondo = pygame.transform.scale(pygame.image.load("Imagenes y demas descargas/pantalla_inicio.png"), (largo, alto))
    fuente = pygame.font.Font('imagenes y demas descargas/PressStart2P.ttf', 20)
    colores = [(92, 225, 230), blanco]
    indice_color, tiempo_anterior = 0, pygame.time.get_ticks()

    while True:
        if manejar_eventos():
            return
        if pygame.time.get_ticks() - tiempo_anterior > 500:
            indice_color = 1 - indice_color
            tiempo_anterior = pygame.time.get_ticks()

        screen.blit(fondo, (0, 0))
        renderizar_texto_con_contorno("Press any key to continue", fuente, colores[indice_color], blanco, (largo // 2-20, alto - 100))
        pygame.display.flip()
        clock.tick(60)
def pantalla_eleccion_modo():
    '''pantalla de eleccion del modo de juego'''
    # Cargar la imagen de fondo
    fondo = pygame.image.load("imagenes y demas descargas/pantalla_eleccion.png")
    fondo = pygame.transform.scale(fondo, (largo , alto))

    # Configuración de la fuente
    fuente = pygame.font.Font('imagenes y demas descargas/PressStart2P.ttf', 40)

    # Opciones de texto y posiciones individuales
    opciones = [
        {"texto": "1. 1 player", "posicion": (largo // 2, alto // 2 - 50)},
        {"texto": "2. 2 players", "posicion": ((largo // 2)+24, (alto // 2)+20)},
        {"texto": "3. Instructions", "posicion": (largo // 2, (alto // 2 + 50)+35)},
    ]

    # Colores iniciales
    COLOR_BASE = (92, 225, 230)
    COLOR_ALTERNADO = (255, 255, 255)

    tiempo_cambio = 500  # Tiempo en ms para alternar el color
    ultima_actualizacion = pygame.time.get_ticks()
    mostrar_color_base = True  # Alternar entre los colores

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return  # Salir de la pantalla de elección

        # Alternar colores de texto
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - ultima_actualizacion >= tiempo_cambio:
            mostrar_color_base = not mostrar_color_base
            ultima_actualizacion = tiempo_actual

        # Definir el color actual
        color_actual = COLOR_BASE if mostrar_color_base else COLOR_ALTERNADO

        # Dibujar el fondo
        screen.blit(fondo, (0, 0))

        # Dibujar las opciones animadas en sus posiciones individuales
        for opcion in opciones:
            texto_surface = fuente.render(opcion["texto"], True, color_actual)
            texto_rect = texto_surface.get_rect(center=opcion["posicion"])
            screen.blit(texto_surface, texto_rect)

                #running = False
        # Actualizar la pantalla
        pygame.display.flip()
        clock.tick(60)

def pantalla_eleccion_personaje():
    '''pantalla de eleccion de personaje'''
    # Cargar la imagen de fondo
    background_imagez = pygame.image.load('Imagenes y demas descargas/eleccion_personajes.png')
    background_image = pygame.transform.scale(background_imagez, (largo, alto))

    # Fuente de letras
    font = pygame.font.Font('imagenes y demas descargas/PressStart2P.ttf', 25)

    # Ubicación del texto animado
    text_data = [
        {'text': 'Press W', 'pos': (5, 520), 'colors': [(255, 255, 255), (92, 225, 230)]},
        {'text': 'Press M', 'pos': (205, 520), 'colors': [(255, 255, 255), (92, 225, 230)]},
        {'text': 'Press R', 'pos': (405, 520), 'colors': [(255, 255, 255), (92, 225, 230)]},
        {'text': 'Press F', 'pos': (615, 520), 'colors': [(255, 255, 255), (92, 225, 230)]},
    ]

    toggle_index = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                #si eligen a un personaje, sale su pantalla de carga
                if event.key == pygame.K_w:  
                    pantalla_de_carga_personaje('pantalla_personajes/colapinto.png', (173, 216, 230), (0, 0, 128), 'Williams')
                elif event.key == pygame.K_r: 
                    pantalla_de_carga_personaje('pantalla_personajes/red bull.png', (255, 0, 0), (0, 0, 128), 'Red Bull')
                elif event.key == pygame.K_f:  
                    pantalla_de_carga_personaje('pantalla_personajes/ferrari.png', (255, 20, 0), (255, 24, 7), 'Ferrari')
                elif event.key == pygame.K_m:
                    pantalla_de_carga_personaje('pantalla_personajes/mclaren.png', (254, 80, 0), (255,200,0), 'Mc Laren')
                return 

        # Dibujar la imagen de fondo
        screen.blit(background_image, (0, 0))

        # Dibujar el texto
        for data in text_data:
            color = data['colors'][toggle_index % 2]
            text_surface = font.render(data['text'], True, color)
            screen.blit(text_surface, data['pos'])

        # Actualizar la pantalla
        pygame.display.flip()

        # Alternar índice de colores
        toggle_index += 1
        pygame.time.delay(500)  # Retraso en la animación
# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
#screen = pygame.display.set_mode((largo, alto))
# Función para mostrar la pantalla de cargar
def pantalla_de_carga_personaje(nombre_archivo, color_principal, color_secundario, nombre):
    '''pantalla de carga dependiendo la eleccion de personaje
    argumentos:
    nombre_archivo(str): nombre del archivo de la imagen
    color_principal(list): indica el color con el que va a ir alternando el titular
    color_barra(list): indica el color de la barra de carga
    nombre(str): nombre de la marca representante'''
    # Colores personalizados segun el personaje elegido
    color_principal = color_principal
    color_barra = color_secundario

    # Fuente
    font_title = pygame.font.Font('imagenes y demas descargas/PressStart2P.ttf', 35)
    font_small = pygame.font.Font('imagenes y demas descargas/PressStart2P.ttf', 30)

    # Cargar la imagen de fondo
    fondo = pygame.image.load(nombre_archivo)
    fondo = pygame.transform.scale(fondo, (largo,alto))

    titular = nombre
    color_titular = [color_principal, blanco]
    color_index = 0  # Para alternar los colores

    # Configuración de la animación de "Cargando..."
    texto_carga = ["Cargando.", "Cargando..", "Cargando..."]
    loading_text_index = 0

    # Barra de carga
    largo_barra_carga = 600
    ancho_barra_carga = 20
    start_time = time.time()

    # Bucle principal
    running = True
    while running:

        # Dibujar la imagen de fondo
        screen.blit(fondo, (0, 0))

        # Alternar colores para "Williams"
        color_index = (color_index + 1) % 2  # Alternar entre 0 y 1
        title_text = font_title.render(titular, True, color_titular[color_index])
        screen.blit(title_text, (30, 50))

        # Dibujar el texto de "Cargando..." animado
        loading_text = font_small.render(texto_carga[loading_text_index], True, blanco)
        screen.blit(loading_text, (largo // 2 - 130, alto - 100))
        loading_text_index = (loading_text_index + 1) % len(texto_carga)

        # Barra de carga
        elapsed_time = time.time() - start_time
        progress = min(1, elapsed_time / 10)  # Progreso de 0 a 1 en 10 segundos
        pygame.draw.rect(screen, color_barra, (
            largo // 2 - largo_barra_carga // 2, alto - 50,
            largo_barra_carga * progress, ancho_barra_carga))

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Actualizar la pantalla
        pygame.display.flip()
        pygame.time.delay(500)  # Retraso para la animación

        # Salir cuando la barra de carga esté completa
        if progress >= 1:
            running = False

    # Finalizar Pygame
    pygame.quit()

def main():
    '''funcion principal del programa'''
    pygame.mixer_music.load('stressed_out.mp3')
    pygame.mixer_music.play(-1)
    pantalla_de_inicio()
    pantalla_eleccion_modo()
    pantalla_eleccion_personaje()
    pygame.quit()

if __name__ == "__main__":
    main()
    
