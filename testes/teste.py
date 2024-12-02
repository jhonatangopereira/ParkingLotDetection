import cv2
from ultralytics import solutions

# Comando para selecionar pontos
solutions.ParkingPtsSelection()

# Captura de vídeo
cap = cv2.VideoCapture("videos/video-teste.mp4")
assert cap.isOpened(), "Erro ao ler o arquivo de vídeo"
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

# Inicialização do gravador de vídeo
video_writer = cv2.VideoWriter("data/parking_management.avi", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

# Inicialização do objeto de gerenciamento de estacionamento com o modelo
parking_manager = solutions.ParkingManagement(
    model="model/yolo11x-obb.pt",  # Caminho para o seu modelo YOLO
    json_file="bounding_boxes-2.json"  # Caminho para o arquivo JSON com as regiões de interesse (vagas)
)

while cap.isOpened():
    ret, im0 = cap.read()
    if not ret:
        break  # Se não houver mais frames, encerre o loop

    # Processar o frame com o modelo de gerenciamento de estacionamento
    im0 = parking_manager.process_data(im0)

    # Exibir o frame processado na janela
    cv2.imshow("Estacionamento Processado", im0)

    # Escrever o frame processado no arquivo de saída
    #video_writer.write(im0)

    # Aguardar 1 ms e verificar se a tecla 'q' foi pressionada para encerrar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break  # Encerra o loop se a tecla 'q' for pressionada

# Liberar os recursos de captura e gravação de vídeo
cap.release()
video_writer.release()
cv2.destroyAllWindows()  # Fecha todas as janelas abertas pelo OpenCV
