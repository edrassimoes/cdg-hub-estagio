# 🖼 Editor de Imagem com OpenCV

Este repositório contém um código Python que permite ajustar a **imagem** em tempo real utilizando a biblioteca **OpenCV**. O código permite modificar os parâmetros de brilho, saturação, contraste e desfoque de uma imagem carregada, com a interação do usuário por meio de **trackbars**.

## Funcionalidades

- **Brilho**: Ajuste do brilho da imagem.
- **Saturação**: Controle da saturação das cores.
- **Contraste**: Modificação do contraste da imagem.
- **Desfoque**: Aplicação de desfoque gaussiano (blur) na imagem.

Essas funcionalidades são aplicadas em tempo real, e a imagem é atualizada conforme o usuário interage com os controles.

## Requisitos

- Python 3
- OpenCV (`opencv-python`)
- NumPy (`numpy`)

### Instalação dos requisitos:

```bash
pip install opencv-python numpy
```

## Como Usar

1. Clone o repositório:

    ```bash
    git clone https://github.com/seu-usuario/nome-do-repositorio.git
    cd nome-do-repositorio
    ```

2. Execute o código Python:

    ```bash
    python editor_imagem.py
    ```

3. O código irá abrir uma janela onde você pode ajustar os parâmetros usando as **trackbars** (barras deslizantes):
   - **Brilho**: Ajuste o brilho da imagem.
   - **Saturação**: Aumente ou diminua a saturação das cores.
   - **Contraste**: Modifique o contraste da imagem.
   - **Desfoque**: Aplique desfoque (blur) na imagem.

4. Pressione a tecla `q` para sair do editor.

### Exemplo de Saída

O editor de imagem permite visualizar a alteração em tempo real. A seguir, a interface mostra uma imagem original e os efeitos aplicados após ajustar os controles deslizantes.

## 🗂 Código

O código principal é dividido em duas funções principais:

- **ajustar_imagem**: Aplica as alterações de brilho, saturação, contraste e desfoque na imagem.
- **on_change**: Função callback chamada sempre que o usuário altera os controles deslizantes.

### Exemplo de código:

```python
import cv2
import numpy as np

def ajustar_imagem(img, brilho, saturacao, contraste, blur):
    """
    Ajusta os parâmetros de brilho, saturação, contraste e desfoque de uma imagem.
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
    """
    brilho = cv2.getTrackbarPos("Brilho", "Editor") - 100
    saturacao = cv2.getTrackbarPos("Saturacao", "Editor") - 100
    contraste = cv2.getTrackbarPos("Contraste", "Editor") / 50.0
    blur = cv2.getTrackbarPos("Desfoque", "Editor")

    img_ajustada = ajustar_imagem(img_original, brilho, saturacao, contraste, blur)
    cv2.imshow("Editor", img_ajustada)
```
