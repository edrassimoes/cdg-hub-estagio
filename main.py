import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

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
    brilho = brilho_scale.get() - 100
    saturacao = saturacao_scale.get() - 100
    contraste = contraste_scale.get() / 50.0
    blur = desfoque_scale.get()

    img_ajustada = ajustar_imagem(img_atual, brilho, saturacao, contraste, blur)
    mostrar_imagem_tk(img_ajustada)

def reset_image():
    # Resetar valores das trackbars
    brilho_scale.set(100)
    saturacao_scale.set(100)
    contraste_scale.set(50)
    desfoque_scale.set(0)

    # Atualiza os ajustes para a nova imagem
    on_change(0)

def mostrar_imagem_tk(img):

    # Converter imagem OpenCV (BGR) para RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(img_pil)

    # Atualizar a imagem no label
    label_imagem.config(image=img_tk)
    label_imagem.image = img_tk

def abrir_imagem():
    global img_atual, img_original
    caminho = filedialog.askopenfilename(filetypes=[("Imagens", "*.jpg *.jpeg *.png *.bmp")])
    if caminho:
        nova_imagem = cv2.imread(caminho)
        if nova_imagem is not None:
            # Dimensões da imagem atual
            altura_atual, largura_atual = img_atual.shape[:2]
            # Dimensões da nova imagem
            altura_nova, largura_nova = nova_imagem.shape[:2]

            # Calcular fator de escala para preservar proporções
            escala = min(largura_atual / largura_nova, altura_atual / altura_nova)
            largura_redimensionada = int(largura_nova * escala)
            altura_redimensionada = int(altura_nova * escala)

            # Redimensionar a nova imagem
            nova_imagem_redimensionada = cv2.resize(nova_imagem, (largura_redimensionada, altura_redimensionada))

            # Calcular tamanhos de bordas
            borda_lateral = (largura_atual - largura_redimensionada) // 2
            borda_vertical = (altura_atual - altura_redimensionada) // 2

            # Adicionar bordas brancas
            nova_imagem_com_borda = cv2.copyMakeBorder(
                nova_imagem_redimensionada,
                top=borda_vertical,
                bottom=altura_atual - altura_redimensionada - borda_vertical,
                left=borda_lateral,
                right=largura_atual - largura_redimensionada - borda_lateral,
                borderType=cv2.BORDER_CONSTANT,
                value=[255, 255, 255]  # Cor branca
            )

            # Atualizar imagens globais
            img_original = nova_imagem_com_borda
            img_atual[:] = nova_imagem_com_borda

            reset_image()

def fechar_aplicacao():
    global running
    running = False
    root.destroy()

# Configurar Tkinter
root = tk.Tk()
root.title("Controle da Aplicação")
root.geometry("1300x900")

# Criar um Frame para os botões
frame_botoes = tk.Frame(root)
frame_botoes.pack(side=tk.BOTTOM, pady=20)

# Botões de controle
btn_upload = tk.Button(frame_botoes, text="Upload de Imagem", command=abrir_imagem)
btn_upload.grid(row=0, column=0, padx=10)

btn_reset = tk.Button(frame_botoes, text="Reset", command=reset_image)
btn_reset.grid(row=0, column=1, padx=10)

btn_fechar = tk.Button(frame_botoes, text="Fechar", command=fechar_aplicacao)
btn_fechar.grid(row=0, column=2, padx=10)

# Criar um Frame para as trackbars, logo abaixo dos botões
frame_controles = tk.Frame(root)
frame_controles.pack(side=tk.TOP, pady=10)

# Criar escalas para brilho, saturação, contraste e desfoque
brilho_scale = tk.Scale(frame_controles, from_=0, to=200, orient="horizontal", label="Brilho", command=on_change)
brilho_scale.set(100)
brilho_scale.pack(side=tk.LEFT, padx=5)

saturacao_scale = tk.Scale(frame_controles, from_=0, to=200, orient="horizontal", label="Saturação", command=on_change)
saturacao_scale.set(100)
saturacao_scale.pack(side=tk.LEFT, padx=5)

contraste_scale = tk.Scale(frame_controles, from_=0, to=100, orient="horizontal", label="Contraste", command=on_change)
contraste_scale.set(50)
contraste_scale.pack(side=tk.LEFT, padx=5)

desfoque_scale = tk.Scale(frame_controles, from_=0, to=20, orient="horizontal", label="Desfoque", command=on_change)
desfoque_scale.set(0)
desfoque_scale.pack(side=tk.LEFT, padx=5)

# Criar um Frame para exibir a imagem
frame_imagem = tk.Frame(root)
frame_imagem.pack(side=tk.TOP, pady=20)

# Label para exibir a imagem do OpenCV
label_imagem = tk.Label(frame_imagem)
label_imagem.pack()

# Carregar imagem inicial
caminho_inicial = 'imagens/cachorro.jpg'
img_original = cv2.imread(caminho_inicial)
if img_original is None:
    print("Imagem inicial não encontrada!")
    exit()

img_atual = img_original.copy()

# Inicializar imagem
on_change(0)

# Iniciar interface gráfica do Tkinter
root.mainloop()
