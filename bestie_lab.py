import streamlit as st
from streamlit_server_state import server_state, server_state_lock

st.set_page_config(page_title="Bestie Lab", page_icon="🕵️‍♀️")

st.title("🕵️‍♀️ Bestie Lab")
st.write("Take the quiz! Your scores will be compared with your friend's in real-time.")

# 1. This creates the "Shared Chalkboard" in the cloud
if "shared_scores" not in server_state:
    with server_state_lock["shared_scores"]:
        server_state["shared_scores"] = {}

# 2. FULL LIST of traits (The "Indicators")
# We categorized these just for the code to read
traits = [
    "Matchmaking (Shipping people)", 
    "Crush Speculation", 
    "Imagining Weddings", 
    "Story-Spinning",
    "Easygoing", 
    "Funny", 
    "Mischievous", 
    "Dependable", 
    "Gaming", 
    "Artsy", 
    "Sporty", 
    "Reading"
]

# 3. User Selection
player_choice = st.radio("Who are you?", ["Friend 1", "Friend 2"])
name = st.text_input("Enter your nickname:", key="name_input")

st.subheader("Rate how much you LOVE these (0-10):")
my_results = []
for t in traits:
    # This creates a slider for EVERY trait in the list above
    val = st.slider(f"{t}", 0, 10, 5, key=f"quiz_{t}_{player_choice}")
    my_results.append(val)

# 4. Save to Cloud
if st.button("Submit to the Cloud ☁️"):
    with server_state_lock["shared_scores"]:
        server_state["shared_scores"][player_choice] = {"name": name, "scores": my_results}
    st.success(f"Scores for {name} saved! Now wait for your friend.")

st.divider()

# 5. The Big Reveal
if st.button("🔍 Check for a Match!"):
    all_data = server_state["shared_scores"]
    
    if "Friend 1" in all_data and "Friend 2" in all_data:
        f1 = all_data["Friend 1"]
        f2 = all_data["Friend 2"]
        
        # Math: Find the total difference between scores
        diff_sum = sum(abs(f1["scores"][i] - f2["scores"][i]) for i in range(len(traits)))
        max_possible_diff = len(traits) * 10
        match_pct = ((max_possible_diff - diff_sum) / max_possible_diff) * 100
        
        st.balloons()
        st.header(f"Results for {f1['name']} & {f2['name']}")
        st.metric(label="Bestie Compatibility Score", value=f"{match_pct:.1f}%")
        
        # Fun Logic: Check if they are both "Matchmakers"
        # (The first 4 traits in our list are the Social Lab traits)
        if f1["scores"][0] > 7 and f2["scores"][0] > 7:
            st.info("💎 True Matchmakers: You both love a good wedding-day imagination!")
    else:
        st.warning("Still waiting for the other person... Make sure both of you hit 'Submit to the Cloud'!")
