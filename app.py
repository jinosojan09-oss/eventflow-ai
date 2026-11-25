import os
import math
import pandas as pd
import streamlit as st
from openai import OpenAI
from agents import ROLES, demo

st.set_page_config(page_title="EventFlow AI", page_icon="🎟️", layout="wide")
st.title("🎟️ EventFlow AI")
st.caption("Your intelligent event production workspace")
with st.sidebar:
    st.header("Event brief")
    name=st.text_input("Event name", "360 Event Demo")
    city=st.text_input("City / country", "Riga, Latvia")
    kind=st.selectbox("Event type", ["Concert", "Club night", "Conference", "Festival", "Cinema screening", "Private event"])
    date=st.date_input("Event date")
    guests=st.number_input("Expected paying guests", min_value=1, value=500)
    lang=st.selectbox("Output language", ["English", "Latvian", "German", "French", "Spanish", "Italian"])
    key=st.text_input("OpenAI API key (optional)", type="password")
    key=key or os.getenv("OPENAI_API_KEY", "")
    st.caption("AI mode sends the event brief and instructions to OpenAI. Without a key, template demo mode is available in English.")
brief=f"Event: {name}; Location: {city}; Type: {kind}; Date: {date}; Guests: {guests}; Output language: {lang}."
tab, budget, reports=st.tabs(["AI workspace", "Budget calculator", "Project manager"])
with budget:
    st.subheader("Financial forecast (EUR)")
    categories=["Venue", "Artists", "Production", "Marketing", "Security", "Hospitality", "Other"]
    costs={c:st.number_input(c+" (€)", min_value=0.0, value=0.0, step=100.0) for c in categories}
    reserve=st.number_input("Contingency (%)", min_value=0.0, max_value=100.0, value=10.0)
    price=st.number_input("Net ticket revenue per guest (€)", min_value=0.0, value=25.0)
    sponsor=st.number_input("Other net revenue (€)", min_value=0.0, value=0.0)
    total=sum(costs.values())*(1+reserve/100)
    revenue=guests*price+sponsor
    a,b,c=st.columns(3)
    a.metric("Total costs",f"€{total:,.2f}")
    b.metric("Projected revenue",f"€{revenue:,.2f}")
    c.metric("Projected profit / loss",f"€{revenue-total:,.2f}")
    st.write("Break-even tickets:", math.ceil(max(0,total-sponsor)/price) if price else ("0" if sponsor>=total else "Not possible at zero ticket revenue"))
    df=pd.DataFrame(list(costs.items())+[("Contingency",total-sum(costs.values())),("Total costs",total),("Projected revenue",revenue),("Projected profit/loss",revenue-total)],columns=["Category","EUR"])
    st.dataframe(df,hide_index=True)
    st.download_button("Download budget CSV",df.to_csv(index=False),"event-budget.csv","text/csv")
    st.caption("Forecast only. Enter net revenue after applicable VAT and ticket fees; include all relevant costs.")
def generate(role, extra):
    context=f"{brief} Forecast costs EUR {total:.2f}; forecast revenue EUR {revenue:.2f}. Additional instructions: {extra}"
    if not key:
        return demo(role,name,city,str(date),guests,kind,total,revenue)
    response=OpenAI(api_key=key,timeout=60,max_retries=1).chat.completions.create(
        model=os.getenv("OPENAI_MODEL","gpt-4o-mini"),
        messages=[{"role":"system","content":ROLES[role]+" Do not invent confirmed venues, prices, bookings or legal facts. Label assumptions. Draft only; never claim external actions were taken."},{"role":"user","content":context}])
    return response.choices[0].message.content or "No response received."
if "outputs" not in st.session_state:
    st.session_state.outputs={}
if "tasks" not in st.session_state:
    st.session_state.tasks={}
with tab:
    role=st.selectbox("Choose your specialist",list(ROLES)[1:])
    extra=st.text_area("Additional instructions",placeholder="Artist details, venue requirements, timing, audience...")
    st.info("AI generation enabled" if key else "Template demo mode — add an API key for personalised AI output.")
    if st.button("Generate",type="primary"):
        try:
            with st.spinner("Preparing your output..."):
                st.session_state.outputs[role]=generate(role,extra)
        except Exception:
            st.error("AI request failed. Check your API key, model access and billing.")
    if role in st.session_state.outputs:
        output=st.session_state.outputs[role]
        st.markdown(output)
        st.download_button("Download result",output,"event-output.md")
with reports:
    st.subheader("Project manager")
    st.caption("Session-based task tracking and daily brief; no emails are sent automatically.")
    for role_name in list(ROLES)[1:]:
        st.session_state.tasks[role_name]=st.checkbox(role_name,value=st.session_state.tasks.get(role_name,False),key="task_"+role_name)
    st.progress(sum(st.session_state.tasks.values())/6)
    if st.button("Generate project brief"):
        try:
            st.session_state.outputs["Project Manager"]=generate("Project Manager",str(st.session_state.tasks)+"\nCompleted drafts: "+", ".join(st.session_state.outputs))
        except Exception:
            st.error("Could not generate brief. Check AI configuration.")
    if "Project Manager" in st.session_state.outputs:
        st.markdown(st.session_state.outputs["Project Manager"])
        st.download_button("Download daily brief",st.session_state.outputs["Project Manager"],"daily-brief.md")
    tasks=pd.DataFrame(st.session_state.tasks.items(),columns=["Task","Complete"])
    st.download_button("Export task tracker for Google Sheets",tasks.to_csv(index=False),"tasks.csv","text/csv")
