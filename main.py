import cv2
import numpy as np
import tkinter as tk
from threading import Thread

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

def on_change(val):
    brilho = cv2.getTrackbarPos("Brilho", "Editor") - 100
    saturacao = cv2.getTrackbarPos("Saturacao", "Editor") - 100
    contraste = cv2.getTrackbarPos("Contraste", "Editor") / 50.0
    blur = cv2.getTrackbarPos("Desfoque", "Editor")

    img_ajustada = ajustar_imagem(img_original, brilho, saturacao, contraste, blur)
    cv2.imshow("Editor", img_ajustada)

def fechar_aplicacao():
    global running
    running = False
    root.destroy()
    cv2.destroyAllWindows()

def iniciar_editor():
    global running
    while running:
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            fechar_aplicacao()
            break

# Configurar Tkinter
root = tk.Tk()
root.title("Controle da Aplicação")
root.geometry("200x100")
btn_fechar = tk.Button(root, text="Fechar", command=fechar_aplicacao)
btn_fechar.pack(expand=True)

# Carregar uma imagem
caminho = 'imagens/cachorro.jpg'
img_original = cv2.imread(caminho)
if img_original is None:
    print("Imagem não encontrada!")
    exit()

# Criar janela do editor
cv2.namedWindow("Editor")
cv2.createTrackbar("Brilho", "Editor", 0, 200, on_change)
cv2.createTrackbar("Saturacao", "Editor", 0, 200, on_change)
cv2.createTrackbar("Contraste", "Editor", 0, 100, on_change)
cv2.createTrackbar("Desfoque", "Editor", 0, 20, on_change)

cv2.setTrackbarPos("Brilho", "Editor", 100)
cv2.setTrackbarPos("Saturacao", "Editor", 100)
cv2.setTrackbarPos("Contraste", "Editor", 50)
cv2.setTrackbarPos("Desfoque", "Editor", 0)

# Inicializar imagem
on_change(0)

# Executar o editor em uma thread separada
running = True
thread_editor = Thread(target=iniciar_editor)
thread_editor.start()

# Iniciar interface gráfica do Tkinter
root.mainloop()
