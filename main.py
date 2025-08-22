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

# Define constants
# Property Details defaults
DEFAULT_NUM_CONTAINERS = 3
DEFAULT_LAND_COST = 190000
DEFAULT_CONTAINER_COST = 18000
DEFAULT_ONE_TIME_COSTS = 40000  # Swimming pool, landscaping, permits, etc.

# Revenue Parameter defaults
DEFAULT_PRICE_PER_NIGHT = 80
DEFAULT_OCCUPANCY_RATE = 60
DEFAULT_DAYS_PER_MONTH = 29

# Monthly Cost defaults
DEFAULT_MORTGAGE_PAYMENT = 800
DEFAULT_UTILITIES_COST_PER_UNIT = 120
DEFAULT_MANAGEMENT_COST = 400
AIRBNB_COMMISSION = 3

# Annual Cost defaults (as percentages)
DEFAULT_PROPERTY_TAX_RATE = 0.25  
DEFAULT_INSURANCE_RATE = 1.0  
DEFAULT_MAINTENANCE_RATE = 2.0  
DEFAULT_REPAIR_RESERVE_RATE = 2.0 

# Investor Profile defaults
DEFAULT_INVESTOR_2_CONTAINERS = 1
DEFAULT_INVESTOR_1_CONTAINERS = DEFAULT_NUM_CONTAINERS - DEFAULT_INVESTOR_2_CONTAINERS


def main():
    st.title("Análisis de Inversión en Propiedades en Costa Rica")
    st.write("Analice la rentabilidad de su inversión en casas contenedor para Airbnb en Guanacaste")

    # Create sidebar for input parameters
    st.sidebar.header("Parámetros de Inversión")

    # Property Details
    st.sidebar.subheader("Detalles de la Propiedad")
    num_containers = st.sidebar.number_input("Número Total de Contenedores", min_value=1, value=DEFAULT_NUM_CONTAINERS)
    land_cost = st.sidebar.number_input("Costo del Terreno (USD)", min_value=0, value=DEFAULT_LAND_COST)
    container_cost = st.sidebar.number_input("Costo por Contenedor (USD)", min_value=0, value=DEFAULT_CONTAINER_COST)
    one_time_costs = st.sidebar.number_input("Costos Únicos (USD)", min_value=0, value=DEFAULT_ONE_TIME_COSTS, help="Piscina, paisajismo, permisos, etc.")

    # Revenue Parameters
    st.sidebar.subheader("Parámetros de Ingresos")
    price_per_night = st.sidebar.number_input("Precio por Noche (USD)", min_value=0, value=DEFAULT_PRICE_PER_NIGHT)
    occupancy_rate = st.sidebar.slider("Tasa de Ocupación (%)", 0, 100, DEFAULT_OCCUPANCY_RATE) / 100
    days_per_month = st.sidebar.number_input("Días por Mes", min_value=28, max_value=31, value=DEFAULT_DAYS_PER_MONTH)

    # Monthly Costs
    st.sidebar.subheader("Costos Mensuales")
    mortgage_payment = st.sidebar.number_input("Pago Mensual de Hipoteca (USD)", min_value=0, value=DEFAULT_MORTGAGE_PAYMENT)
    utilities_cost = st.sidebar.number_input("Servicios Públicos Mensuales por Contenedor (USD)", min_value=0, value=DEFAULT_UTILITIES_COST_PER_UNIT)
    management_cost = st.sidebar.number_input("Administración de Propiedad Mensual (USD)", min_value=0, value=DEFAULT_MANAGEMENT_COST)
    airbnb_commission = st.sidebar.slider("Comisión de Airbnb (%)", 0, 30, AIRBNB_COMMISSION) / 100

    # Annual Costs
    st.sidebar.subheader("Costos Anuales (% del Valor de la Propiedad)")
    property_tax_rate = st.sidebar.slider("Tasa de Impuesto de Propiedad (%)", 0.0, 5.0, DEFAULT_PROPERTY_TAX_RATE) / 100
    insurance_rate = st.sidebar.slider("Tasa de Seguro (%)", 0.0, 5.0, DEFAULT_INSURANCE_RATE) / 100
    maintenance_rate = st.sidebar.slider("Tasa de Mantenimiento (%)", 0.0, 5.0, DEFAULT_MAINTENANCE_RATE) / 100
    repair_reserve_rate = st.sidebar.slider("Tasa de Reserva para Reparaciones (%)", 0.0, 5.0, DEFAULT_REPAIR_RESERVE_RATE) / 100

    # Investor Profile
    st.sidebar.subheader("Perfil del Inversor")
    investor_1_containers = st.sidebar.number_input("Inversor 1: Número de Contenedores", min_value=0, value=DEFAULT_INVESTOR_1_CONTAINERS)
    investor_2_containers = st.sidebar.number_input("Inversor 2: Número de Contenedores", min_value=0, value=DEFAULT_INVESTOR_2_CONTAINERS)

    # Calculate initial investment
    total_container_cost = num_containers * container_cost
    total_investment = land_cost + total_container_cost + one_time_costs

    # Display initial investment breakdown
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Costo del Terreno", f"${land_cost:,}")
    with col2:
        st.metric("Costo de Contenedores", f"${total_container_cost:,}")
    with col3:
        st.metric("Costos Únicos", f"${one_time_costs:,}")
    with col4:
        st.metric("Inversión Total", f"${total_investment:,}")

    # Calculate monthly revenue
    daily_revenue_per_container = price_per_night
    monthly_revenue_per_container = daily_revenue_per_container * days_per_month * occupancy_rate
    total_monthly_gross_revenue = monthly_revenue_per_container * num_containers
    
    # Apply Airbnb commission
    airbnb_commission_amount = total_monthly_gross_revenue * airbnb_commission
    total_monthly_revenue = total_monthly_gross_revenue - airbnb_commission_amount

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
        'Reserva para Reparaciones': monthly_repair_reserve,
        'Comisión Airbnb': airbnb_commission_amount
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

    st.header("Retorno Por Inversor")
    investor_1_monthly_revenue = total_monthly_revenue * investor_1_containers / num_containers
    # Investor 1 owns the land, and therefore the mortgage is paid in full by investor 1
    investor_1_monthly_expenses = mortgage_payment + (total_monthly_expenses - mortgage_payment) * investor_1_containers / num_containers
    investor_1_monthly_profit = investor_1_monthly_revenue - investor_1_monthly_expenses
    investor_1_annual_profit = investor_1_monthly_profit * 12
    investor_1_roi = (investor_1_annual_profit / total_investment) * 100
    investor_1_annual_yield = (investor_1_annual_profit / total_investment) * 100

    investor_2_monthly_revenue = total_monthly_revenue * investor_2_containers / num_containers
    # investor 2 does not pay mortgage, so we subtract the monthly mortgage payment from the total monthly expenses
    investor_2_monthly_expenses = (total_monthly_expenses - mortgage_payment) * investor_2_containers / num_containers
    investor_2_monthly_profit = investor_2_monthly_revenue - investor_2_monthly_expenses
    investor_2_annual_profit = investor_2_monthly_profit * 12
    investor_2_roi = (investor_2_annual_profit / total_investment) * 100
    investor_2_annual_yield = (investor_2_annual_profit / total_investment) * 100

    st.dataframe(pd.DataFrame({
        "Inversor 1": [investor_1_containers, investor_1_monthly_revenue, investor_1_monthly_expenses, investor_1_monthly_profit, investor_1_annual_profit, investor_1_roi, investor_1_annual_yield],
        "Inversor 2": [investor_2_containers, investor_2_monthly_revenue, investor_2_monthly_expenses, investor_2_monthly_profit, investor_2_annual_profit, investor_2_roi, investor_2_annual_yield]
    }, index=["Contenedores", "Ingresos Mensuales", "Gastos Mensuales", "Beneficio Mensual", "Beneficio Anual", "ROI", "Rendimiento Anual"]))

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
    
    occupancy_variations = np.array([0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
    price_variations = np.array([40, 50, 60, 70, 80, 90, 100])
    
    profits = np.zeros((len(occupancy_variations), len(price_variations)))
    
    for i, occ in enumerate(occupancy_variations):
        for j, price in enumerate(price_variations):
            monthly_gross_rev = price * days_per_month * occ * num_containers
            monthly_airbnb_commission = monthly_gross_rev * airbnb_commission
            monthly_net_rev = monthly_gross_rev - monthly_airbnb_commission
            annual_profit = (monthly_net_rev - total_monthly_expenses + airbnb_commission_amount) * 12
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
