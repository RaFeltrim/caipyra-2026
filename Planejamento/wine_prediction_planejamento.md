# Planejamento de Melhoria - wine_prediction

## 📦 Nome do Projeto
**`wine_prediction`** (Wine Quality & Characteristic Predictor)

---

## 🔍 O Que o Projeto Faz
É um repositório voltado para modelagem de Machine Learning com o objetivo de classificar ou prever a qualidade de vinhos com base em características físico-químicas (como pH, acidez, teor alcoólico, sulfatos, etc.), comumente baseado no clássico dataset Wine Quality.

---

## 🛠️ Como Melhorá-lo
Podemos migrar este projeto de um script tradicional/sequencial para uma arquitetura moderna e escalável de Inteligência Artificial usando os conceitos do Caipyra 2026:

### 1. Dask para Processamento e AutoML Paralelo
* **Dask DataFrames**: Substituir o uso do Pandas por **Dask DataFrames** (`dask.dataframe`) para ler, limpar e pré-processar os dados físico-químicos. Isso prepara o projeto para lidar com conjuntos de dados massivos de vinícolas que excedem a memória RAM local.
* **Hiperparametrização Distribuída**: Utilizar a integração do Dask com Scikit-Learn (`dask_ml.model_selection.GridSearchCV`) para treinar e buscar hiperparâmetros de múltiplos modelos preditivos de forma concorrente em todos os núcleos de CPU disponíveis, reduzindo drasticamente o tempo de otimização dos classificadores.

### 2. Rede Neural com PyTorch & Loop de Treino Fluente
* **Modelagem de Deep Learning**: Substituir ou complementar os modelos clássicos de ML (como Decision Trees) por uma rede neural profunda (Multi-Layer Perceptron) implementada de forma nativa no **PyTorch**.
* **Clean Code & Modularização**:
  * Criar um arquivo `dataset.py` contendo uma classe customizada `WineDataset` herdando de `torch.utils.data.Dataset`, responsável pela normalização dos dados (z-score) e divisão estruturada.
  * Estruturar o `model.py` com uma classe `WineClassifier` estendendo `nn.Module` de forma limpa, com camadas lineares, ativações ReLU, Batch Normalization e Dropout para evitar overfitting.
  * Separar rigorosamente a lógica em módulos específicos: `train.py` (loop de treinamento), `eval.py` (validação e cálculo de métricas) e `main.py` (ponto de entrada). Evitar notebooks `.ipynb` monolíticos, conforme sugerido pelo palestrante Moacir Antonelli Ponti.
* **Garantia de Reprodutibilidade**: Adicionar uma função robusta para fixar as sementes randômicas (`torch.manual_seed()`, `np.random.seed()`, etc.) para assegurar que as métricas obtidas sejam replicáveis em qualquer ambiente.

---

## 🚀 Por Que Melhorá-lo
* **Alinhamento com PDI**: O projeto serve como a vitrine perfeita de **Redes Neurais com PyTorch** e **Computação Paralela com Dask**, duas habilidades essenciais para demonstrar capacidade avançada de Engenharia de Dados em larga escala (visando a transição para o Azure Data Engineering Team) e para os requisitos acadêmicos rigorosos do ICMC-USP em processamento distribuído.
* **Demonstração de Portfólio**: Transforma um repositório com lógica clássica de iniciante em ciência de dados em um exemplo de alto nível de engenharia de MLOps com paralelização e modularização limpa de código de produção.
