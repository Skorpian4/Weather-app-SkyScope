import customtkinter as ctk
from PIL import Image, ImageTk
import requests
import json
import geocoder
import tkinter as tk
import os

cidade = ""
pais = ""
termo = ""
favoritos = []
listbox = None 
city_frame = None 

with open('translations.json', 'r', encoding='utf-8') as f:
    translations = json.load(f)

png_icons = {
    "home": "images/home_icon.png",
    "clock": "images/clock_icon.png",
    "favorite": "images/favorite_icon.png",
    "settings": "images/settings_icon.png",
    "lupa": "images/lupa_icon.png",
    "notfound": "images/not_found_icon.png",
    "darklupa": "images/dark_lupa.png",
    "darkhome": "images/dark_home.png",
    "darksettings": "images/dark_settings.png",
    "darkclock": "images/dark_clock.png",
    "darkfavorite": "images/dark_favorite.png"
}

current_translation = translations["translations"]["pt"]  # Idioma padrão

def load_favorites():
    global favoritos
    try:
        if os.path.exists('favorites.json'):
            with open('favorites.json', 'r', encoding='utf-8') as f:
                favoritos = json.load(f)
        else:
            favoritos = []
    except Exception as e:
        print(f"Erro ao carregar favoritos: {e}")
        favoritos = []

def save_favorites():
    try:
        with open('favorites.json', 'w', encoding='utf-8') as f:
            json.dump(favoritos, f, ensure_ascii=False)
    except Exception as e:
        print(f"Erro ao salvar favoritos: {e}")

def add_to_favorites():
    global favoritos, cidade, pais
    
    cidade_input = infocidade.get().strip() if 'infocidade' in globals() and infocidade.winfo_exists() else ""
    
    if cidade_input:
        partes = cidade_input.split(",")
        cidade_to_add = partes[0].strip()
        pais_to_add = partes[-1].strip() if len(partes) > 1 else ""
    else:
        cidade_to_add = cidade
        pais_to_add = pais
    
    if not cidade_to_add:
        messagebox = ctk.CTkToplevel(root)
        messagebox.title(current_translation[0].get("error", "Error"))
        messagebox.geometry("300x150")
        messagebox.resizable(False, False)
        messagebox.transient(root)
        messagebox.grab_set()
        
        x = root.winfo_x() + (root.winfo_width() / 2) - (300 / 2)
        y = root.winfo_y() + (root.winfo_height() / 2) - (150 / 2)
        messagebox.geometry(f"+{int(x)}+{int(y)}")
        
        label = ctk.CTkLabel(
            messagebox, 
            text=current_translation[0].get("no_city_selected", "No city selected"),
            font=("Arial", 16)
        )
        label.pack(pady=30)
        
        ok_button = ctk.CTkButton(
            messagebox, 
            text="OK",
            command=messagebox.destroy,
            width=100
        )
        ok_button.pack(pady=10)
        return
    
    favorite = {
        "city": cidade_to_add,
        "country": pais_to_add
    }
    
    if not any(fav["city"] == cidade_to_add and fav["country"] == pais_to_add for fav in favoritos):
        favoritos.append(favorite)
        save_favorites()
        
        messagebox = ctk.CTkToplevel(root)
        messagebox.title(current_translation[0].get("success", "Success"))
        messagebox.geometry("300x150")
        messagebox.resizable(False, False)
        messagebox.transient(root)
        messagebox.grab_set()
        
        x = root.winfo_x() + (root.winfo_width() / 2) - (300 / 2)
        y = root.winfo_y() + (root.winfo_height() / 2) - (150 / 2)
        messagebox.geometry(f"+{int(x)}+{int(y)}")
        
        label = ctk.CTkLabel(
            messagebox, 
            text=current_translation[0].get("favorite_added", "City added to favorites"),
            font=("Arial", 16)
        )
        label.pack(pady=30)
        
        ok_button = ctk.CTkButton(
            messagebox, 
            text="OK",
            command=messagebox.destroy,
            width=100
        )
        ok_button.pack(pady=10)
        
        if 'setlabel' in globals() and setlabel.winfo_exists():
            current_screen = setlabel.cget("text")
            if current_screen == current_translation[0].get("favorites", "Favorites"):
                show_favorites()
    else:
        messagebox = ctk.CTkToplevel(root)
        messagebox.title(current_translation[0].get("info", "Information"))
        messagebox.geometry("300x150")
        messagebox.resizable(False, False)
        messagebox.transient(root)
        messagebox.grab_set()
        
        x = root.winfo_x() + (root.winfo_width() / 2) - (300 / 2)
        y = root.winfo_y() + (root.winfo_height() / 2) - (150 / 2)
        messagebox.geometry(f"+{int(x)}+{int(y)}")
        
        label = ctk.CTkLabel(
            messagebox, 
            text=current_translation[0].get("already_favorite", "This city is already in favorites"),
            font=("Arial", 16)
        )
        label.pack(pady=30)
        
        ok_button = ctk.CTkButton(
            messagebox, 
            text="OK",
            command=messagebox.destroy,
            width=100
        )
        ok_button.pack(pady=10)

def remove_from_favorites(index):
    global favoritos
    
    if 0 <= index < len(favoritos):
        del favoritos[index]
        save_favorites()
        show_favorites()  

def show_favorites():
    global result_frame
    
    limpar_janela()
    menu()
    
    if modo_var.get() == 1: 
        root.configure(fg_color="#E6E6E6")
        setlabel.configure(
            text=current_translation[0].get("favorites", "Favorites"),
            fg_color='#A4A4A4',
            bg_color='#A4A4A4',
            text_color='black' 
        )
    else:  # Dark mode
        root.configure(fg_color="#5882FA")
        setlabel.configure(
            text=current_translation[0].get("favorites", "Favorites"),
            fg_color='#000000',
            bg_color='#000000',
            text_color='white' 
        )
    
    if 'favoritos' not in globals():
        load_favorites()
    
    result_frame = ctk.CTkFrame(
        root, 
        fg_color='#D8D8D8' if modo_var.get() == 1 else '#2E64FE', 
        width=600, 
        height=280
    )
    result_frame.place(x=110, y=80)
    
    favorites_title = ctk.CTkLabel(
        result_frame, 
        text=current_translation[0].get("favorites_list", "Favorite Locations"),
        font=("Arial", 22, "bold"),
        text_color='black' if modo_var.get() == 1 else 'white'
    )
    favorites_title.place(x=20, y=10)
    
    # Add button to add current location to favorites
    add_button = ctk.CTkButton(
        result_frame,
        text=current_translation[0].get("add_favorite", "Add Current Location"),
        command=add_to_favorites,
        font=("Arial", 14),
        width=200,
        height=32,
        fg_color="#088A08" if modo_var.get() == 1 else "#04B404",
        text_color="white"
    )
    add_button.place(x=380, y=10)
    
    scrollable_frame = ctk.CTkScrollableFrame(
        result_frame,
        width=560,
        height=200,
        fg_color='#D8D8D8' if modo_var.get() == 1 else '#2E64FE'
    )
    scrollable_frame.place(x=20, y=60)
    
    # Display favorites
    if favoritos:
        for i, fav in enumerate(favoritos):
            # Create a frame for each favorite
            fav_frame = ctk.CTkFrame(
                scrollable_frame,
                fg_color='#C0C0C0' if modo_var.get() == 1 else '#0080FF',
                height=40,
                width=540
            )
            fav_frame.pack(pady=5, fill="x")
            
            # City label
            city_label = ctk.CTkLabel(
                fav_frame,
                text=f"{fav['city']}, {fav['country']}",
                font=("Arial", 16),
                text_color='black' if modo_var.get() == 1 else 'white'
            )
            city_label.place(x=10, y=10)
            
            # View button
            view_button = ctk.CTkButton(
                fav_frame,
                text=current_translation[0].get("view", "View"),
                command=lambda c=fav['city'], p=fav['country']: view_favorite(c, p),
                font=("Arial", 14),
                width=80,
                height=30,
                fg_color="#0080FF" if modo_var.get() == 1 else "#0404B4",
                text_color="white"
            )
            view_button.place(x=350, y=5)
            
            # Remove button
            remove_button = ctk.CTkButton(
                fav_frame,
                text=current_translation[0].get("remove", "Remove"),
                command=lambda idx=i: remove_from_favorites(idx),
                font=("Arial", 14),
                width=80,
                height=30,
                fg_color="#DF0101" if modo_var.get() == 1 else "#B40404",
                text_color="white"
            )
            remove_button.place(x=450, y=5)
    else:
        # Show message when no favorites
        empty_label = ctk.CTkLabel(
            scrollable_frame,
            text=current_translation[0].get("no_favorites", "No favorite locations yet"),
            font=("Arial", 16),
            text_color='black' if modo_var.get() == 1 else 'white'
        )
        empty_label.pack(pady=20)

def view_favorite(city, country):
    global cidade, pais
    
    cidade = city
    pais = country
        
    prevatual()
    
    if 'infocidade' in globals() and infocidade.winfo_exists():
        infocidade.delete(0, tk.END)
        infocidade.insert(0, f"{city}, {country}")

    gettempo()

def initialize_favorites():
    load_favorites()

def limpar_janela():
    global listbox, city_frame
    if listbox is not None:
        try:
            listbox.destroy()
        except tk.TclError:
            pass  
        listbox = None
    
    if 'city_frame' in globals() and city_frame is not None:
        try:
            city_frame.destroy()
        except tk.TclError:
            pass
        city_frame = None 
    
    # Agora limpar o resto da janela
    for widget in root.winfo_children():
        widget.destroy()

def converter_temperatura(temp_kelvin):
    """ Converte Kelvin para a unidade selecionada (Celsius ou Fahrenheit). """
    if unit_var.get() == "Celsius":
        return round(temp_kelvin - 273.15, 2)
    elif unit_var.get() == "Fahrenheit":
        return round((temp_kelvin - 273.15) * 9 / 5 + 32, 2)

def locatual():
    global result_frame, infoloclabel, cidade, pais, loclabel

    result_frame = ctk.CTkFrame(
        root, 
        fg_color='#D8D8D8' if modo_var.get() == 1 else '#2E64FE', 
        width=300, 
        height=150
    )
    result_frame.place(x=110, y=120)

    infoloclabel = ctk.CTkLabel(
        result_frame, 
        text='', 
        font=custom_font2,
        text_color='black' if modo_var.get() == 1 else 'white'
    )
    infoloclabel.place(x=20, y=20)

    def get_location():
        g = geocoder.ip('me')
        if g.ok:
            return g.latlng  
        else:
            return None

    location = get_location()
    if location:
        print(f'Sua localização aproximada: Latitude {location[0]}, Longitude {location[1]}')
    else:
        print('Não foi possível obter sua localização.')

    def get_weather(lat, lon, api_key):
        url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=kelvin&lang={lang_var.get()}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    if location:
        weather_data = get_weather(location[0], location[1], API_KEY)
        if weather_data:
            cidade = weather_data['name']
            pais = weather_data['sys']['country']
            
            city_text = f"{current_translation[0]['city']}: {cidade}, {pais}"
            loclabel.configure(
                text=city_text,
                text_color='black' if modo_var.get() == 1 else 'white',
                font=custom_font2
            )
            
            fav_button = ctk.CTkButton(
                city_frame,
                text="★",  
                width=30,
                height=30,
                fg_color="#FFA500",  
                hover_color="#FF8C00",
                text_color="white",
                corner_radius=15,
                command=add_to_favorites
            )
            text_width = len(city_text) * 10  
            fav_button.place(x=text_width + 10, y=0)
            
            temp = converter_temperatura(weather_data['main']['temp'])
            infoloclabel.configure(
                text=(
                    f"{current_translation[0]['Description']}: "
                    f"{weather_data['weather'][0]['description'].capitalize()} \n"
                    f"{current_translation[0]['Temperature']}: {temp:.2f}°{unit_var.get()[0]}"
                )
            )
    else:
        loclabel.configure(text='Não foi possível obter sua localização.')

def gettempo():
    global cidade, pais, infoloclabel, result_frame, city_frame

    # Obter o texto do campo de busca
    cidade_input = infocidade.get().strip()
    if cidade_input:
        # Extrair cidade e país do campo de busca
        partes = cidade_input.split(",")
        cidade = partes[0].strip()
        pais = partes[-1].strip() if len(partes) > 1 else ""

    # Garantir que temos um frame de resultado com o tema correto
    if 'result_frame' not in globals() or not result_frame.winfo_exists():
        result_frame = ctk.CTkFrame(
            root, 
            fg_color='#D8D8D8' if modo_var.get() == 1 else '#2E64FE', 
            width=300, 
            height=150
        )
        result_frame.place(x=110, y=120)
        
        infoloclabel = ctk.CTkLabel(
            result_frame, 
            text='', 
            font=custom_font2,
            text_color='black' if modo_var.get() == 1 else 'white'
        )
        infoloclabel.place(x=20, y=20)
    else:
        # Atualizar cores do frame existente
        result_frame.configure(fg_color='#D8D8D8' if modo_var.get() == 1 else '#2E64FE')
        infoloclabel.configure(text_color='black' if modo_var.get() == 1 else 'white')

    if not cidade:
        return  # Se não tiver cidade definida, sai.

    # 1) Buscar lat/lon da cidade
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={cidade},{pais}&limit=1&appid={API_KEY}&lang={lang_var.get()}"
    geo_res = requests.get(geo_url)
    if geo_res.status_code == 200:
        geo_data = geo_res.json()
        if geo_data:
            lat = geo_data[0]['lat']
            lon = geo_data[0]['lon']

            # 2) Buscar clima
            weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&lang={lang_var.get()}"
            weather_res = requests.get(weather_url)
            if weather_res.status_code == 200:
                weather_data = weather_res.json()
                temp = converter_temperatura(weather_data['main']['temp'])
                desc = weather_data['weather'][0]['description']
                city_name = weather_data['name']
                country_code = weather_data['sys']['country']

                # Modifica aqui para criar um frame para o rótulo e botão em vez de apenas um rótulo
                if 'city_frame' in globals() and city_frame.winfo_exists():
                    city_frame.destroy()
                
                city_frame = ctk.CTkFrame(
                    root,
                    fg_color='transparent',
                    width=400,
                    height=40
                )
                city_frame.place(x=110, y=80)
                
                # Rótulo da cidade
                city_label = ctk.CTkLabel(
                    city_frame, 
                    text=f"{current_translation[0]['city']}: {city_name}, {country_code}",
                    text_color='black' if modo_var.get() == 1 else 'white',
                    font=custom_font2
                )
                city_label.place(x=0, y=0)
                
                # Botão de favoritos ao lado do rótulo
                fav_button = ctk.CTkButton(
                    city_frame,
                    text="★",  # Estrela como símbolo de favorito
                    width=30,
                    height=30,
                    fg_color="#FFA500",  # Cor laranja para o botão
                    hover_color="#FF8C00",
                    text_color="white",
                    corner_radius=15,
                    command=add_to_favorites
                )
                # Posiciona o botão logo após o texto da cidade
                text_width = len(f"{current_translation[0]['city']}: {city_name}, {country_code}") * 10  # Estimativa da largura
                fav_button.place(x=text_width + 10, y=0)
                
                infoloclabel.configure(
                    text=(
                        f"{current_translation[0]['Description']}: {desc}\n"
                        f"{current_translation[0]['Temperature']}: {temp:.2f}°{unit_var.get()[0]}"
                    ),
                    text_color='black' if modo_var.get() == 1 else 'white'
                )
            else:
                infoloclabel.configure(
                    text=current_translation[0]["not_found"],
                    font=custom_font2,
                    text_color='black' if modo_var.get() == 1 else 'white',
                    image=img_notfound,
                    compound="right"
                )
    else:
        infoloclabel.configure(
            text=current_translation[0]["not_found"],
            font=custom_font2,
            text_color='black' if modo_var.get() == 1 else 'white',
            image=img_notfound,
            compound="right"
        )

def menu():
    global setlabel, loclabel, infoloclabel, sidebar, topbar
    
    if modo_var.get() == 1:  # Light mode
        root.configure(fg_color="#E6E6E6")
        sidebar = ctk.CTkFrame(root, width=80, corner_radius=0, fg_color='#D8D8D8')
        topbar = ctk.CTkFrame(root, height=50, corner_radius=0, fg_color='#A4A4A4')
    else:  # Dark mode (default)
        root.configure(fg_color="#5882FA")
        sidebar = ctk.CTkFrame(root, width=80, corner_radius=0, fg_color='#2E2E2E')
        topbar = ctk.CTkFrame(root, height=50, corner_radius=0, fg_color='#000000')
    
    sidebar.pack(side="left", fill="y")
    topbar.pack(fill="x")

    sidebar_fg = '#D8D8D8' if modo_var.get() == 1 else '#2E2E2E'
    
    if modo_var.get() == 1:  # Light mode
        current_home = img_darkhome
        current_clock = img_darkclock
        current_location = img_darkfavorite
        current_settings = img_darksettings
    else:  # Dark mode
        current_home = img_home
        current_clock = img_clock
        current_location = img_favorite
        current_settings = img_settings

    # Manter botões da sidebar
    btn_home = ctk.CTkButton(
        sidebar, image=current_home, text="", width=50, height=50,
        fg_color=sidebar_fg, command=prevatual
    )
    btn_home.place(x=15, y=20)

    btn_clock = ctk.CTkButton(
        sidebar, image=current_clock, text="", width=50, height=50,
        fg_color=sidebar_fg, command=setup_5day_forecast
    )
    btn_clock.place(x=15, y=100)

    btn_location = ctk.CTkButton(
        sidebar, image=current_location, text="", width=50, height=50,
        fg_color=sidebar_fg, command=show_favorites
    )
    btn_location.place(x=15, y=180)

    btn_settings = ctk.CTkButton(
        sidebar, image=current_settings, text="", width=50, height=50,
        fg_color=sidebar_fg, command=config_settings
    )
    btn_settings.place(x=15, y=320)

    setlabel = ctk.CTkLabel(root, text='', font=custom_font2)
    setlabel.place(x=110, y=20)

    loclabel = ctk.CTkLabel(root, text='', font=custom_font2)
    loclabel.place(x=110, y=80)
    
def buscar_cidades(event=None):
    global termo, listbox

    termo = infocidade.get().strip()

    if not termo:
        # Esconde a listbox se o campo estiver vazio
        if listbox is not None:
            try:
                listbox.place_forget()
            except tk.TclError:
                pass  # Ignora erro se a listbox já foi destruída
        return

    # Verifica se a listbox existe e é válida, ou cria uma nova
    if listbox is None or not listbox.winfo_exists():
        # Remove qualquer listbox antiga antes de criar uma nova
        if listbox is not None:
            try:
                listbox.destroy()
            except tk.TclError:
                pass  # Ignora erro se a listbox já foi destruída
        
        # Criação de uma nova Listbox
        listbox = tk.Listbox(root, height=5, width=35, bg='#F0F0F0', font=("Arial", 12))
        # Bind do evento de seleção
        listbox.bind("<ButtonRelease-1>", selecionar_cidade)
    
    # Posicionar a listbox exatamente abaixo do campo de entrada
    x_position = infocidade.winfo_x()
    y_position = infocidade.winfo_y() + infocidade.winfo_height()
    listbox.place(x=x_position, y=y_position)

    url = f"http://api.openweathermap.org/geo/1.0/direct?q={termo}&limit=10&appid={API_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        cidades = response.json()

        listbox.delete(0, 'end')
        for c in cidades:
            nome = f"{c['name']}, {c.get('state', '')}, {c['country']}"
            listbox.insert('end', nome)

    except requests.exceptions.RequestException as e:
        print("Erro na requisição:", e)

def selecionar_cidade(event):
    global cidade, pais, listbox, city_frame

    if listbox is None or not listbox.winfo_exists():
        return
        
    try:
        index = listbox.curselection()
        if not index:  # Se não houver seleção, tenta pegar o item ativo
            selecao = listbox.get(tk.ACTIVE)
        else:
            selecao = listbox.get(index)

        if selecao:
            infocidade.delete(0, tk.END)
            infocidade.insert(0, selecao)
            listbox.place_forget()  # Esconde a listbox após a seleção

            # Separar nome da cidade e país
            partes = selecao.split(",")
            cidade = partes[0].strip()
            pais = partes[-1].strip()

            # Verifica qual tela está ativa para chamar a função apropriada
            try:
                current_screen = setlabel.cget("text")
                if current_screen == current_translation[0]["forecast_5_days"]:
                    get_5day_forecast()
                else:
                    gettempo()
            except (tk.TclError, Exception) as e:
                print(f"Erro ao determinar a tela atual: {e}")
                # Fallback - tenta chamar gettempo se houver erro
                gettempo()
    except (tk.TclError, Exception) as e:
        print(f"Erro ao selecionar cidade: {e}")

def prevatual():
    global infocidade, listbox, city_frame, loclabel

    limpar_janela()
    menu()
    
    # Aplicar tema baseado no modo selecionado
    if modo_var.get() == 1:  # Modo claro
        root.configure(fg_color="#E6E6E6")
        setlabel.configure(
            text=current_translation[0]["current_forecast"],
            fg_color='#A4A4A4',
            bg_color='#A4A4A4',
            text_color='black' 
        )
    else:  # Modo escuro (padrão)
        root.configure(fg_color="#5882FA")
        setlabel.configure(
            text=current_translation[0]["current_forecast"],
            fg_color='#000000',
            bg_color='#000000',
            text_color='white' 
        )

    infocidade = ctk.CTkEntry(
        root, placeholder_text=current_translation[0]["city_placeholder"],
        font=custom_font2, width=200, corner_radius=10, 
        bg_color='#A4A4A4' if modo_var.get() == 1 else '#000000'
    )
    infocidade.place(x=540, y=10)
    infocidade.bind("<KeyRelease>", buscar_cidades)
    infocidade.bind("<Return>", lambda event: gettempo())
    
    # Criar o city_frame
    city_frame = ctk.CTkFrame(
        root,
        fg_color='transparent',
        width=400,
        height=40
    )
    city_frame.place(x=110, y=80)

    # IMPORTANTE: Criar o loclabel inicialmente vazio no city_frame 
    loclabel = ctk.CTkLabel(
        city_frame, 
        text='',
        font=custom_font2,
        text_color='black' if modo_var.get() == 1 else 'white'
    )
    loclabel.place(x=0, y=0)
    
    # Preencher o campo de pesquisa com a cidade anterior se existir
    if cidade and pais:
        infocidade.delete(0, tk.END)
        infocidade.insert(0, f"{cidade}, {pais}")
        # Definir explicitamente o texto do loclabel com a cidade atual
        loclabel.configure(text=f"{current_translation[0]['city']}: {cidade}, {pais}")
        
        # Adicionar botão de favoritos ao lado do texto da cidade
        fav_button = ctk.CTkButton(
            city_frame,
            text="★",  # Estrela como símbolo de favorito
            width=30,
            height=30,
            fg_color="#FFA500",  # Cor laranja para o botão
            hover_color="#FF8C00",
            text_color="white",
            corner_radius=15,
            command=add_to_favorites
        )
        # Posiciona o botão logo após o texto da cidade
        text_width = len(f"{current_translation[0]['city']}: {cidade}, {pais}") * 10  # Estimativa da largura
        fav_button.place(x=text_width + 10, y=0)
        
        # Buscar o clima da cidade atual
        gettempo()
    else:
        # Exibir informações meteorológicas da localização atual
        locatual()

def get_5day_forecast():
    global cidade, pais, result_frame, city_frame
        
    # Obter o texto do campo de busca
    cidade_input = infocidade.get().strip()
    if cidade_input:
        # Extrair cidade e país do campo de busca
        partes = cidade_input.split(",")
        cidade = partes[0].strip()
        pais = partes[-1].strip() if len(partes) > 1 else ""
    
    # First make sure we have a result frame to display content in
    if 'result_frame' not in globals() or not result_frame.winfo_exists():
        result_frame = ctk.CTkFrame(
            root, 
            fg_color='#D8D8D8' if modo_var.get() == 1 else '#2E64FE', 
            width=600, 
            height=250
        )
        result_frame.place(x=110, y=150)  # Ajustado para ficar abaixo do city_frame
    else:
        # Atualizar cores do frame existente
        result_frame.configure(fg_color='#D8D8D8' if modo_var.get() == 1 else '#2E64FE')
    
    # Limpar o frame de resultado existente
    for widget in result_frame.winfo_children():
        widget.destroy()
    
    if cidade:
        Api_key = '344ca4445c87003f84ffbe7f96e79a30'
        url = f'https://api.openweathermap.org/data/2.5/forecast?q={cidade},{pais}&appid={Api_key}&lang={lang_var.get()}'
        res = requests.get(url)

        if res.status_code == 200:  
            weather = res.json()
            
            # Vamos organizar os dados por dia
            daily_forecasts = {}
            
            for item in weather['list']:
                # Extrair só a parte da data (sem a hora)
                date = item['dt_txt'].split()[0]
                
                # Se ainda não temos este dia, inicializar
                if date not in daily_forecasts:
                    daily_forecasts[date] = {
                        'temps': [],
                        'descriptions': [],
                        'icons': []
                    }
                
                # Adicionar dados deste horário
                daily_forecasts[date]['temps'].append(item['main']['temp'])
                daily_forecasts[date]['descriptions'].append(item['weather'][0]['description'])
                daily_forecasts[date]['icons'].append(item['weather'][0]['icon'])
            
            # Agora vamos criar um resumo para cada dia
            forecast_info = []
            
            import datetime
            
            for date, data in daily_forecasts.items():
                # Calcular a temperatura mínima e máxima do dia (em vez da média)
                min_temp = min(data['temps'])
                max_temp = max(data['temps'])
                min_temp_converted = converter_temperatura(min_temp)
                max_temp_converted = converter_temperatura(max_temp)
                
                # Encontrar a descrição mais comum
                from collections import Counter
                most_common_desc = Counter(data['descriptions']).most_common(1)[0][0]
                
                # Formatar a data para exibição mais amigável
                date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
                formatted_date = date_obj.strftime('%d/%m/%Y')
                day_name = date_obj.strftime('%A')
                
                # Traduzir o nome do dia se necessário
                if lang_var.get() == 'pt':
                    days_pt = {
                        'Monday': 'Segunda-feira',
                        'Tuesday': 'Terça-feira',
                        'Wednesday': 'Quarta-feira',
                        'Thursday': 'Quinta-feira',
                        'Friday': 'Sexta-feira',
                        'Saturday': 'Sábado',
                        'Sunday': 'Domingo'
                    }
                    day_name = days_pt.get(day_name, day_name)
                elif lang_var.get() == 'es':
                    days_es = {
                        'Monday': 'Lunes',
                        'Tuesday': 'Martes',
                        'Wednesday': 'Miércoles',
                        'Thursday': 'Jueves',
                        'Friday': 'Viernes',
                        'Saturday': 'Sábado',
                        'Sunday': 'Domingo'
                    }
                    day_name = days_es.get(day_name, day_name)
                
                # Montar o texto de previsão para este dia
                day_forecast = f'{day_name} - {formatted_date}\n'
                day_forecast += f'{current_translation[0]["Temperature"]} min: {min_temp_converted:.1f}°{unit_var.get()[0]}, max: {max_temp_converted:.1f}°{unit_var.get()[0]}\n'
                day_forecast += f'{current_translation[0]["Description"]}: {most_common_desc.capitalize()}'
                
                forecast_info.append(day_forecast)
            
            # Limitar a 5 dias
            forecast_info = forecast_info[:5]

            # Create the forecast textbox inside the frame
            result_textbox = ctk.CTkTextbox(
                result_frame, 
                font=custom_font2, 
                width=580, 
                height=230,
                text_color='black' if modo_var.get() == 1 else 'white',
                fg_color='#D8D8D8' if modo_var.get() == 1 else '#2E64FE'
            )
            result_textbox.pack(padx=10, pady=10)

            result_textbox.insert("0.0", '\n\n'.join(forecast_info))
            result_textbox.configure(state="disabled")
            
            # Limpe o city_frame e recrie os widgets
            for widget in city_frame.winfo_children():
                widget.destroy()
                
            # Rótulo da cidade
            city_label = ctk.CTkLabel(
                city_frame, 
                text=f"{current_translation[0]['city']}: {weather['city']['name']}, {weather['city']['country']}",
                text_color='black' if modo_var.get() == 1 else 'white',
                font=custom_font2
            )
            city_label.place(x=0, y=0)
            
            # Botão de favoritos ao lado do rótulo
            fav_button = ctk.CTkButton(
                city_frame,
                text="★",  # Estrela como símbolo de favorito
                width=30,
                height=30,
                fg_color="#FFA500",  # Cor laranja para o botão
                hover_color="#FF8C00",
                text_color="white",
                corner_radius=15,
                command=add_to_favorites
            )
            # Posiciona o botão logo após o texto da cidade
            text_width = len(f"{current_translation[0]['city']}: {weather['city']['name']}, {weather['city']['country']}") * 10  # Estimativa da largura
            fav_button.place(x=text_width + 10, y=0)
            
        else:
            # Display error message when API request fails
            error_label = ctk.CTkLabel(
                result_frame, 
                text=current_translation[0]["not_found"],
                font=custom_font2,
                text_color='black' if modo_var.get() == 1 else 'white',
                image=img_notfound,
                compound="right"
            )
            error_label.place(relx=0.5, rely=0.5, anchor='center')
    else:
        # Se não houver cidade selecionada, exibe mensagem solicitando a seleção
        empty_label = ctk.CTkLabel(
            result_frame, 
            text=current_translation[0]["select_city"],
            font=custom_font2,
            text_color='black' if modo_var.get() == 1 else 'white'
        )
        empty_label.place(relx=0.5, rely=0.5, anchor='center')

def setup_5day_forecast():
    global infocidade, result_frame, listbox, loclabel, city_frame
    
    limpar_janela()
    menu()
    
    # Configure the UI appearance with theme support
    if modo_var.get() == 1:  # Modo claro
        root.configure(fg_color="#E6E6E6")
        setlabel.configure(
            text=current_translation[0]["forecast_5_days"],
            fg_color='#A4A4A4', 
            bg_color='#A4A4A4',
            text_color='black'
        )
    else:  # Modo escuro (padrão)
        root.configure(fg_color="#5882FA") 
        setlabel.configure(
            text=current_translation[0]["forecast_5_days"],
            fg_color='#000000', 
            bg_color='#000000',
            text_color='white'
        )

    # Create the search field with theme-appropriate background
    infocidade = ctk.CTkEntry(
        root, 
        placeholder_text=current_translation[0]["city_placeholder"],
        font=custom_font2, 
        width=200, 
        corner_radius=10, 
        bg_color='#A4A4A4' if modo_var.get() == 1 else '#000000'
    )
    infocidade.place(x=540, y=10)
    infocidade.bind("<KeyRelease>", buscar_cidades)
    infocidade.bind("<Return>", lambda event: get_5day_forecast())
    
    # Criar o city_frame
    city_frame = ctk.CTkFrame(
        root,
        fg_color='transparent',
        width=400,
        height=40
    )
    city_frame.place(x=110, y=80)

    # Criar o loclabel inicialmente vazio no city_frame
    loclabel = ctk.CTkLabel(
        city_frame, 
        text='',
        font=custom_font2,
        text_color='black' if modo_var.get() == 1 else 'white'
    )
    loclabel.place(x=0, y=0)
    
    # Create the initial result frame with theme colors
    result_frame = ctk.CTkFrame(
        root, 
        fg_color='#D8D8D8' if modo_var.get() == 1 else '#2E64FE', 
        width=600, 
        height=250
    )
    result_frame.place(x=110, y=120)  # Ajustado para ficar mais próximo do city_frame
    
    if cidade and pais:
        infocidade.delete(0, tk.END)
        infocidade.insert(0, f"{cidade}, {pais}")
        get_5day_forecast()
    else:
        empty_label = ctk.CTkLabel(
            result_frame, 
            text=current_translation[0]["select_city"],
            font=custom_font2,
            text_color='black' if modo_var.get() == 1 else 'white'
        )
        empty_label.place(relx=0.5, rely=0.5, anchor='center')

def config_settings():
    global sidebar, topbar, img_home, img_clock, img_location, img_settings
    global img_darkhome, img_darkclock, img_darklocation, img_darksettings
    global current_translation
    
    limpar_janela()
    menu()
    
    root.configure(fg_color="#E6E6E6" if modo_var.get() == 1 else "#5882FA")
    setlabel.configure(
        text=current_translation[0]["settings"],
        fg_color='#A4A4A4' if modo_var.get() == 1 else '#000000', 
        bg_color='#A4A4A4' if modo_var.get() == 1 else '#000000',
        text_color='black' if modo_var.get() == 1 else 'white'
    )
    
    settings_frame = ctk.CTkFrame(
        root, 
        fg_color='#D8D8D8' if modo_var.get() == 1 else '#2E64FE', 
        width=600, 
        height=280
    )
    settings_frame.place(x=110, y=80)
    
    # Set text color based on theme mode
    text_color = 'black' if modo_var.get() == 1 else 'white'
    
    appearance_title = ctk.CTkLabel(
        settings_frame, 
        text=current_translation[0]["appearance"], 
        font=("Arial", 20, "bold"),
        text_color=text_color
    )
    appearance_title.place(x=20, y=20)
    
    mode_label = ctk.CTkLabel(
        settings_frame, 
        text=current_translation[0]["theme_mode"], 
        font=custom_font2,
        text_color=text_color
    )
    mode_label.place(x=40, y=60)
    
    def on_theme_change():
        toggle_theme()
    
    rb_light = ctk.CTkRadioButton(
        settings_frame, 
        text=current_translation[0]["light_mode"], 
        variable=modo_var, 
        value=1,
        command=on_theme_change,  
        font=("Arial", 16),
        text_color=text_color
    )
    rb_light.place(x=40, y=90)
    
    rb_dark = ctk.CTkRadioButton(
        settings_frame, 
        text=current_translation[0]["dark_mode"], 
        variable=modo_var, 
        value=2,
        command=on_theme_change,  
        font=("Arial", 16),
        text_color=text_color
    )
    rb_dark.place(x=40, y=120)
    
    units_title = ctk.CTkLabel(
        settings_frame, 
        text=current_translation[0]["units"], 
        font=("Arial", 20, "bold"),
        text_color=text_color
    )
    units_title.place(x=300, y=20)
    
    temp_label = ctk.CTkLabel(
        settings_frame, 
        text=current_translation[0]["temperature_unit"], 
        font=custom_font2,
        text_color=text_color
    )
    temp_label.place(x=320, y=60)
    
    rb_celsius = ctk.CTkRadioButton(
        settings_frame, 
        text=current_translation[0]["celsius"], 
        variable=unit_var, 
        value="Celsius",
        font=("Arial", 16),
        text_color=text_color
    )
    rb_celsius.place(x=320, y=90)
    
    rb_fahrenheit = ctk.CTkRadioButton(
        settings_frame, 
        text=current_translation[0]["fahrenheit"], 
        variable=unit_var, 
        value="Fahrenheit",
        font=("Arial", 16),
        text_color=text_color
    )
    rb_fahrenheit.place(x=320, y=120)
    
    language_title = ctk.CTkLabel(
        settings_frame, 
        text=current_translation[0]["language"], 
        font=("Arial", 20, "bold"),
        text_color=text_color
    )
    language_title.place(x=20, y=160)
    
    language_options = ["Português", "English", "Español"]
    language_codes = {"Português": "pt", "English": "en", "Español": "es"}
    
    def change_language(choice):
        global current_translation
        lang_code = language_codes[choice]
        lang_var.set(lang_code)
        current_translation = translations["translations"][lang_code]
        config_settings() 
    
    current_lang_name = next(
        (name for name, code in language_codes.items() if code == lang_var.get()), 
        "Português"
    )
    
    language_dropdown = ctk.CTkOptionMenu(
        settings_frame,
        values=language_options,
        command=change_language,
        width=200,
        font=("Arial", 16),
        variable=ctk.StringVar(value=current_lang_name)
    )
    language_dropdown.place(x=40, y=200)

def toggle_theme():
    global img_home, img_clock, img_favorite, img_settings
    
    if modo_var.get() == 1:  # Light mode
        root.configure(fg_color="#E6E6E6")
        if 'sidebar' in globals() and sidebar.winfo_exists():
            sidebar.configure(fg_color='#D8D8D8')
        if 'topbar' in globals() and topbar.winfo_exists():
            topbar.configure(fg_color='#A4A4A4')
        if 'result_frame' in globals() and result_frame.winfo_exists():
            result_frame.configure(fg_color='#D8D8D8')
            for widget in result_frame.winfo_children():
                if isinstance(widget, ctk.CTkLabel) or isinstance(widget, ctk.CTkTextbox):
                    widget.configure(text_color='black')
        
        # Update the settings frame if it exists
        settings_frames = [widget for widget in root.winfo_children() 
                          if isinstance(widget, ctk.CTkFrame) 
                          and widget not in (sidebar, topbar)]
        
        for frame in settings_frames:
            frame.configure(fg_color='#D8D8D8')
            # Update all widgets inside the frame
            for widget in frame.winfo_children():
                if isinstance(widget, ctk.CTkLabel):
                    widget.configure(text_color='black')
                elif isinstance(widget, ctk.CTkRadioButton):
                    widget.configure(text_color='black')
        
        if 'setlabel' in globals() and setlabel.winfo_exists():
            setlabel.configure(text_color='black', fg_color='#A4A4A4', bg_color='#A4A4A4')
        if 'loclabel' in globals() and loclabel.winfo_exists():
            loclabel.configure(text_color='black')
        if 'infoloclabel' in globals() and infoloclabel.winfo_exists():
            infoloclabel.configure(text_color='black')
        
        img_home = ctk.CTkImage(Image.open(png_icons["darkhome"]), size=(30, 30))
        img_clock = ctk.CTkImage(Image.open(png_icons["darkclock"]), size=(30, 30))
        img_favorite = ctk.CTkImage(Image.open(png_icons["darkfavorite"]), size=(30, 30))
        img_settings = ctk.CTkImage(Image.open(png_icons["darksettings"]), size=(30, 30))
        
    else:  # Dark mode
        root.configure(fg_color="#5882FA")
        if 'sidebar' in globals() and sidebar.winfo_exists():
            sidebar.configure(fg_color='#2E2E2E')
        if 'topbar' in globals() and topbar.winfo_exists():
            topbar.configure(fg_color='#000000')
        if 'result_frame' in globals() and result_frame.winfo_exists():
            result_frame.configure(fg_color='#2E64FE')
            # Update text color in result frame
            for widget in result_frame.winfo_children():
                if isinstance(widget, ctk.CTkLabel) or isinstance(widget, ctk.CTkTextbox):
                    widget.configure(text_color='white')
        
        # Update the settings frame if it exists
        settings_frames = [widget for widget in root.winfo_children() 
                          if isinstance(widget, ctk.CTkFrame) 
                          and widget not in (sidebar, topbar)]
        
        for frame in settings_frames:
            frame.configure(fg_color='#2E64FE')
            # Update all widgets inside the frame
            for widget in frame.winfo_children():
                if isinstance(widget, ctk.CTkLabel):
                    widget.configure(text_color='white')
                elif isinstance(widget, ctk.CTkRadioButton):
                    widget.configure(text_color='white')
        
        # Update label text colors if they exist
        if 'setlabel' in globals() and setlabel.winfo_exists():
            setlabel.configure(text_color='white', fg_color='#000000', bg_color='#000000')
        if 'loclabel' in globals() and loclabel.winfo_exists():
            loclabel.configure(text_color='white')
        if 'infoloclabel' in globals() and infoloclabel.winfo_exists():
            infoloclabel.configure(text_color='white')
        
        img_home = ctk.CTkImage(Image.open(png_icons["home"]), size=(30, 30))
        img_clock = ctk.CTkImage(Image.open(png_icons["clock"]), size=(30, 30)) 
        img_favorite = ctk.CTkImage(Image.open(png_icons["favorite"]), size=(30, 30))
        img_settings = ctk.CTkImage(Image.open(png_icons["settings"]), size=(30, 30))
    
    update_sidebar_buttons()
    
    # If we're in the settings screen, refresh it to apply the theme properly
    if 'setlabel' in globals() and setlabel.winfo_exists():
        current_screen = setlabel.cget("text")
        if current_screen == current_translation[0]["settings"]:
            config_settings()

def update_sidebar_buttons():
    """Atualiza os botões da sidebar com os ícones corretos"""
    if 'sidebar' not in globals() or not sidebar.winfo_exists():
        return
        
    # Set appropriate button background color based on theme
    sidebar_fg = '#D8D8D8' if modo_var.get() == 1 else '#2E2E2E'
    
    for widget in sidebar.winfo_children():
        if isinstance(widget, ctk.CTkButton):
            # Update button background color
            widget.configure(fg_color=sidebar_fg)
            
            # Update button icon based on position
            if widget.winfo_y() == 20:  # Home button
                widget.configure(image=img_home)
            elif widget.winfo_y() == 100:  # Clock button
                widget.configure(image=img_clock)
            elif widget.winfo_y() == 180:  # Location button
                widget.configure(image=img_location)
            elif widget.winfo_y() == 320:  # Settings button
                widget.configure(image=img_settings)

def save_settings():
    toggle_theme()
    
    messagebox = ctk.CTkToplevel(root)
    messagebox.title(current_translation[0]["success"])
    messagebox.geometry("300x150")
    messagebox.resizable(False, False)
    messagebox.transient(root)  
    messagebox.grab_set()  
    
    x = root.winfo_x() + (root.winfo_width() / 2) - (300 / 2)
    y = root.winfo_y() + (root.winfo_height() / 2) - (150 / 2)
    messagebox.geometry(f"+{int(x)}+{int(y)}")
    
    label = ctk.CTkLabel(
        messagebox, 
        text=current_translation[0]["settings_saved"],
        font=("Arial", 16)
    )
    label.pack(pady=30)
    
    ok_button = ctk.CTkButton(
        messagebox, 
        text="OK",
        command=messagebox.destroy,
        width=100
    )
    ok_button.pack(pady=10)
    
    messagebox.after(2000, lambda: [messagebox.destroy(), prevatual()])

# Criação da janela principal
root = ctk.CTk()
root.geometry("800x400")
ctk.set_appearance_mode("dark")
root.resizable(False, False)
root.title("SkyScope")

# Ajustar ícone
img = Image.open("images/logo2.png")
img = img.resize((64, 64), Image.LANCZOS)
img.save("images/icon.ico", format="ICO")
root.iconbitmap("images/icon.ico")

# Variáveis
modo_var = ctk.IntVar(value=2)
lang_var = ctk.StringVar(value='pt')
unit_var = ctk.StringVar(value='Celsius')
medida = ctk.StringVar(value='°C')
API_KEY = "344ca4445c87003f84ffbe7f96e79a30"

# Carregar ícones
img_home = ctk.CTkImage(Image.open(png_icons["home"]), size=(30, 30))
img_clock = ctk.CTkImage(Image.open(png_icons["clock"]), size=(30, 30))
img_favorite = ctk.CTkImage(Image.open(png_icons["favorite"]), size=(30, 30))
img_settings = ctk.CTkImage(Image.open(png_icons["settings"]), size=(30, 30))
img_lupa = ctk.CTkImage(Image.open(png_icons["lupa"]), size=(30, 30))
img_notfound = ctk.CTkImage(Image.open(png_icons["notfound"]), size=(30, 30))
img_darklupa = ctk.CTkImage(Image.open(png_icons["darklupa"]), size=(30, 30))
img_darkhome = ctk.CTkImage(Image.open(png_icons["darkhome"]), size=(30, 30))
img_darkclock = ctk.CTkImage(Image.open(png_icons["darkclock"]), size=(30, 30))
img_darkfavorite = ctk.CTkImage(Image.open(png_icons["darkfavorite"]), size=(30, 30))
img_darksettings = ctk.CTkImage(Image.open(png_icons["darksettings"]), size=(30, 30))

custom_font1 = ("Arial", 40)
custom_font2 = ("Arial", 20)

menu()
prevatual()
initialize_favorites()

root.mainloop()