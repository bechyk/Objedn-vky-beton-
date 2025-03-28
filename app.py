
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Cesta k souboru s daty
DATA_FILE = 'objednavky_betonu.xlsx'

# Načtení dat
def load_data():
    try:
        data = pd.read_excel(DATA_FILE)
    except FileNotFoundError:
        data = pd.DataFrame(columns=['Datum', 'Objekt', 'Konstrukce', 'Typ betonu', 'Objednané množství [m3]',
                                     'Skutečné množství [m3]', 'Typ vykládky', 'Zodpovědná osoba',
                                     'Začátek betonáže', 'Blokace komunikace', 'Poznámka'])
    return data

# Uložení dat
def save_data(data):
    data.to_excel(DATA_FILE, index=False)

# Hlavní funkce aplikace
def main():
    st.title('Správa objednávek betonáží')

    menu = ['Přidat objednávku', 'Zobrazit objednávky']
    choice = st.sidebar.selectbox('Menu', menu)

    data = load_data()

    if choice == 'Přidat objednávku':
        st.subheader('Přidat novou objednávku')

        with st.form(key='order_form'):
            col1, col2 = st.columns(2)

            with col1:
                datum = st.date_input('Datum betonáže', min_value=datetime.today())
                objekt = st.selectbox('Objekt', ['A', 'B', 'C', 'D'])
                konstrukce = st.text_input('Konstrukce')
                typ_betonu = st.selectbox('Typ betonu', ['C12/15', 'C20/25', 'C30/37, 90d'])
                objednane_mnozstvi = st.number_input('Objednané množství [m3]', min_value=0.0, step=0.1)

            with col2:
                skutecne_mnozstvi = st.number_input('Skutečné množství [m3]', min_value=0.0, step=0.1)
                typ_vykladky = st.selectbox('Typ vykládky', ['pumpa 24m', 'pumpa 42m', 'pumpa 56m'])
                zodpovedna_osoba = st.text_input('Zodpovědná osoba')
                zacatek_betonaze = st.time_input('Začátek betonáže')
                blokace_komunikace = st.text_input('Blokace komunikace')
                poznamka = st.text_area('Poznámka')

            submit_button = st.form_submit_button(label='Uložit objednávku')

        if submit_button:
            new_order = pd.DataFrame({
                'Datum': [datum],
                'Objekt': [objekt],
                'Konstrukce': [konstrukce],
                'Typ betonu': [typ_betonu],
                'Objednané množství [m3]': [objednane_mnozstvi],
                'Skutečné množství [m3]': [skutecne_mnozstvi],
                'Typ vykládky': [typ_vykladky],
                'Zodpovědná osoba': [zodpovedna_osoba],
                'Začátek betonáže': [zacatek_betonaze],
                'Blokace komunikace': [blokace_komunikace],
                'Poznámka': [poznamka]
            })

            data = pd.concat([data, new_order], ignore_index=True)
            save_data(data)
            st.success('Objednávka byla úspěšně přidána!')

    elif choice == 'Zobrazit objednávky':
        st.subheader('Přehled objednávek')

        if data.empty:
            st.warning('Žádné objednávky k zobrazení.')
        else:
            today = datetime.today().date()
            tomorrow = today + timedelta(days=1)

            def stav_objednavky(datum):
                if pd.isna(datum):
                    return "?"
                elif datum.date() == today:
                    return "DNES"
                elif datum.date() == tomorrow:
                    return "ZÍTRA"
                elif datum.date() < today:
                    return "MINULOST"
                else:
                    return "PLÁN"

            data['Stav'] = data['Datum'].apply(stav_objednavky)

            stav_filter = st.radio('Zobrazit objednávky:', ['Vše', 'DNES', 'ZÍTRA', 'PLÁN', 'MINULOST'])

            if stav_filter != 'Vše':
                data = data[data['Stav'] == stav_filter]

            st.dataframe(data)

           import io  # přidej nahoru do souboru, pokud tam ještě není

# Vygenerování Excelu do paměti (buffer)
excel_buffer = io.BytesIO()
data.to_excel(excel_buffer, index=False, engine='openpyxl')
excel_buffer.seek(0)

# Tlačítko pro stažení
st.download_button(
    label='Stáhnout objednávky jako Excel',
    data=excel_buffer,
    file_name='objednavky_betonu.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)

if __name__ == '__main__':
    main()
