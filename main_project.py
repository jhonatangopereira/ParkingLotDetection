import cv2, json, numpy as np
import envio_dados
from ultralytics import solutions

def send_aplication():
    pass

def load_video():
    cap = cv2.VideoCapture("videos/video-teste.mp4")
    assert cap.isOpened(), "Erro ao ler o arquivo de vídeo"
    w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Codec compatível com MP4
    video_writer = cv2.VideoWriter("parking_management.mp4", fourcc, fps, (w, h))
    return cap, video_writer

def init_manager():
    """Inicializar o objeto de gerenciamento de estacionamento com o modelo"""
    parking_manager = solutions.ParkingManagement(
        model="model/yolov8n-obb.pt",
        json_file="bounding_boxes-2.json"
    )
    return parking_manager

def map_vacancies():
    with open("bounding_boxes-2.json", "r") as file:
        parking_spots = json.load(file)
    return [{"id": index + 1, "points": spot["points"], "occupied": False} for index, spot in enumerate(parking_spots)]

def analyze_parking_spots(frame, spots):
    status_list = []
    for spot in spots:
        points = np.array(spot["points"], dtype=np.int32)  # Pontos da região
        x, y, w, h = cv2.boundingRect(points)  # Calcula o retângulo delimitador
        roi = frame[y:y + h, x:x + w]  # Recorta a região de interesse (ROI)

        # Calcula a cor média na região
        mean_color = cv2.mean(roi)[:3]  # Ignora o canal alpha
        if mean_color[1] > mean_color[2]:  # Verde > Vermelho
            spot["occupied"] = False
        else:
            spot["occupied"] = True

        # Adiciona o status da vaga à lista
        status_list.append({
            "id": spot["id"],
            "occupied": spot["occupied"]
        })
    return status_list

def save_status_to_file(status_list, frame_count):
    with open("parking_status.json", "a") as file:
        frame_status = {
            "frame": frame_count,
            "status": status_list
        }
        json.dump(frame_status, file)
        file.write("\n")  # Adiciona uma nova linha para cada frame
        return frame_status

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
    processed_data = ""
    while cap.isOpened():
        ret, im0 = cap.read()

        if not ret:
            break
        frame_count += 1

        if frame_count % 2 == 0:  # Exibe e grava a cada 10 frames
            processed_data = parking_manager.process_data(im0)
            status_list = analyze_parking_spots(processed_data, map_parking)
            status_json = save_status_to_file(status_list, frame_count)
            video_writer.write(processed_data)
            #enviar_dados(status_json, frame_count)
            cv2.imshow("Estacionamento Processado", processed_data)



        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar os recursos de captura e gravação de vídeo
    cap.release()
    video_writer.release()
    cv2.destroyAllWindows()  # Fecha todas as janelas abertas pelo OpenCV

if __name__ == '__main__':
    main()