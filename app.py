import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np # Required for audio generation

# --- HELPER FUNCTIONS ---
def _safe_rerun():
    if hasattr(st, "rerun"): st.rerun()
    else: st.experimental_rerun()

def _build_graph():
    # Set k=4, even number is required for Watts-Strogatz!
    G = nx.watts_strogatz_graph(15, 4, 0.3, seed=42)
    cc = nx.closeness_centrality(G)
    # Select the most central node
    true_zero = sorted(cc.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
    return G, true_zero

def run():
    st.title("🕵️‍♂️ Case 1: Ghost Protocol (Networks)")

    # State Init
    if "math_mode" not in st.session_state: st.session_state["math_mode"] = False
    if "G" not in st.session_state:
        G, true_zero = _build_graph()
        st.session_state["G"] = G
        st.session_state["true_zero"] = true_zero

    # Story / Math Transition
    if not st.session_state["math_mode"]:
        st.markdown("**Mission:** Locate the 'Main Server' responsible for the virus. If you shut down the wrong server, the hospital system crashes!")
        st.info("💡 Hint: Which node reaches others the fastest (Most Central)?")
    else:
        st.markdown(r"### 📐 MATHEMATICAL CONFRONTATION: Closeness Centrality$$ C(x) = \frac{1}{\sum_{y} d(x, y)} $$")

    col1, col2 = st.columns([2, 1])

    with col1:
        G = st.session_state["G"]
        pos = nx.spring_layout(G, seed=42)
        fig, ax = plt.subplots(figsize=(6, 4))
        nx.draw(G, pos, with_labels=True, node_color="skyblue", edge_color="gray", node_size=500, ax=ax)
        st.pyplot(fig)

    with col2:
        st.subheader("📡 Server Analysis")
        guess = st.number_input("Suspect ID:", min_value=0, max_value=14, step=1)

        if st.button("Scan System"):
            if int(guess) == int(st.session_state["true_zero"]):
                # --- SUCCESS BLOCK ---
                st.success("SUCCESS! Source Isolated.")
                st.balloons()
                st.caption("✅ **Real World:** This algorithm is also used to detect bot accounts.")
                
                # Inventory
                st.session_state["inventory_audio_file"] = "Project_Moriarty_Log.wav"
                st.toast("🎒 Inventory: Audio File")

                # Sound Effect (White Noise + 42Hz)
                sample_rate = 44100
                t = np.linspace(0, 2, 2 * sample_rate, endpoint=False)
                audio_data = np.sin(2 * np.pi * 42 * t) * 0.1 + np.random.normal(0, 0.5, t.shape)
                st.audio(audio_data, sample_rate=sample_rate)
                st.caption("🔊 Recovered File (Very Noisy!)")

            else:
                # --- ERROR/ETHICS BLOCK ---
                st.error("CRITICAL ERROR: You Shut Down the Wrong Server!")
                st.warning("""
                **Field Report:** The server you shut down was the **London City Hospital** database. 
                The system crashed. In network analysis, a 'False Positive' carries vital risks.
                """)

    st.divider()
    if st.button("🔴 Red Pill: Break the Analogy"):
        st.session_state["math_mode"] = not st.session_state["math_mode"]
        _safe_rerun()

    with st.expander("🛠️ Reality Check"):
        st.write("**Question:** If `p=0.0`, what does the network look like?")
        # 'Regular Ring Lattice' is the technical term for p=0
        ans = st.radio("Answer:", ["Chaos", "Regular Ring", "Star"])
        if ans == "Regular Ring": st.success("Correct!"); 
        elif ans: st.error("Wrong.")


def main():
    run()


if __name__ == "__main__":
    main()