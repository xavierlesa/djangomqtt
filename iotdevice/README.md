## Flujo de registro (Frontend)


1. Abrir la app del mobile e ir a `(+) add device` y escanear el QR (esto registra el device a mi nodo)
2. Poner el device en modo `config`
3. Conectarse el nodo wifi desde el mobile `node-id_device`
4. La app automaticamente genera el pass_key (uuid + register_key) y lo guarda en el device
5. Configurar el `SSID` y `Pass` para el device
6. Desconectar la app y conectar a wifi nuevamente (así registra el device)
7. Ya se puede entrar desde el QR (el QR es el endpoint del device https://iot.foosible.com/device/uuid)


## Registro de dipositivo (Backend) - seguridad I

1. Crea un `token` para el usuario, en base a su `ID` y un `Key` autogenerado
2. Carga/Registra un id_device (uuid) a mi nodo
3. Espera a que el `device` se conecte para validar el `token` y autenticar
4. Al autenticar guarda el `device` en el nodo para que sea accesible desde el endpoint

## Registro de dipositivo (Backend) - seguridad II

1. Crea un `device_token` para el device, en base a su `id_device` y un `Key` autogenerado
2. Carga/Registra un id_device (uuid) a mi nodo
3. Espera a que el `device` se conecte para validar el `token` y autenticar
4. Al autenticar guarda el `device` en el nodo para que sea accesible desde el endpoint


## Comunicación

[DEVICE] -> UUID + TOKEN -> SHA -> BASE64 -> // -> BASE64 -> AUTH -> [SERVER]













Contacto: pablo@redinova.com

NOTAS: 

Soluciones de internet de las cosas que eficientizan el consumo eléctrico, especialmente en los locales o plantas con ascensores y escaleras mecánicas.

Un sensor vale 1.500 pesos o 100 dólares y el servicio para éste vale unos 225 o 15 dólares pesos por mes por unidad.

"Son precios que para una industria o un local no resultan onerosos, la instalación es muy rápida y la mejora de la eficiencia se estima en un 30%", aseguró.

Hacia el consumidor residencial, la previsión es ofrecer sensores al 50% del valor y un servicio que no excedería los 50 pesos mensuales.

Entre otras opciones, el consumidor podría estimar el consumo eléctrico por electrodoméstico para poder establecer un uso más eficiente de cada uno de ellos.

