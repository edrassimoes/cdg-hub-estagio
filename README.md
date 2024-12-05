# 🖼 Projeto de efeitos de imagem com OpenCV

Este projeto permite a aplicação de diferentes efeitos de imagem, como ajuste de brilho, saturação, contraste e desfoque, usando a biblioteca OpenCV. A interface gráfica foi desenvolvida com Tkinter, permitindo a interação simples e intuitiva com os ajustes.

---
## Funcionalidades:

### Brilho
O **brilho** ajusta a intensidade da luz em cada pixel da imagem. A faixa de ajuste vai de **-255 a +255**, onde:
- **0** significa nenhum ajuste de brilho (imagem original).
- **Valores negativos** escurecem a imagem, diminuindo a intensidade dos pixels.
- **Valores positivos** clareiam a imagem, aumentando a intensidade dos pixels.

### Saturação
A **saturação** controla a pureza das cores da imagem. A faixa de valores também vai de **0 a 255**, onde:
- **0** resulta em uma imagem em tons de cinza (sem saturação).
- **255** representa cores completamente saturadas, ou seja, cores mais vivas e intensas.

### Contraste
O **contraste** altera a diferença entre as partes mais claras e mais escuras da imagem. O contraste é ajustado usando um fator de multiplicação, onde:
- **1.0** (ou o valor padrão de 50 na interface) representa nenhum ajuste de contraste.
- **Valores maiores** aumentam a diferença entre os pixels claros e escuros, tornando a imagem visualmente mais dramática.
- **Valores menores** suavizam o contraste, resultando em uma imagem com menos distinção entre as sombras e as luzes.

### Desfoque (Blur)
O **desfoque** é aplicado usando a técnica de **GaussianBlur**, que suaviza a imagem aplicando uma média ponderada dos pixels em uma vizinhança. A intensidade do desfoque é controlada por um valor entre **0 a 20**:
- **0** significa sem desfoque (imagem original).
- **Valores maiores** resultam em um desfoque maior, suavizando as transições e criando um efeito de suavização na imagem.

---

## Interface Gráfica

A interface gráfica é construída com o Tkinter e exibe os seguintes elementos:

1. **Botões de Controle**:
   - **Upload de Imagem**: Carregar uma nova imagem para aplicar os efeitos.
   - **Reset**: Restaurar os valores dos controles para os padrões iniciais.
   - **Fechar**: Encerrar a aplicação.

2. **Trackbars (Sliders)**:
   - **Brilho**: Ajusta o brilho da imagem.
   - **Saturação**: Modifica a saturação das cores.
   - **Contraste**: Ajusta a diferença entre as áreas claras e escuras.
   - **Desfoque**: Aplica desfoque na imagem.

As trackbars permitem ajustar interativamente os parâmetros da imagem em tempo real.

3. **Área de Exibição de Imagem**:
   - A imagem carregada é exibida no centro da interface, com a possibilidade de aplicar os ajustes diretamente.

---

## ⚙ Instalação

### Pré-requisitos
Certifique-se de ter o Python 3.x instalado. Além disso, instale as dependências necessárias:

```bash
pip install opencv-python numpy pillow
```

### Como Executar
Clone este repositório e execute o script principal:

```bash
python main.py
```

---

## Explicação Técnica

A manipulação de imagem é feita principalmente usando a biblioteca **OpenCV**. A imagem é carregada em formato BGR (Blue, Green, Red) e, para ajustes como brilho e saturação, convertemos a imagem para o modelo de cor **HSV** (Hue, Saturation, Value). Isso nos permite manipular mais facilmente o brilho e a saturação separadamente, sem afetar a tonalidade da imagem.

- **Brilho**: É ajustado somando ou subtraindo um valor da componente **Value (V)** da imagem no espaço HSV. A função `np.clip` é usada para garantir que os valores resultantes fiquem dentro da faixa válida de 0 a 255.
  
- **Saturação**: Similar ao brilho, a saturação é ajustada modificando a componente **Saturation (S)** da imagem no espaço HSV, utilizando também a função `np.clip` para manter os valores válidos.

- **Contraste**: O contraste é ajustado multiplicando os valores dos pixels pela constante de contraste, que é aplicada na imagem depois da conversão para o espaço de cor RGB.

- **Desfoque**: A função `cv2.GaussianBlur` aplica um filtro de desfoque gaussiano à imagem, suavizando as transições entre os pixels.

Cada ajuste é aplicado individualmente, permitindo ao usuário ver o efeito em tempo real através da interface gráfica.
