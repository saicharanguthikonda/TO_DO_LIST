import streamlit as st
from datetime import date, datetime
import csv
import io
import uuid

st.set_page_config(
    page_title="TaskFlow - To-Do List",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="expanded",
)

THEMES = {
    "☀️ Bright": {
        "bg": "#F7F9FC", "card": "#FFFFFF", "text": "#172033",
        "muted": "#667085", "accent": "#2563EB", "accent2": "#1D4ED8",
        "border": "#E4E7EC", "success": "#16A34A", "danger": "#DC2626",
    },
    "🌙 Dark": {
        "bg": "#0F172A", "card": "#1E293B", "text": "#F8FAFC",
        "muted": "#CBD5E1", "accent": "#60A5FA", "accent2": "#3B82F6",
        "border": "#334155", "success": "#4ADE80", "danger": "#F87171",
    },
    "❄️ Cool": {
        "bg": "#EFF8FF", "card": "#FFFFFF", "text": "#0C2D48",
        "muted": "#486581", "accent": "#0284C7", "accent2": "#0369A1",
        "border": "#BAE6FD", "success": "#059669", "danger": "#DC2626",
    },
    "🔥 Warm": {
        "bg": "#FFF7ED", "card": "#FFFFFF", "text": "#431407",
        "muted": "#7C2D12", "accent": "#EA580C", "accent2": "#C2410C",
        "border": "#FED7AA", "success": "#16A34A", "danger": "#DC2626",
    },
    "🌲 Forest": {
        "bg": "#F0FDF4", "card": "#FFFFFF", "text": "#052E16",
        "muted": "#3F6212", "accent": "#16A34A", "accent2": "#15803D",
        "border": "#BBF7D0", "success": "#15803D", "danger": "#DC2626",
    },
    "💜 Purple": {
        "bg": "#FAF5FF", "card": "#FFFFFF", "text": "#2E1065",
        "muted": "#6B21A8", "accent": "#9333EA", "accent2": "#7E22CE",
        "border": "#E9D5FF", "success": "#16A34A", "danger": "#DC2626",
    },
}

if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "theme" not in st.session_state:
    st.session_state.theme = "☀️ Bright"

if "editing_id" not in st.session_state:
    st.session_state.editing_id = None

theme = THEMES[st.session_state.theme]

st.markdown(
    f"""
    <style>
    .stApp {{
        background: {theme["bg"]};
        color: {theme["text"]};
    }}
    [data-testid="stSidebar"] {{
        background: {theme["card"]};
        border-right: 1px solid {theme["border"]};
    }}
    .main-title {{
        font-size: 3rem;
        font-weight: 800;
        color: {theme["accent"]};
        margin-bottom: 0;
    }}
    .subtitle {{
        color: {theme["muted"]};
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }}
    .metric-card {{
        background: {theme["card"]};
        border: 1px solid {theme["border"]};
        border-radius: 16px;
        padding: 18px;
        text-align: center;
        box-shadow: 0 3px 12px rgba(0,0,0,.05);
    }}
    .metric-number {{
        font-size: 2rem;
        font-weight: 800;
        color: {theme["accent"]};
    }}
    .metric-label {{
        color: {theme["muted"]};
        font-weight: 600;
    }}
    .task-card {{
        background: {theme["card"]};
        border: 1px solid {theme["border"]};
        border-radius: 16px;
        padding: 18px;
        margin: 10px 0;
    }}
    .task-title {{
        font-size: 1.15rem;
        font-weight: 750;
        color: {theme["text"]};
    }}
    .task-description {{
        color: {theme["muted"]};
        margin-top: 5px;
    }}
    .badge {{
        display: inline-block;
        padding: 4px 9px;
        border-radius: 999px;
        font-size: .78rem;
        font-weight: 700;
        margin-right: 5px;
        background: {theme["bg"]};
        border: 1px solid {theme["border"]};
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

def add_task(title, description, priority, status, due_date):
    st.session_state.tasks.append({
        "id": str(uuid.uuid4()),
        "title": title.strip(),
        "description": description.strip(),
        "priority": priority,
        "status": status,
        "due_date": due_date.isoformat() if due_date else "",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "completed_at": "",
    })

def get_due_status(task):
    if not task["due_date"] or task["status"] == "Completed":
        return ""
    due = date.fromisoformat(task["due_date"])
    if due < date.today():
        return "Overdue"
    if due == date.today():
        return "Due today"
    return ""

def update_task(task_id, title, description, priority, status, due_date):
    for task in st.session_state.tasks:
        if task["id"] == task_id:
            old_status = task["status"]
            task["title"] = title.strip()
            task["description"] = description.strip()
            task["priority"] = priority
            task["status"] = status
            task["due_date"] = due_date.isoformat() if due_date else ""
            if status == "Completed" and old_status != "Completed":
                task["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            elif status != "Completed":
                task["completed_at"] = ""
            break

def delete_task(task_id):
    st.session_state.tasks = [
        task for task in st.session_state.tasks if task["id"] != task_id
    ]

def set_status(task_id, status):
    for task in st.session_state.tasks:
        if task["id"] == task_id:
            task["status"] = status
            task["completed_at"] = (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if status == "Completed" else ""
            )
            break

def export_csv(tasks):
    output = io.StringIO()
    fields = [
        "title", "description", "priority", "status",
        "due_date", "created_at", "completed_at"
    ]
    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()
    for task in tasks:
        writer.writerow({field: task.get(field, "") for field in fields})
    return output.getvalue()

with st.sidebar:
    st.markdown("## ⚙️ TaskFlow")
    st.caption("Python + Streamlit To-Do Manager")

    selected_theme = st.selectbox(
        "🎨 Choose Theme",
        list(THEMES.keys()),
        index=list(THEMES.keys()).index(st.session_state.theme),
    )

    if selected_theme != st.session_state.theme:
        st.session_state.theme = selected_theme
        st.rerun()

    st.divider()
    st.markdown("### 📌 Quick Actions")

    if st.button("🧹 Clear Completed", use_container_width=True):
        before = len(st.session_state.tasks)
        st.session_state.tasks = [
            task for task in st.session_state.tasks
            if task["status"] != "Completed"
        ]
        removed = before - len(st.session_state.tasks)
        st.success(f"Removed {removed} completed task(s).")

    st.divider()
    st.markdown("### ℹ️ About")
    st.caption(
        "A complete To-Do application built entirely with Python and Streamlit. "
        "Tasks are maintained in Streamlit session state."
    )

st.markdown('<div class="main-title">✅ TaskFlow</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Organize your work. Track your progress. Finish your goals.</div>',
    unsafe_allow_html=True,
)

total = len(st.session_state.tasks)
pending = sum(t["status"] == "Pending" for t in st.session_state.tasks)
progress = sum(t["status"] == "In Progress" for t in st.session_state.tasks)
completed = sum(t["status"] == "Completed" for t in st.session_state.tasks)
overdue = sum(get_due_status(t) == "Overdue" for t in st.session_state.tasks)

cols = st.columns(5)
metrics = [
    ("📋", "Total", total),
    ("⏳", "Pending", pending),
    ("🔄", "In Progress", progress),
    ("✅", "Completed", completed),
    ("🚨", "Overdue", overdue),
]
for col, (icon, label, value) in zip(cols, metrics):
    with col:
        st.markdown(
            f'<div class="metric-card"><div class="metric-number">{icon} {value}</div>'
            f'<div class="metric-label">{label}</div></div>',
            unsafe_allow_html=True,
        )

st.write("")

tab_add, tab_tasks = st.tabs(["➕ Add Task", "📝 My Tasks"])

with tab_add:
    st.subheader("Create a New Task")
    with st.form("add_task_form", clear_on_submit=True):
        c1, c2 = st.columns([2, 1])
        with c1:
            title = st.text_input("Task Title *", placeholder="e.g. Complete Python assignment")
            description = st.text_area(
                "Description",
                placeholder="Add useful details about this task...",
                height=100,
            )
        with c2:
            priority = st.selectbox("Priority", ["Low", "Medium", "High", "Urgent"], index=1)
            status = st.selectbox("Status", ["Pending", "In Progress", "Completed"])
            due_date = st.date_input("Due Date", value=None)

        submitted = st.form_submit_button("🚀 Add Task", use_container_width=True)

        if submitted:
            if not title.strip():
                st.error("Task title cannot be empty.")
            else:
                add_task(title, description, priority, status, due_date)
                st.success("Task added successfully!")
                st.rerun()

with tab_tasks:
    st.subheader("Your Tasks")

    f1, f2, f3 = st.columns([2, 1, 1])
    with f1:
        search = st.text_input("🔎 Search", placeholder="Search title or description...")
    with f2:
        status_filter = st.selectbox(
            "Status", ["All", "Pending", "In Progress", "Completed"]
        )
    with f3:
        priority_filter = st.selectbox(
            "Priority", ["All", "Low", "Medium", "High", "Urgent"]
        )

    filtered = []
    for task in st.session_state.tasks:
        matches_search = (
            not search.strip()
            or search.lower() in task["title"].lower()
            or search.lower() in task["description"].lower()
        )
        matches_status = status_filter == "All" or task["status"] == status_filter
        matches_priority = priority_filter == "All" or task["priority"] == priority_filter

        if matches_search and matches_status and matches_priority:
            filtered.append(task)

    st.caption(f"Showing {len(filtered)} of {len(st.session_state.tasks)} task(s).")

    if not filtered:
        st.info("No tasks found. Add a task or change your filters.")
    else:
        for task in filtered:
            due_status = get_due_status(task)

            with st.container():
                st.markdown('<div class="task-card">', unsafe_allow_html=True)

                left, right = st.columns([4, 1])

                with left:
                    completed_mark = "~~" if task["status"] == "Completed" else ""
                    st.markdown(
                        f'<div class="task-title">{completed_mark}{task["title"]}{completed_mark}</div>',
                        unsafe_allow_html=True,
                    )

                    if task["description"]:
                        st.markdown(
                            f'<div class="task-description">{task["description"]}</div>',
                            unsafe_allow_html=True,
                        )

                    badges = (
                        f'<span class="badge">Priority: {task["priority"]}</span>'
                        f'<span class="badge">Status: {task["status"]}</span>'
                    )
                    if task["due_date"]:
                        badges += f'<span class="badge">Due: {task["due_date"]}</span>'
                    if due_status:
                        badges += f'<span class="badge">🚨 {due_status}</span>'

                    st.markdown(badges, unsafe_allow_html=True)

                with right:
                    if task["status"] == "Completed":
                        if st.button("↩️ Reopen", key=f"reopen_{task['id']}", use_container_width=True):
                            set_status(task["id"], "Pending")
                            st.rerun()
                    else:
                        if st.button("✅ Complete", key=f"complete_{task['id']}", use_container_width=True):
                            set_status(task["id"], "Completed")
                            st.rerun()

                a, b = st.columns([1, 1])
                with a:
                    with st.popover("✏️ Edit"):
                        st.markdown("### Edit Task")
                        edit_title = st.text_input(
                            "Title",
                            value=task["title"],
                            key=f"title_{task['id']}",
                        )
                        edit_description = st.text_area(
                            "Description",
                            value=task["description"],
                            key=f"description_{task['id']}",
                        )
                        edit_priority = st.selectbox(
                            "Priority",
                            ["Low", "Medium", "High", "Urgent"],
                            index=["Low", "Medium", "High", "Urgent"].index(task["priority"]),
                            key=f"priority_{task['id']}",
                        )
                        edit_status = st.selectbox(
                            "Status",
                            ["Pending", "In Progress", "Completed"],
                            index=["Pending", "In Progress", "Completed"].index(task["status"]),
                            key=f"status_{task['id']}",
                        )
                        edit_due = (
                            date.fromisoformat(task["due_date"])
                            if task["due_date"] else None
                        )
                        edit_due = st.date_input(
                            "Due Date",
                            value=edit_due,
                            key=f"due_{task['id']}",
                        )

                        if st.button("💾 Save Changes", key=f"save_{task['id']}", use_container_width=True):
                            if not edit_title.strip():
                                st.error("Task title cannot be empty.")
                            else:
                                update_task(
                                    task["id"],
                                    edit_title,
                                    edit_description,
                                    edit_priority,
                                    edit_status,
                                    edit_due,
                                )
                                st.success("Task updated.")
                                st.rerun()

                with b:
                    if st.button("🗑️ Delete", key=f"delete_{task['id']}", use_container_width=True):
                        delete_task(task["id"])
                        st.rerun()

                st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    if st.session_state.tasks:
        csv_data = export_csv(filtered)
        st.download_button(
            "⬇️ Export Visible Tasks as CSV",
            data=csv_data,
            file_name=f"taskflow_{date.today().isoformat()}.csv",
            mime="text/csv",
            use_container_width=True,
        )

st.divider()
st.caption("TaskFlow • Built with Python + Streamlit • No external frontend framework")
