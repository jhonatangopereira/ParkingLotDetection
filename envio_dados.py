
import requests

def enviar_dados(frame_status, frame_count):
    try:
        url = ""  #
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer seu_token_aqui"  # Remova ou modifique conforme necessário
        }

        response = requests.post(url, json=frame_status, headers=headers)

        if response.status_code == 200:
            print("Frame {} enviado com sucesso!".format(frame_count))
        else:
            print("Erro ao enviar Frame {}: {}".format(frame_count, response.status_code))
            print("Mensagem de erro:", response.text)

    except requests.exceptions.RequestException as e:
        print("Erro de conexão ao enviar Frame {}: {}".format(frame_count, e))


