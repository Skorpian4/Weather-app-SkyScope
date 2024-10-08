import customtkinter as ctk
from PIL import Image
import requests
import geocoder

ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("dark-blue")  

# Criando a janela
janela = ctk.CTk()
janela.geometry('600x400')
janela.resizable(False,False)
janela.title('Weather App')

#Personaliza tamanho texto
custom_font = ("Arial", 30, 'bold')
custom_font2 = ("Arial", 20, 'bold')
custom_def = ("Arial", 15, 'bold')

# Função para limpar a janela
def limpar_janela():
    for widget in janela.winfo_children():
        widget.destroy()

def clique():
    limpar_janela() #limpa janela

    image2 = ctk.CTkImage(light_image=Image.open('images/capa.png'),
                     dark_image=Image.open('images/capa.png'), #coloca a imagem
                     size=(250, 250))
    
    frame = ctk.CTkFrame(janela,width=300, height=400, fg_color='#232323')
    frame.pack(side='right')

    image_label = ctk.CTkLabel(janela, image=image2, text="")
    image_label.place(x=20, y=60)
        
    janela_label = ctk.CTkLabel(janela, text='Escolha uma opção', fg_color='#232323',font=custom_font2)
    janela_label.place(x=380, y=20)

    #botão para procurar temperatura por cidade
    janela_btn = ctk.CTkButton(janela, text='Procurar por cidade', corner_radius=20, command=procurarcidade, width=200, height=40, hover_color='#1F77B4', text_color='white', bg_color='#232323')
    janela_btn.place(x=380, y=80)

    #botão para procurar temperatura por país
    janela_btn1 = ctk.CTkButton(janela, text='Previsão 5 dias', corner_radius=20, command=Previsão5dias, width=200, height=40, hover_color='#1F77B4', text_color='white', bg_color='#232323')
    janela_btn1.place(x=380, y=140)

    #botão para procurar temperatura por localização atual
    janela_btn2 = ctk.CTkButton(janela, text='Localização atual', corner_radius=20,command=localizacaoatual, width=200, height=40, hover_color='#1F77B4', text_color='white', bg_color='#232323')
    janela_btn2.place(x=380, y=200)

def procurarcidade():
    global result_label
    limpar_janela()

    # Entrada da informação da cidade
    infocidade = ctk.CTkEntry(janela, placeholder_text='Cidade', font=custom_font2, width=200, height=50)
    infocidade.pack(pady=10)

    result_label = ctk.CTkLabel(janela, text='')
    result_label.pack(pady=20)

    def gettempo():
        cidade = infocidade.get()  # Recebe nome da cidade
        if cidade:  # Verifica se a cidade foi inserida
            Api_key = '344ca4445c87003f84ffbe7f96e79a30'
            url = f'https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={Api_key}&lang=pt'
            res = requests.get(url)


            if res.status_code == 200:  # Verifica se a requisição foi bem-sucedida
                weather = res.json()
                temperature = weather['main']['temp'] - 273.15
                description = weather['weather'][0]['description']
                city = weather['name']
                country = weather['sys']['country']

                result_label.configure(text=f'Temperatura: {temperature:.2f}°C\n'
                                                f'Descrição: {description}\n'
                                                f'Cidade: {city}, {country}',
                                           text_color='white', font=custom_font2)
            else:
                result_label.configure(janela, text='Cidade não encontrada!', font=custom_font2, text_color='white')

    # Botão para buscar o tempo
    search_btn = ctk.CTkButton(janela, text='Procurar Tempo', font=custom_font2, command= gettempo,text_color='white', corner_radius=20, width=200, height=40)
    search_btn.pack(pady=10)

    back_btn = ctk.CTkButton(janela, text='Voltar', font=custom_font2, command= clique,text_color='white', corner_radius=20, width=200, height=40)
    back_btn.pack(pady=10)

def Previsão5dias():
    limpar_janela()#limpa janela

    infocidade = ctk.CTkEntry(janela, placeholder_text='Cidade', font=custom_font2, width=200, height=50)
    infocidade.pack(pady=10)

    infopaiscodigo = ctk.CTkEntry(janela, placeholder_text='Codigo Pais', font=custom_font2, width=200, height=50)
    infopaiscodigo.pack(pady=10)

    result_label = ctk.CTkLabel(janela, text='')
    result_label.pack(pady=20)
    
    def getprevisao():
        cidade = infocidade.get()  # Recebe nome da cidade
        paiscodigo = infopaiscodigo.get()  # Recebe código do país (Exemplo: PT para Portugal)
        
        if cidade and paiscodigo:  # Verifica se ambos os campos foram preenchidos
            Api_key = '344ca4445c87003f84ffbe7f96e79a30'
            url = f'https://api.openweathermap.org/data/2.5/forecast?q={cidade},{paiscodigo}&appid={Api_key}&lang=pt'
            res = requests.get(url)

            if res.status_code == 200:  # Verifica se a requisição foi bem-sucedida
                weather = res.json()
                forecast_info = []

                for i in range(0, 40, 8):  # Pega uma previsão a cada 24 horas 
                    temp = weather['list'][i]['main']['temp'] - 273.15  # Converte para Celsius
                    description = weather['list'][i]['weather'][0]['description']
                    date_time = weather['list'][i]['dt_txt']  # Data e hora da previsão

                    # Adiciona as informações da previsão formatadas
                    forecast_info.append(f'{date_time}\nTemperatura: {temp:.2f}°C\nDescrição: {description}\n')

                # Atualiza o label com as previsões
                limpar_janela()
                # Criar o CTkTextbox com barra de rolagem
                result_textbox = ctk.CTkTextbox(janela, wrap="word", font=custom_font2, width=200, height=200)
                result_textbox.pack(expand=True, fill="both", padx=10, pady=20)

                # Inserir o texto da previsão no CTkTextbox
                result_textbox.insert("0.0", '\n\n'.join(forecast_info))

                # Desabilitar a edição para tornar o CTkTextbox somente leitura
                result_textbox.configure(state="disabled")

                # Botão para buscar o tempo
                search_btn = ctk.CTkButton(janela, text='Procurar por outra Cidade', font=custom_font2,command=getprevisao, text_color='white', corner_radius=20, width=200, height=40)
                search_btn.pack(pady=10)  

                back_btn = ctk.CTkButton(janela, text='Voltar', font=custom_font2, command= clique,text_color='white', corner_radius=20, width=200, height=40)
                back_btn.pack(pady=10)
            else:
                result_label.configure(text='Cidade não encontrada!',text_color='white', font=custom_font2)

    # Botão para buscar o tempo
    search_btn = ctk.CTkButton(janela, text='Procurar Tempo', font=custom_font2,command=getprevisao, text_color='white', corner_radius=20, width=200, height=40)
    search_btn.pack(pady=10)  

    back_btn = ctk.CTkButton(janela, text='Voltar', font=custom_font2, command= clique,text_color='white', corner_radius=20, width=200, height=40)
    back_btn.pack(pady=10)

def localizacaoatual():
    limpar_janela()

    result_label = ctk.CTkLabel(janela, text='')
    result_label.pack(pady=20)

    def get_location():
        g = geocoder.ip('me')
        if g.ok:
            return g.latlng  # Retorna latitude e longitude
        else:
            return None

    location = get_location()
    if location:
        print(f'Sua localização aproximada: Latitude {location[0]}, Longitude {location[1]}')
    else:
        print('Não foi possível obter sua localização.')

    def get_weather(lat, lon, api_key):
        url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=pt'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return None

    Api_key = '344ca4445c87003f84ffbe7f96e79a30' #chave

    if location:
        weather_data = get_weather(location[0], location[1], Api_key)
        if weather_data:
            result_label.configure(text= f"Clima atual em {weather_data['name']}: {weather_data['weather'][0]['description'].capitalize()} \n Temperatura: {weather_data['main']['temp']}°C", text_color='white', font=custom_font2)
        else:
            result_label.configure('Não foi possível obter as informações do clima.')
    else:
        result_label.configure('Não foi possível obter sua localização.')

    back_btn = ctk.CTkButton(janela, text='Voltar', font=custom_font2, command= clique,text_color='white', corner_radius=20, width=200, height=40)
    back_btn.pack(pady=10)
#inicio programa
clique()

janela.mainloop()