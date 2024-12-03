import cv2
import numpy as np

def ajustar_imagem(img, brilho, saturacao, contraste, blur):
    """
    Ajusta os parâmetros de brilho, saturação, contraste e desfoque de uma imagem.

    Esta função converte a imagem de BGR para HSV para ajustar o brilho e a saturação,
    e depois converte de volta para BGR. Em seguida, aplica um ajuste de contraste utilizando
    a função convertScaleAbs e, se solicitado, aplica um desfoque gaussiano na imagem.

    Parâmetros:
    img (ndarray): A imagem de entrada no formato BGR.
    brilho (int): O valor de ajuste de brilho. Pode ser negativo para diminuir o brilho.
    saturacao (int): O valor de ajuste de saturação. Pode ser negativo para diminuir a saturação.
    contraste (float): O fator de contraste a ser aplicado, onde 1.0 é o valor original.
    blur (int): O raio do desfoque gaussiano a ser aplicado. Se maior que 0, o desfoque é aplicado.

    Retorna:
    ndarray: A imagem ajustada após as modificações de brilho, saturação, contraste e desfoque.
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

def on_change(val):
    """
    Função de callback para ser chamada sempre que um controle deslizante (trackbar) for alterado.

    Essa função captura os valores ajustados nos controles de brilho, saturação, contraste e desfoque,
    chama a função `ajustar_imagem` para aplicar essas modificações e exibe a imagem resultante.

    Parâmetros:
    val (int): Valor do controle deslizante (não utilizado diretamente, mas necessário para o callback).
    """
    brilho = cv2.getTrackbarPos("Brilho", "Editor") - 100
    saturacao = cv2.getTrackbarPos("Saturacao", "Editor") - 100
    contraste = cv2.getTrackbarPos("Contraste", "Editor") / 50.0
    blur = cv2.getTrackbarPos("Desfoque", "Editor")

    img_ajustada = ajustar_imagem(img_original, brilho, saturacao, contraste, blur)
    cv2.imshow("Editor", img_ajustada)

# Carregar imagem
# caminho = input('Digite o caminho para onde a imagem se encontra: ')
caminho = 'imagens/cachorro.jpg'
img_original = cv2.imread(caminho)
if img_original is None:
    print("Imagem nao encontrada!")
    exit()

# Create window before trackbars
cv2.namedWindow("Editor")

# Create all trackbars without value pointers
cv2.createTrackbar("Brilho", "Editor", 0, 200, on_change)
cv2.createTrackbar("Saturacao", "Editor", 0, 200, on_change)
cv2.createTrackbar("Contraste", "Editor", 0, 100, on_change)
cv2.createTrackbar("Desfoque", "Editor", 0, 20, on_change)

# Set initial values for trackbars
cv2.setTrackbarPos("Brilho", "Editor", 100)
cv2.setTrackbarPos("Saturacao", "Editor", 100)
cv2.setTrackbarPos("Contraste", "Editor", 50)
cv2.setTrackbarPos("Desfoque", "Editor", 0)

# Call on_change to initialize the image
on_change(0)

# Loop principal
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cv2.destroyAllWindows()
