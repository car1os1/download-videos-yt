from pydrive.auth import GoogleAuth
import pandas as pd
from pytube import YouTube
from pydrive.drive import GoogleDrive


# URL
file_url = 'https://docs.google.com/spreadsheets/d/1n1aIZCd2oukqUKn1GwGYaCwnvzlecR_Hill0KYN6YdQ/export?format=csv'

directorio_credenciales= "credentials_module.json"
id_folder = '1btybpaOtx2t3lwo9hLN0H1cKVM-QLRwQ'


def login(): 
    GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = directorio_credenciales
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(directorio_credenciales)

    if gauth.credentials is None:
        gauth.LocalWebserverAuth(port_numbers=[8092])
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()

    gauth.SaveCredentialsFile(directorio_credenciales)
    return gauth  # Devuelve el objeto gauth
# ...

# ...

def subir_archivo(video, id_folder): 
    credenciales = login()  
    drive = GoogleDrive(credenciales)  
    
    # Obtén el título del video sin caracteres no permitidos en nombres de archivo
    video_title = video.title.replace('/', '_').replace('\\', '_').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')
    
    # Genera la ruta del archivo con el título corregido
    archivo_title = f'YT/{video_title}.mp4'
    
    archivo = drive.CreateFile({'parents': [{"kind": "drive#fileLink", "id": id_folder}]})
    archivo['title'] = archivo_title
    
    # Obtén el nombre del archivo descargado
    archivo_descargado = f'./YT/{video_title}.mp4'
    
    # Imprime la ruta completa del archivo descargado antes de intentar abrirlo
    print(f'Ruta del archivo descargado: {archivo_descargado}')
    
    archivo.SetContentFile(archivo_descargado)
    archivo.Upload()




def main():
    # Leer los datos de la hoja 
    df = pd.read_csv(file_url)

    # Acceder a los datos de la columna 'videos'
    videos_yt = df['videos']
    videos = videos_yt.values

    # para descargar el video
    for link_video in videos: 
        yt = YouTube(link_video)
        video = yt.streams.get_highest_resolution()
        video.download('./YT')

        subir_archivo(yt, id_folder)  # Cambia 'video' por 'yt'

    print(videos)


if __name__ == "__main__":
    main()
