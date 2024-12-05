import pandas as pd
import re


def format_telephone_number(string):
    match = re.search(
        r'(\+?\d{1,3})?[\s\-\.]?\(?(\d{3})\)?[\s\-\.]?(\d{3})[\s\-\.]?(\d{4})(?:.*?(ext\.?|x|#)?\s*(\d+))?',
        string,
        re.IGNORECASE
    )
    if match:
        number = '-'.join(filter(None, match.groups()[1:4]))

        prefix = match.group(1)
        if prefix:
            prefix = prefix.lstrip("+")
            prefix = prefix.lstrip("0")
            prefix = "+" + prefix
            number = f"{prefix} {number}"

        extension = match.group(6) if match.group(6) else None

        if extension:
            number = f"{number} EXT {extension}"

        return number
    return None


ruta_del_archivo = './Initial_load/datos_ventas.csv'

df = pd.read_csv(ruta_del_archivo)

df['ID_Venta'] = df['ID_Venta'].astype(str).str.strip()

df['Producto'] = df['Producto'].astype(str).apply(lambda text: re.sub(r'[^a-zA-Z0-9 ]', '', text)).str.upper()

df['Ciudad'] = df['Ciudad'].astype(str).apply(lambda text: re.sub(r'[^a-zA-Z0-9 ]', '', text)).str.upper()

df['Categoria'] = df['Categoria'].astype(str).apply(lambda text: re.sub(r'[^a-zA-Z0-9 ]', '', text)).str.upper()

df['Precio_Unitario'] = pd.to_numeric(df['Precio_Unitario'], errors='coerce')

df['Cantidad'] = pd.to_numeric(df['Cantidad'], errors='coerce')

df['Fecha_Venta'] = df['Fecha_Venta'].str.replace(r'^[^\w_]+|[^\w_]+$', '', regex=True)
df['Fecha_Venta'] = df['Fecha_Venta'].str.replace(r'^_+|_+$', '', regex=True)
df['Fecha_Venta'] = pd.to_datetime(df['Fecha_Venta'], format='%Y-%m-%d').dt.date

df['Cliente'] = df['Cliente'].astype(str).apply(lambda text: re.sub(r'[^a-zA-Z0-9 ]', '', text)).str.upper().str.strip()

df['Email'] = df['Email'].str.replace(r'^[^\w_]+|[^\w_]+$', '', regex=True)
df['Email'] = df['Email'].str.replace(r'^_+|_+$', '', regex=True)

df[['Telefono_Formateado']] = df['Telefono'].apply(lambda x: pd.Series(format_telephone_number(x)))

df['Direccion_Formateada'] = df['Direccion'].str.replace('\n', ' ', regex=False) ##La dirección tenía saldo de línea

df['Metodo_Pago'] = df['Metodo_Pago'].astype(str).apply(lambda text: re.sub(r'[^a-zA-Z0-9 ]', '', text)).str.upper().str.strip()

df['Estado'] = df['Estado'].astype(str).apply(lambda text: re.sub(r'[^a-zA-Z0-9 ]', '', text)).str.upper().str.strip()

df['Comentario'] = df['Comentario'].astype(str).apply(lambda text: re.sub(r'[^a-zA-Z0-9 ]', '', text)).str.upper().str.strip()

df['Descuento'] = pd.to_numeric(df['Descuento'], errors='coerce')

df['Total'] = df['Precio_Unitario'] * df['Cantidad']

df['total_con_descuento'] = df['Total'] * (1 - df['Descuento'] / 100)

print(df)

df.to_csv("./Result/datos_ventas_clean.csv", index= False)