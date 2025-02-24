def main():
    print("Hello from streamlit-properties!")


if __name__ == "__main__":
    main()
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Análisis de Inversión en Propiedades en Costa Rica", layout="wide")

def main():
    st.title("Análisis de Inversión en Propiedades en Costa Rica")
    st.write("Analice la rentabilidad de su inversión en casas contenedor para Airbnb en Guanacaste")

    # Create sidebar for input parameters
    st.sidebar.header("Parámetros de Inversión")

    # Property Details
    st.sidebar.subheader("Detalles de la Propiedad")
    num_containers = st.sidebar.number_input("Número de Contenedores", min_value=1, value=4)
    land_cost = st.sidebar.number_input("Costo del Terreno (USD)", min_value=0, value=100000)
    container_cost = st.sidebar.number_input("Costo por Contenedor (USD)", min_value=0, value=16000)

    # Revenue Parameters
    st.sidebar.subheader("Parámetros de Ingresos")
    price_per_night = st.sidebar.number_input("Precio por Noche (USD)", min_value=0, value=60)
    occupancy_rate = st.sidebar.slider("Tasa de Ocupación (%)", 0, 100, 70) / 100
    days_per_month = st.sidebar.number_input("Días por Mes", min_value=28, max_value=31, value=29)

    # Monthly Costs
    st.sidebar.subheader("Costos Mensuales")
    mortgage_payment = st.sidebar.number_input("Pago Mensual de Hipoteca (USD)", min_value=0, value=1200)
    utilities_cost = st.sidebar.number_input("Servicios Públicos Mensuales por Contenedor (USD)", min_value=0, value=100)
    management_cost = st.sidebar.number_input("Administración de Propiedad Mensual (USD)", min_value=0, value=300)

    # Annual Costs
    st.sidebar.subheader("Costos Anuales (% del Valor de la Propiedad)")
    property_tax_rate = st.sidebar.slider("Tasa de Impuesto de Propiedad (%)", 0.0, 5.0, 0.25) / 100
    insurance_rate = st.sidebar.slider("Tasa de Seguro (%)", 0.0, 5.0, 1.0) / 100
    maintenance_rate = st.sidebar.slider("Tasa de Mantenimiento (%)", 0.0, 5.0, 2.0) / 100
    repair_reserve_rate = st.sidebar.slider("Tasa de Reserva para Reparaciones (%)", 0.0, 5.0, 1.0) / 100

    # Calculate initial investment
    total_container_cost = num_containers * container_cost
    total_investment = land_cost + total_container_cost

    # Display initial investment breakdown
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Costo del Terreno", f"${land_cost:,}")
    with col2:
        st.metric("Costo de Contenedores", f"${total_container_cost:,}")
    with col3:
        st.metric("Inversión Total", f"${total_investment:,}")

    # Calculate monthly revenue
    daily_revenue_per_container = price_per_night
    monthly_revenue_per_container = daily_revenue_per_container * days_per_month * occupancy_rate
    total_monthly_revenue = monthly_revenue_per_container * num_containers

    # Calculate monthly expenses
    total_utilities = utilities_cost * num_containers
    
    property_value = total_investment
    monthly_property_tax = (property_value * property_tax_rate) / 12
    monthly_insurance = (property_value * insurance_rate) / 12
    monthly_maintenance = (property_value * maintenance_rate) / 12
    monthly_repair_reserve = (property_value * repair_reserve_rate) / 12

    expenses = {
        'Hipoteca': mortgage_payment,
        'Servicios Públicos': total_utilities,
        'Administración': management_cost,
        'Impuesto de Propiedad': monthly_property_tax,
        'Seguro': monthly_insurance,
        'Mantenimiento': monthly_maintenance,
        'Reserva para Reparaciones': monthly_repair_reserve
    }

    total_monthly_expenses = sum(expenses.values())

    # Calculate profitability metrics
    monthly_profit = total_monthly_revenue - total_monthly_expenses
    annual_profit = monthly_profit * 12
    roi = (annual_profit / total_investment) * 100
    annual_yield = (annual_profit / total_investment) * 100
    payback_period = total_investment / annual_profit if annual_profit > 0 else float('inf')
    monthly_profit_per_container = (total_monthly_revenue / num_containers) - (total_monthly_expenses / num_containers)
    break_even_months = container_cost / monthly_profit_per_container if monthly_profit_per_container > 0 else float('inf')

    # Display key metrics
    st.header("Métricas Financieras Clave")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Ingresos Mensuales", f"${total_monthly_revenue:,.2f}")
    with col2:
        st.metric("Gastos Mensuales", f"${total_monthly_expenses:,.2f}")
    with col3:
        st.metric("Beneficio Mensual", f"${monthly_profit:,.2f}")
    with col4:
        st.metric("Beneficio Anual", f"${annual_profit:,.2f}")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("ROI", f"{roi:.2f}%")
    with col2:
        st.metric("Rendimiento Anual", f"{annual_yield:.2f}%")
    with col3:
        st.metric("Período de Recuperación", f"{payback_period:.1f} años")
    with col4:
        st.metric("Punto de Equilibrio", f"{break_even_months:.1f} meses/contenedor")

    # Display monthly expenses breakdown
    st.header("Desglose de Gastos Mensuales")
    expenses_df = pd.DataFrame.from_dict(expenses, orient='index', columns=['Costo Mensual'])
    expenses_df['Costo Anual'] = expenses_df['Costo Mensual'] * 12
    expenses_df = expenses_df.round(2)

    # Create pie chart for expenses
    fig = px.pie(values=expenses_df['Costo Mensual'], 
                 names=expenses_df.index,
                 title='Distribución de Gastos Mensuales')
    st.plotly_chart(fig)

    # Display expenses table
    st.dataframe(expenses_df.style.format("${:,.2f}"))

    # Sensitivity Analysis
    st.header("Análisis de Sensibilidad")
    
    occupancy_variations = np.array([0.5, 0.6, 0.7, 0.8, 0.9])
    price_variations = np.array([80, 90, 100, 110, 120])
    
    profits = np.zeros((len(occupancy_variations), len(price_variations)))
    
    for i, occ in enumerate(occupancy_variations):
        for j, price in enumerate(price_variations):
            monthly_rev = price * days_per_month * occ * num_containers
            annual_profit = (monthly_rev - total_monthly_expenses) * 12
            profits[i, j] = annual_profit

    sensitivity_df = pd.DataFrame(profits, 
                                index=[f'{int(x*100)}%' for x in occupancy_variations],
                                columns=[f'${x}' for x in price_variations])

    # Create heatmap
    fig = px.imshow(profits,
                    labels=dict(x="Precio por Noche", y="Tasa de Ocupación", color="Beneficio Anual"),
                    x=[f'${x}' for x in price_variations],
                    y=[f'{int(x*100)}%' for x in occupancy_variations],
                    title="Análisis de Sensibilidad del Beneficio Anual",
                    color_continuous_scale="RdYlGn")
    
    fig.update_layout(
        xaxis_title="Precio por Noche (USD)",
        yaxis_title="Tasa de Ocupación"
    )
    
    st.plotly_chart(fig)

    # Display sensitivity table
    st.write("Análisis de Sensibilidad del Beneficio Anual (USD)")
    st.dataframe(sensitivity_df.style.format("${:,.2f}"))

if __name__ == "__main__":
    main()
