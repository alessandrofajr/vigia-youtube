# Vigia do YouTube

O bot Vigia do YouTube é capaz de monitorar canais na plataforma de vídeos do Google e disparar um e-mail caso um material tenha sido removido, ocultado ou apagado. 

Além disso, ele mantém um registro do título, descrição, visualizações, likes e outras informações sobre cada upload feito por um canal, mantendo os registros em uma planilha do Google Sheets.

### O que você precisa para usar
Esta ferramenta usa algumas APIs. Você precisará de:
- Uma chave da API do YouTube (existem inúmeros tutoriais na internet sobre como obtê-la, [veja um exemplo](https://medium.com/swlh/how-to-get-youtubes-api-key-7c28b59b1154))
- Uma chave de API do Google Sheets ([siga o passo a passo da bilbioteca gspread](https://docs.gspread.org/en/latest/oauth2.html#enable-api-access), utilizada no projeto). A modalidade usada é "For Bots: Using Service Account".
    - Depois de obter o JSON com suas credenciais, codifique o conteúdo do arquivo usando Base64 e armazene o valor em uma variável de ambiente. [Veja como realizar o encoding com Base64 aqui](https://www.geeksforgeeks.org/encoding-and-decoding-base64-strings-in-python/). O código do Vigia do YouTube prevê a decodificação.
- Caso você queira usar o script `send_notification.py`, você precisará de uma chave de API do SendGrid. [Veja aqui um guia para obter sua chave](https://docs.sendgrid.com/for-developers/sending-email/api-getting-started).

### Próximos passos
- Quebrar o código em funções menores e independentes
- Criar método para permitir que seja possível, após obter os dados do YouTube, escolher entre salvar um CSV localmente, enviar a tabela para um Google Sheets ou salvar os dados em um banco de dados MongoDB
- Criar uma documentação mais detalhada sobre como obter cada chave de API

Contribuições são bem-vindas.

### Agradecimentos

Agradeço [@cuducos](https://github.com/cuducos) e [@turicas](https://github.com/turicas) pelas orientações durante o desenvolvimento do projeto e [@gfelitti](https://github.com/gfelitti) por inspirar o trabalho – a [@novelodata](https://github.com/novelo-io) mantém um monitoramento de canais de extrema direita no Brasil.

## English description:

YouTube Sentinel Bot can monitor channels on Google's video platform and send an email if any material has been removed, hidden, or deleted.

It keeps track of the title, description, views, likes, and other information about each upload, keeping the data in a Google Sheets spreadsheet.

### What you need to use it
This tool uses some APIs. You will need:
- A YouTube API key (there are numerous tutorials on the internet on how to obtain one, [here's an example](https://medium.com/swlh/how-to-get-youtubes-api-key-7c28b59b1154)).
- A Google Sheets API key ([follow the step-by-step guide from the gspread library](https://docs.gspread.org/en/latest/oauth2.html#enable-api-access) used in the project). The mode used is "For Bots: Using Service Account."
    - After obtaining the JSON file with your credentials, encode the file's content using Base64 and store the value in an environment variable. [See how to perform Base64 encoding here](https://www.geeksforgeeks.org/encoding-and-decoding-base64-strings-in-python/). The YouTube Sentinel Bot code provides decoding functionality.
- If you want to use the `send_notification.py` script, you will need a SendGrid API key. [Here's a guide to obtaining your key](https://docs.sendgrid.com/for-developers/sending-email/api-getting-started).

### Next steps
- Break the code into smaller and independent functions.
- Create a method to allow choosing between saving data to a local CSV file, sending the table to a Google Sheets spreadsheet, or saving the data in a MongoDB database after retrieving the data from YouTube.
- Create more detailed documentation on how to obtain each API key.

Contributions are welcome.

### Acknowledgments

Thanks to [@cuducos](https://github.com/cuducos) and [@turicas](https://github.com/turicas) for their guidance during the project's development, and [@gfelitti](https://github.com/gfelitti) for inspiring the work - [@novelodata](https://github.com/novelo-io) maintains monitoring of far-right channels in Brazil.