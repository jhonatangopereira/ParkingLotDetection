import cv2

# Abrir o arquivo de vídeo
cap = cv2.VideoCapture("videos/video-teste.mp4")
assert cap.isOpened(), "Erro ao abrir o arquivo de vídeo"

# Obter o FPS (frames por segundo) do vídeo
fps = cap.get(cv2.CAP_PROP_FPS)

# Definir o tempo de delay em segundos (por exemplo, 1 segundo)
delay_in_seconds = 1

# Calcular o número de frames para esperar (delay em segundos * FPS)
frame_to_capture = int(fps * delay_in_seconds)

# Mover para o frame desejado
cap.set(cv2.CAP_PROP_POS_FRAMES, frame_to_capture)

# Capturar o frame após o delay
ret, frame = cap.read()
if not ret:
    print("Erro ao capturar o frame")
else:
    # Salvar o frame como uma imagem
    cv2.imwrite("frame_", frame)

# Liberar o vídeo
cap.release()
