"""Specialist prompts and offline demonstration templates."""
ROLES = {
    "Project Manager": "Coordinate event workstreams. Summarise progress, blockers, owners and next actions in a daily brief.",
    "Event Planner": "Produce a practical event plan with milestones, staffing, accessibility, risks and contingency measures.",
    "Budget Analyst": "Interpret the supplied financial forecast; propose cost controls and scenarios without changing the calculated totals.",
    "Venue Assistant": "Draft a venue enquiry asking about availability, capacity, rental, technical facilities, accessibility, security and bar arrangements.",
    "Schedule Manager": "Create a proposed run of show including load-in, soundcheck, doors, acts, breaks and teardown.",
    "Marketing Assistant": "Create a promotional strategy, social captions, content calendar and calls to action without invented claims.",
    "Communication Agent": "Draft professional sponsor, artist or supplier correspondence as requested."
}

def demo(role,name,city,date,guests,kind,total,revenue):
    header=f"## {name} — {role}\n\n{kind} | {city} | {date} | {guests} expected guests\n\n*Illustrative template; verify all details.*\n\n"
    drafts={
        "Event Planner": "- Confirm objectives, audience, venue and capacity.\n- Book suppliers and artists; confirm permits and accessibility requirements.\n- Prepare staffing, ticketing and safety plans.\n- Reconfirm all deliveries and schedules before event day.\n- Review feedback and settle invoices after the event.",
        "Budget Analyst": f"- Forecast costs: EUR {total:,.2f}\n- Forecast revenue: EUR {revenue:,.2f}\n- Forecast balance: EUR {revenue-total:,.2f}\n- Obtain written quotes, confirm tax treatment and track actual expenses.",
        "Venue Assistant": f"Dear Venue Team,\n\nWe are planning {name} in {city} on {date} for approximately {guests} guests. Could you confirm availability, standing/seated capacity, rental fees, technical equipment, accessibility, staffing, security, cleaning and bar arrangements?\n\nKind regards,\nEvent Production Team",
        "Schedule Manager": "| Proposed time | Activity |\n|---|---|\n| 15:00 | Load-in |\n| 17:00 | Technical checks |\n| 18:00 | Staff briefing |\n| 19:00 | Doors |\n| 20:00 | Main programme |\n| 23:00 | Close and teardown |\n\nAdjust all times to confirmed venue and artist arrangements.",
        "Marketing Assistant": f"**Announcement:** Save the date! {name} is coming to {city} on {date}. Follow us for confirmed details.\n\n**Campaign:** Announcement, lineup reveal, ticket launch, weekly updates and final countdown. Publish only verified information.",
        "Communication Agent": f"Dear Partner,\n\nWe are organising {name} on {date} in {city} and would like to explore a collaboration. Please let us know your availability and requirements.\n\nBest regards,\nEvent Production Team",
        "Project Manager": "- Review the task tracker.\n- Confirm venue, budget and suppliers.\n- Assign owners and deadlines to outstanding work.\n- Check approvals and event risks before publishing."
    }
    return header+drafts[role]
