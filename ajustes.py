import cv2
import numpy as np

def ajustar_imagem(img, brilho, saturacao, contraste, blur):
    """
    Ajusta a imagem com base nos parâmetros de brilho, saturação, contraste e desfoque.

    Parâmetros:
    img (numpy.ndarray): A imagem original a ser ajustada.
    brilho (int): Valor para ajustar o brilho. O valor positivo aumenta o brilho e o negativo reduz. Valores típicos variam de -255 a 255.
    saturacao (int): Valor para ajustar a saturação. O valor positivo aumenta a saturação e o negativo a reduz. Valores típicos variam de -255 a 255.
    contraste (float): Fator de contraste, onde 1.0 mantém o contraste original e valores acima de 1.0 aumentam o contraste, enquanto valores abaixo de 1.0 o diminuem.
    blur (int): Valor para aplicar desfoque. O valor 0 significa sem desfoque, e valores positivos aplicam desfoque gaussiano. Valores típicos variam de 0 a 20.

    Retorna:
    numpy.ndarray: A imagem ajustada.
    """
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
    """
    Função chamada quando há uma alteração em uma das trackbars, ajustando a imagem com base nos novos valores e exibindo-a.

    Parâmetros:
    brilho_scale (tk.Scale): Trackbar de brilho, que determina o valor de ajuste de brilho.
    saturacao_scale (tk.Scale): Trackbar de saturação, que determina o valor de ajuste de saturação.
    contraste_scale (tk.Scale): Trackbar de contraste, que determina o fator de contraste.
    desfoque_scale (tk.Scale): Trackbar de desfoque, que determina o valor de desfoque aplicado.
    img_atual (numpy.ndarray): A imagem original que será ajustada.
    label_imagem (tk.Label): O widget Tkinter onde a imagem ajustada será exibida.
    mostrar_imagem_tk (function): Função que exibe a imagem ajustada no Tkinter.
    """
    brilho = brilho_scale.get() - 100
    saturacao = saturacao_scale.get() - 100
    contraste = contraste_scale.get() / 50.0
    blur = desfoque_scale.get()

    img_ajustada = ajustar_imagem(img_atual, brilho, saturacao, contraste, blur)
    mostrar_imagem_tk(img_ajustada, label_imagem)

def reset_image(brilho_scale, saturacao_scale, contraste_scale, desfoque_scale, on_change_callback):
    """
    Reseta os valores das trackbars para os valores padrão e aplica os ajustes na imagem.

    Parâmetros:
    brilho_scale (tk.Scale): Trackbar de brilho, que será resetado.
    saturacao_scale (tk.Scale): Trackbar de saturação, que será resetado.
    contraste_scale (tk.Scale): Trackbar de contraste, que será resetado.
    desfoque_scale (tk.Scale): Trackbar de desfoque, que será resetado.
    on_change_callback (function): Função de callback que será chamada para aplicar os ajustes à imagem após o reset.
    """
    # Resetar valores das trackbars
    brilho_scale.set(100)
    saturacao_scale.set(100)
    contraste_scale.set(50)
    desfoque_scale.set(0)

    # Atualiza os ajustes para a nova imagem
    on_change_callback(0)

