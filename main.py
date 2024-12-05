import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from ajustes import on_change, reset_image

def mostrar_imagem_tk(img, label_imagem):
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

            reset_image(brilho_scale, saturacao_scale, contraste_scale, desfoque_scale, lambda val: on_change(brilho_scale, saturacao_scale, contraste_scale, desfoque_scale, img_atual, label_imagem, mostrar_imagem_tk))

def fechar_aplicacao():
    global running
    running = False
    root.destroy()

# Configura o Tkinter
root = tk.Tk()
root.title("Controle da Aplicação")
root.geometry("1300x900")

# Gera os botões
frame_botoes = tk.Frame(root)
frame_botoes.pack(side=tk.BOTTOM, pady=20)
btn_upload = tk.Button(frame_botoes, text="Upload de Imagem", command=abrir_imagem)
btn_upload.grid(row=0, column=0, padx=10)
btn_reset = tk.Button(frame_botoes, text="Reset", command=lambda: reset_image(brilho_scale, saturacao_scale, contraste_scale, desfoque_scale, lambda val: on_change(brilho_scale, saturacao_scale, contraste_scale, desfoque_scale, img_atual, label_imagem, mostrar_imagem_tk)))
btn_reset.grid(row=0, column=1, padx=10)
btn_fechar = tk.Button(frame_botoes, text="Fechar", command=fechar_aplicacao)
btn_fechar.grid(row=0, column=2, padx=10)

# Gera as trackbars
frame_controles = tk.Frame(root)
frame_controles.pack(side=tk.TOP, pady=10)
brilho_scale = tk.Scale(frame_controles, from_=0, to=200, orient="horizontal", label="Brilho", command=lambda val: on_change(brilho_scale, saturacao_scale, contraste_scale, desfoque_scale, img_atual, label_imagem, mostrar_imagem_tk))
brilho_scale.set(100)
brilho_scale.pack(side=tk.LEFT, padx=5)
saturacao_scale = tk.Scale(frame_controles, from_=0, to=200, orient="horizontal", label="Saturação", command=lambda val: on_change(brilho_scale, saturacao_scale, contraste_scale, desfoque_scale, img_atual, label_imagem, mostrar_imagem_tk))
saturacao_scale.set(100)
saturacao_scale.pack(side=tk.LEFT, padx=5)
contraste_scale = tk.Scale(frame_controles, from_=0, to=100, orient="horizontal", label="Contraste", command=lambda val: on_change(brilho_scale, saturacao_scale, contraste_scale, desfoque_scale, img_atual, label_imagem, mostrar_imagem_tk))
contraste_scale.set(50)
contraste_scale.pack(side=tk.LEFT, padx=5)
desfoque_scale = tk.Scale(frame_controles, from_=0, to=20, orient="horizontal", label="Desfoque", command=lambda val: on_change(brilho_scale, saturacao_scale, contraste_scale, desfoque_scale, img_atual, label_imagem, mostrar_imagem_tk))
desfoque_scale.set(0)
desfoque_scale.pack(side=tk.LEFT, padx=5)

# Gera a imagem inicial
frame_imagem = tk.Frame(root)
frame_imagem.pack(side=tk.TOP, pady=20)
label_imagem = tk.Label(frame_imagem)
label_imagem.pack()
caminho_inicial = 'imagens/cachorro.jpg'
img_original = cv2.imread(caminho_inicial)
if img_original is None:
    print("Imagem inicial não encontrada!")
    exit()
img_atual = img_original.copy()
on_change(brilho_scale, saturacao_scale, contraste_scale, desfoque_scale, img_atual, label_imagem, mostrar_imagem_tk)

# Inicia a interface gráfica
root.mainloop()
