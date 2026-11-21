import streamlit as st
import graphviz
import os

from ai_engine import generate_architecture_components


# Graphviz PATH
os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz\bin"


def get_project_components(project_idea):
    result = generate_architecture_components(project_idea)

    if not result:
        return None

    return result


def show_architecture_diagram(project_idea=""):

    st.subheader("📊 AI Architecture Diagram")

    data = get_project_components(project_idea)

    if not data:
        st.error("Unable to generate architecture diagram.")
        return

    nodes = data.get("nodes", [])
    edges = data.get("edges", [])

    diagram = graphviz.Digraph()

    diagram.attr(
        rankdir="TB",
        bgcolor="#0E1117",
        pad="0.4",
        nodesep="0.6",
        ranksep="0.8"
    )

    diagram.attr(
        "node",
        shape="box",
        style="rounded,filled",
        fillcolor="#241547",
        color="#A78BFA",
        fontcolor="white",
        fontname="Arial",
        fontsize="12",
        margin="0.25"
    )

    diagram.attr(
        "edge",
        color="#A78BFA",
        arrowsize="0.8",
        penwidth="1.5"
    )

    valid_ids = set()

    # Add Nodes
    for node in nodes:

        node_id = str(node.get("id", "")).strip()
        label = str(node.get("label", "")).strip()

        if node_id and label:

            valid_ids.add(node_id)
            diagram.node(node_id, label)

    # Add Edges
    for edge in edges:

        source = str(edge.get("from", "")).strip()
        target = str(edge.get("to", "")).strip()

        if source in valid_ids and target in valid_ids:
            diagram.edge(source, target)

    # Display diagram
    st.graphviz_chart(
        diagram,
        use_container_width=True
    )

    st.success("Architecture diagram generated successfully!")

    # Generate PNG
    png_bytes = diagram.pipe(format="png")

    # Create reports folder
    os.makedirs("reports", exist_ok=True)

    # Save PNG for PDF report
    image_path = os.path.join(
        "reports",
        "architecture_diagram.png"
    )

    with open(image_path, "wb") as file:
        file.write(png_bytes)

    st.success("Diagram saved for PDF report!")

    # Download PNG
    st.download_button(
        label="📥 Download Architecture Diagram (PNG)",
        data=png_bytes,
        file_name="ArchitecAI_Architecture.png",
        mime="image/png",
        use_container_width=True
    )

    # Download DOT
    st.download_button(
        label="📥 Download Diagram Source (DOT)",
        data=diagram.source,
        file_name="ArchitecAI_Architecture.dot",
        mime="text/plain",
        use_container_width=True
    )

    return png_bytes