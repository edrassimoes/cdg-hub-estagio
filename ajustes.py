import cv2
import numpy as np

def ajustar_imagem(img, brilho, saturacao, contraste, blur):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    # Ajustar brilho
    v = cv2.add(v, brilho)
    v = np.clip(v, 0, 255)

    # Ajustar saturacao
    s = cv2.add(s, saturacao)
    s = np.clip(s, 0, 255)

    # Combinar HSV de volta
    hsv = cv2.merge((h, s, v))
    ajustada = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # Ajustar contraste
    ajustada = cv2.convertScaleAbs(ajustada, alpha=contraste, beta=0)

    # Aplicar desfoque
    if blur > 0:
        ajustada = cv2.GaussianBlur(ajustada, (2 * blur + 1, 2 * blur + 1), 0)

    return ajustada

def on_change(brilho_scale, saturacao_scale, contraste_scale, desfoque_scale, img_atual, label_imagem, mostrar_imagem_tk):
    brilho = brilho_scale.get() - 100
    saturacao = saturacao_scale.get() - 100
    contraste = contraste_scale.get() / 50.0
    blur = desfoque_scale.get()

    img_ajustada = ajustar_imagem(img_atual, brilho, saturacao, contraste, blur)
    mostrar_imagem_tk(img_ajustada, label_imagem)

def reset_image(brilho_scale, saturacao_scale, contraste_scale, desfoque_scale, on_change_callback):
    # Resetar valores das trackbars
    brilho_scale.set(100)
    saturacao_scale.set(100)
    contraste_scale.set(50)
    desfoque_scale.set(0)

    # Atualiza os ajustes para a nova imagem
    on_change_callback(0)
