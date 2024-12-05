# 🖼 Projeto de Efeitos de Imagem

Este projeto permite a aplicação de diferentes efeitos de imagem, como ajuste de brilho, saturação, contraste e desfoque, usando a biblioteca OpenCV. A interface gráfica foi desenvolvida com Tkinter, permitindo a interação simples e intuitiva com os ajustes.

---
## Como funciona?
As imagens digitais, como as que manipuladas com o OpenCV, seguem geralmente o modelo RGB (Red, Green, Blue - Vermelho, Verde, Azul), onde cada pixel da imagem é composto por uma combinação desses três canais de cor e cada um destes canais é representado por 8 bits.

Outro modelo muito utilizado para processamento de imagens é o HSV (Hue, Saturation, Value - Matiz, Saturação, Brilho). Nesse modelo, as cores são representadas de forma diferente:

- Matiz define a tonalidade da cor (como vermelho, azul ou verde) e é medido em graus.
- Saturação controla a intensidade ou vivacidade da cor e é definida por 8 bits.
- Brilho ajusta a luminosidade da cor e é definido por 8 bits.

**Afinal, o que são os 8 bits?**

Um bit é a unidade mais simples de informação em computação e pode assumir dois valores: 0 ou 1. Quando usamos 8 bits para representar a intensidade de uma cor ou um canal de uma imagem, estamos trabalhando com uma combinação de bits.

Para calcular o número total de resultados possíveis, usamos a fórmula:

$$2^8 = 256$$


Isso ocorre porque, para cada um dos 8 bits, existem 2 opções possíveis (0 ou 1). Esses 256 valores podem ser usados para representar a intensidade de um canal de cor em uma imagem, como discutimos acima. Por exemplo:

- No modelo RGB:
   - 0 representa a ausência total de cor (preto absoluto).
   - 255 representa a intensidade máxima da cor, seu ponto mais brilhante.


- No modelo HSV:
  - Para a saturação, 0 significa que a cor é completamente desbotada (tons de cinza), enquanto 255 significa uma cor extremamente vibrante.
  - Para o brilho, 0 significa ausência de luz (preto absoluto), enquanto 255 é a intensidade máxima da luz para a cor atual.

**🎨 E quantas cores temos?**

No modelo RGB, por exemplo, cada pixel é reprentado por 24 bits, onde:
- 8 bits para o canal vermelho (0 a 255),
- 8 bits para o canal verde (0 a 255),
- 8 bits para o canal azul (0 a 255).

Com isso, cada pixel pode representar mais de 16 milhões de combinações de cores diferentes.

---

## Interface Gráfica

A interface gráfica é construída com o Tkinter e exibe os seguintes elementos:

1. **Botões de Controle**:
   - **Upload de Imagem**: Carregar uma nova imagem para aplicar os efeitos.
   - **Reset**: Restaurar os valores dos controles para os padrões iniciais.
   - **Fechar**: Encerrar a aplicação.

2. **Trackbars (Sliders)**:
   - **Brilho**: Modifica a luminosidade da imagem, clareando ou escurecendo as áreas.
   - **Saturação**: Controla a intensidade das cores, ou seja, quão "vivas" ou "cinzas" elas aparecem.
   - **Contraste**: Altera a diferença entre as partes mais claras e mais escuras da imagem.
   - **Desfoque**: Suaviza as transições entre os pixels, reduzindo o nível de detalhe.

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
