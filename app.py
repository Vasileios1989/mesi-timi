import streamlit as st
import pandas as pd

st.set_page_config(page_title="Υπολογιστής μέσης τιμής", page_icon="📈")

st.title("📈 Υπολογιστής μέσης τιμής αγοράς")
st.write(
    "Γράψε τις αγορές σου στον πίνακα. "
    "Για νέα γραμμή πάτα το + στο τέλος του πίνακα."
)

# Πίνακας αγορών (μπορείς να αλλάξεις τα νούμερα και να προσθέσεις γραμμές)
start_data = pd.DataFrame(
    {
        "Μετοχές": [10.0, 5.0],
        "Τιμή αγοράς ($)": [20.0, 25.0],
    }
)

purchases = st.data_editor(
    start_data,
    num_rows="dynamic",
    key="purchases",
)

current_price = st.number_input(
    "Τρέχουσα τιμή μετοχής ($)", min_value=0.0, value=30.0, step=0.1
)

# Καθαρισμός: κρατάμε μόνο γραμμές με έγκυρους αριθμούς
purchases = purchases.dropna()
purchases = purchases[(purchases["Μετοχές"] > 0) & (purchases["Τιμή αγοράς ($)"] > 0)]

if purchases.empty:
    st.info("Συμπλήρωσε τουλάχιστον μία αγορά στον πίνακα.")
    st.stop()

# Υπολογισμοί
total_shares = purchases["Μετοχές"].sum()
total_cost = (purchases["Μετοχές"] * purchases["Τιμή αγοράς ($)"]).sum()
average_price = total_cost / total_shares
current_value = total_shares * current_price
profit = current_value - total_cost
profit_pct = profit / total_cost * 100

st.subheader("Αποτελέσματα")

col1, col2 = st.columns(2)
col1.metric("Σύνολο μετοχών", f"{total_shares:,.2f} μετοχές")
col2.metric("Μέση τιμή αγοράς", f"{average_price:,.2f} $")

col3, col4 = st.columns(2)
col3.metric("Επενδυμένο ποσό", f"{total_cost:,.2f} $")
col4.metric("Τρέχουσα αξία", f"{current_value:,.2f} $")

st.metric(
    "Κέρδος / Ζημιά",
    f"{profit:,.2f} $",
    delta=f"{profit_pct:,.2f} % (επί του επενδυμένου ποσού)",
)

if profit >= 0:
    st.success("Είσαι θετικός (κέρδος) με αυτή την τιμή.")
else:
    st.error("Είσαι αρνητικός (ζημιά) με αυτή την τιμή.")

# Γράφημα
st.subheader("Γράφημα")
chart_data = pd.DataFrame(
    {
        "Τιμή αγοράς": purchases["Τιμή αγοράς ($)"].values,
        "Μέση τιμή": average_price,
        "Τρέχουσα τιμή": current_price,
    },
    index=[f"Αγορά {i}" for i in range(1, len(purchases) + 1)],
)
st.line_chart(chart_data)
