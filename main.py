import cv2, json, numpy as np
from ultralytics import solutions

def send_aplication():
    pass

def load_video():
    cap = cv2.VideoCapture("videos/video-teste.mp4")
    assert cap.isOpened(), "Erro ao ler o arquivo de vídeo"
    # Obter propriedades do vídeo
    w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
    video_writer = cv2.VideoWriter("data/parking_management.avi", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
    return cap, video_writer

def init_manager():
    # Inicializar o objeto de gerenciamento de estacionamento com o modelo
    parking_manager = solutions.ParkingManagement(
        model="model/yolo11x-obb.pt",  # Caminho para o modelo YOLO
        json_file="bounding_boxes.json"  # Caminho para o arquivo JSON com as regiões de interesse
    )
    return parking_manager

def map_vacancies():
    # Carrega o arquivo JSON
    with open("bounding_boxes.json", "r") as file:
        parking_spots = json.load(file)

    mapped_spots = []

    for index, points in enumerate(parking_spots, start=1):
        print("Vaga {} : Pontos {}".format(index, points))
        mapped_spots.append({"id": index, "points": points["points"], "occupied": False})

    return mapped_spots

def main():
    # Comando para selecionar pontos
    solutions.ParkingPtsSelection()

    # Carregar vídeo
    cap , video_writer = load_video()

    # Inicializar o objeto de gerenciamento de estacionamento com o modelo
    parking_manager = init_manager()

    #mapear as vagas
    map_parking = map_vacancies()

    frame_count = 0
    while cap.isOpened():
        ret, im0 = cap.read()

        if not ret:
            break
        frame_count += 1
        if frame_count % 5 == 0:  # Exibe e grava a cada 10 frames
            processed_data = parking_manager.process_data(im0)
            cv2.imshow("Estacionamento Processado", processed_data)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar os recursos de captura e gravação de vídeo
    cap.release()
    video_writer.release()
    cv2.destroyAllWindows()  # Fecha todas as janelas abertas pelo OpenCV

if __name__ == '__main__':
    main()