import requests

url = "https://www.comdinheiro.com.br/Clientes/API/EndPoint001.php"

querystring = {"code":"import_data"}

payload = "username=credito.mercado&password=Credito%26mercado1&URL=HistoricoIndicadoresFundos001.php%3F%26cnpjs%3D13077415000105%26data_ini%3D25032024%26data_fim%3D23092024%26indicadores%3Dret_03m%2Bret_06m%2Bret_12m%2Bret_24m%2Bret_12m_aa%26op01%3Dtabela_h%26num_casas%3D2%26enviar_email%3D0%26periodicidade%3Dmes%26cabecalho_excel%3Dmodo2%26transpor%3D0%26asc_desc%3Ddesc%26tipo_grafico%3Dlinha%26relat_alias_automatico%3Dcmd_alias_01&format=json3"
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

print(response.text)