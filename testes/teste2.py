import cv2
from ultralytics import solutions

# Comando para selecionar pontos
solutions.ParkingPtsSelection()

# Carregar vídeo
cap = cv2.VideoCapture("videos/video-teste.mp4")
assert cap.isOpened(), "Erro ao ler o arquivo de vídeo"

# Obter propriedades do vídeo
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))


# Inicializar o objeto de gerenciamento de estacionamento com o modelo
parking_manager = solutions.ParkingManagement(
    model="yolo11x-obb.pt",  # Caminho para o modelo YOLO
    json_file="bounding_boxes-2.json"  # Caminho para o arquivo JSON com as regiões de interesse
)

frame_count = 0
while cap.isOpened():
    ret, im0 = cap.read()
    if not ret:
        break
    frame_count += 1
    if frame_count % 5 == 0:  # Exibe e grava a cada 10 frames
        im0 = parking_manager.process_data(im0)
        #video_writer.write(im0)
        cv2.imshow("Estacionamento Processado", im0)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# Liberar os recursos de captura e gravação de vídeo
cap.release()
#video_writer.release()
cv2.destroyAllWindows()  # Fecha todas as janelas abertas pelo OpenCV