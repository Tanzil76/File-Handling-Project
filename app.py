import streamlit as st
from pathlib import Path
from datetime import datetime

# ----------------------------------------------------------------------
# PAGE CONFIG + THEME
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="File Manager Studio",
    page_icon="📁",
    layout="centered",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
    .stApp {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    }
    section[data-testid="stSidebar"] {
        background: #0b1120;
        border-right: 1px solid #1e293b;
    }
    h1, h2, h3, p, label, span, div {
        color: #e2e8f0 !important;
    }
    .hero {
        padding: 1.5rem 1.75rem;
        border-radius: 16px;
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 30px rgba(79, 70, 229, 0.35);
    }
    .hero h1 { color: white !important; margin: 0; font-size: 1.8rem; }
    .hero p { color: #e0e7ff !important; margin-top: .35rem; margin-bottom: 0; }
    .card {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 14px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1rem;
    }
    .stButton>button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1.2rem;
        font-weight: 600;
        transition: transform 0.15s ease;
    }
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 14px rgba(99, 102, 241, 0.4);
    }
    .stTextInput>div>div>input, .stTextArea textarea {
        background: #0b1120 !important;
        color: #e2e8f0 !important;
        border-radius: 8px !important;
        border: 1px solid #334155 !important;
    }
    .footer-note {
        text-align: center;
        color: #64748b !important;
        font-size: 0.8rem;
        margin-top: 2rem;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Working directory for all file operations (keeps the demo self-contained)
WORKDIR = Path("file_manager_workspace")
WORKDIR.mkdir(exist_ok=True)

# ----------------------------------------------------------------------
# HERO HEADER
# ----------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <h1>📁 File Manager Studio</h1>
        <p>Create, read, update &amp; delete files — with a clean UI on top of Python's pathlib.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------
# SIDEBAR NAVIGATION
# ----------------------------------------------------------------------
st.sidebar.markdown("### ⚙️ Operations")
menu = st.sidebar.radio(
    "Choose an action",
    ["🆕 Create", "📖 Read", "✏️ Update", "🗑️ Delete", "🗂️ Browse"],
    label_visibility="collapsed",
)

st.sidebar.markdown("---")
st.sidebar.caption(f"Workspace: `{WORKDIR.resolve().name}/`")
files = sorted(p.name for p in WORKDIR.glob("*") if p.is_file())
st.sidebar.metric("Files in workspace", len(files))

# ----------------------------------------------------------------------
# HELPERS
# ----------------------------------------------------------------------
def resolve(name: str) -> Path:
    return WORKDIR / name

# ----------------------------------------------------------------------
# CREATE
# ----------------------------------------------------------------------
if menu == "🆕 Create":
    st.subheader("🆕 Create a new file")
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        name = st.text_input("File name", placeholder="notes.txt")
        content = st.text_area("Content", placeholder="Write something...", height=160)
        if st.button("Create File", use_container_width=True):
            if not name.strip():
                st.error("Please enter a file name.")
            else:
                path = resolve(name)
                if path.exists():
                    st.error(f"⚠️ '{name}' already exists.")
                else:
                    path.write_text(content)
                    st.success(f"✅ '{name}' created successfully!")
                    st.balloons()
        st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# READ
# ----------------------------------------------------------------------
elif menu == "📖 Read":
    st.subheader("📖 Read a file")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    if files:
        name = st.selectbox("Select a file", files) if files else None
    else:
        name = st.text_input("File name", placeholder="notes.txt")
    if st.button("Read File", use_container_width=True):
        path = resolve(name) if name else None
        if not name or not path.exists():
            st.error("❌ No such file exists.")
        else:
            content = path.read_text()
            st.success(f"Showing contents of '{name}'")
            st.code(content or "(file is empty)", language="text")
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# UPDATE
# ----------------------------------------------------------------------
elif menu == "✏️ Update":
    st.subheader("✏️ Update a file")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    name = st.selectbox("Select a file", files) if files else st.text_input("File name")
    operation = st.radio(
        "Operation", ["Rename", "Append content", "Overwrite content"], horizontal=True
    )

    if operation == "Rename":
        new_name = st.text_input("New file name", placeholder="renamed.txt")
        if st.button("Rename", use_container_width=True):
            path = resolve(name)
            new_path = resolve(new_name)
            if not name or not path.exists():
                st.error("❌ No such file exists.")
            elif new_path.exists():
                st.error(f"⚠️ '{new_name}' already exists.")
            else:
                path.rename(new_path)
                st.success(f"✅ Renamed to '{new_name}'")

    elif operation == "Append content":
        data = st.text_area("Content to append", height=120)
        if st.button("Append", use_container_width=True):
            path = resolve(name)
            if not name or not path.exists():
                st.error("❌ No such file exists.")
            else:
                with open(path, "a") as fs:
                    fs.write("\n" + data)
                st.success(f"✅ Appended to '{name}'")

    else:  # Overwrite content
        data = st.text_area("New content", height=120)
        if st.button("Overwrite", use_container_width=True):
            path = resolve(name)
            if not name or not path.exists():
                st.error("❌ No such file exists.")
            else:
                path.write_text(data)
                st.success(f"✅ Overwrote '{name}'")
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# DELETE
# ----------------------------------------------------------------------
elif menu == "🗑️ Delete":
    st.subheader("🗑️ Delete a file")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    name = st.selectbox("Select a file", files) if files else st.text_input("File name")
    confirm = st.checkbox("I understand this cannot be undone")
    if st.button("Delete File", use_container_width=True, disabled=not confirm):
        path = resolve(name)
        if not name or not path.exists():
            st.error("❌ No such file exists.")
        else:
            path.unlink()
            st.success(f"✅ '{name}' deleted successfully")
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# BROWSE
# ----------------------------------------------------------------------
elif menu == "🗂️ Browse":
    st.subheader("🗂️ Workspace files")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    if not files:
        st.info("No files yet — create one to get started!")
    else:
        for f in files:
            p = resolve(f)
            stat = p.stat()
            size_kb = stat.st_size / 1024
            modified = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
            col1, col2, col3 = st.columns([3, 1, 2])
            col1.write(f"📄 **{f}**")
            col2.write(f"{size_kb:.1f} KB")
            col3.write(modified)
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------
st.markdown(
    '<p class="footer-note">Built with Python &amp; Streamlit · File Manager Studio</p>',
    unsafe_allow_html=True,
)