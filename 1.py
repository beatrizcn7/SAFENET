# ----------------- Bibliotecas ---------------
# Importar a principal biblioteca de Machine Learning e Deep Learning.
# Criar, treinar e implementar modelos de redes neurais.
import tensorflow as tf
# Importar a API de alto nível que facilita a construção e treino de redes neurais dentro do TensorFlow
from tensorflow.keras import layers, models
# Importar a biblioteca para contar o tempo
import time

# --------------------- Modelo ------------------
# Carregar o modelo salvo para a propriedade "Material + Ano"
base_model = tf.keras.models.load_model(
    'Modelos/ResNet/Tentativa 1 - Material + Estrutura (Com Tentativa 1 - Material).h5')

# Remover a última camada do modelo base
base_model = models.Model(inputs=base_model.input, outputs=base_model.layers[-2].output)

# Congelar as camadas do modelo base
for layer in base_model.layers:
    layer.trainable = False

# Usar a entrada existente do modelo base
inputs = base_model.input  # Usar diretamente a entrada do modelo base
x = base_model.output      # Obter a saída da penúltima camada do modelo base

# Criar uma camada densa com 11 classes (saída da classificação) e função de ativação softmax
outputs = layers.Dense(11, activation='softmax')(x)

# Criar o modelo final
model = models.Model(inputs=inputs, outputs=outputs)

# Compilar o modelo com o otimizador, função de perda e métricas
model.compile(optimizer=tf.keras.optimizers.Adam(),
              loss=tf.keras.losses.SparseCategoricalCrossentropy(),
              metrics=['accuracy'])

# Função para carregar e processar os dados dos ficheiros TFRecord
def parse_tfrecord(example):
    # Definir o formato dos dados no TFRecord
    feature_description = {
        'image/encoded': tf.io.FixedLenFeature([], tf.string),
        'image/object/class/label': tf.io.FixedLenFeature([], tf.int64),
    }
    return tf.io.parse_single_example(example, feature_description)

# Função para carregar o dataset a partir de vários ficheiros TFRecord
def load_dataset(file_paths):
    # Criar um dataset a partir de múltiplos arquivos TFRecord
    raw_dataset = tf.data.TFRecordDataset(file_paths)
    return raw_dataset.map(parse_tfrecord).map(
        lambda x: (
            tf.image.resize(tf.image.decode_jpeg(x['image/encoded'], channels=3), [224, 224]),
            x['image/object/class/label']
        )
    )

# Pastas dos ficheiros TFRecords (Treino e Teste)
train_tfrecords = tf.io.gfile.glob('Pasta Final TFRecord - Material + Ano + Estrutura/Treino/*.tfrecord')
val_tfrecords = tf.io.gfile.glob('Pasta Final TFRecord - Material + Ano + Estrutura/Validação/*.tfrecord')

# Carregar os ficheiros TFRecords
train_dataset = load_dataset(train_tfrecords).batch(32).prefetch(tf.data.AUTOTUNE)
val_dataset = load_dataset(val_tfrecords).batch(32).prefetch(tf.data.AUTOTUNE)

# Início da contagem de tempo
start_time = time.time()

# Treinar o modelo
history = model.fit(
    train_dataset,
    validation_data=val_dataset,
    epochs=10
)

# Carregar o conjunto de teste
test_tfrecords = tf.io.gfile.glob('Pasta Final TFRecord - Material + Ano + Estrutura/Teste/*.tfrecord')
test_dataset = load_dataset(test_tfrecords).batch(32).prefetch(tf.data.AUTOTUNE)

# Avaliar o modelo no conjunto de teste
test_loss, test_accuracy = model.evaluate(test_dataset)

end_time = time.time()  # Fim
total_time = (end_time - start_time) / 60  # Converter para minutos

# Imprimir o tempo total
print(f"Tempo total: {total_time:.2f} minutos")

# Imprime os resultados da perda e da exatidão dos dados teste
print(f'Teste Loss: {test_loss}')
print(f'Teste Accuracy: {test_accuracy}')