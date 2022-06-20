# get-chords-api

get-chords-api es un API sencilla construida con Python y Django Rest Framework que analiza un archivo de audio mp3 o wav de una canción y devuelve los acordes de dicha canción.

## Cómo funciona

El API get-chords-api utiliza el sistema de complementos <a href="http://vamp-plugins.org/">Vamp</a> para el análisis de características de audio, mediante el módulo <a href="https://pypi.org/project/vamp/">VamPy</a>.

El complemento Vamp funciona de la siguiente manera:

Recibe un stream de datos de audio, los analiza y devuelve, dependiendo del plugin usado, multiples salidas con información descriptiva de los datos de audio.

<img src="http://vamp-plugins.org/images/vamp-overview-webscale.png">

En este caso, el plugin usado se llama <a href="http://www.isophonics.net/nnls-chroma">Chordino</a>, el cual hace posible la transcripción simple de acordes.

Para sacar acordes de una canción, el API realiza lo siguiente:

* Recibe el archivo de audio desde el cliente y lo almacena en una ruta temporal del servidor.
* Luego se usa el módulo de python <a href="https://pypi.org/project/librosa/">Librosa</a> para cargar el archivo de audio y devolver los datos de audio decodificados.
* Posterior, se invoca a vamp.process_audio, donde se le pasa como argumentos los datos de audio decodificados, el sample rate y el tipo de plugin a usar (nnls-chroma:chordino) 
* Vamp retorna los acordes con su respectiva linea de tiempo.

En código, su implementación sería de esta manera:

```python
audio_path = '/path/of/audio/example.wav'
data, rate = librosa.load(audio_path)
chords = vamp.process_audio(data, rate, 'nnls-chroma:chordino')
print(chords)
```
## Endpoint
El endpoind del API get-chords-api es: http://127.0.0.1:8000/api

## Resources
Los recursos que expone el api se detallan a continuación:
```
POST     /chord_analizer         Envia una canción mp3 o wav al servidor y retorna los acordes respectivos.
POST     /chords/create_chord    Envia una canción mp3 o wav al servidor e información metadata de la misma
                                 y retorna los acordes respectivos. Toda esta información se guarda en una 
                                 base de datos Posgresql.
GET      /chords/list            Recupera una lista de todas las canciones (que fueron guardadas en la base)
                                 con sus respectivos acordes e información de metadata.
GET      /chords/details/{id}    Recupera los acordes e información metadata de una canción en particular.
PUT      /chords/details/{id}    Actualiza información de una canción en particular.
DELETE   /chords/details/{id}    Elimina una canción en particular de la base de datos.
```
Nota: Se creó una base de datos con el propósito de guardar información histórica de todas las transcripciones de acordes. 

## Uso del API

Existen tres formas de testear el API:

* Mediante el uso de herramientas de testing (Postman, SOAP UI, etc).
* Creando un Cliente Rest en cualquier lenguaje de programación.
* Mediante la característica "The Browsable Api" que ofrece Django Rest Framework

### Mediante Postman:
![image](https://user-images.githubusercontent.com/55906900/174547325-10728370-9237-4335-9263-469342c92376.png)

### Mediante Cliente Rest (Java):

```Java
OkHttpClient client = new OkHttpClient().newBuilder()
  .build();
MediaType mediaType = MediaType.parse("text/plain");
RequestBody body = new MultipartBody.Builder().setType(MultipartBody.FORM)
  .addFormDataPart("audio_file","/C:/Users/Joshua/Desktop/a_sus_pies.mp3",
    RequestBody.create(MediaType.parse("application/octet-stream"),
    new File("/C:/Users/Joshua/Desktop/a_sus_pies.mp3")))
  .build();
Request request = new Request.Builder()
  .url("http://127.0.0.1:8000/api/chord_analizer")
  .method("POST", body)
  .build();
Response response = client.newCall(request).execute();
```

### Mediante The Browsable Api:
![image](https://user-images.githubusercontent.com/55906900/174548162-c4f23955-2ec5-4858-92ff-f29aa51fddc7.png)


La devolución de acordes es de esta manera:

```json
{
    "id": 3,
    "audio_file": "/media/a_sus_pies.mp3",
    "chords": "[{'timestamp':  0.371519274, 'label': 'N'}, {'timestamp':  1.207437641, 'label': 'Am'}, {'timestamp':  3.343673469, 'label': 'Dm7'}, {'timestamp':  6.315827664, 'label': 'Abaug'}, {'timestamp':  8.637823129, 'label': 'Am'}, {'timestamp':  13.746213151, 'label': 'Dm7'}, {'timestamp':  16.253968253, 'label': 'A/E'}, {'timestamp':  18.668843537, 'label': 'E'}, {'timestamp':  24.706031746, 'label': 'Dm'}, {'timestamp':  27.028027210, 'label': 'G'}, {'timestamp':  31.021859410, 'label': 'C'}, {'timestamp':  33.158095238, 'label': 'F'}, {'timestamp':  36.966167800, 'label': 'Dm'}, {'timestamp':  43.374875283, 'label': 'E'}, {'timestamp':  46.532789115, 'label': 'E7'}, {'timestamp':  47.833106575, 'label': 'A'}, {'timestamp':  51.548299319, 'label': 'Dm7'}, {'timestamp':  54.148934240, 'label': 'G7'}, {'timestamp':  58.049886621, 'label': 'C'}, {'timestamp':  60.279002267, 'label': 'F'}, {'timestamp':  63.715555555, 'label': 'Dm7'}, {'timestamp':  66.223310657, 'label': 'Bm7b5'}, {'timestamp':  70.774421768, 'label': 'E'}, {'timestamp':  74.303854875, 'label': 'Am'}, {'timestamp':  77.368888888, 'label': 'E7/G#'}, {'timestamp':  82.012879818, 'label': 'C/G'}, {'timestamp':  84.613514739, 'label': 'D/F#'}, {'timestamp':  87.028390022, 'label': 'Dm'}, {'timestamp':  89.536145124, 'label': 'E7'}, {'timestamp':  94.458775510, 'label': 'Am'}, {'timestamp':  96.873650793, 'label': 'E7/G#'}, {'timestamp':  101.610521541, 'label': 'C/G'}, {'timestamp':  104.211156462, 'label': 'D/F#'}, {'timestamp':  106.068752834, 'label': 'Fmaj7'}, {'timestamp':  107.369070294, 'label': 'F6'}, {'timestamp':  109.133786848, 'label': 'E7'}, {'timestamp':  113.963537414, 'label': 'Am'}, {'timestamp':  116.471292517, 'label': 'Dm'}, {'timestamp':  118.979047619, 'label': 'E7/G#'}, {'timestamp':  121.301043083, 'label': 'Am'}, {'timestamp':  123.901678004, 'label': 'F'}, {'timestamp':  126.223673469, 'label': 'Dm7'}, {'timestamp':  128.824308390, 'label': 'B7'}, {'timestamp':  131.146303854, 'label': 'E'}, {'timestamp':  133.561179138, 'label': 'A/C#'}, {'timestamp':  135.976054421, 'label': 'Dm'}, {'timestamp':  138.576689342, 'label': 'B'}, {'timestamp':  140.805804988, 'label': 'E'}, {'timestamp':  143.313560090, 'label': 'F6'}, {'timestamp':  145.914195011, 'label': 'E7'}, {'timestamp':  147.771791383, 'label': 'Am'}, {'timestamp':  152.137142857, 'label': 'Dm'}, {'timestamp':  154.552018140, 'label': 'F/C'}, {'timestamp':  155.666575963, 'label': 'Bm7b5'}, {'timestamp':  158.174331065, 'label': 'Bb'}, {'timestamp':  159.381768707, 'label': 'E7'}, {'timestamp':  160.960725623, 'label': 'E'}, {'timestamp':  163.468480725, 'label': 'Dm7'}, {'timestamp':  169.041269841, 'label': 'G'}, {'timestamp':  172.756462585, 'label': 'Dm7b5/C'}, {'timestamp':  174.149659863, 'label': 'C'}, {'timestamp':  175.171337868, 'label': 'F'}, {'timestamp':  178.886530612, 'label': 'Dm7'}, {'timestamp':  181.301405895, 'label': 'Bm7b5'}, {'timestamp':  186.595555555, 'label': 'E'}, {'timestamp':  189.939229024, 'label': 'Am'}, {'timestamp':  192.725623582, 'label': 'C#dim'}, {'timestamp':  193.840181405, 'label': 'Dm7'}, {'timestamp':  196.069297052, 'label': 'G'}, {'timestamp':  199.598730158, 'label': 'F6'}, {'timestamp':  200.527528344, 'label': 'C'}, {'timestamp':  202.292244897, 'label': 'F'}, {'timestamp':  205.728798185, 'label': 'Dm7'}, {'timestamp':  208.236553287, 'label': 'Bm7b5'}, {'timestamp':  212.230385487, 'label': 'E'}, {'timestamp':  216.224217687, 'label': 'Am'}, {'timestamp':  219.289251700, 'label': 'E7/G#'}, {'timestamp':  224.026122448, 'label': 'C/G'}, {'timestamp':  226.626757369, 'label': 'D/F#'}, {'timestamp':  229.134512471, 'label': 'F6'}, {'timestamp':  231.549387755, 'label': 'E7'}, {'timestamp':  236.564897959, 'label': 'Am'}, {'timestamp':  238.979773242, 'label': 'E7/G#'}, {'timestamp':  243.623764172, 'label': 'C/G'}, {'timestamp':  246.317278911, 'label': 'D/F#'}, {'timestamp':  248.639274376, 'label': 'F6'}, {'timestamp':  251.147029478, 'label': 'E7'}, {'timestamp':  256.162539682, 'label': 'Am7'}, {'timestamp':  258.484535147, 'label': 'Dm'}, {'timestamp':  260.899410430, 'label': 'E7/G#'}, {'timestamp':  263.407165532, 'label': 'Am'}, {'timestamp':  266.100680272, 'label': 'F'}, {'timestamp':  268.236916099, 'label': 'Dm7'}, {'timestamp':  270.837551020, 'label': 'B7'}, {'timestamp':  273.252426303, 'label': 'E'}, {'timestamp':  275.667301587, 'label': 'A7/C#'}, {'timestamp':  278.082176870, 'label': 'Dm'}, {'timestamp':  280.589931972, 'label': 'B7/D#'}, {'timestamp':  283.004807256, 'label': 'E'}, {'timestamp':  285.419682539, 'label': 'F6'}, {'timestamp':  287.927437641, 'label': 'E'}, {'timestamp':  290.249433106, 'label': 'Bm7b5'}, {'timestamp':  291.271111111, 'label': 'Fmaj7'}, {'timestamp':  293.128707482, 'label': 'Dm'}, {'timestamp':  295.264943310, 'label': 'E7'}, {'timestamp':  297.772698412, 'label': 'Bbm'}, {'timestamp':  300.187573696, 'label': 'Ebm7'}, {'timestamp':  302.602448979, 'label': 'F7'}, {'timestamp':  304.924444444, 'label': 'Cm7b5/Bb'}, {'timestamp':  306.224761904, 'label': 'Bbm'}, {'timestamp':  307.525079365, 'label': 'F#maj7'}, {'timestamp':  309.939954648, 'label': 'Ebm7'}, {'timestamp':  312.354829931, 'label': 'Cm7b5'}, {'timestamp':  314.955464852, 'label': 'F7'}, {'timestamp':  317.556099773, 'label': 'Am'}, {'timestamp':  319.785215419, 'label': 'Dm7'}, {'timestamp':  322.478730158, 'label': 'E7/G#'}, {'timestamp':  324.986485260, 'label': 'Am7'}, {'timestamp':  327.401360544, 'label': 'F'}, {'timestamp':  329.723356009, 'label': 'Dm7'}, {'timestamp':  332.323990929, 'label': 'B7'}, {'timestamp':  333.717188208, 'label': 'Bm7b5'}, {'timestamp':  334.831746031, 'label': 'E7'}, {'timestamp':  337.153741496, 'label': 'A7/C#'}, {'timestamp':  339.661496598, 'label': 'Dm'}, {'timestamp':  342.169251700, 'label': 'B/D#'}, {'timestamp':  344.212607709, 'label': 'Emaj7'}, {'timestamp':  346.906122448, 'label': 'F6'}, {'timestamp':  349.506757369, 'label': 'E'}, {'timestamp':  356.658503401, 'label': 'Bdim'}, {'timestamp':  357.958820861, 'label': 'F'}, {'timestamp':  359.073378684, 'label': 'G6'}, {'timestamp':  360.095056689, 'label': 'Dm'}, {'timestamp':  364.088888888, 'label': 'E7'}, {'timestamp':  368.547120181, 'label': 'Am'}, {'timestamp':  379.135419501, 'label': 'Bb7/D'}, {'timestamp':  381.085895691, 'label': 'C#m6'}, {'timestamp':  383.686530612, 'label': 'N'}]"
}
```


El tag chords contiene un conjunto de valores de tipo timestamp y label:
* El timestamp describe el tiempo en segundos de manera ascendente.
* El label describe el acorde.

La relación timestamp-label muestra al usuario el tiempo exacto en que el acorde suena mientras la canción se reproduce.

## Notas
El API get-chords-api fue creado para ser usado en otros proyectos de caracter personales. 
Está propenso a errores debido a que es la versión 1.0
El API se conecta a una base de datos postgresql. Para generar las tablas se debe ejecutar los comandos makemigrations y migrate.





