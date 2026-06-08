import torch
import torch.nn as nn
from dataclasses import dataclass, field
from typing import Dict, Tuple

@dataclass
class EncoderConfig:
    """Configuração estruturada para parametrização do EventEncoder."""
    numeric_features: Tuple[str, ...] = ("amount",)
    categorical_cardinality: Dict[str, int] = field(
        default_factory=lambda: {"device": 4, "country": 6}
    )
    embed_dim: int = 64
    hidden_dim: int = 128


class EventEncoder(nn.Module):
    """Codificador heterogêneo idiomático para processamento de dados tabulares/eventos."""
    def __init__(self, config: EncoderConfig):
        super().__init__()
        self.config = config
        
        # Inicialização dinâmica das camadas de embedding para dados categóricos
        self.embeddings = nn.ModuleDict({
            feat: nn.Embedding(num_embeddings=cardinality, embedding_dim=config.embed_dim)
            for feat, cardinality in config.categorical_cardinality.items()
        })
        
        # Cálculo exato da dimensão interna de entrada pós-concatenação
        num_numeric_inputs = len(config.numeric_features)
        num_categorical_inputs = len(config.categorical_cardinality)
        total_input_dim = (num_categorical_inputs * config.embed_dim) + num_numeric_inputs
        
        # Rede de processamento (MLP) baseada em código limpo e acoplamento fraco
        self.mlp = nn.Sequential(
            nn.Linear(total_input_dim, config.hidden_dim),
            nn.ReLU(),
            nn.Linear(config.hidden_dim, config.hidden_dim)
        )
        
    def forward(self, batch: Dict[str, torch.Tensor]) -> torch.Tensor:
        """
        Executa o mapeamento e concatenação paralela das features.
        
        Args:
            batch: Dicionário contendo Tensores do PyTorch mapeados por nome de feature.
        """
        encoded_features = []
        
        # 1. Processamento e extração das representações latentes (Categorical)
        for feat in self.config.categorical_cardinality.keys():
            # batch[feat] deve conter tensores do tipo LongTensor (índices)
            embedded = self.embeddings[feat](batch[feat])
            encoded_features.append(embedded)
            
        # 2. Alinhamento dimensional das características numéricas
        for feat in self.config.numeric_features:
            numeric_tensor = batch[feat]
            # Garante que dados unidimensionais de batches possuam shape [Batch_Size, 1]
            if numeric_tensor.dim() == 1:
                numeric_tensor = numeric_tensor.unsqueeze(-1)
            encoded_features.append(numeric_tensor)
            
        # 3. Concatenação de todas as dimensões de características tratadas
        x = torch.cat(encoded_features, dim=-1)
        
        # 4. Projeção final via camadas lineares
        return self.mlp(x)


if __name__ == "__main__":
    # Teste unitário funcional para validação de integridade do shape
    configura_teste = EncoderConfig()
    modelo = EventEncoder(configura_teste)
    
    # Criação de um lote (batch) simulado contendo 3 instâncias de dados
    batch_simulado = {
        "device": torch.tensor([0, 2, 1], dtype=torch.long),
        "country": torch.tensor([5, 3, 0], dtype=torch.long),
        "amount": torch.tensor([150.50, 2300.00, 42.10], dtype=torch.float32)
    }
    
    saida = modelo(batch_simulado)
    print("Instanciação concluída com sucesso.")
    print(f"Shape de saída esperado do Batch: [3, {configura_teste.hidden_dim}]")
    print(f"Shape obtido de fato: {list(saida.shape)}")
